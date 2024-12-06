from abc import ABC, abstractmethod
from typing import List, Optional, Union

import aiohttp
from ambient_backend_api_client import (
    ApiClient,
    Cluster,
    ClustersApi,
    Configuration,
    DockerClusterData,
)
from ambient_backend_api_client import NodeOutput as Node
from ambient_backend_api_client import NodeRoleEnum, NodesApi, UpdateCluster
from result import Err, Ok, Result

from ambient_client_common.models.cluster_diff import (
    ClusterDiff,
    ReconciliationPlan,
    ReconciliationStep,
)
from ambient_client_common.repositories.docker_repo import DockerRepo
from ambient_client_common.repositories.node_repo import NodeRepo
from ambient_client_common.utils import logger


class ClusterConfigService(ABC):
    @abstractmethod
    async def generate_diff(self, cluster_id: int) -> Result[ClusterDiff, str]:
        pass

    @abstractmethod
    async def plan_reconciliation(
        self, diff: ClusterDiff
    ) -> Result[ReconciliationPlan, str]:
        pass

    @abstractmethod
    async def reconcile(self, plan: ReconciliationPlan) -> Result[str, str]:
        pass


class DockerClusterConfigService(ClusterConfigService):
    def __init__(
        self, docker_repo: DockerRepo, node_repo: NodeRepo, api_config: Configuration
    ):
        self.api_config = api_config
        self.docker_repo = docker_repo
        self.node_repo = node_repo

    async def refresh_node(self) -> Node:
        current_node = self.node_repo.get_node_data()
        updated_node: Optional[Node] = None
        resp_text: Optional[str] = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_config.host}/nodes/{current_node.id}",
                    headers={"Authorization": f"Bearer {self.api_config.access_token}"},
                ) as response:
                    resp_text = await response.text()
                    response.raise_for_status()
                    node_d = await response.json()
                    updated_node = Node.model_validate(node_d)
                    logger.debug(
                        "Node refreshed: {}", updated_node.model_dump_json(indent=4)
                    )
        except Exception as e:
            err_msg = f"Failed to refresh node: {e}"
            if resp_text:
                err_msg += f"\n{resp_text}"
            logger.error(err_msg)
            raise Exception(err_msg) from e

        if updated_node:
            self.node_repo.save_node_data(updated_node)
            return updated_node

    async def generate_diff(
        self, cluster_id: Union[int, None]
    ) -> Result[ClusterDiff, str]:
        logger.info("Generating diff for cluster: {}", cluster_id)

        # retrieve current state from device
        docker_info = self.docker_repo.get_docker_info()
        logger.debug(f"Current state: {docker_info.model_dump_json(indent=4)}")

        if cluster_id is None:
            logger.info("Desired state is absent. Cluster should not exist.")
            return Ok(ClusterDiff(current_state=docker_info.Swarm, desired_state=None))

        # Fetch the desired state from the backend
        cluster: Optional[Cluster] = None
        async with ApiClient(self.api_config) as api_client:
            clusters_api = ClustersApi(api_client)
            try:
                cluster = await clusters_api.get_cluster_clusters_cluster_id_get(
                    cluster_id
                )
                logger.debug(f"Fetched cluster: {cluster.model_dump_json(indent=4)}")
            except Exception as e:
                return Err(f"Failed to fetch cluster {cluster_id} from backend: {e}")

        return Ok(ClusterDiff(current_state=docker_info.Swarm, desired_state=cluster))

    async def plan_reconciliation(
        self, diff: ClusterDiff
    ) -> Result[ReconciliationPlan, str]:
        logger.info("Planning reconciliation ...")
        reconciliation_plan = ReconciliationPlan(
            steps=[], cluster_id=diff.desired_state.id if diff.desired_state else None
        )
        logger.debug(f"Diff: {diff.model_dump_json(indent=4)}")
        if diff.desired_state is None:
            logger.info("Desired state is absent. Cluster should not exist.")
            reconciliation_plan.steps.append(
                ReconciliationStep(
                    action=handle_cluster_should_not_exist(
                        docker_repo=self.docker_repo
                    ),
                    changes={"cluster_id": None},
                )
            )
            logger.debug(f"Reconciliation plan: {reconciliation_plan}")
            return Ok(reconciliation_plan)

        try:
            manager_nodes: List[Node] = await self._get_manager_nodes(
                diff.desired_state.id
            )
            logger.debug("retrived {} manager nodes", len(manager_nodes))
            node = await self.refresh_node()
            if self.node_repo.get_node_data().role == NodeRoleEnum.MANAGER:
                # handle cluster manager join or create
                logger.info("Node role is manager.")
                reconciliation_plan.steps.append(
                    ReconciliationStep(
                        action=handle_cluster_manager_join_or_create(
                            cluster=diff.desired_state,
                            manager_nodes=manager_nodes,
                            docker_repo=self.docker_repo,
                            api_config=self.api_config,
                            node=node,
                        ),
                        changes={"cluster_id": diff.desired_state.id},
                    )
                )
            elif self.node_repo.get_node_data().role == NodeRoleEnum.WORKER:
                # handle cluster worker join
                logger.info("Node role is worker.")
                reconciliation_plan.steps.append(
                    ReconciliationStep(
                        action=handle_cluster_worker_join(),
                        msg="Cluster worker will join cluster.",
                    )
                )
            else:
                logger.error("Node role is not set.")
                return Err("Node role is not set.")
        except Exception as e:
            logger.error(f"Failed to plan reconciliation: {e}")
            return Err(f"Failed to plan reconciliation: {e}")

        logger.debug(f"Reconciliation plan: {reconciliation_plan}")
        return Ok(reconciliation_plan)

    async def reconcile(self, plan: ReconciliationPlan) -> Result[str, str]:
        logger.info("Reconciling ...")
        return await plan.execute()

    async def _get_manager_nodes(self, cluster_id: int) -> List[Node]:
        async with ApiClient(self.api_config) as api_client:
            nodes_api = NodesApi(api_client)
            try:
                nodes_response = await nodes_api.get_nodes_nodes_get(
                    role="manager", cluster_id=cluster_id
                )
                nodes = nodes_response.results
                return nodes
            except Exception as e:
                logger.error(f"Failed to fetch manager nodes: {e}")
                return []


