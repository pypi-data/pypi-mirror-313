import asyncio
import json
from typing import Dict, List, Optional, Tuple, Union

import aiohttp
import async_lru
import docker
import docker.types
from ambient_backend_api_client import NodeOutput as Node
from ambient_backend_api_client import RequestedServiceSpec, ServiceCreate
from ambient_base_plugin.models.configuration import ConfigPayload
from docker_swarm_plugin.models.service_models import DockerServiceAttrs
from docker_swarm_plugin.models.service_models import (
    ServiceNodeRelationshipWithDockerAttrs as ServiceNodeRelationship,
)
from docker_swarm_plugin.models.service_models import ServiceWithDockerAttrs as Service
from docker_swarm_plugin.models.service_models import SyncSurveyReport
from pydantic import ValidationError

from ambient_client_common.repositories.docker_repo import DockerRepo
from ambient_client_common.utils import logger

Pair = Tuple[Optional[DockerServiceAttrs], Optional[ServiceNodeRelationship]]


class ServiceConfigSvc:
    def __init__(self, docker_repo: DockerRepo, config_payload: ConfigPayload) -> None:
        self.docker_client: docker.DockerClient = docker_repo.client
        self.config_payload = config_payload
        self.api_config = config_payload.api_config

    async def run_system_sweep(self, node: Node) -> None:
        """Run a system sweep on the given node.
        Running a system sweep in this context is to
        check the current status of services on the node
        and update the status of the services via the API.

        Args:
            node (Node): Node object.
        """
        logger.info("Running system sweep on node: {}", node.id)
        # gather local service data
        local_services = gather_local_services(self.docker_client)
        logger.info("Gathered {} local services", len(local_services))

        # gather services from API
        logger.debug("Getting token ...")
        token = await self.config_payload.get_token()
        logger.info("Retrieved token. [{} chars]", len(token))
        logger.info("token from get_token: {}", token)
        backend_services, parent_services = (
            await get_service_node_relationships_from_api(
                node_id=node.id, base_url=self.api_config.host, token=token
            )
        )
        logger.info("Gathered {} backend services", len(backend_services))

        # compare and diff services
        logger.info("Pairing services ...")
        service_pairs = pair_services(local_services, backend_services, parent_services)
        logger.debug("Service pairs: {}", service_pairs)
        grouped_pairs = group_services(service_pairs)
        logger.debug("Grouped pairs: {}", grouped_pairs)
        logger.info(
            "Total services: {}, grouped pairs: {}",
            len(service_pairs),
            sum(len(v) for v in grouped_pairs.values()),
        )

        # update service data via API
        await handle_paired(
            pairs=grouped_pairs["paired"],
            base_url=self.api_config.host,
            token=self.api_config.access_token,
            node_id=node.id,
        )
        logger.info("Handled paired services")

        # create out of sync services
        await handle_local_only(
            pairs=grouped_pairs["local_only"],
            node_id=node.id,
            base_url=self.api_config.host,
            token=self.api_config.access_token,
        )
        logger.info("Handled local only services")

        # mark out of sync services
        await handle_backend_only(
            pairs=grouped_pairs["backend_only"],
            base_url=self.api_config.host,
            token=self.api_config.access_token,
        )
        logger.info("Handled backend only services")

        logger.info("ServiceConfigSvc system sweep complete")

    async def handle_service_event(self, service_id: int) -> None:
        """Handle a service event."""

        logger.info("Handling service event for service: {}", service_id)

        token = await self.config_payload.get_token()
        logger.debug("Retrieved token. [{} chars]", len(token))

        # get service from API
        try:
            backend_service = await get_service(
                service_id=service_id,
                base_url=self.api_config.host,
                token=token,
            )
            if not backend_service:
                # hande error
                return await handle_service_event_error(
                    base_url=self.api_config.host,
                    token=token,
                    service_id=service_id,
                    node_id=self.config_payload.node_id,
                    error="Failed to get service from API",
                    local_service=None,
                )
            logger.info(
                "Retrieved service from API: {} ... \
[{} total fields, {} populated fields]",
                backend_service.model_dump_json()[:20],
                len(backend_service.model_dump().keys()),
                len(backend_service.model_dump(exclude_unset=True).keys()),
            )

            # get deployment
            deployment = await get_service_node_relationship(
                base_url=self.api_config.host,
                service_id=service_id,
                node_id=self.config_payload.node_id,
                token=token,
            )
            if not deployment:
                # hande error
                err_msg = "Failed to get service node relationship from API"
                logger.error(err_msg)
                return await handle_service_event_error(
                    base_url=self.api_config.host,
                    token=token,
                    service_id=service_id,
                    node_id=self.config_payload.node_id,
                    error=err_msg,
                    local_service=None,
                    existing_deployment=None,
                )
            logger.info(
                "Retrieved deployment from API: {} ... \
[{} total fields, {} populated fields]",
                deployment.model_dump_json()[:20],
                len(deployment.model_dump().keys()),
                len(deployment.model_dump(exclude_unset=True).keys()),
            )
        except Exception as e:
            logger.error("Failed to get service and deployment: {}", e)
            return await handle_service_event_error(
                base_url=self.api_config.host,
                token=token,
                service_id=service_id,
                node_id=self.config_payload.node_id,
                error="Failed to get service and deployment",
                local_service=None,
            )

        # find matching service in local services
        local_services = gather_local_services(self.docker_client)
        logger.info("Found {} local services", len(local_services))
        matching_local_service = find_matching_local_service(
            backend_service=deployment,
            parent_service=backend_service,
            local_services=local_services,
        )

        updated_local_service: Optional[DockerServiceAttrs] = None
        try:
            # if match, enforce requested spec
            if matching_local_service:
                logger.info(
                    "Found matching local service: {}", matching_local_service.Spec.Name
                )
                updated_local_service = enforce_requested_spec(
                    matching_local_service,
                    deployment,
                    backend_service,
                    client=self.docker_client,
                )
                if not updated_local_service:
                    # hande error
                    err_msg = "Failed to enforce requested spec"
                    logger.error(err_msg)
                    return await handle_service_event_error(
                        base_url=self.api_config.host,
                        token=token,
                        service_id=service_id,
                        node_id=self.config_payload.node_id,
                        error=err_msg,
                        local_service=None,
                        existing_deployment=deployment,
                    )
                logger.info(
                    "Enforced requested spec on local service: {}",
                    updated_local_service.Spec.Name,
                )

            # if no match, create service
            else:
                updated_local_service = create_local_service(
                    parent_service=backend_service, client=self.docker_client
                )
                if not updated_local_service:
                    # handle error
                    err_msg = "Failed to create local service"
                    logger.error(err_msg)
                    return await handle_service_event_error(
                        base_url=self.api_config.host,
                        token=token,
                        service_id=service_id,
                        node_id=self.config_payload.node_id,
                        error=err_msg,
                        local_service=None,
                        existing_deployment=deployment,
                    )
                logger.info(
                    "Created local service: {}", updated_local_service.Spec.Name
                )
        except Exception as e:
            logger.error(
                "Failed to enforce requested spec or create local service: {}", e
            )
            return await handle_service_event_error(
                base_url=self.api_config.host,
                token=token,
                service_id=service_id,
                node_id=self.config_payload.node_id,
                error="Failed to enforce requested spec or create local service",
                local_service=None,
                existing_deployment=deployment,
            )

        # handle success
        return await handle_service_event_success(
            base_url=self.api_config.host,
            token=token,
            service_id=service_id,
            node_id=self.config_payload.node_id,
            local_service=updated_local_service,
        )


