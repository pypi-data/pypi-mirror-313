import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class RemoteManager(BaseModel):
    NodeID: str
    Addr: str


class DockerClusterVersion(BaseModel):
    Index: int


class DockerClusterOrchestration(BaseModel):
    TaskHistoryRetentionLimit: int


class DockerclusterRaft(BaseModel):
    SnapshotInterval: int
    KeepOldSnapshots: int
    LogEntriesForSlowFollowers: int
    ElectionTick: int
    HeartbeatTick: int


class DockerClusterDispatcher(BaseModel):
    HeartbeatPeriod: int


class DockerClusterCAConfig(BaseModel):
    NodeCertExpiry: int


class DockerClusterEncryptionConfig(BaseModel):
    AutoLockManagers: bool


class DockerClusterSpec(BaseModel):
    Name: str
    Labels: Dict[str, str]
    Orchestration: DockerClusterOrchestration
    Raft: DockerclusterRaft
    Dispatcher: DockerClusterDispatcher
    CAConfig: DockerClusterCAConfig
    TaskDefaults: Dict[str, Any]
    EncryptionConfig: DockerClusterEncryptionConfig


class DockerTLSInfo(BaseModel):
    TrustRoot: str
    CertIssuerSubject: str
    CertIssuerPublicKey: str


class DockerCluster(BaseModel):
    ID: str
    Version: DockerClusterVersion
    CreatedAt: datetime.datetime
    UpdatedAt: datetime.datetime
    Spec: DockerClusterSpec
    TLSInfo: DockerTLSInfo
    RootRotationInProgress: bool
    DefaultAddrPool: List[str]
    SubnetSize: int
    DataPathPort: int


class JoinTokensData(BaseModel):
    Worker: str
    Manager: str


class DockerRoleEnum(str, Enum):
    Manager = "manager"
    Worker = "worker"


class DockerSwarmInfo(BaseModel):
    NodeID: str
    NodeAddr: str
    LocalNodeState: str
    ControlAvailable: bool
    Error: str = ""
    RemoteManagers: Optional[List[RemoteManager]] = None
    Nodes: int = 0
    Managers: int = 0
    Cluster: Optional[DockerCluster] = None


class SwarmAttrs(BaseModel):
    ID: str
    Version: DockerClusterVersion
    CreatedAt: datetime.datetime
    UpdatedAt: datetime.datetime
    Spec: DockerClusterSpec
    TLSInfo: DockerTLSInfo
    SubnetSize: int
    DataPathPort: int
    JoinTokens: JoinTokensData


class DockerInfo(BaseModel):
    Swarm: DockerSwarmInfo
    Name: str
    Labels: List[Any]
    ID: str
    Containers: int
    ContainersRunning: int
    ContainersPaused: int
    ContainersStopped: int
    Images: int