# handle cluster should not exist
async def handle_cluster_should_not_exist(docker_repo: DockerRepo) -> Result[str, str]:
    if docker_repo.is_node_part_of_cluster():
        docker_repo.leave_cluster()
        return Ok("Cluster left.")
    else:
        logger.info("Cluster does not exist on this node.")
        return Ok("Cluster does not exist on this node.")


async def handle_cluster_manager_join_or_create(
    cluster: Cluster,
    manager_nodes: List[Node],
    node: Node,
    docker_repo: DockerRepo,
    api_config: Configuration,
) -> Result[str, str]:
    logger.info("Handling cluster manager join or create ...")
    # is this node already part of a swarm?
    docker_info = docker_repo.get_docker_info()
    if docker_repo.is_node_part_of_cluster():
        # yes, this node is already part of a swarm
        logger.info("This node is already part of a swarm.")
        # does the cluster ID match the current cluster?
        if (
            cluster.docker_data
            and docker_info.Swarm.Cluster
            and (
                cluster.docker_data.cluster_id
                == docker_repo.get_docker_info().Swarm.Cluster.ID
            )
        ):
            # yes, the cluster ID matches the current cluster
            logger.info("Cluster ID matches the current cluster.")
            # is this node a manager?
            if docker_info.Swarm.NodeID in [
                remote_manager.NodeID
                for remote_manager in docker_info.Swarm.RemoteManagers
            ]:
                # yes, nothing to do
                logger.info("This node is already a manager in the cluster.")
                return Ok("This node is already a manager in the cluster.")
            else:
                # no, this node is not a manager
                # leave cluster and join as manager
                logger.info(
                    "This node is not a manager in the cluster. Leaving cluster ..."
                )
                docker_repo.leave_cluster()
                logger.info("Cluster left. Joining cluster as a manager ...")
                return await join_cluster(
                    NodeRoleEnum.MANAGER, manager_nodes, docker_repo
                )
        else:
            # no, the cluster ID does not match the current cluster
            # leave cluster and join as manager
            logger.info(
                "Cluster ID does not match the current cluster. Leaving cluster ..."
            )
            docker_repo.leave_cluster()
            logger.info("Cluster left. Joining cluster as a manager ...")
            # make sure that this isn't the first node in the cluster
            if manager_nodes != [node]:
                logger.info("This is not the first node in the cluster.")
                logger.debug("Manager nodes: {}", manager_nodes)
                logger.debug("Current node: {}", [node])
                return await join_cluster(
                    NodeRoleEnum.MANAGER, manager_nodes, docker_repo
                )
            logger.info("This is the first node in the cluster.")

    # no, this node is not part of a swarm
    logger.info("This node is not part of a swarm.")
    # has the cluster been initiated?

    if len(manager_nodes) > 1:
        # yes, the cluster has been initiated
        # join as manager
        logger.info("Cluster has been initiated. Joining cluster as a manager ...")
        return await join_cluster(NodeRoleEnum.MANAGER, manager_nodes, docker_repo)
    else:
        # no, the cluster has not been initiated
        # create cluster
        logger.info("Cluster has not been initiated. Creating cluster ...")
        ad_addr_if = next(
            (
                i.ipv4_address
                for i in node.interfaces
                if i.name.startswith(("eth", "wlan"))
            ),
            None,
        )
        if not ad_addr_if:
            logger.error("Failed to get advertise address.")
            return Err("Failed to get advertise address.")
        docker_repo.create_cluster(ad_addr_if)
        logger.info("Cluster created.")
        # update cluster initiated status
        docker_info = docker_repo.get_docker_info()
        updated_cluster_data = UpdateCluster.model_validate(cluster.model_dump())
        updated_cluster_data.docker_data = DockerClusterData(
            initiated=True,
            cluster_id=docker_info.Swarm.Cluster.ID,
            remote_managers=[
                rm.model_dump() for rm in docker_info.Swarm.RemoteManagers
            ],
        )
        return await update_cluster_docker_data(
            updated_cluster_data, cluster.id, api_config
        )