async def handle_service_event_error(
    base_url: str,
    token: str,
    service_id: int,
    node_id: int,
    error: str,
    local_service: Optional[DockerServiceAttrs],
    existing_deployment: Optional[ServiceNodeRelationship] = None,
) -> None:
    # update service deployment
    logger.info("Handling service event error ...")
    try:
        updated_deployment = ServiceNodeRelationship(
            service_id=service_id,
            node_id=node_id,
            state=existing_deployment.state if existing_deployment else None,
            status="failure",
            error=error,
            docker_service_attrs=local_service,
        )
        logger.debug(
            "Updated deployment: {}", updated_deployment.model_dump_json(indent=4)
        )
        return await update_service_node_relationship(
            base_url=base_url,
            token=token,
            service_node_relationship=updated_deployment,
        )
    except Exception as e:
        logger.error("Failed to handle service event error: {}", e)


async def handle_service_event_success(
    base_url: str,
    token: str,
    service_id: int,
    node_id: int,
    local_service: DockerServiceAttrs,
) -> None:
    logger.info("Handling service event success ...")
    # update service deployment
    updated_deployment = ServiceNodeRelationship(
        service_id=service_id,
        node_id=node_id,
        state="deployed",
        status="success",
        docker_service_attrs=local_service,
    )
    return await update_service_node_relationship(
        base_url=base_url,
        token=token,
        service_node_relationship=updated_deployment,
    )


