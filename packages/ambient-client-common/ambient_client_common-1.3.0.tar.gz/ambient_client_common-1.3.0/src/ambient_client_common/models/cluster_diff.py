from typing import Any, Dict, List, Optional, Tuple, Union

from ambient_backend_api_client import Cluster
from pydantic import BaseModel, model_validator
from result import Err, Ok, Result

from ambient_client_common.models.docker_models import DockerSwarmInfo
from ambient_client_common.utils import logger


class DiffableFields(BaseModel):
    name: Tuple[str, str]
    name_equal: bool = False

    @model_validator(mode="after")
    def validate_name(self):
        if self.name[0] == self.name[1]:
            self.name_equal = True


class ClusterDiff(BaseModel):
    desired_state: Union[Cluster, None]
    current_state: DockerSwarmInfo
    diff: Optional[DiffableFields] = None

    @model_validator(mode="after")
    def generate_diff(self):
        self.diff = DiffableFields(
            name=(
                self.desired_state.name if self.desired_state else "",
                (
                    self.current_state.Cluster.Spec.Name
                    if self.current_state.Cluster
                    else ""
                ),
            )
        )


class ReconciliationStep(BaseModel):
    changes: Dict[str, Any]
    action: Any

    async def execute(self) -> Result[str, str]:
        return await self.action


class ReconciliationPlan(BaseModel):
    steps: List[ReconciliationStep]
    cluster_id: Optional[int] = None
    msg: Optional[str] = None

    async def execute(self) -> Result[str, str]:
        logger.info(f"Executing reconciliation plan for cluster {self.cluster_id}")
        try:
            for step in self.steps:
                logger.info(f"Executing reconciliation step: {step}")
                result = await step.execute()
                if result.is_err():
                    logger.error(
                        f"Reconciliation failed for cluster \
    {self.cluster_id}: {result.unwrap_err()}"
                    )
                    return result
                else:
                    logger.info(f"Reconciliation step successful: {result.unwrap()}")
                    step.changes = {"status": "success", "msg": result.unwrap()}
        except Exception as e:
            logger.error(f"Reconciliation failed for cluster {self.cluster_id}: {e}")
            return Err(f"Reconciliation failed for cluster {self.cluster_id}: {e}")
        return Ok("Reconciliation successful")