async def join_cluster(
    role: NodeRoleEnum, manager_nodes: List[Node], docker_repo: DockerRepo
) -> Result[str, str]:
    logger.info("Joining cluster as a manager ...")
    # cycle through manager nodes until we successfully join the cluster
    join_token: Optional[str] = None
    for manager_node in manager_nodes:
        logger.info(
            "Getting join token from manager node: {} - {}",
            manager_node.name,
            manager_node.docker_swarm_info.node_addr,
        )
        join_token = await get_join_token(
            manager_node.docker_swarm_info.node_addr, role.value
        )
        if join_token:
            logger.info("Join token received: {}", join_token)
            break
    if join_token:
        logger.info("Joining cluster ...")
        if docker_repo.join_cluster(
            remote_addrs=[node.docker_swarm_info.node_addr for node in manager_nodes],
            join_token=join_token,
        ):
            logger.info("Cluster joined successfully.")
            return Ok("Cluster joined successfully.")
        else:
            logger.error("Failed to join cluster.")
            return Err("Failed to join cluster.")
    else:
        logger.error("Failed to get join token.")
        return Err("Failed to get join token.")


async def handle_cluster_worker_join(
    cluster: Cluster,
    manager_nodes: List[Node],
    docker_repo: DockerRepo,
    api_config: Configuration,
) -> Result[str, str]:
    # is this node already part of a swarm?
    docker_info = docker_repo.get_docker_info()
    if docker_repo.is_node_part_of_cluster():
        # yes, this node is already part of a swarm
        # does the cluster ID match the current cluster?
        if cluster.docker_data.cluster_id == docker_info.Swarm.Cluster.ID:
            # yes, the cluster ID matches the current cluster
            # is this node a worker?
            if docker_info.Swarm.NodeID not in [
                manager.NodeID for manager in docker_info.Swarm.RemoteManagers
            ]:
                # yes, nothing to do
                logger.info("This node is already a worker in the cluster.")
                return Ok("This node is already a worker in the cluster.")
            else:
                # no, this node is not a worker
                # leave cluster and join as worker
                logger.info(
                    "This node is not a worker in the cluster. Leaving cluster ..."
                )
                docker_repo.leave_cluster()
                logger.info("Cluster left. Joining cluster as a worker ...")
                return await join_cluster(
                    NodeRoleEnum.WORKER, manager_nodes, docker_repo
                )
        else:
            # no, the cluster ID does not match the current cluster
            # leave cluster and join as worker
            logger.info(
                "Cluster ID does not match the current cluster. Leaving cluster ..."
            )
            docker_repo.leave_cluster()
            logger.info("Cluster left. Joining cluster as a worker ...")
            return await join_cluster(NodeRoleEnum.WORKER, manager_nodes, docker_repo)
    else:
        # no, this node is not part of a swarm
        # join as worker
        logger.info("Joining cluster as a worker ...")
        return await join_cluster(NodeRoleEnum.WORKER, manager_nodes, docker_repo)


async def get_join_token(manager_addr: str, role: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://{manager_addr}/data/swarm/join-token?role={role}"
        ) as response:
            response.raise_for_status()
            data = await response.json()
            logger.debug("Join token response: {}", data)
            return data["join_token"]


async def update_cluster_docker_data(
    data: UpdateCluster, cluster_id: int, api_config: Configuration
) -> Result[str, str]:
    logger.info("Patching cluster with data: {}", data.model_dump_json(indent=4))
    logger.debug("Cluster ID: {}", cluster_id)

    try:
        async with ApiClient(api_config) as api_client:
            clusters_api = ClustersApi(api_client)
            cluster = await clusters_api.update_cluster_clusters_cluster_id_put(
                cluster_id, data
            )
            logger.debug("Cluster patched: {}", cluster.model_dump_json(indent=4))
            return Ok("Cluster patched successfully")
    except Exception as e:
        err_msg = f"Failed to PUT cluster: {e}"
        logger.error(err_msg)
        return Err(err_msg)