def create_local_service(
    parent_service: Service, client: docker.DockerClient
) -> Optional[DockerServiceAttrs]:
    """Create a local service from the backend service."""
    logger.info(
        "Creating service using docker client. Service name: {}, image: {}",
        parent_service.name,
        parent_service.requested_service_spec.image,
    )
    try:
        labels = parent_service.requested_service_spec.labels
        if labels:
            requested_labels_dict = {
                label.split("=")[0]: label.split("=")[1]
                for label in parent_service.requested_service_spec.labels
            }
        else:
            requested_labels_dict = {}
        requested_spec = parent_service.requested_service_spec
        docker_service = client.services.create(
            image=requested_spec.image,
            maxreplicas=requested_spec.replicas,
            container_labels=requested_labels_dict,
            endpoint_spec=build_endpoint_spec(parent_service),
            env=requested_spec.env_vars,
            hostname=requested_spec.hostname if requested_spec.hostname else None,
            labels=requested_labels_dict,
            mounts=requested_spec.mounts,
            name=parent_service.name,
            networks=requested_spec.networks,
        )
        return DockerServiceAttrs.model_validate(docker_service.attrs)
    except docker.errors.APIError as e:
        logger.error("Encountered API error: {}", e)
        # run update if error code 409
        if e.response.status_code == 409:
            logger.info("Service already exists. Updating service ...")
            existing_service = get_local_service(client, parent_service.name)
            if not existing_service:
                logger.error("Failed to get existing service")
                return None
            return update_local_service(
                local_service=existing_service,
                parent_service=parent_service,
                client=client,
            )
    except Exception as e:
        logger.error("Failed to create service using docker client: {}", e)
        return None


def get_local_service(
    client: docker.DockerClient, name: str
) -> Optional[DockerServiceAttrs]:
    """Get a local service from the given Docker client."""
    logger.info("Getting local service ...")
    try:
        service = client.services.list(filters={"name": name})[0]
        return DockerServiceAttrs.model_validate(service.attrs)
    except Exception as e:
        logger.error("Failed to get local service: {}", e)
        return None


def update_local_service(
    local_service: DockerServiceAttrs,
    parent_service: Service,
    client: docker.DockerClient,
) -> Optional[DockerServiceAttrs]:
    """Update a local service from the backend service."""
    logger.info(
        "Updating service using docker client. Service name: {}, image: {}",
        parent_service.name,
        parent_service.requested_service_spec.image,
    )
    try:
        labels = parent_service.requested_service_spec.labels
        if labels:
            requested_labels_dict = {
                label.split("=")[0]: label.split("=")[1]
                for label in parent_service.requested_service_spec.labels
            }
        else:
            requested_labels_dict = {}
        requested_spec = parent_service.requested_service_spec
        existing_service = client.services.get(local_service.ID)
        docker_service = existing_service.update(
            image=requested_spec.image,
            maxreplicas=requested_spec.replicas,
            container_labels=requested_labels_dict,
            endpoint_spec=build_endpoint_spec(parent_service),
            env=requested_spec.env_vars,
            hostname=requested_spec.hostname if requested_spec.hostname else None,
            labels=requested_labels_dict,
            mounts=requested_spec.mounts,
            name=parent_service.name,
            networks=requested_spec.networks,
        )
        logger.info("new service: {}", docker_service)
        logger.info("Service updated. Reloading service ...")
        existing_service.reload()
        return DockerServiceAttrs.model_validate(existing_service.attrs)
    except Exception as e:
        logger.error("Failed to update service using docker client: {}", e)
        return None


def build_endpoint_spec(parent_service: Service) -> Optional[docker.types.EndpointSpec]:
    """Build enpoint spec for creating a service locally"""
    if not parent_service.requested_service_spec.ports:
        return None

    logger.info("building endpoint spec ...")
    ports_dict = {}  # {publish_port: target_port}
    for ports in parent_service.requested_service_spec.ports:
        port_list = ports.split(":")
        if len(port_list) != 2:
            logger.error("Invalid port format: {}", ports)
            continue
        ports_dict[int(port_list[0])] = int(port_list[1])

    logger.info("ports_dict: {}", ports_dict)

    endpoint_spec = docker.types.EndpointSpec(
        mode="vip",
        ports=ports_dict,
    )
    logger.info("endpoint_spec: {}", endpoint_spec)
    return endpoint_spec


def enforce_requested_spec(
    local_service: DockerServiceAttrs,
    backend_service: ServiceNodeRelationship,
    parent_service: Service,
    client: docker.DockerClient,
) -> DockerServiceAttrs:
    """Enforce the requested spec on the local service."""
    sync_report = determine_in_sync(local_service, backend_service, parent_service)
    if sync_report.in_sync:
        logger.info("Service is in sync. No need to enforce requested spec.")
        return local_service
    else:
        logger.info("Service is out of sync. Need to enfore requested spec ...")
        return update_local_service(local_service, parent_service, client)


