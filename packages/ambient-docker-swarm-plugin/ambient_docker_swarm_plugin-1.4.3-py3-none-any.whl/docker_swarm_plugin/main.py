from logging import Logger
from typing import Any, Optional, Union

import aiohttp
from ambient_backend_api_client import ApiClient, Cluster, ClustersApi, Configuration
from ambient_backend_api_client import NodeOutput as Node
from ambient_base_plugin import BasePlugin, hookimpl
from ambient_base_plugin.models.configuration import ConfigPayload
from ambient_base_plugin.models.message import Message
from docker_swarm_plugin.services.cluster_config_service import (
    ClusterConfigService,
    DockerClusterConfigService,
)
from docker_swarm_plugin.services.service_config_service import ServiceConfigSvc
from fastapi import HTTPException
from pydantic import ValidationError

from ambient_client_common import config
from ambient_client_common.models.docker_models import SwarmAttrs
from ambient_client_common.repositories.docker_repo import DockerRepo
from ambient_client_common.repositories.node_repo import NodeRepo

logger: Optional[Logger] = None


class DockerSwarmPlugin(BasePlugin):
    def __init__(self) -> None:
        self.node_repo: Optional[NodeRepo] = None
        self.docker_repo: Optional[DockerRepo] = None
        self.api_config: Optional[Configuration] = None
        self.logger: Optional[Logger] = None
        self.cluster_config_service: Optional[ClusterConfigService] = None
        self.service_config_svc: Optional[ServiceConfigSvc] = None

    @hookimpl
    async def run_system_sweep(self, node: Node) -> None:
        logger.info("Running system sweep from the Docker Swarm Plugin ...")
        if node.role.value == "worker":
            logger.info("Cannot run docker swarm system sweep on worker node")
            return
        await self.service_config_svc.run_system_sweep(node)

    async def configure(
        self, config: ConfigPayload, logger: Union[Logger, Any] = None
    ) -> None:
        self.node_repo = config.node_repo
        self.docker_repo = config.docker_repo
        self.api_config = config.api_config
        self.set_logger(logger)
        self.cluster_config_service = DockerClusterConfigService(
            docker_repo=self.docker_repo,
            node_repo=self.node_repo,
            api_config=self.api_config,
        )
        self.service_config_svc = ServiceConfigSvc(
            docker_repo=self.docker_repo, config_payload=config
        )
        logger.info("Configured DockerSwarmPlugin")

    def set_logger(self, logger_: Logger) -> None:
        global logger
        logger = logger_
        self.logger = logger_

    async def handle_event(self, message: Message) -> None:
        """Handle incoming messages

        Args:
            message (Message): Incoming message

        Returns:
            None
        """
        logger.info("Handling event [from docker swarm plugin handler] ...")
        if "CLUSTER_EVENT" in message.topic:
            return await self.handle_cluster_event(message)
        elif "SERVICE_EVENT" in message.topic:
            service_id = int(message.topic.split("/")[-2])
            logger.info(f"Handling service event for service: {service_id}")
            return await self.service_config_svc.handle_service_event(
                service_id=service_id
            )
        else:
            logger.error(f"Unsupported message topic: {message.topic}")

    async def handle_cluster_event(self, message: Message) -> None:
        """Handle cluster event

        Args:
            message (Message): Incoming message

        Returns:
            None
        """
        logger.info("Handling cluster event ...")
        logger.debug(f"Handling cluster event: {message.model_dump_json(indent=4)}")
        await self.reconcile_cluster()

    async def reconcile_cluster(self) -> None:
        # fetch node from from backend
        try:
            current_node_data: Node = self.node_repo.get_node_data(strict=True)
            logger.info("retrieved node data from local repo")
            fetched_node_data = await fetch_node_data(
                current_node_data.id, self.api_config
            )
            logger.info("fetched node data from backend")
            self.node_repo.save_node_data(fetched_node_data)
            logger.debug(
                f"Fetched node data: {fetched_node_data.model_dump_json(indent=4)}"
            )
        except Exception as e:
            logger.error(f"Failed to fetch node data: {e}")
            return

        try:
            # create diff
            diff_result = await self.cluster_config_service.generate_diff(
                cluster_id=fetched_node_data.cluster_id
            )
            if diff_result.is_err():
                logger.error(f"Failed to generate diff: {diff_result.unwrap_err()}")
                return
            diff = diff_result.unwrap()
            logger.debug(f"Generated diff: {diff.model_dump_json(indent=4)}")

            # generate plan
            logger.debug("Generating reconciliation plan ...")
            plan_result = await self.cluster_config_service.plan_reconciliation(diff)
            if plan_result.is_err():
                logger.error(f"Failed to generate plan: {plan_result.unwrap_err()}")
                return
            plan = plan_result.unwrap()
            logger.debug(f"Generated plan: {plan}")

            # execute plan
            logger.debug("Executing reconciliation plan ...")
            await self.cluster_config_service.reconcile(plan=plan)
        except Exception as e:
            logger.error(f"Failed to reconcile cluster: {e}")
            return

    async def handle_api_request(
        self, method: str, path: str, data: Optional[None] = None
    ) -> Any:
        logger.info("Handling API request ...")
        method = method.lower()
        if method.upper() == "POST" and "onboarding" in path:
            logger.info("Handling onboarding request ...")
            return await self.handle_onboarding_request()
        elif method.upper() == "GET" and "swarm_info" in path:
            return await self.get_swarm_info()
        logger.error("Unsupported method. Method: {}, Path: {}", method, path)
        raise HTTPException(status_code=405, detail="Method not allowed")

    async def handle_onboarding_request(self) -> None:
        await self.reconcile_cluster()

    async def get_swarm_info(self) -> SwarmAttrs:
        logger.info("Getting swarm info ...")
        try:
            swarm_info = self.docker_repo.get_swarm_info()
        except ValidationError as e:
            logger.error(f"Failed to get swarm info: {e}")
            raise HTTPException(status_code=400, detail="Failed to get swarm info")
        return swarm_info


async def fetch_node_data(node_id: int, api_config: Configuration) -> Node:
    logger.info("Fetching node data from backend [Node ID: {}]", node_id)
    logger.debug("api_config token: {}", api_config.access_token)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{config.settings.backend_api_url}/nodes/{node_id}",
            headers={
                "Authorization": f"Bearer {api_config.access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        ) as response:
            response.raise_for_status()
            node_data = await response.json()
            return Node.model_validate(node_data)


async def fetch_cluster_data(cluster_id: str, api_config: Configuration) -> Cluster:
    async with ApiClient(api_config) as api_client:
        clusters_api = ClustersApi(api_client)
        cluster = await clusters_api.get_cluster_clusters_cluster_id_get(cluster_id)
        return cluster
