from typing import Any, cast, Dict, List, Optional, Tuple, Union

from aporia.as_code.resources.base import BaseResource, CompareStatus
from aporia.as_code.resources.custom_metrics import CustomMetric
from aporia.as_code.resources.dataset import Dataset
from aporia.as_code.resources.version import Version
from aporia.sdk.client import Client
from aporia.sdk.datasets import DatasetSchema, FieldType
from aporia.sdk.messaging import MessagingIntegrationType
from aporia.sdk.monitors import (
    AverageMethod,
    BaselineConfiguration,
    create_monitor_configuration,
    DetectionMethod,
    FocalConfiguration,
    MetricType,
)
from aporia.sdk.monitors import Monitor as _Monitor
from aporia.sdk.monitors import (
    MonitorConfiguration,
    MonitorType,
    PeriodType,
    SegmentIdentification,
    Severity,
    ThresholdConfiguration,
    TimePeriod,
)
from aporia.sdk.segments import Segment


def _is_feature_monitor(monitor_type: MonitorType) -> bool:
    return monitor_type in [
        MonitorType.DATA_DRIFT,
        MonitorType.MISSING_VALUES,
        MonitorType.METRIC_CHANGE,
        MonitorType.NEW_VALUES,
        MonitorType.VALUES_RANGE,
    ]


def _is_prediction_monitor(monitor_type: MonitorType) -> bool:
    return monitor_type in [
        MonitorType.PREDICTION_DRIFT,
        MonitorType.MISSING_VALUES,
        MonitorType.PERFORMANCE_DEGRADATION,
        MonitorType.VALUES_RANGE,
        MonitorType.NEW_VALUES,
    ]