async def get_service_node_relationship(
    base_url: str, service_id: int, node_id: int, token: str
) -> Optional[ServiceNodeRelationship]:
    """Get the service node relationship."""
    logger.info("Getting service node relationship ...")
    url = f"{base_url}/services/{service_id}/node_relationships/{node_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        try:
            resp, resp_text = await make_api_request(session, url, headers)
            resp.raise_for_status()
            return ServiceNodeRelationship.model_validate_json(resp_text)
        except Exception as e:
            logger.error("Failed to get service node relationship: {}", e)
            return None


@async_lru.alru_cache(maxsize=128, ttl=60)
async def get_service_cached(
    service_id: int, base_url: str, token: str
) -> Optional[Service]:
    """Get the service from the cache."""
    return await get_service(service_id, base_url, token)


async def get_service(service_id: int, base_url: str, token: str) -> Optional[Service]:
    logger.info("Getting service ...")
    resp_text: Optional[str] = None
    url = f"{base_url}/services/{service_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    logger.debug("Request full URL: GET - {}", url)
    logger.debug("Headers: {}", headers)
    async with aiohttp.ClientSession() as session:
        try:
            resp, resp_text = await make_api_request(session, url, headers)
            logger.debug("Response: {}", resp_text)
            resp.raise_for_status()
            return Service.model_validate_json(resp_text)
        except Exception as e:
            logger.error(
                "Failed to get service: {}",
                (str(e) + "\n" + resp_text) if resp_text else e,
            )
            return None


def find_matching_local_service(
    backend_service: ServiceNodeRelationship,
    parent_service: Service,
    local_services: List[DockerServiceAttrs],
) -> Optional[DockerServiceAttrs]:
    """Find the matching local service."""
    logger.info("Finding matching local service ...")
    try:
        for local_service in local_services:
            logger.debug(
                "Comparing local service: {} with backend service: {} ...",
                local_service.Spec.Name,
                parent_service.name,
            )
            if match_service(local_service, backend_service, parent_service):
                logger.info("Found matching local service: {}", local_service.Spec.Name)
                return local_service
        logger.info("No matching local service found")
        return None
    except Exception as e:
        logger.error("Failed to find matching local service: {}", e)
        return None


def gather_local_services(client: docker.DockerClient) -> List[DockerServiceAttrs]:
    """Gather the current services from the given Docker client.

    Args:
        client (docker.DockerClient): The Docker client to use.

    Returns:
        List[DockerServiceAttrs]: The list of current services.
    """
    logger.info("Gathering current services ...")
    services = client.services.list()
    logger.info("Collected {} services", len(services))
    # for service in services:
    #     logger.debug("service data: {}", json.dumps(service.attrs, indent=4))

    # return [DockerServiceAttrs.model_validate(service.attrs) for service in services]
    parsed_models = []
    for service in services:
        try:
            parsed_models.append(DockerServiceAttrs.model_validate(service.attrs))
        except ValidationError as e:
            logger.error("Failed to parse service: {}", e)
    return parsed_models


async def make_api_request(
    session: aiohttp.ClientSession,
    url: str,
    headers: dict,
    method: str = "get",
    data: Union[dict, None] = None,
) -> Tuple[aiohttp.ClientResponse, str]:
    max_redirects = 10
    for i in range(max_redirects):
        logger.info("Fetching URL: {} [redirects: {}]", url, i)
        method_call = getattr(session, method)
        resp: aiohttp.ClientResponse
        if data:
            async with method_call(
                url, headers=headers, allow_redirects=False, json=data
            ) as resp:
                if resp.status in (301, 302, 303, 307, 308):
                    url = resp.headers["Location"]
                    logger.info("Redirecting to: {}", url)
                    continue
                else:
                    resp_text = await resp.text()
                    return resp, resp_text
        else:
            async with method_call(url, headers=headers, allow_redirects=False) as resp:
                if resp.status in (301, 302, 303, 307, 308):
                    url = resp.headers["Location"]
                    logger.info("Redirecting to: {}", url)
                    continue
                else:
                    resp_text = await resp.text()
                    return resp, resp_text
    raise Exception("Too many redirects")


async def get_services_from_api(
    node_id: int, base_url: str, token: str
) -> List[Service]:
    logger.info("Getting services from API ...")
    resp_text: Optional[str] = None
    url = f"{base_url}/nodes/{node_id}/services/"
    headers = {"Authorization": f"Bearer {token}"}
    logger.debug("Request full URL: GET - {}", url)
    logger.debug("Headers: {}", headers)
    async with aiohttp.ClientSession() as session:
        try:
            resp, resp_text = await make_api_request(session, url, headers)
            logger.debug("Response: {}", resp_text)
            resp.raise_for_status()
            data: dict = await resp.json()
            count = data.get("count", 0)
            logger.info("Got {} services from API", count)
            services = data.get("results", [])
            return [Service.model_validate(service) for service in services]
        except Exception as e:
            logger.error(
                "Failed to get services from API: {}",
                (str(e) + "\n" + resp_text) if resp_text else e,
            )
            return []


