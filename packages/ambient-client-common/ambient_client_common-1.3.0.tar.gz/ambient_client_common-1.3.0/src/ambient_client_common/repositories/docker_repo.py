import json
from typing import List

import docker

from ambient_client_common.models.docker_models import DockerInfo, SwarmAttrs
from ambient_client_common.utils import logger


class DockerRepo:
    def __init__(self, client: docker.DockerClient):
        self.client = client
        self.api_client = client.api

    def is_node_part_of_cluster(self) -> bool:
        return self.get_docker_info().Swarm.Cluster is not None

    def get_docker_info(self) -> DockerInfo:
        logger.info("Retrieving Docker info")
        docker_info_dict = self.api_client.info()
        logger.debug("Docker info: {}", json.dumps(docker_info_dict, indent=4))
        return DockerInfo.model_validate(docker_info_dict)

    def get_swarm_info(self) -> SwarmAttrs:
        swarm_dict = self.client.swarm.attrs
        logger.debug("Swarm info: {}", json.dumps(swarm_dict, indent=4))
        return SwarmAttrs.model_validate(swarm_dict)

    def leave_cluster(self) -> str:
        """Leave the cluster

        Returns:
            str: the Cluster ID that was left
        """
        cluster_id = self.get_docker_info().Swarm.Cluster.ID
        logger.info("Removing cluster: {}", cluster_id)
        self.client.swarm.leave(force=True)
        logger.info("Cluster removed")
        return cluster_id

    def create_cluster(self, advertise_addr: str) -> None:
        # cluster_name = cluster.name
        logger.info("Creating cluster with advertise address {}", advertise_addr)
        ad_addr = self.__get_advertise_addr()
        if not ad_addr:
            ad_addr = advertise_addr
        # listen_addr = ad_addr
        self.client.swarm.init(
            advertise_addr=ad_addr,
        )

    def join_cluster(self, remote_addrs: List[str], join_token: str) -> bool:
        logger.info("Joining cluster")
        return self.client.swarm.join(remote_addrs, join_token)

    def __get_advertise_addr(self):
        return self.get_docker_info().Swarm.NodeAddr
