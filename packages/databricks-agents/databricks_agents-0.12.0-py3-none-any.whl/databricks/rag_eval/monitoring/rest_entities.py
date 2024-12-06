"""REST API entities for monitoring."""

import dataclasses
from typing import Literal, Optional

from dataclasses_json import config, dataclass_json

from . import entities

_FIELD_IS_UPDATABLE = "FIELD_IS_UPDATABLE"


@dataclass_json
@dataclasses.dataclass
class AssessmentConfig:
    name: Optional[str] = None


@dataclass_json
@dataclasses.dataclass
class EvaluationConfig:
    metrics: Optional[list[AssessmentConfig]] = None


@dataclass_json
@dataclasses.dataclass
class SamplingConfig:
    sampling_rate: Optional[float] = None


@dataclass_json
@dataclasses.dataclass
class ScheduleConfig:
    frequency_interval: Optional[int] = None
    frequency_unit: Optional[str] = None
    pause_status: Optional[Literal["UNPAUSED", "PAUSED"]] = None


def ExcludeIfNone(value):
    return value is None


@dataclass_json
@dataclasses.dataclass
class Monitor:
    experiment_id: Optional[str] = dataclasses.field(
        default=None,
        metadata={**config(exclude=ExcludeIfNone), _FIELD_IS_UPDATABLE: False},
    )
    workspace_path: Optional[str] = dataclasses.field(
        default=None,
        metadata={**config(exclude=ExcludeIfNone), _FIELD_IS_UPDATABLE: False},
    )
    evaluation_config: Optional[EvaluationConfig] = dataclasses.field(
        default=None, metadata=config(exclude=ExcludeIfNone)
    )
    sampling: Optional[SamplingConfig] = dataclasses.field(
        default=None, metadata=config(exclude=ExcludeIfNone)
    )
    schedule: Optional[ScheduleConfig] = dataclasses.field(
        default=None, metadata=config(exclude=ExcludeIfNone)
    )

    def get_update_mask(self) -> str:
        """Get the update mask for the fields that have changed."""
        return ",".join(
            field.name
            for field in dataclasses.fields(self)
            if getattr(self, field.name) is not None
            and field.metadata.get(_FIELD_IS_UPDATABLE, True)
        )


@dataclass_json
@dataclasses.dataclass
class MonitorInfo:
    monitor: Optional[Monitor] = None
    dashboard_id: Optional[str] = None
    evaluated_traces_table: Optional[str] = None

    def to_monitor(self, endpoint_name: str) -> entities.Monitor:
        """Converts the REST API response to a Python Monitor object."""
        monitor = self.monitor or Monitor()
        sampling_config = monitor.sampling or SamplingConfig()
        evaluation_config = monitor.evaluation_config or EvaluationConfig()
        schedule_config = monitor.schedule or ScheduleConfig()
        assessment_configs = evaluation_config.metrics or []
        return entities.Monitor(
            endpoint_name=endpoint_name,
            dashboard_id=self.dashboard_id,
            evaluated_traces_table=self.evaluated_traces_table,
            experiment_id=monitor.experiment_id,
            workspace_path=monitor.workspace_path,
            monitoring_config=entities.MonitoringConfig(
                sample=sampling_config.sampling_rate,
                metrics=[metric.name for metric in assessment_configs],
                periodic=entities.PeriodicMonitoringConfig(
                    interval=schedule_config.frequency_interval,
                    unit=schedule_config.frequency_unit,
                ),
                paused=(
                    schedule_config.pause_status == entities.SchedulePauseStatus.PAUSED
                ),
            ),
        )