async def get_service_node_relationships_from_api(
    node_id: int, base_url: str, token: str
) -> Tuple[List[ServiceNodeRelationship], Dict[int, Service]]:
    services = await get_services_from_api(node_id, base_url, token)
    awaitables = [
        get_service_node_relationship_from_api(service.id, node_id, base_url, token)
        for service in services
    ]
    return (await asyncio.gather(*awaitables)), {
        service.id: service for service in services
    }


async def get_service_node_relationship_from_api(
    service_id: int, node_id: int, base_url: str, token: str
) -> ServiceNodeRelationship:
    logger.info("Getting service node relationship from API ...")
    resp_text: Optional[str] = None
    url = f"{base_url}/services/{service_id}/node_relationships/{node_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    logger.debug("Request full URL: GET - {}", url)
    logger.debug("Headers: {}", headers)
    async with aiohttp.ClientSession() as session:
        try:
            resp, resp_text = await make_api_request(session, url, headers)
            logger.debug("Response: {}", resp_text)
            resp.raise_for_status()
            return ServiceNodeRelationship.model_validate_json(resp_text)
        except Exception as e:
            logger.error(
                "Failed to get service node relationship from API: {}",
                (str(e) + "\n" + resp_text) if resp_text else e,
            )


def match_service(
    local_service: DockerServiceAttrs,
    backend_service: ServiceNodeRelationship,
    parent_service: Service,
) -> bool:
    if not backend_service.docker_service_attrs:
        return False
    local_name = local_service.Spec.Name
    backend_name = parent_service.name
    logger.debug(
        "Matching local service: {} with backend service: {}",
        local_name,
        backend_name,
    )
    return local_name == backend_name


def pair_services(
    local_services: List[DockerServiceAttrs],
    backend_services: List[ServiceNodeRelationship],
    parent_services: Dict[int, Service],
) -> List[Pair]:
    """Pair the local services with the backend services.

    Args:
        local_services (List[DockerServiceAttrs]): The local services.
        backend_services (List[ServiceNodeRelationship]): The backend
            service node relationships.

    Returns:
        List[Pair]: The paired services.
            [
                (local_service, backend_service),
                (local_service, None),
                (None, backend_service),
                ...
            ]
    """

    logger.info("Pairing services ...")
    pairs = []
    seen_ids = set()
    seen_local_names = set()

    for local_service in local_services:
        logger.debug("Pairing local service: {}", local_service.Spec.Name)
        for backend_service in backend_services:
            parent_service = parent_services.get(backend_service.service_id)
            if not parent_service:
                logger.error(
                    "Parent service not found for service: {}",
                    backend_service.service_id,
                )
                continue
            matched_service = match_service(
                local_service, backend_service, parent_service
            )
            if matched_service:
                logger.debug("Matched service: {}", backend_service)
                pairs.append((local_service, backend_service))
                seen_ids.add(backend_service.service_id)
                seen_local_names.add(local_service.Spec.Name)
                break
        if local_service.Spec.Name not in seen_local_names:
            logger.debug(
                "No match found for local service: {}", local_service.Spec.Name
            )
            pairs.append((local_service, None))

    for backend_service in backend_services:
        if backend_service.service_id not in seen_ids:
            logger.debug(
                "No match found for backend service: {}", backend_service.service_id
            )
            pairs.append((None, backend_service))

    logger.info("Parsed {} pairs", len(pairs))
    return pairs


def group_services(pairs: List[Pair]) -> Dict[str, List[Pair]]:
    """Group the pairs of services by their name.

    Args:
        pairs (List[Pair]): The pairs of services.

    Returns:
        Dict[str, List[Pair]]: The grouped pairs.
    """
    logger.info("Grouping services ...")
    grouped = {"paired": [], "local_only": [], "backend_only": []}

    for local_service, backend_service in pairs:
        if local_service and backend_service:
            grouped["paired"].append((local_service, backend_service))
        elif local_service:
            grouped["local_only"].append((local_service, None))
        elif backend_service:
            grouped["backend_only"].append((None, backend_service))

    logger.info(
        "Grouped services: {} paired, {} local only, {} backend only",
        len(grouped["paired"]),
        len(grouped["local_only"]),
        len(grouped["backend_only"]),
    )

    return grouped