class Monitor(BaseResource):
    def __init__(
        self,
        resource_name: str,
        /,
        *,
        # Monitoring Types
        monitor_type: Union[MonitorType, str],
        detection_method: Union[DetectionMethod, str],
        # Dataset Parameters
        focal: FocalConfiguration,
        # Alert parameters
        severity: Union[Severity, str],
        # Optional Monitor Parameters
        scheduling: Optional[str] = None,
        comment: Optional[str] = None,
        is_active: bool = True,
        creator: Optional[str] = None,
        version: Optional[Version] = None,
        version_id: Optional[str] = None,
        segment: Optional[Segment] = None,
        segment_id: Optional[str] = None,
        segment_value: Optional[Any] = None,
        # Optional Dataset Parameters
        baseline: Optional[BaselineConfiguration] = None,
        baseline_segment: Optional[Segment] = None,
        baseline_version: Optional[Version] = None,
        dataset: Optional[Dataset] = None,
        raw_inputs: Optional[List[str]] = None,
        features: Optional[List[str]] = None,
        predictions: Optional[List[str]] = None,
        is_embedding_monitor: bool = False,
        min_focal_prediction_count: Optional[int] = None,
        min_baseline_prediction_count: Optional[int] = None,
        # Optional Logic Evaluation Parameters
        percentage: Optional[int] = None,
        thresholds: Optional[ThresholdConfiguration] = None,
        sensitivity: Optional[float] = None,
        alert_on_increase_only: Optional[bool] = None,
        min: Optional[int] = None,
        max: Optional[int] = None,
        staleness_period: Optional[TimePeriod] = None,
        distance: Optional[float] = None,
        new_values_ratio_threshold: Optional[float] = None,
        new_values_count_threshold: Optional[int] = None,
        # Optional Metric Parameters
        metric: Optional[Union[MetricType, str]] = None,
        k: Optional[int] = None,
        prediction_class: Optional[Any] = None,
        prediction_threshold: Optional[float] = None,
        average_method: Optional[Union[AverageMethod, str]] = None,
        custom_metric: Optional[CustomMetric] = None,
        custom_metric_id: Optional[str] = None,
        quantile: Optional[float] = None,
        # Optional Alert Parameters
        messaging: Optional[Dict[MessagingIntegrationType, List[str]]] = None,
        emails: Optional[List[str]] = None,
        group_by_time: Optional[bool] = None,
        group_by_entity: Optional[bool] = None,
        alert_group_time_unit: Optional[PeriodType] = None,
        alert_group_time_quantity: Optional[int] = None,
        # Optional rename
        name: Optional[str] = None,
    ):
        self.name = resource_name
        if name is None:
            name = resource_name

        monitor_type = MonitorType(monitor_type)
        detection_method = DetectionMethod(detection_method)
        severity = Severity(severity)

        # TODO: Add by types
        use_predictions = _is_prediction_monitor(monitor_type)
        use_features = _is_feature_monitor(monitor_type)

        if dataset is not None:
            dataset_schema = cast(DatasetSchema, dataset._args["schema"])
            if len(dataset_schema.raw_inputs) > 0:
                raw_inputs = [
                    raw_input.name
                    for raw_input in dataset_schema.raw_inputs
                    if (raw_input.type is FieldType.EMBEDDING and is_embedding_monitor)
                    or (raw_input.type is not FieldType.EMBEDDING and not is_embedding_monitor)
                ]
            if len(dataset_schema.features) > 0:
                features = [
                    feature.name
                    for feature in dataset_schema.features
                    if (feature.type is FieldType.EMBEDDING and is_embedding_monitor)
                    or (feature.type is not FieldType.EMBEDDING and not is_embedding_monitor)
                ]
            if len(dataset_schema.predictions) > 0:
                predictions = [
                    prediction.name
                    for prediction in dataset_schema.predictions
                    if (prediction.type is FieldType.EMBEDDING and is_embedding_monitor)
                    or (prediction.type is not FieldType.EMBEDDING and not is_embedding_monitor)
                ]

        monitor_configuration = create_monitor_configuration(
            monitor_type=monitor_type,
            detection_method=detection_method,
            focal=focal,
            severity=severity,
            baseline=baseline,
            raw_inputs=raw_inputs if use_features else None,
            features=features if use_features else None,
            predictions=predictions if use_predictions else None,
            is_embedding_monitor=is_embedding_monitor,
            metric=metric,
            percentage=percentage,
            thresholds=thresholds,
            sensitivity=sensitivity,
            alert_on_increase_only=alert_on_increase_only,
            min=min,
            max=max,
            staleness_period=staleness_period,
            min_focal_prediction_count=min_focal_prediction_count,
            min_baseline_prediction_count=min_baseline_prediction_count,
            custom_metric_id=custom_metric.name
            if custom_metric is not None
            else custom_metric_id
            if custom_metric_id is not None
            else None,
            distance=distance,
            new_values_count_threshold=new_values_count_threshold,
            new_values_ratio_threshold=new_values_ratio_threshold,
            messaging=messaging,
            segment_identification=SegmentIdentification(group="PLACEHOLDER", value=segment_value)
            if segment is not None
            else SegmentIdentification(group=segment_id, value=segment_value)
            if segment_id is not None
            else None,
            version=version_id if version_id is not None else None,
            emails=emails,
            k=k,
            prediction_class=prediction_class,
            prediction_threshold=prediction_threshold,
            average_method=AverageMethod(average_method) if average_method is not None else None,
            quantile=quantile,
            group_by_time=group_by_time,
            group_by_entity=group_by_entity,
            alert_group_time_unit=alert_group_time_unit,
            alert_group_time_quantity=alert_group_time_quantity,
        )

        # TODO: Test these things. Also with update
        if segment is not None:
            segment.dependants.append(
                (
                    self,
                    lambda data, monitor: monitor.setarg("segment_id", data["id"]),
                )
            )
        if baseline_segment is not None:
            baseline_segment.dependants.append(
                (
                    self,
                    lambda data, monitor: monitor.setarg("baseline_segment_id", data["id"]),
                )
            )
        if baseline_version is not None:
            baseline_version.dependants.append(
                (
                    self,
                    lambda data, monitor: monitor.setarg("baseline_version_id", data["id"]),
                )
            )
        if version is not None:
            version.dependants.append(
                (self, lambda data, monitor: monitor.setarg("version_id", data["id"]))
            )
        if custom_metric is not None:
            custom_metric.dependants.append(
                (self, lambda data, monitor: monitor.setarg("custom_metric_id", data["id"]))
            )

        self._args = {
            "name": name,
            "monitor_type": monitor_type,
            "configuration": monitor_configuration,
            "is_active": is_active,
        }

        if scheduling is not None:
            self._args["scheduling"] = scheduling
        if comment is not None:
            self._args["comment"] = comment
        if creator is not None:
            self._args["creator"] = creator

    def setarg(self, arg_name: str, arg_value: Any):
        # Model ID is added to the configuration by the SDK
        if arg_name == "segment_id":
            monitor_configuration = cast(MonitorConfiguration, self._args["configuration"])
            monitor_configuration.identification.segment.group = arg_value
            return
        if arg_name == "baseline_segment_id":
            monitor_configuration = cast(MonitorConfiguration, self._args["configuration"])
            monitor_configuration.baseline.segmentGroupId = arg_value
            return
        if arg_name == "baseline_version_id":
            monitor_configuration = cast(MonitorConfiguration, self._args["configuration"])
            monitor_configuration.baseline.model_version_id = arg_value
            return
        if arg_name == "version_id":
            monitor_configuration = cast(MonitorConfiguration, self._args["configuration"])
            monitor_configuration.identification.models.version = arg_value
            return
        if arg_name == "custom_metric_id":
            monitor_configuration = cast(MonitorConfiguration, self._args["configuration"])
            monitor_configuration.metric.id = arg_value
            return
        self._args[arg_name] = arg_value

    def compare(self, resource_data: Dict) -> CompareStatus:
        if self._args["configuration"].identification.models.id == "":
            self._args["configuration"].identification.models.id = self._args["model_id"]
        if all(
            [
                self._args["name"] == resource_data["name"],
                self._args.get("comment") == resource_data["comment"],
                self._args["is_active"] == resource_data["is_active"],
                self._args["configuration"].to_dict() == resource_data["configuration"],
            ]
        ):
            return CompareStatus.SAME
        elif any(
            [
                self._args["model_id"]
                != resource_data["configuration"]["identification"]["models"]["id"],
            ]
        ):
            return CompareStatus.MISMATCHED
        else:
            return CompareStatus.UPDATEABLE

    def create(self, client: Client) -> Tuple[str, Dict]:
        monitor = _Monitor.create(client=client, **self._args)
        return monitor.id, monitor.raw_data

    @classmethod
    def read(cls, client: Client, id: str) -> Dict:
        return _Monitor.read(client=client, id=id).raw_data

    def update(self, client: Client, id: str) -> Dict:
        monitor = _Monitor.read(client=client, id=id)
        monitor.update(**self._args)
        return monitor.raw_data

    @classmethod
    def delete(cls, client: Client, id: str):
        _Monitor.delete_by_id(client=client, id=id)

    def get_diff(self, resource_data: Dict) -> Dict:
        diffs = {}
        if self._args["name"] != resource_data["name"]:
            diffs["name"] = (resource_data["name"], self._args["name"])
        if "comment" in self._args:
            if self._args["comment"] != resource_data["comment"]:
                diffs["comment"] = (resource_data["comment"], self._args["comment"])
        if self._args["is_active"] != resource_data["is_active"]:
            diffs["is_active"] = (resource_data["is_active"], self._args["is_active"])
        if self._args["configuration"].to_dict() != resource_data["configuration"]:
            diffs["configuration"] = (
                resource_data["configuration"],
                self._args["configuration"].to_dict(),
            )
        return diffs
