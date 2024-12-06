import dataclasses
from typing import Literal, Optional, Union

from dataclasses_json import dataclass_json

from databricks.rag_eval.utils.enum_utils import StrEnum


class SchedulePauseStatus(StrEnum):
    UNPAUSED = "UNPAUSED"
    PAUSED = "PAUSED"


@dataclass_json
@dataclasses.dataclass
class PeriodicMonitoringConfig:
    """
    Configuration for a periodic monitor of a serving endpoint. All fields are optional for upsert
    semantics.
    """

    interval: Optional[int] = None
    unit: Optional[Union[Literal["HOURS"] | Literal["DAYS"] | Literal["WEEKS"]]] = None


@dataclass_json
@dataclasses.dataclass
class MonitoringConfig:
    """
    Configuration for monitoring a serving endpoint. All fields are optional for upsert semantics.
    """

    sample: Optional[float] = None
    metrics: Optional[list[str]] = None
    periodic: Optional[PeriodicMonitoringConfig] = None
    paused: Optional[bool] = None


@dataclass_json
@dataclasses.dataclass
class Monitor:
    """
    The monitor for a serving endpoint.
    """

    endpoint_name: str
    dashboard_id: str
    evaluated_traces_table: str
    monitoring_config: MonitoringConfig
    experiment_id: str
    workspace_path: str