async def handle_paired(
    pairs: List[Pair], base_url: str, token: str, node_id: int
) -> None:
    """Handle the paired services.

    Args:
        pairs (List[Pair]): The paired services.
    """

    logger.info("Handling paired services ...")

    # mismatched in this context means the services are not in sync
    mismatched_pairs = []
    matched_pairs = []

    for local_service, backend_service in pairs:
        parent_service = await get_service_cached(
            backend_service.service_id, base_url, token
        )
        if determine_in_sync(local_service, backend_service, parent_service).in_sync:
            matched_pairs.append((local_service, backend_service))
        else:
            mismatched_pairs.append((local_service, backend_service))

    logger.info("In-sync: {} services", len(matched_pairs))
    logger.info("Out-of-sync: {} services", len(mismatched_pairs))

    await handle_paired_mismatched(mismatched_pairs, base_url, token, node_id)
    await handle_paired_and_in_sync(matched_pairs, base_url, token)

    logger.info("Handled paired services.")


def determine_in_sync(
    local_service: DockerServiceAttrs,
    backend_service: ServiceNodeRelationship,
    parent_service: Service,
) -> SyncSurveyReport:
    """Determine if the local service matches the backend service

    Args:
        local_service (DockerServiceAttrs): local service
        backend_service (ServiceNodeRelationship): backend service node relationship

    Returns:
        bool: True if the services match, False otherwise
    """
    logger.info(
        "Determining match for local service: {} and backend service: {}",
        local_service.Spec.Name,
        parent_service.name,
    )

    sync_report = SyncSurveyReport()

    # both are not none test
    if local_service is None or backend_service is None:
        logger.info("Not a match - one of the services is None")
        return sync_report
    logger.debug("both inputs are not None test passed")
    sync_report.both_inputs_are_not_none = True

    # image test
    if (
        local_service.Spec.TaskTemplate.ContainerSpec.Image
        != parent_service.requested_service_spec.image
    ):
        logger.info("Not a match - image mismatch")
        return sync_report
    logger.debug("image test passed")
    sync_report.image_in_sync = True

    # ports test
    requested_ports: List[Tuple[int, int]] = []
    for ports in parent_service.requested_service_spec.ports:
        try:
            target_port = int(ports.split(":")[0])
            published_port = int(ports.split(":")[1])
            requested_ports.append((target_port, published_port))
        except Exception as e:
            logger.error("Failed to parse ports. Value: {}, error: {}", ports, e)
            return sync_report
    for port in local_service.Endpoint.Spec.Ports:
        if (port.TargetPort, port.PublishedPort) not in requested_ports:
            logger.info("Not a match - ports mismatch")
            logger.debug("requested ports: {}", requested_ports)
            logger.debug(
                "local ports: {}",
                [
                    (port.TargetPort, port.PublishedPort)
                    for port in local_service.Endpoint.Spec.Ports
                ],
            )
            return sync_report
    local_ports = [
        (port.TargetPort, port.PublishedPort)
        for port in local_service.Endpoint.Spec.Ports
    ]
    for port in requested_ports:
        if port not in local_ports:
            logger.info("Not a match - ports mismatch")
            return sync_report
    logger.debug("ports test passed")
    sync_report.ports_in_sync = True

    # replicas test
    if (
        local_service.Spec.Mode.Replicated.Replicas
        != parent_service.requested_service_spec.replicas
    ):
        logger.info("Not a match - replicas mismatch")
        return sync_report
    logger.debug("replicas test passed")
    sync_report.replicas_in_sync = True

    # labels test
    requested_labels = (
        {
            label.split("=")[0]: label.split("=")[1]
            for label in parent_service.requested_service_spec.labels
        }
        if parent_service.requested_service_spec.labels
        else {}
    )
    if local_service.Spec.Labels != requested_labels:
        logger.info("Not a match - labels mismatch")
        return sync_report
    logger.debug("labels test passed")
    sync_report.labels_in_sync = True

    # env vars test
    local_env_vars = local_service.Spec.TaskTemplate.ContainerSpec.Env
    requested_env_vars = parent_service.requested_service_spec.env_vars
    # the bool checks are for comparing [] to None
    if local_env_vars != requested_env_vars and bool(local_env_vars) != bool(
        requested_env_vars
    ):
        logger.info("Not a match - env vars mismatch")
        logger.debug("local env vars: {}", local_env_vars)
        logger.debug("requested env vars: {}", requested_env_vars)
        return sync_report
    logger.debug("env vars test passed")
    sync_report.env_vars_in_sync = True

    # hostname test
    local_hostname = local_service.Spec.TaskTemplate.ContainerSpec.Hostname
    requested_hostname = parent_service.requested_service_spec.hostname
    if (
        local_hostname != requested_hostname
        and bool(local_hostname) != bool(requested_hostname)
        and requested_hostname is not None
    ):
        logger.info("Not a match - hostname mismatch")
        logger.debug("local hostname: {}", local_hostname)
        logger.debug("requested hostname: {}", requested_hostname)
        return sync_report
    logger.debug("hostname test passed")
    sync_report.hostname_in_sync = True

    # mounts test
    requested_mounts = parent_service.requested_service_spec.mounts
    local_mounts = [
        f"{mount.Source}:{mount.Target}:rw"
        for mount in local_service.Spec.TaskTemplate.ContainerSpec.Mounts
    ]
    if requested_mounts != local_mounts and bool(requested_mounts) != bool(
        local_mounts
    ):
        logger.info("Not a match - mounts mismatch")
        logger.debug("requested mounts: {}", requested_mounts)
        logger.debug("local mounts: {}", local_mounts)
        return sync_report
    logger.debug("mounts test passed")
    sync_report.mounts_in_sync = True

    # TODO: Network test, need to query every network from docker client
    # to find it's ID, and then use that to determine if the network is in sync

    logger.info("service {} is in sync", local_service.Spec.Name)
    return sync_report


