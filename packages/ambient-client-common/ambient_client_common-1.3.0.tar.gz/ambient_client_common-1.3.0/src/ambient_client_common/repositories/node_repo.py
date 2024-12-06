import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from ambient_backend_api_client import NodeOutput as Node

from ambient_client_common.utils import logger


class NodeRepo(ABC):
    @abstractmethod
    def save_node_data(self, node: Node) -> None:
        """Save the node data to the repository.

        Args:
            node (Node): Node data
        """

    @abstractmethod
    def get_node_data(self, strict: bool = False) -> Union[Node, None]:
        """Get the node data from the repository.

        Returns:
            Node: Node data or None if not found
            strict (bool): If True, raise an exception if the node data is not found
        """

    @abstractmethod
    def get_node_id(self) -> int:
        """Get the node ID.

        Returns:
            int: Node ID
        """

    @abstractmethod
    def clear_node_data(self) -> None:
        """Clear the node data from the repository."""


class FileNodeRepo(NodeRepo):
    def __init__(self):
        self.home_path = Path.home() / ".ambient"
        self.node_data_path = self.home_path / ".node_data.json"

        self._init_files()

    def _init_files(self):
        if not self.node_data_path.exists():
            self._write_to_file(self.node_data_path, b"")

    def _write_to_file(self, file_path: Path, data: bytes):
        with open(file_path, "wb") as f:
            f.write(data)

    def save_node_data(self, node: Node) -> None:
        self._write_to_file(
            self.node_data_path, node.model_dump_json(indent=4).encode()
        )

    def get_node_id(self) -> Union[int, None]:
        logger.debug("Reading node ID from file: {}", self.node_data_path)
        node_data = self.get_node_data()
        if node_data:
            logger.debug("Node ID: {}", node_data.id)
            return node_data.id
        return os.getenv("AMBIENT_NODE_ID", None)

    def get_node_data(self, strict: bool = False) -> Union[Node, None]:
        logger.debug("Reading node data from file: {}", self.node_data_path)
        with open(self.node_data_path, "rb") as f:
            contents = f.read().decode()
            logger.debug("Node data: {}", contents)
            if strict:
                return Node.model_validate_json(contents)
            if not contents or contents == "":
                logger.info("No node data found")
                return None
            return Node.model_validate_json(contents)

    def clear_node_data(self) -> None:
        self._write_to_file(self.node_data_path, b"")