async def handle_paired_mismatched(
    pairs: List[Pair], base_url: str, token: str, node_id: int
) -> None:
    """Handle the paired mismatched services.

    Args:
        pairs (List[Pair]): The paired mismatched services.
        base_url (str): The base URL of the API.
        token (str): The token to use.
        node_id (str): The ID of the node.
    """
    logger.info("Handling paired mismatched services ...")
    local_only = []
    backend_only = []
    for local_service, backend_service in pairs:
        if not local_service:
            backend_only.append((None, backend_service))
            continue
        if not backend_service:
            local_only.append((local_service, None))
            continue
        await handle_out_of_sync_services(
            [(local_service, backend_service)], base_url, token, node_id
        )

    await handle_local_only(local_only, node_id, base_url, token)
    await handle_backend_only(backend_only, base_url, token)


async def handle_out_of_sync_services(
    pairs: List[Pair], base_url: str, token: str, node_id: int
) -> None:
    """Handle the out of sync services.

    Args:
        pairs (List[Pair]): The out of sync services.
        base_url (str): The base URL
        token (str): The token to use
        node_id (int): The ID of the node
    """

    logger.info("Handling out of sync services ...")

    # update the docker attributes of the service node relationship
    # and change state to deployed and status to pending
    for local_service, backend_service in pairs:
        await update_service_node_relationship(
            base_url=base_url,
            token=token,
            service_node_relationship=ServiceNodeRelationship(
                service_id=backend_service.service_id,
                node_id=node_id,
                state=backend_service.state,
                status="pending",
                error="Service is out of sync",
                docker_service_attrs=local_service.model_dump(),
            ),
        )
        logger.info(
            "Updated service node relationship for service: {}",
            backend_service.service_id,
        )
    logger.info("Handled out of sync services.")


async def handle_paired_and_in_sync(
    pairs: List[Pair], base_url: str, token: str
) -> None:
    """Handle the in-sync services.

    Args:
        pairs (List[Pair]): The in-sync services.
        base_url (str): The base URL of the API.
        token (str): The token to use.
    """
    logger.info("Handling in-sync services ...")
    # update the docker attributes of the service node relationship
    # and change state to deployed and status to success
    for local_service, backend_service in pairs:
        await update_service_node_relationship(
            base_url=base_url,
            token=token,
            service_node_relationship=ServiceNodeRelationship(
                service_id=backend_service.service_id,
                node_id=backend_service.node_id,
                state="deployed",
                status="success",
                docker_service_attrs=local_service.model_dump(),
            ),
        )
        logger.info(
            "Updated service node relationship for service: {}",
            backend_service.service_id,
        )
    logger.info("Handled in-sync services.")


async def handle_local_only(
    pairs: List[Pair], node_id: int, base_url: str, token: str
) -> None:
    """Handle the local only services.

    Args:
        pairs (List[Pair]): The local only services.
        node_id (int): The ID of the node.
        base_url (str): The base URL of the API.
        token (str): The token to use.
    """
    logger.info("Handling local only services ...")
    logger.debug("Local only pairs: {}", pairs)
    # create out of sync services in the API
    for local_service, _ in pairs:
        logger.info("Creating out of sync service: {}", local_service.Spec.Name)
        local_mounts = local_service.Spec.TaskTemplate.ContainerSpec.Mounts
        new_service = await create_service(
            base_url=base_url,
            token=token,
            service_request=ServiceCreate(
                name=local_service.Spec.Name,
                resource_type="service",
                description=f"Service imported from Node {node_id}",
                desired_state="created",
                node_ids=[node_id],
                requested_service_spec=RequestedServiceSpec(
                    image=local_service.Spec.TaskTemplate.ContainerSpec.Image,
                    tags=["imported"],
                    ports=[
                        f"{port.TargetPort}:{port.PublishedPort}"
                        for port in local_service.Endpoint.Spec.Ports
                    ],
                    replicas=local_service.Spec.Mode.Replicated.Replicas,
                    labels=[
                        f"{key}={value}"
                        for key, value in local_service.Spec.Labels.items()
                    ],
                    env_vars=local_service.Spec.TaskTemplate.ContainerSpec.Env,
                    hostname=local_service.Spec.TaskTemplate.ContainerSpec.Hostname,
                    mounts=[
                        f"{mount.Type}:{mount.Source}:{mount.Target}"
                        for mount in local_mounts
                    ],
                ),
            ),
        )
        await update_service_node_relationship(
            base_url=base_url,
            token=token,
            service_node_relationship=ServiceNodeRelationship(
                service_id=new_service.id,
                node_id=node_id,
                state="created",
                status="success",
                docker_service_attrs=local_service.model_dump(),
            ),
        )


async def handle_backend_only(pairs: List[Pair], base_url: str, token: str) -> None:
    """Handle the backend only services.

    Args:
        pairs (List[Pair]): The backend only services.
        base_url (str): The base URL of the API.
        token (str): The token to use.
    """
    # mark the services as out of sync
    for _, backend_service in pairs:
        await update_service(
            base_url=base_url,
            token=token,
            service_id=backend_service.id,
            state="requested",
        )


async def update_service(base_url: str, token: str, service_id: int, **values) -> None:
    """Update the service with the given ID.

    Args:
        base_url (str): The base URL of the API.
        token (str): The token to use.
        service_id (int): The ID of the service to update.
        **values: The values to update.
    """
    logger.info("Updating service: {}", service_id)
    resp_text: Optional[str] = None
    url = f"{base_url}/services/{service_id}/"
    logger.debug("PATCH {}", url)
    headers = {"Authorization": f"Bearer {token}"}

    try:
        async with aiohttp.ClientSession() as session:
            response, resp_text = await make_api_request(
                session, url, headers, method="patch", data=values
            )
            logger.debug("Response: {}", resp_text)
            response.raise_for_status()
            logger.info("Updated service: {}", service_id)
            get_service_cached.cache_invalidate(service_id, base_url, token)
    except Exception as e:
        logger.error("Failed to update service: {}", resp_text if resp_text else e)


async def create_service(
    base_url: str, token: str, service_request: ServiceCreate
) -> Service:
    """Create a service with the given request.

    Args:
        base_url (str): The base URL of the API.
        token (str): The token to use.
        service_request (ServiceCreate): The service request.
    """
    logger.info("Creating service ...")
    resp_text: Optional[str] = None
    url = f"{base_url}/services/"
    logger.debug("POST {}", url)
    headers = {"Authorization": f"Bearer {token}"}

    async with aiohttp.ClientSession() as session:
        try:
            resp, resp_text = await make_api_request(
                session, url, headers, method="post", data=service_request.model_dump()
            )
            # resp_text = await resp.text()
            logger.debug("Response: {}", json.dumps(resp_text, indent=4))
            resp.raise_for_status()
            logger.info("Created service")
            return Service.model_validate_json(resp_text)
        except Exception as e:
            logger.error(
                "Failed to create service: {}",
                json.dumps(resp_text, indent=4) if resp_text else e,
            )


async def update_service_node_relationship(
    base_url: str, token: str, service_node_relationship: ServiceNodeRelationship
) -> None:
    """Update the service node relationship with the given request.

    Args:
        base_url (str): The base URL of the API.
        token (str): The token to use.
        service_node_relationship (ServiceNodeRelationship): The service
            node relationship.
    """
    logger.info("Updating service node relationship ...")
    resp_text: Optional[str] = None
    url = f"{base_url}/services/node_relationships"
    logger.debug("PUT {}", url)
    headers = {"Authorization": f"Bearer {token}"}

    async with aiohttp.ClientSession() as session:
        try:
            resp, resp_text = await make_api_request(
                session,
                url,
                headers,
                method="put",
                data=service_node_relationship.model_dump(),
            )
            logger.debug("Response: {}", json.dumps(resp_text, indent=4))
            resp.raise_for_status()
            logger.info("Updated service node relationship")
        except Exception as e:
            logger.error(
                "Failed to update service node relationship: {}",
                json.dumps(resp_text, indent=4) if resp_text else e,
            )
