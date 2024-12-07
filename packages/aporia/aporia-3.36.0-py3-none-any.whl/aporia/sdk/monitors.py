from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

from pydantic import BaseModel, root_validator, validator

from aporia.sdk.base import BaseAporiaResource
from aporia.sdk.client import Client
from aporia.sdk.messaging import MessagingIntegrationType
from aporia.sdk.metrics import AverageMethod, MetricType

SEGMENT_ID_ALL_DATA = "ALLDATA"


class MonitorType(Enum):
    MODEL_ACTIVITY = "model_activity"
    DATA_DRIFT = "data_drift"
    PREDICTION_DRIFT = "prediction_drift"
    MISSING_VALUES = "missing_values"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    MODEL_STALENESS = "model_staleness"
    METRIC_CHANGE = "metric_change"
    CUSTOM_METRIC_MONITOR = "custom_metric"
    VALUES_RANGE = "values_range"
    NEW_VALUES = "new_values"


class DetectionMethod(Enum):
    ANOMALY = "anomaly"
    PERCENTAGE = "percentage"
    ABSOLUTE = "absolute"
    COMPARED_TO_SEGMENT = "segment"
    COMPARED_TO_TRAINING = "training"


class SourceType(Enum):
    SERVING = "SERVING"
    TRAINING = "TRAINING"


class PeriodType(Enum):
    HOURS = "h"
    DAYS = "d"
    WEEKS = "w"
    MONTHS = "M"


class TimePeriod(BaseModel):
    count: int
    type: PeriodType

    def to_string(self) -> str:
        return f"{self.count}{self.type.value}"

    @classmethod
    def from_string(cls, s) -> "TimePeriod":
        c = s[:-1]
        t = PeriodType(s[-1])
        return cls(count=c, type=t)


# TODO: Rename stuff to match Python conventions
class FocalConfiguration(BaseModel):
    source: SourceType = SourceType.SERVING
    timePeriod: Optional[TimePeriod] = None  # Missing for staleness
    skipPeriod: Optional[TimePeriod] = None
    alignBinsWithBaseline: Optional[bool] = None  # Needed (as True) for drift/histogram

    @validator("timePeriod", pre=True)
    def _parse_time_period(cls, value):
        if isinstance(value, str):
            return TimePeriod.from_string(value)
        return value

    @validator("skipPeriod", pre=True)
    def _parse_skip_period(cls, value):
        if isinstance(value, str):
            return TimePeriod.from_string(value)
        return value

    @validator("source")
    def _validate_source(cls, value):
        if value is not SourceType.SERVING:
            raise ValueError("For focal, source must always be serving")
        return value

    @validator("alignBinsWithBaseline")
    def _validate_align_bins_with_baseline(cls, value):
        if value is not True:
            raise ValueError("If alignBinsWithBaseline appears, it must be True")
        return value

    def to_dict(self):
        result = {
            "source": self.source.value,
        }
        if self.timePeriod is not None:
            result["timePeriod"] = self.timePeriod.to_string()
        if self.skipPeriod is not None:
            result["skipPeriod"] = self.skipPeriod.to_string()
        if self.alignBinsWithBaseline is not None:
            result["alignBinsWithBaseline"] = self.alignBinsWithBaseline

        return result


class BaselineConfiguration(BaseModel):
    source: SourceType
    timePeriod: Optional[TimePeriod] = None  # Actual time to compare to
    skipPeriod: Optional[TimePeriod] = None  # By default, equal to Focal. Doesn't exist on training
    aggregationPeriod: Optional[
        TimePeriod
    ] = None  # Does't exist on drift/histogram # TODO: Also on new values and value range. Check WTF is it
    segmentValue: Optional[Union[str, int, float]] = None
    segmentGroupId: Optional[str] = None
    model_version_id: Optional[str] = None

    @validator("timePeriod", pre=True)
    def _parse_time_period(cls, value):
        if isinstance(value, str):
            return TimePeriod.from_string(value)
        return value

    @validator("skipPeriod", pre=True)
    def _parse_skip_period(cls, value):
        if isinstance(value, str):
            return TimePeriod.from_string(value)
        return value

    @validator("aggregationPeriod", pre=True)
    def _parse_aggregation_period(cls, value):
        if isinstance(value, str):
            return TimePeriod.from_string(value)
        return value

    @validator("skipPeriod", always=True)
    def _validate_skip_period(cls, value, values):
        if values["source"] is SourceType.TRAINING:
            if value is not None:
                # TODO: Asserting this fails because UI does stupid things -.-
                # raise ValueError("For training baseline, skipPeriod must not appear")
                return None
        # TODO: This is basically defaulted in the global monitor validator
        # elif values["source"] is SourceType.SERVING:
        #     if value is None:
        #         raise ValueError("For serving baseline, skipPeriod must appear")
        return value

    @validator("timePeriod", always=True)
    def _validate_time_period(cls, value, values):
        if values["source"] is SourceType.SERVING:
            if value is None:
                raise ValueError("For serving baseline, timePeriod must appear")
        else:
            if value is not None:
                # TODO: Asserting this fails because UI does stupid things -.-
                # raise ValueError("For training baseline, timePeriod must not appear")
                return None
        return value

    def to_dict(self):
        result = {"source": self.source.value}
        if self.timePeriod is not None:
            result["timePeriod"] = self.timePeriod.to_string()
        if self.skipPeriod is not None:
            result["skipPeriod"] = self.skipPeriod.to_string()
        if self.aggregationPeriod is not None:
            result["aggregationPeriod"] = self.aggregationPeriod.to_string()
        # TODO: Validate these fields
        if self.segmentGroupId is not None:
            if self.segmentGroupId == SEGMENT_ID_ALL_DATA:
                result["segmentGroupId"] = None
            else:
                result["segmentGroupId"] = self.segmentGroupId
        if self.segmentValue is not None:
            result["segmentValue"] = self.segmentValue
        if self.model_version_id is not None:
            result["model_version_id"] = self.model_version_id

        return result


class MetricConfiguration(BaseModel):
    type: MetricType
    # Necessary for custom metrics
    id: Optional[str] = None
    # Necessary for general metrics
    metricAtK: Optional[int] = None  # TODO: Almost always 3 -.- Gubkin
    threshold: Optional[float] = None
    metricPerClass: Optional[Any] = None
    average: Optional[AverageMethod] = None
    quantile: Optional[float] = None
    # TODO: Maybe add class for Aporia metrics

    # TODO: Add validators for params by metric types

    @validator("id", always=True)
    def _validate_id(cls, value, values):
        if values["type"] is MetricType.CUSTOM_METRIC:
            if value is None:
                raise ValueError("For custom metrics, id must appear")
        else:
            if value is not None:
                raise ValueError("id must only appear for custom metrics")
        return value

    def to_dict(self):
        result = {"type": self.type.value}
        if self.id is not None:
            result["id"] = self.id
        if self.metricAtK is not None:
            result["metricAtK"] = self.metricAtK
        if self.threshold is not None:
            result["threshold"] = self.threshold
        if self.metricPerClass is not None:
            result["metricPerClass"] = self.metricPerClass
        if self.average is not None:
            result["average"] = self.average.value
        if self.quantile is not None:
            result["quantile"] = self.quantile

        return result


class LogicEvaluationType(Enum):
    RATIO = "RATIO"
    RANGE = "RANGE"
    TIME_SERIES_ANOMALY = "TIME_SERIES_ANOMALY"
    APORIA_DRIFT_SCORE = "APORIA_DRIFT_SCORE"
    MODEL_STALENESS = "MODEL_STALENESS"
    VALUES_RANGE = "VALUES_RANGE"


class ThresholdConfiguration(BaseModel):
    numeric: Optional[float] = None
    categorical: Optional[float] = None

    def to_dict(self):
        result = {}

        if self.numeric is not None:
            result["numeric"] = self.numeric
        if self.categorical is not None:
            result["categorical"] = self.categorical

        return result


class LogicEvaluationConfiguration(BaseModel):
    name: LogicEvaluationType
    # Needed for range (Both must exist, if one isn't used, it should be null)
    min: Optional[float] = None
    # Also needed for ratio (float) and staleness (TimePeriod)
    max: Optional[Union[float, TimePeriod]] = None
    # Needed for timeseries anomaly
    sensitivity: Optional[float] = None
    testOnlyIncrease: Optional[bool] = None
    # Needed for Aporia drift score
    thresholds: Optional[ThresholdConfiguration] = None
    # Needed for non-absolute Value range
    distance: Optional[float] = None
    # Needed for new-values value range
    new_values_count_threshold: Optional[int] = None
    new_values_ratio_threshold: Optional[float] = None

    @validator("max", pre=True)
    def _parse_max(cls, value):
        if isinstance(value, str):
            return TimePeriod.from_string(value)
        return value

    @root_validator()
    def _validate_logic_evaluation(cls, values):
        if values["name"] is LogicEvaluationType.RANGE:
            if isinstance(values["max"], TimePeriod):
                raise ValueError("max must be a float or None for Range logic evaluation")
            if (
                values["sensitivity"] is not None
                or values["testOnlyIncrease"] is not None
                or values["thresholds"] is not None
                or values["distance"] is not None
            ):
                raise ValueError("Only min and max can appear for Range logic evaluation")

        if values["name"] is LogicEvaluationType.VALUES_RANGE:
            if isinstance(values["max"], TimePeriod):
                raise ValueError("max must be a float or None for Range logic evaluation")
            if isinstance(values["min"], TimePeriod):
                raise ValueError("min must be a float or None for Range logic evaluation")
            if (
                values["sensitivity"] is not None
                or values["thresholds"] is not None
                or values["testOnlyIncrease"] is not None
            ):
                raise ValueError("Only min and max can appear for Value Range logic evaluation")

        if values["name"] is LogicEvaluationType.RATIO:
            if isinstance(values["max"], TimePeriod):
                raise ValueError("max must be a float for Ratio logic evaluation")
            if (
                values["sensitivity"] is not None
                or values["testOnlyIncrease"] is not None
                or values["thresholds"] is not None
                or values["distance"] is not None
                or values["new_values_count_threshold"] is not None
                or values["new_values_ratio_threshold"] is not None
            ):
                raise ValueError("Only min and max can appear for Ratio logic evaluation")

        if values["name"] is LogicEvaluationType.MODEL_STALENESS:
            if not isinstance(values["max"], TimePeriod):
                raise ValueError("max must be a TimePeriod for Stalenss logic evaluation")
            if (
                values["sensitivity"] is not None
                or values["testOnlyIncrease"] is not None
                or values["thresholds"] is not None
                or values["distance"] is not None
                or values["new_values_count_threshold"] is not None
                or values["new_values_ratio_threshold"] is not None
                or values["min"] is not None
            ):
                raise ValueError("Only max can appear for Staleness logic evaluation")

        if values["name"] is LogicEvaluationType.TIME_SERIES_ANOMALY:
            if values["sensitivity"] is None:
                raise ValueError("sensitivity must appear for Timeseries Anomaly Logic Evaluation")
            if (
                values["max"] is not None
                or values["min"] is not None
                or values["thresholds"] is not None
                or values["distance"] is not None
                or values["new_values_count_threshold"] is not None
                or values["new_values_ratio_threshold"] is not None
            ):
                raise ValueError(
                    "Only sensitivity can appear for Timeseries Anomaly logic evaluation"
                )

        if values["name"] is LogicEvaluationType.APORIA_DRIFT_SCORE:
            if values["thresholds"] is None:
                raise ValueError("thresholds must appear for Aporia Drift Score Logic Evaluation")
            if (
                values["max"] is not None
                or values["min"] is not None
                or values["sensitivity"] is not None
                or values["testOnlyIncrease"] is not None
                or values["distance"] is not None
                or values["new_values_count_threshold"] is not None
                or values["new_values_ratio_threshold"] is not None
            ):
                raise ValueError(
                    "Only thresholds can appear for Aporia Drift Score logic evaluation"
                )

        return values

    def to_dict(self):
        result = {"name": self.name.value}

        if self.min is not None:
            result["min"] = self.min
        if self.max is not None:
            if isinstance(self.max, TimePeriod):
                result["max"] = self.max.to_string()
            else:
                result["max"] = self.max
        if self.sensitivity is not None:
            result["sensitivity"] = self.sensitivity
        if self.testOnlyIncrease is not None:
            result["testOnlyIncrease"] = self.testOnlyIncrease
        if self.thresholds is not None:
            result["thresholds"] = self.thresholds.to_dict()

        if self.distance is not None:
            result["distance"] = self.distance

        if self.new_values_count_threshold is not None:
            result["new_values_count_threshold"] = self.new_values_count_threshold
        if self.new_values_ratio_threshold is not None:
            result["new_values_ratio_threshold"] = self.new_values_ratio_threshold

        return result


class PreConditionType(Enum):
    MIN_BASELINE_DATA_POINTS = "MIN_BASELINE_DATA_POINTS"
    MIN_FOCAL_DATA_POINTS = "MIN_FOCAL_DATA_POINTS"
    FOCAL_DATA_VALUE_IN_RANGE = "FOCAL_DATA_VALUE_IN_RANGE"


class PreConditionConfiguration(BaseModel):
    name: PreConditionType
    # Needed for MIN_BASELINE_DATA_POINTS
    value: Optional[int] = None
    # Needed for FOCAL_DATA_VALUE_IN_RANGE
    min: Optional[float] = None

    @root_validator()
    def _validate_pre_condition(cls, values):
        if values["name"] is PreConditionType.MIN_BASELINE_DATA_POINTS:
            if values["value"] is None:
                raise ValueError("value must appear for MIN_BASELINE_DATA_POINTS PreCondition")
            if values["min"] is not None:
                raise ValueError("Only value can appear for MIN_BASELINE_DATA_POINTS PreCondition")
        if values["name"] is PreConditionType.FOCAL_DATA_VALUE_IN_RANGE:
            # TODO: Min doesn't have to appear, appearantly. It just skips the test :(
            # if values["min"] is None:
            #     raise ValueError("min must appear for FOCAL_DATA_VALUE_IN_RANGE PreCondition")
            if values["value"] is not None:
                raise ValueError("Only min can appear for FOCAL_DATA_VALUE_IN_RANGE PreCondition")

        return values

    def to_dict(self):
        result = {"name": self.name.value}

        if self.min is not None:
            result["min"] = self.min
        if self.value is not None:
            result["value"] = self.value

        return result


class ActionType(Enum):
    ALERT = "ALERT"


class Severity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AlertType(Enum):
    MODEL_STALENESS = "model_staleness"
    METRIC_CHANGE = "metric_change"
    NEW_VALUES = "new_values"
    VALUES_RANGE = "values_range"
    DATA_DRIFT_ANOMALY = "data_drift_anomaly"
    DATA_DRIFT_SEGMENT_CHANGE = "data_drift_segment_change"
    DATA_DRIFT_TRAINING = "data_drift_training"
    PREDICTION_DRIFT_ANOMALY = "prediction_drift_anomaly"
    PREDICTION_DRIFT_SEGMENT_CHANGE = "prediction_drift_segment_change"
    PREDICTION_DRIFT_TRAINING = "prediction_drift_training"
    FEATURE_MISSING_VALUES_CHANGE = "feature_missing_values_change"
    FEATURE_MISSING_VALUES_ANOMALY = "feature_missing_values_anomaly"
    FEATURE_MISSING_VALUES_THRESHOLD = "feature_missing_values_threshold"
    FEATURE_MISSING_VALUES_SEGMENT_CHANGE = "feature_missing_values_segment_change"
    MODEL_ACTIVITY_THRESHOLD = "model_activity_threshold"
    MODEL_ACTIVITY_ANOMALY = "model_activity_anomaly"
    MODEL_ACTIVITY_CHANGE = "model_activity_change"


class VisualizationType(Enum):
    DISTRIBUTION_COMPARE_CHART = "distribution_compare_chart"
    RANGE_LINE_CHART = "range_line_chart"
    VALUE_OVER_TIME = "value_over_time"
    EMBEDDING_DRIFT_CHART = "embedding_drift_chart"
    VALUES_CANDLESTICK_CHART = "values_candlestick_chart"


class ActionConfiguration(BaseModel):
    type: ActionType
    severity: Severity
    alertType: AlertType
    description: str
    notification: List  # TODO: Look deeper into that
    action_schema: str = "v1"  # TODO: Realize what to do with it
    visualization: Optional[VisualizationType] = None
    alertGroupByTime: Optional[bool] = None
    alertGroupByEntity: Optional[bool] = None
    alertGroupTimeUnit: Optional[PeriodType] = None
    alertGroupTimeQuantity: Optional[int] = None

    def to_dict(self):
        result = {
            "type": self.type.value,
            "severity": self.severity.value,
            "alertType": self.alertType.value,
            "description": self.description,
            "notification": self.notification,
            "schema": self.action_schema,
            "alertGroupByTime": self.alertGroupByTime if self.alertGroupByTime else False,
            "alertGroupByEntity": self.alertGroupByEntity if self.alertGroupByEntity else True,
            "alertGroupTimeUnit": str(self.alertGroupTimeUnit.value)
            if self.alertGroupTimeUnit
            else str(PeriodType.DAYS.value),
            "alertGroupTimeQuantity": self.alertGroupTimeQuantity
            if self.alertGroupTimeQuantity
            else 1,
        }

        if self.visualization is not None:
            result["visualization"] = self.visualization.value

        return result


class ModelIdentification(BaseModel):
    id: str
    version: Optional[
        str
    ] = None  # None indicates all versions # TODO: Saw one saying "all_versions" as well?? Validate that

    def to_dict(self):
        return self.dict()


class SegmentIdentification(BaseModel):
    group: Optional[str] = None
    value: Optional[Union[str, int, float]] = None  # None indicates all segment values

    def to_dict(self):
        return self.dict()


class Identification(BaseModel):
    models: ModelIdentification
    segment: SegmentIdentification
    # TODO: Check if actuals are needed
    raw_inputs: Optional[List[str]] = None
    features: Optional[List[str]] = None
    predictions: Optional[List[str]] = None

    def to_dict(self):
        result = {
            "models": self.models.to_dict(),
            "segment": self.segment.to_dict(),
        }
        if self.raw_inputs is not None:
            result["raw_inputs"] = self.raw_inputs
        if self.features is not None:
            result["features"] = self.features
        if self.predictions is not None:
            result["predictions"] = self.predictions

        return result


class MonitorConfiguration(BaseModel):
    identification: Identification
    focal: FocalConfiguration
    metric: MetricConfiguration
    actions: List[ActionConfiguration]
    baseline: Optional[BaselineConfiguration] = None
    logicEvaluations: Optional[List[LogicEvaluationConfiguration]] = None
    preConditions: Optional[List[PreConditionConfiguration]] = None
    # TODO: Add cross-configuration validators

    @root_validator()
    def _validate_monitor_configuration(cls, values):
        if values.get("baseline") is not None:
            # For non-training monitors, skipPeriod defaults to the focal timePeriod, unless it's per segment
            if values["baseline"].source is SourceType.SERVING:
                # TODO: Fix that, as this sets skipPeriod even when using segments
                # TODO: CRITICAL BUG! This ruins the type infering
                if (
                    values["baseline"].segmentValue is None
                    and values["baseline"].segmentGroupId is None
                ):
                    if values["baseline"].skipPeriod is None:
                        values["baseline"].skipPeriod = values["focal"].timePeriod

            # For anomaly detection monitors, aggregationPeriod defaults to timePeriod
            if values["logicEvaluations"][0].name is LogicEvaluationType.TIME_SERIES_ANOMALY:
                if values["baseline"].aggregationPeriod is None:
                    values["baseline"].aggregationPeriod = values["focal"].timePeriod

        return values

    def to_dict(self):
        result = {
            "identification": self.identification.to_dict(),
            "configuration": {
                "focal": self.focal.to_dict(),
                "metric": self.metric.to_dict(),
                "actions": [action.to_dict() for action in self.actions],
            },
        }
        if self.baseline is not None:
            result["configuration"]["baseline"] = self.baseline.to_dict()
        if self.logicEvaluations is not None:
            result["configuration"]["logicEvaluations"] = [
                logic_evaluation.to_dict() for logic_evaluation in self.logicEvaluations
            ]
        if self.preConditions is not None:
            result["configuration"]["preConditions"] = [
                precondition.to_dict() for precondition in self.preConditions
            ]

        return result


class Monitor(BaseAporiaResource):
    def __init__(self, client: Client, data: Dict):
        self.client = client
        self.__update_members(data)

    def __update_members(self, data: Dict):
        self.raw_data = data
        self.id = data["id"]
        self.name = data["name"]
        self.type = MonitorType(data["type"])

    @classmethod
    def get_all(cls, client: Client, model_id: Optional[str] = None) -> List["Monitor"]:
        response = client.send_request("/monitors", "GET")

        client.assert_response(response)

        return [
            cls(client=client, data=entry)
            for entry in response.json()
            if model_id is None
            or entry["configuration"]["identification"]["models"]["id"] == model_id
        ]

    @classmethod
    def create(
        cls,
        client: Client,
        model_id: str,
        name: str,
        monitor_type: MonitorType,
        configuration: MonitorConfiguration,
        scheduling: Optional[str] = None,  # TODO: Optionally infer from configuration
        comment: Optional[str] = None,
        creator: Optional[str] = None,
        is_active: bool = True,
    ) -> "Monitor":
        monitor_type = MonitorType(monitor_type)

        if scheduling is None:
            if configuration.focal.timePeriod is None:
                scheduling = "0 * * * *"
            else:
                # if configuration.focal.timePeriod.count == 1:
                if configuration.focal.timePeriod.type is PeriodType.HOURS:
                    scheduling = "*/5 * * * *"  # Every 5 minutes
                elif configuration.focal.timePeriod.type is PeriodType.DAYS:
                    scheduling = "0 */4 * * *"  # Every 4 hours
                elif configuration.focal.timePeriod.type is PeriodType.WEEKS:
                    scheduling = "0 */12 * * *"  # Every 12 hours
                elif configuration.focal.timePeriod.type is PeriodType.MONTHS:
                    scheduling = "0 0 */2 * *"

        configuration.identification.models.id = model_id

        if scheduling is None:
            raise ValueError("Scheduling must be defined")

        response = client.send_request(
            "/monitors",
            "POST",
            {
                "name": name,
                "type": monitor_type.value,
                "scheduling": scheduling,
                "configuration": configuration.to_dict(),
                "comment": comment,
                "creator_id": creator,
                "is_active": is_active,
            },
        )

        client.assert_response(response)

        return cls(client=client, data=response.json())

    @classmethod
    def read(cls, client: Client, id: str) -> "Monitor":
        response = client.send_request(f"/monitors/{id}", "GET")
        client.assert_response(response)
        return cls(client=client, data=response.json())

    def update(
        self,
        name: Optional[str] = None,
        monitor_type: Optional[MonitorType] = None,
        scheduling: Optional[str] = None,
        configuration: Optional[MonitorConfiguration] = None,
        comment: Optional[str] = None,
        creator: Optional[str] = None,
        is_active: bool = True,
        **kwargs,
    ):
        args = {}
        if name is not None:
            args["name"] = name
        if monitor_type is not None:
            args["type"] = MonitorType(monitor_type).value
        if scheduling is not None:
            args["scheduling"] = scheduling
        if configuration is not None:
            args["configuration"] = configuration.to_dict()
        if comment is not None:
            args["comment"] = comment
        if creator is not None:
            args["creator"] = creator
        if is_active is not None:
            args["is_active"] = is_active
        response = self.client.send_request(
            f"/monitors/{self.id}",
            "PUT",
            args,
        )
        self.client.assert_response(response)
        self.__update_members(response.json())

    def delete(self):
        response = self.client.send_request(f"/monitors/{self.id}", "DELETE")
        self.client.assert_response(response)

    @staticmethod
    def delete_by_id(client: Client, id: str):
        response = client.send_request(f"/monitors/{id}", "DELETE")
        client.assert_response(response)


def __get_alert_description_range(min: Any, max: Any) -> str:
    if min is not None and max is not None:
        return "between <b>{min_threshold}</b> to <b>{max_threshold}</b>"
    if min is not None:
        return "above <b>{min_threshold}</b>"
    if max is not None:
        return "below <b>{max_threshold}</b>"
    raise ValueError("Bad configuration: Both min and max weren't supplied")


def __get_alert_field_description_if_needed(metric: MetricType) -> str:
    metrics_with_fields = [
        "missing_count",
        "mean",
        "min",
        "max",
        "sum",
        "variance",
        "std",
        "mse",
        "rmse",
        "mae",
        "precision",
        "recall",
        "f1",
        "accuracy",
        "tp_count",
        "tn_count",
        "fp_count",
        "fn_count",
        "wape",
        "mape",
        "auc_roc",
        "logloss",
    ]
    if metric.value in metrics_with_fields:
        return "of <b>{field}</b> {importance} "
    return ""


def _MonitorParamBuilder(
    alert_type: AlertType,
    metric_builder: Callable[..., MetricConfiguration],
    description_builder: Callable[..., str],
    logic_evaluation_builder: Callable[..., LogicEvaluationConfiguration],
    precondition_builder: Optional[Callable[..., Optional[PreConditionConfiguration]]] = None,
    needed_args: Optional[List[Union[str, List[str]]]] = None,
    visualization_builder: Optional[Callable[..., VisualizationType]] = None,
):
    class _MonitorParams:
        def __init__(self, **kw):
            self.alert_type = AlertType(alert_type)
            if needed_args is not None:
                for arg in needed_args:
                    if isinstance(arg, list):
                        if not any(optional_arg in kw.keys() for optional_arg in arg):
                            raise ValueError(
                                f"One of {arg} must be supplied for {alert_type.value} monitor"
                            )
                    else:
                        if kw[arg] is None:
                            raise ValueError(
                                f"Argument {arg} must be supplied for {alert_type.value} monitor"
                            )
            self.kw = kw

        @property
        def metric(self):
            return metric_builder(**self.kw)

        @property
        def description(self):
            return description_builder(**self.kw)

        @property
        def logic_evaluation(self):
            return logic_evaluation_builder(**self.kw)

        @property
        def precondition(self):
            if precondition_builder is not None:
                return precondition_builder(**self.kw)
            return None

        @property
        def visualization(self):
            if visualization_builder is not None:
                return VisualizationType(visualization_builder(**self.kw))
            return None

    return _MonitorParams


def build_drift_metric(**kw) -> MetricConfiguration:
    type = MetricType.HISTOGRAM
    if kw["metric"] is not None:
        type = MetricType(kw["metric"])
    elif kw["is_embedding"]:
        type = MetricType.EUCLIDEAN_DISTANCE
    return MetricConfiguration(type=type)


def _get_min_percentage(kw: dict):
    """If percentage exists, will use percentage. Otherwise, uses min. If both don't exist, will return None."""
    return 1 - (kw["percentage"] / 100) if kw.get("percentage") is not None else kw.get("min")


def _get_max_percentage(kw: dict):
    """If percentage exists, will use percentage. Otherwise, uses max. If both don't exist, will return None."""
    return 1 + (kw["percentage"] / 100) if kw.get("percentage") is not None else kw.get("max")


_MONITOR_PARAMETERS = {
    MonitorType.MODEL_ACTIVITY: {
        DetectionMethod.ANOMALY: _MonitorParamBuilder(
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.COUNT),
            alert_type=AlertType.MODEL_ACTIVITY_ANOMALY,
            visualization_builder=lambda **kw: VisualizationType.RANGE_LINE_CHART,
            description_builder=lambda **kw: "An anomaly in the number of total predictions was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on total predictions count history, the count was expected to be between <b>{last_lower_bound}</b> to <b>{last_upper_bound}</b>, but <b>{focal_value}</b> was received. <br /><br /> Total prediction anomaly might occur because: <ul><li>Natural changes in model invocations</li><li>Serving environment fault</li><li>Malicious attempt to analyse model behaviour</li></ul>",
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.TIME_SERIES_ANOMALY,
                sensitivity=kw["sensitivity"],
                testOnlyIncrease=kw["testOnlyIncrease"],
            ),
            needed_args=["sensitivity", "baseline"],
        ),
        DetectionMethod.PERCENTAGE: _MonitorParamBuilder(
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.COUNT),
            alert_type=AlertType.MODEL_ACTIVITY_CHANGE,
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            description_builder=lambda **kw: (
                "An anomaly in the number of total predictions was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on total predictions count history average and on defined ratio threshold, the count was expected to be "
                + __get_alert_description_range(
                    min=_get_min_percentage(kw), max=_get_max_percentage(kw)
                )
                + ", but <b>{focal_value}</b> was received. <br /><br /> Total prediction anomaly might occur because: <ul><li>Natural changes in model invocations</li><li>Serving environment fault</li><li>Malicious attempt to analyse model behaviour</li></ul>"
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RATIO,
                min=_get_min_percentage(kw),
                max=_get_max_percentage(kw),
            ),
            needed_args=[["percentage", "min", "max"], "baseline"],
        ),
        DetectionMethod.ABSOLUTE: _MonitorParamBuilder(
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.COUNT),
            alert_type=AlertType.MODEL_ACTIVITY_THRESHOLD,
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            description_builder=lambda **kw: (
                "An anomaly in the number of total predictions within the defined limits was detected.<br />The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>.<br /><br />Based on defined limits, the count was expected to be "
                + __get_alert_description_range(min=kw["min"], max=kw["max"])
                + ", but <b>{focal_value}</b> was received.<br />"
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RANGE, min=kw["min"], max=kw["max"]
            ),
            needed_args=[["min", "max"]],
        ),
    },
    MonitorType.DATA_DRIFT: {
        DetectionMethod.ANOMALY: _MonitorParamBuilder(
            alert_type=AlertType.DATA_DRIFT_ANOMALY,
            visualization_builder=lambda **kw: VisualizationType.EMBEDDING_DRIFT_CHART
            if kw["is_embedding"]
            else VisualizationType.DISTRIBUTION_COMPARE_CHART,
            metric_builder=build_drift_metric,
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RANGE, min=0, max=kw["max"]
            )
            if kw["is_embedding"]
            else LogicEvaluationConfiguration(
                name=LogicEvaluationType.APORIA_DRIFT_SCORE, thresholds=kw["thresholds"]
            ),
            description_builder=lambda **kw: f"A data drift was detected in feature <b>'{{field}}'</b> {{importance}}.{'' if kw['is_embedding'] else '{drift_score_text}'}<br /> The drift was observed in the <b>{{model}}</b> model, in version <b>{{model_version}}</b> for the <b>last {{focal_time_period}} ({{focal_times}})</b> <b>{{focal_segment}}</b> compared to the <b>last {{baseline_time_period}} ({{baseline_times}})</b>. <br /><br /> Data drift can have a significant effect on model behavior and may lead to unexpected results.<br /><br /> Data drift might occur because: <ul><li>Natural changes in data</li><li>Data store / provider schema changes</li><li>Data store / provider issues</li><li>Data processing issues</li></ul>",
            needed_args=[["thresholds", "max"], "baseline"],
        ),
        DetectionMethod.COMPARED_TO_SEGMENT: _MonitorParamBuilder(
            alert_type=AlertType.DATA_DRIFT_SEGMENT_CHANGE,
            visualization_builder=lambda **kw: VisualizationType.EMBEDDING_DRIFT_CHART
            if kw["is_embedding"]
            else VisualizationType.DISTRIBUTION_COMPARE_CHART,
            metric_builder=build_drift_metric,
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RANGE, min=0, max=kw["max"]
            )
            if kw["is_embedding"]
            else LogicEvaluationConfiguration(
                name=LogicEvaluationType.APORIA_DRIFT_SCORE, thresholds=kw["thresholds"]
            ),
            description_builder=lambda **kw: f"A data drift was detected in feature <b>'{{field}}'</b> {{importance}}.{'' if kw['is_embedding'] else '{drift_score_text}'}<br /> The drift was observed in the <b>{{model}}</b> model, in version <b>{{model_version}}</b> for the <b>last {{focal_time_period}} ({{focal_times}})</b> <b>{{focal_segment}}</b> compared to the <b>last {{baseline_time_period}} ({{baseline_times}})</b> <b>{{baseline_segment}}</b>. <br /><br /> Data drift can have a significant effect on model behavior and may lead to unexpected results.<br /><br /> Data drift might occur because: <ul><li>Natural changes in data</li><li>Data store / provider schema changes</li><li>Data store / provider issues</li><li>Data processing issues</li></ul>",
            needed_args=[["thresholds", "max"], "baseline"],
        ),
        DetectionMethod.COMPARED_TO_TRAINING: _MonitorParamBuilder(
            alert_type=AlertType.DATA_DRIFT_TRAINING,
            visualization_builder=lambda **kw: VisualizationType.EMBEDDING_DRIFT_CHART
            if kw["is_embedding"]
            else VisualizationType.DISTRIBUTION_COMPARE_CHART,
            metric_builder=build_drift_metric,
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RANGE, min=0, max=kw["max"]
            )
            if kw["is_embedding"]
            else LogicEvaluationConfiguration(
                name=LogicEvaluationType.APORIA_DRIFT_SCORE, thresholds=kw["thresholds"]
            ),
            description_builder=lambda **kw: f"A data drift was detected in feature <b>'{{field}}'</b> {{importance}}.{'' if kw['is_embedding'] else '{drift_score_text}'}<br /> The drift was observed in the <b>{{model}}</b> model, in version <b>{{model_version}}</b> for the <b>last {{focal_time_period}} ({{focal_times}})</b> <b>{{focal_segment}}</b> compared to the <b>Training</b> data. <br /><br /> Data drift can have a significant effect on model behavior and may lead to unexpected results.<br /><br /> Data drift might occur because: <ul><li>Natural changes in data</li><li>Data store / provider schema changes</li><li>Data store / provider issues</li><li>Data processing issues</li></ul>",
            needed_args=[["thresholds", "max"], "baseline"],
        ),
    },
    MonitorType.PREDICTION_DRIFT: {
        DetectionMethod.ANOMALY: _MonitorParamBuilder(
            alert_type=AlertType.PREDICTION_DRIFT_ANOMALY,
            visualization_builder=lambda **kw: VisualizationType.EMBEDDING_DRIFT_CHART
            if kw["is_embedding"]
            else VisualizationType.DISTRIBUTION_COMPARE_CHART,
            metric_builder=build_drift_metric,
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RANGE, min=0, max=kw["max"]
            )
            if kw["is_embedding"]
            else LogicEvaluationConfiguration(
                name=LogicEvaluationType.APORIA_DRIFT_SCORE, thresholds=kw["thresholds"]
            ),
            description_builder=lambda **kw: f"A prediction drift was detected in prediction <b>'{{field}}'</b> {{importance}}.{'' if kw['is_embedding'] else '{drift_score_text}'}<br /> The drift was observed in the <b>{{model}}</b> model, in version <b>{{model_version}}</b> for the <b>last {{focal_time_period}} ({{focal_times}})</b> <b>{{focal_segment}}</b> compared to the <b>last {{baseline_time_period}} ({{baseline_times}})</b>. <br /><br /> Prediction drift indicates a significant change in model's behavior. In some cases, it is a strong indicator for concept drift.<br /><br /> Prediction drift might occur because: <ul><li>Natural changes in data</li><li>Data store / provider schema changes</li><li>Data store / provider issues</li><li>Data processing issues</li></ul>",
            needed_args=[["thresholds", "max"], "baseline"],
        ),
        DetectionMethod.COMPARED_TO_SEGMENT: _MonitorParamBuilder(
            alert_type=AlertType.PREDICTION_DRIFT_SEGMENT_CHANGE,
            visualization_builder=lambda **kw: VisualizationType.EMBEDDING_DRIFT_CHART
            if kw["is_embedding"]
            else VisualizationType.DISTRIBUTION_COMPARE_CHART,
            metric_builder=build_drift_metric,
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RANGE, min=0, max=kw["max"]
            )
            if kw["is_embedding"]
            else LogicEvaluationConfiguration(
                name=LogicEvaluationType.APORIA_DRIFT_SCORE, thresholds=kw["thresholds"]
            ),
            description_builder=lambda **kw: f"A prediction drift was detected in prediction <b>'{{field}}'</b> {{importance}}.{'' if kw['is_embedding'] else '{drift_score_text}'}<br /> The drift was observed in the <b>{{model}}</b> model, in version <b>{{model_version}}</b> for the <b>last {{focal_time_period}} ({{focal_times}})</b> <b>{{focal_segment}}</b> compared to the <b>last {{baseline_time_period}} ({{baseline_times}})</b> <b>{{baseline_segment}}</b>. <br /><br /> Prediction drift indicates a significant change in model's behavior. In some cases, it is a strong indicator for concept drift.<br /><br /> Prediction drift might occur because: <ul><li>Natural changes in data</li><li>Data store / provider schema changes</li><li>Data store / provider issues</li><li>Data processing issues</li></ul>",
            needed_args=[["thresholds", "max"], "baseline"],
        ),
        DetectionMethod.COMPARED_TO_TRAINING: _MonitorParamBuilder(
            alert_type=AlertType.PREDICTION_DRIFT_TRAINING,
            visualization_builder=lambda **kw: VisualizationType.EMBEDDING_DRIFT_CHART
            if kw["is_embedding"]
            else VisualizationType.DISTRIBUTION_COMPARE_CHART,
            metric_builder=build_drift_metric,
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RANGE, min=0, max=kw["max"]
            )
            if kw["is_embedding"]
            else LogicEvaluationConfiguration(
                name=LogicEvaluationType.APORIA_DRIFT_SCORE, thresholds=kw["thresholds"]
            ),
            description_builder=lambda **kw: f"A prediction drift was detected in prediction <b>'{{field}}'</b> {{importance}}.{'' if kw['is_embedding'] else '{drift_score_text}'}<br /> The drift was observed in the <b>{{model}}</b> model, in version <b>{{model_version}}</b> for the <b>last {{focal_time_period}} ({{focal_times}})</b> <b>{{focal_segment}}</b> compared to the <b>Training</b> data. <br /><br /> Prediction drift indicates a significant change in model's behavior. In some cases, it is a strong indicator for concept drift.<br /><br /> Prediction drift might occur because: <ul><li>Natural changes in data</li><li>Data store / provider schema changes</li><li>Data store / provider issues</li><li>Data processing issues</li></ul>",
            needed_args=[["thresholds", "max"], "baseline"],
        ),
    },
    MonitorType.MISSING_VALUES: {
        DetectionMethod.ANOMALY: _MonitorParamBuilder(
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.MISSING_RATIO),
            alert_type=AlertType.FEATURE_MISSING_VALUES_ANOMALY,
            visualization_builder=lambda **kw: VisualizationType.RANGE_LINE_CHART,
            description_builder=lambda **kw: "An anomaly was detected in the ratio of missing values of feature <b>'{field}'</b> {importance}.<br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on missing ratio history, the ratio was expected to be between <b>{last_lower_bound}</b> to <b>{last_upper_bound}</b>, but <b>{focal_value}</b> was received. <br /><br /> Missing data can have a significant effect on model behavior and may lead to unexpected results. <br /><br /> Missing data might occur because: <ul><li>Serving environment fault</li><li>Data store / provider schema changes</li><li>Changes in internal API</li><li>Changes in model subject input</li></ul>",
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.TIME_SERIES_ANOMALY,
                sensitivity=kw["sensitivity"],
                testOnlyIncrease=kw["testOnlyIncrease"],
            ),
            precondition_builder=lambda **kw: (
                PreConditionConfiguration(
                    name=PreConditionType.FOCAL_DATA_VALUE_IN_RANGE, min=kw["min"]
                )
                if kw["min"] is not None
                else None
            ),
            needed_args=["sensitivity", "baseline"],
        ),
        DetectionMethod.PERCENTAGE: _MonitorParamBuilder(
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.MISSING_RATIO),
            alert_type=AlertType.FEATURE_MISSING_VALUES_CHANGE,
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            description_builder=lambda **kw: (
                "An anomaly in the ratio of missing values of feature <b>'{field}'</b> {importance} was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on missing ratio history average and on defined ratio threshold, the ratio was expected to be "
                + __get_alert_description_range(
                    min=_get_min_percentage(kw), max=_get_max_percentage(kw)
                )
                + ", but <b>{focal_value}</b> was received. <br /><br /> Missing data can have a significant effect on model behavior and may lead to unexpected results. <br /><br /> Missing data might occur because: <ul><li>Serving environment fault</li><li>Data store / provider schema changes</li><li>Changes in internal API</li><li>Changes in model subject input</li></ul>"
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RATIO,
                min=_get_min_percentage(kw),
                max=_get_max_percentage(kw),
            ),
            precondition_builder=lambda **kw: (
                PreConditionConfiguration(
                    name=PreConditionType.FOCAL_DATA_VALUE_IN_RANGE, min=kw["min"]
                )
                if kw["min"] is not None
                else None
            ),
            needed_args=[["percentage", "min", "max"], "baseline"],
        ),
        DetectionMethod.ABSOLUTE: _MonitorParamBuilder(
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.MISSING_RATIO),
            alert_type=AlertType.FEATURE_MISSING_VALUES_THRESHOLD,
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            description_builder=lambda **kw: (
                "An anomaly in the ratio of missing values of feature <b>'{field}'</b> {importance} within the defined limits was detected.<br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on defined limits, the missing ratio was expected to be "
                + __get_alert_description_range(min=kw["min"], max=kw["max"])
                + ", but <b>{focal_value}</b> was received.<br /><br /> Missing data can have a significant effect on model behavior and may lead to unexpected results. <br /><br /> Missing data might occur because: <ul><li>Serving environment fault</li><li>Data store / provider schema changes</li><li>Changes in internal API</li><li>Changes in model subject input</li></ul>"
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RANGE, min=kw["min"], max=kw["max"]
            ),
            needed_args=[["min", "max"]],
        ),
        DetectionMethod.COMPARED_TO_SEGMENT: _MonitorParamBuilder(
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.MISSING_RATIO),
            alert_type=AlertType.FEATURE_MISSING_VALUES_SEGMENT_CHANGE,
            visualization_builder=lambda **kw: VisualizationType.DISTRIBUTION_COMPARE_CHART,
            description_builder=lambda **kw: (
                "An anomaly in the ratio of missing values of feature <b>'{field}'</b> {importance} within the defined limits was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b> compared to the <b>last {baseline_time_period} ({baseline_times})</b> <b>{baseline_segment}</b>. <br /><br /> Based on defined ratio threshold, the ratio was expected to be "
                + __get_alert_description_range(
                    min=1 + (kw["percentage"] / 100), max=1 - (kw["percentage"] / 100)
                )
                + ", but <b>{focal_value}</b> was received. <br /><br /> Missing data can have a significant effect on model behavior and may lead to unexpected results. <br /><br /> Missing data might occur because: <ul><li>Serving environment fault</li><li>Data store / provider schema changes</li><li>Changes in internal API</li><li>Changes in model subject input</li></ul>"
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RATIO,
                max=_get_max_percentage(kw),
                min=_get_min_percentage(kw),
            ),
            precondition_builder=lambda **kw: (
                PreConditionConfiguration(
                    name=PreConditionType.FOCAL_DATA_VALUE_IN_RANGE, min=kw["min"]
                )
                if kw["min"] is not None
                else None
            ),
            needed_args=[["percentage", "min", "max"], "baseline"],
        ),
    },
    MonitorType.PERFORMANCE_DEGRADATION: {
        DetectionMethod.ANOMALY: _MonitorParamBuilder(
            visualization_builder=lambda **kw: VisualizationType.RANGE_LINE_CHART,
            alert_type=AlertType.METRIC_CHANGE,
            metric_builder=lambda **kw: MetricConfiguration(
                type=kw["metric"],
                metricAtK=kw["k"],
                threshold=kw["threshold"],
                metricPerClass=kw["prediction_class"],
                average=kw["average_method"],
                quantile=kw["quantile"],
            ),
            description_builder=lambda **kw: (
                "An anomaly in the value of the <b>'{metric}'</b> "
                + __get_alert_field_description_if_needed(MetricType(kw["metric"]))
                + "was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on metric history, the ratio was expected to be "
                + "between <b>{last_lower_bound}</b> to <b>{last_upper_bound}</b>, but <b>{focal_value}</b> was received."
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.TIME_SERIES_ANOMALY,
                sensitivity=kw["sensitivity"],
                testOnlyIncrease=kw["testOnlyIncrease"],
            ),
            needed_args=["metric", "sensitivity", "baseline"],
        ),
        DetectionMethod.PERCENTAGE: _MonitorParamBuilder(
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            alert_type=AlertType.METRIC_CHANGE,
            metric_builder=lambda **kw: MetricConfiguration(
                type=kw["metric"],
                metricAtK=kw["k"],
                threshold=kw["threshold"],
                metricPerClass=kw["prediction_class"],
                average=kw["average_method"],
                quantile=kw["quantile"],
            ),
            description_builder=lambda **kw: (
                "An anomaly in the value of the <b>'{metric}'</b> "
                + __get_alert_field_description_if_needed(MetricType(kw["metric"]))
                + "was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on metric history average and on defined threshold, the value was expected to be "
                + __get_alert_description_range(
                    min=_get_min_percentage(kw), max=_get_max_percentage(kw)
                )
                + ", but <b>{focal_value}</b> was received."
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RATIO,
                min=_get_min_percentage(kw),
                max=_get_max_percentage(kw),
            ),
            needed_args=["metric", ["percentage", "min", "max"], "baseline"],
        ),
        DetectionMethod.ABSOLUTE: _MonitorParamBuilder(
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            alert_type=AlertType.METRIC_CHANGE,
            metric_builder=lambda **kw: MetricConfiguration(
                type=kw["metric"],
                metricAtK=kw["k"],
                threshold=kw["threshold"],
                metricPerClass=kw["prediction_class"],
                average=kw["average_method"],
                quantile=kw["quantile"],
            ),
            description_builder=lambda **kw: (
                "An anomaly in the value of the <b>'{metric}'</b> "
                + __get_alert_field_description_if_needed(MetricType(kw["metric"]))
                + "within the defined limits was detected.<br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on defined limits, the metric value was expected to be "
                + __get_alert_description_range(min=kw["min"], max=kw["max"])
                + ", but <b>{focal_value}</b> was received."
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RANGE,
                min=kw["min"],
                max=kw["max"],
            ),
            needed_args=["metric", ["min", "max"]],
        ),
        DetectionMethod.COMPARED_TO_SEGMENT: _MonitorParamBuilder(
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            alert_type=AlertType.METRIC_CHANGE,
            metric_builder=lambda **kw: MetricConfiguration(
                type=kw["metric"],
                metricAtK=kw["k"],
                threshold=kw["threshold"],
                metricPerClass=kw["prediction_class"],
                average=kw["average_method"],
                quantile=kw["quantile"],
            ),
            description_builder=lambda **kw: (
                "An anomaly in the value of the <b>'{metric}'</b> "
                + __get_alert_field_description_if_needed(MetricType(kw["metric"]))
                + "within the defined limits was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b> compared to the <b>last {baseline_time_period} ({baseline_times})</b> <b>{baseline_segment}</b>. <br /><br /> Based on defined ratio threshold, the ratio was expected to be "
                + __get_alert_description_range(
                    min=_get_min_percentage(kw), max=_get_max_percentage(kw)
                )
                + ", but <b>{focal_value}</b> was received."
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RATIO,
                min=_get_min_percentage(kw),
                max=_get_max_percentage(kw),
            ),
            needed_args=["metric", ["percentage", "min", "max"], "baseline"],
        ),
        DetectionMethod.COMPARED_TO_TRAINING: _MonitorParamBuilder(
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            alert_type=AlertType.METRIC_CHANGE,
            metric_builder=lambda **kw: MetricConfiguration(
                type=kw["metric"],
                metricAtK=kw["k"],
                threshold=kw["threshold"],
                metricPerClass=kw["prediction_class"],
                average=kw["average_method"],
                quantile=kw["quantile"],
            ),
            description_builder=lambda **kw: (
                "An anomaly in the value of the <b>'{metric}'</b> "
                + __get_alert_field_description_if_needed(MetricType(kw["metric"]))
                + "within the defined limits was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b> compared to <b>Training</b> data. <br /><br /> Based on defined ratio threshold, the ratio was expected to be "
                + __get_alert_description_range(
                    min=_get_min_percentage(kw), max=_get_max_percentage(kw)
                )
                + ", but <b>{focal_value}</b> was received."
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RATIO,
                min=_get_min_percentage(kw),
                max=_get_max_percentage(kw),
            ),
            needed_args=["metric", ["percentage", "min", "max"], "baseline"],
        ),
    },
    MonitorType.METRIC_CHANGE: {
        DetectionMethod.ANOMALY: _MonitorParamBuilder(
            visualization_builder=lambda **kw: VisualizationType.RANGE_LINE_CHART,
            alert_type=AlertType.METRIC_CHANGE,
            metric_builder=lambda **kw: MetricConfiguration(
                type=kw["metric"],
                metricAtK=kw["k"],
                threshold=kw["threshold"],
                metricPerClass=kw["prediction_class"],
                average=kw["average_method"],
                quantile=kw["quantile"],
            ),
            description_builder=lambda **kw: (
                "An anomaly in the value of the <b>'{metric}'</b> "
                + __get_alert_field_description_if_needed(MetricType(kw["metric"]))
                + "was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on metric history, the ratio was expected to be "
                + "between <b>{last_lower_bound}</b> to <b>{last_upper_bound}</b>, but <b>{focal_value}</b> was received."
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.TIME_SERIES_ANOMALY,
                sensitivity=kw["sensitivity"],
                testOnlyIncrease=kw["testOnlyIncrease"],
            ),
            needed_args=["metric", "baseline", "sensitivity"],
        ),
        DetectionMethod.PERCENTAGE: _MonitorParamBuilder(
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            alert_type=AlertType.METRIC_CHANGE,
            metric_builder=lambda **kw: MetricConfiguration(
                type=kw["metric"],
                metricAtK=kw["k"],
                threshold=kw["threshold"],
                metricPerClass=kw["prediction_class"],
                average=kw["average_method"],
                quantile=kw["quantile"],
            ),
            description_builder=lambda **kw: (
                "An anomaly in the value of the <b>'{metric}'</b> "
                + __get_alert_field_description_if_needed(MetricType(kw["metric"]))
                + "was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on metric history average and on defined threshold, the value was expected to be "
                + __get_alert_description_range(
                    min=_get_min_percentage(kw), max=_get_max_percentage(kw)
                )
                + ", but <b>{focal_value}</b> was received."
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RATIO,
                min=_get_min_percentage(kw),
                max=_get_max_percentage(kw),
            ),
            needed_args=["metric", ["percentage", "min", "max"], "baseline",],
        ),
        DetectionMethod.ABSOLUTE: _MonitorParamBuilder(
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            alert_type=AlertType.METRIC_CHANGE,
            metric_builder=lambda **kw: MetricConfiguration(
                type=kw["metric"],
                metricAtK=kw["k"],
                threshold=kw["threshold"],
                metricPerClass=kw["prediction_class"],
                average=kw["average_method"],
                quantile=kw["quantile"],
            ),
            description_builder=lambda **kw: (
                "An anomaly in the value of the <b>'{metric}'</b> "
                + __get_alert_field_description_if_needed(MetricType(kw["metric"]))
                + "within the defined limits was detected.<br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on defined limits, the metric value was expected to be "
                + __get_alert_description_range(min=kw["min"], max=kw["max"])
                + ", but <b>{focal_value}</b> was received."
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RANGE, min=kw["min"], max=kw["max"]
            ),
            needed_args=["metric", ["min", "max"]],
        ),
        DetectionMethod.COMPARED_TO_SEGMENT: _MonitorParamBuilder(
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            alert_type=AlertType.METRIC_CHANGE,
            metric_builder=lambda **kw: MetricConfiguration(
                type=kw["metric"],
                metricAtK=kw["k"],
                threshold=kw["threshold"],
                metricPerClass=kw["prediction_class"],
                average=kw["average_method"],
                quantile=kw["quantile"],
            ),
            description_builder=lambda **kw: (
                "An anomaly in the value of the <b>'{metric}'</b> "
                + __get_alert_field_description_if_needed(MetricType(kw["metric"]))
                + "within the defined limits was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b> compared to the <b>last {baseline_time_period} ({baseline_times})</b> <b>{baseline_segment}</b>. <br /><br /> Based on defined ratio threshold, the ratio was expected to be "
                + __get_alert_description_range(
                    min=_get_min_percentage(kw), max=_get_max_percentage(kw)
                )
                + ", but <b>{focal_value}</b> was received."
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RATIO,
                min=_get_min_percentage(kw),
                max=_get_max_percentage(kw),
            ),
            needed_args=["metric", "baseline", ["percentage", "min", "max"]],
        ),
        DetectionMethod.COMPARED_TO_TRAINING: _MonitorParamBuilder(
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            alert_type=AlertType.METRIC_CHANGE,
            metric_builder=lambda **kw: MetricConfiguration(
                type=kw["metric"],
                metricAtK=kw["k"],
                threshold=kw["threshold"],
                metricPerClass=kw["prediction_class"],
                average=kw["average_method"],
                quantile=kw["quantile"],
            ),
            description_builder=lambda **kw: (
                "An anomaly in the value of the <b>'{metric}'</b> "
                + __get_alert_field_description_if_needed(MetricType(kw["metric"]))
                + "within the defined limits was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b> compared to <b>Training</b> data. <br /><br /> Based on defined ratio threshold, the ratio was expected to be "
                + __get_alert_description_range(
                    min=_get_min_percentage(kw), max=_get_max_percentage(kw)
                )
                + ", but <b>{focal_value}</b> was received."
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RATIO,
                min=_get_min_percentage(kw),
                max=_get_max_percentage(kw),
            ),
            needed_args=["metric", "baseline", ["percentage", "min", "max"]],
        ),
    },
    MonitorType.MODEL_STALENESS: {
        DetectionMethod.ABSOLUTE: _MonitorParamBuilder(
            alert_type=AlertType.MODEL_STALENESS,
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.LAST_VERSION_CREATION),
            description_builder=lambda **kw: "Model <b>{model}</b> was detected as stale. <br /> The current version in production <b>{model_version}</b> was deployed over <b>{time_threshold}</b> ago.<br /><br /> It is recommended to update the model in <b>{environment}</b>.",
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.MODEL_STALENESS, max=kw["staleness_period"]
            ),
            needed_args=["staleness_period"],
        ),
    },
    MonitorType.CUSTOM_METRIC_MONITOR: {
        DetectionMethod.ANOMALY: _MonitorParamBuilder(
            visualization_builder=lambda **kw: VisualizationType.RANGE_LINE_CHART,
            alert_type=AlertType.METRIC_CHANGE,
            metric_builder=lambda **kw: MetricConfiguration(
                type=MetricType.CUSTOM_METRIC, id=kw["custom_metric_id"]
            ),
            description_builder=lambda **kw: (
                "An anomaly in the value of the <b>'{metric}'</b> "
                + __get_alert_field_description_if_needed(MetricType.CUSTOM_METRIC)
                + "was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on metric history, the ratio was expected to be "
                + "between <b>{last_lower_bound}</b> to <b>{last_upper_bound}</b>, but <b>{focal_value}</b> was received."
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.TIME_SERIES_ANOMALY,
                sensitivity=kw["sensitivity"],
                testOnlyIncrease=kw["testOnlyIncrease"],
            ),
            needed_args=["custom_metric_id", "baseline", "sensitivity"],
        ),
        DetectionMethod.PERCENTAGE: _MonitorParamBuilder(
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            alert_type=AlertType.METRIC_CHANGE,
            metric_builder=lambda **kw: MetricConfiguration(
                type=MetricType.CUSTOM_METRIC, id=kw["custom_metric_id"]
            ),
            description_builder=lambda **kw: (
                "An anomaly in the value of the <b>'{metric}'</b> "
                + __get_alert_field_description_if_needed(MetricType.CUSTOM_METRIC)
                + "was detected. <br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on metric history average and on defined threshold, the value was expected to be "
                + __get_alert_description_range(
                    min=_get_min_percentage(kw), max=_get_max_percentage(kw)
                )
                + ", but <b>{focal_value}</b> was received."
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RATIO,
                min=_get_min_percentage(kw),
                max=_get_max_percentage(kw),
            ),
            needed_args=["custom_metric_id", "baseline", ["percentage", "min", "max"]],
        ),
        DetectionMethod.ABSOLUTE: _MonitorParamBuilder(
            visualization_builder=lambda **kw: VisualizationType.VALUE_OVER_TIME,
            alert_type=AlertType.METRIC_CHANGE,
            metric_builder=lambda **kw: MetricConfiguration(
                type=MetricType.CUSTOM_METRIC, id=kw["custom_metric_id"]
            ),
            description_builder=lambda **kw: (
                "An anomaly in the value of the <b>'{metric}'</b> "
                + __get_alert_field_description_if_needed(MetricType.CUSTOM_METRIC)
                + "within the defined limits was detected.<br /> The anomaly was observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on defined limits, the metric value was expected to be "
                + __get_alert_description_range(min=kw["min"], max=kw["max"])
                + ", but <b>{focal_value}</b> was received."
            ),
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.RANGE, min=kw["min"], max=kw["max"]
            ),
            needed_args=["custom_metric_id", ["min", "max"]],
        ),
    },
    MonitorType.VALUES_RANGE: {
        DetectionMethod.PERCENTAGE: _MonitorParamBuilder(
            alert_type=AlertType.VALUES_RANGE,
            visualization_builder=lambda **kw: VisualizationType.VALUES_CANDLESTICK_CHART,
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.MIN_MAX),
            description_builder=lambda **kw: "Unexpected values were detected in feature <b>'{field}'</b> {importance}. <br /> The values were observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b> compared to the <b>last {baseline_time_period} ({baseline_times})</b>. <br /><br /> Based on defined limits, the values were expected to be <b>{value_thresholds}</b>, but values <b>{unexpected_values}</b> were received.",
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.VALUES_RANGE, distance=kw["distance"]
            ),
            needed_args=["distance", "baseline"],
        ),
        DetectionMethod.ABSOLUTE: _MonitorParamBuilder(
            alert_type=AlertType.VALUES_RANGE,
            visualization_builder=lambda **kw: VisualizationType.VALUES_CANDLESTICK_CHART,
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.MIN_MAX),
            description_builder=lambda **kw: "Unexpected values were detected in feature <b>'{field}'</b> {importance}. <br /> The values were observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b>. <br /><br /> Based on defined limits, the values were expected to be <b>{value_thresholds}</b>, but values <b>{unexpected_values}</b> were received.",
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.VALUES_RANGE, min=kw["min"], max=kw["max"]
            ),
            needed_args=[["min", "max"]],
        ),
        DetectionMethod.COMPARED_TO_SEGMENT: _MonitorParamBuilder(
            alert_type=AlertType.VALUES_RANGE,
            visualization_builder=lambda **kw: VisualizationType.VALUES_CANDLESTICK_CHART,
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.MIN_MAX),
            description_builder=lambda **kw: "Unexpected values were detected in feature <b>'{field}'</b> {importance}. <br /> The values were observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b> compared to the <b>last {baseline_time_period} ({baseline_times})</b> <b>{baseline_segment}</b>. <br /><br /> Based on defined limits, the values were expected to be <b>{value_thresholds}</b>, but values <b>{unexpected_values}</b> were received.'",
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.VALUES_RANGE, distance=kw["distance"]
            ),
            needed_args=["distance", "baseline"],
        ),
        DetectionMethod.COMPARED_TO_TRAINING: _MonitorParamBuilder(
            alert_type=AlertType.VALUES_RANGE,
            visualization_builder=lambda **kw: VisualizationType.VALUES_CANDLESTICK_CHART,
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.MIN_MAX),
            description_builder=lambda **kw: "Unexpected values were detected in feature <b>'{field}'</b> {importance}. <br /> The values were observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b> compared to <b>Training</b> data. <br /><br /> Based on defined limits, the values were expected to be <b>{value_thresholds}</b>, but values <b>{unexpected_values}</b> were received.",
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.VALUES_RANGE, distance=kw["distance"]
            ),
            needed_args=["distance", "baseline"],
        ),
    },
    MonitorType.NEW_VALUES: {
        DetectionMethod.PERCENTAGE: _MonitorParamBuilder(
            alert_type=AlertType.NEW_VALUES,
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.UNIQUE_VALUES),
            description_builder=lambda **kw: "New values were detected in feature <b>'{field}'</b> {importance}. <br /> The values were observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b> compared to the <b>last {baseline_time_period} ({baseline_times})</b>. <br /><br /> Based on defined limits, the following new values <b>{unexpected_values}</b> were received.",
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.VALUES_RANGE,
                new_values_ratio_threshold=kw["new_values_ratio_threshold"],
                new_values_count_threshold=kw["new_values_count_threshold"],
            ),
            needed_args=[["new_values_ratio_threshold", "new_values_count_threshold"], "baseline"],
        ),
        DetectionMethod.COMPARED_TO_SEGMENT: _MonitorParamBuilder(
            alert_type=AlertType.NEW_VALUES,
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.UNIQUE_VALUES),
            description_builder=lambda **kw: "New values were detected in feature <b>'{field}'</b> {importance}. <br /> The values were observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b> compared to the <b>last {baseline_time_period} ({baseline_times})</b> <b>{baseline_segment}</b>. <br /><br /> Based on defined limits, the following new values <b>{unexpected_values}</b> were received.",
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.VALUES_RANGE,
                new_values_ratio_threshold=kw["new_values_ratio_threshold"],
                new_values_count_threshold=kw["new_values_count_threshold"],
            ),
            needed_args=[["new_values_ratio_threshold", "new_values_count_threshold"], "baseline"],
        ),
        DetectionMethod.COMPARED_TO_TRAINING: _MonitorParamBuilder(
            alert_type=AlertType.NEW_VALUES,
            metric_builder=lambda **kw: MetricConfiguration(type=MetricType.UNIQUE_VALUES),
            description_builder=lambda **kw: "New values were detected in feature <b>'{field}'</b> {importance}. <br /> The values were observed in the <b>{model}</b> model, in version <b>{model_version}</b> for the <b>last {focal_time_period} ({focal_times})</b> <b>{focal_segment}</b> compared to <b>Training</b> data. <br /><br /> Based on defined limits, the following new values <b>{unexpected_values}</b> were received.",
            logic_evaluation_builder=lambda **kw: LogicEvaluationConfiguration(
                name=LogicEvaluationType.VALUES_RANGE,
                new_values_ratio_threshold=kw["new_values_ratio_threshold"],
                new_values_count_threshold=kw["new_values_count_threshold"],
            ),
            needed_args=[["new_values_ratio_threshold", "new_values_count_threshold"], "baseline"],
        ),
    },
}


def create_monitor_configuration(
    monitor_type: MonitorType,
    detection_method: DetectionMethod,
    focal: FocalConfiguration,
    severity: Severity,
    baseline: Optional[BaselineConfiguration] = None,
    raw_inputs: Optional[List[str]] = None,
    features: Optional[List[str]] = None,
    predictions: Optional[List[str]] = None,
    is_embedding_monitor: bool = False,
    metric: Optional[Union[MetricType, str]] = None,
    percentage: Optional[int] = None,
    thresholds: Optional[ThresholdConfiguration] = None,
    sensitivity: Optional[float] = None,
    alert_on_increase_only: Optional[bool] = None,
    min: Optional[int] = None,
    max: Optional[int] = None,
    distance: Optional[float] = None,
    new_values_ratio_threshold: Optional[float] = None,
    new_values_count_threshold: Optional[int] = None,
    staleness_period: Optional[TimePeriod] = None,
    min_focal_prediction_count: Optional[int] = None,
    min_baseline_prediction_count: Optional[int] = None,
    version: Optional[str] = None,
    segment_identification: Optional[SegmentIdentification] = None,
    messaging: Optional[Dict[MessagingIntegrationType, List[str]]] = None,
    emails: Optional[List[str]] = None,
    k: Optional[int] = None,
    prediction_class: Optional[Any] = None,
    prediction_threshold: Optional[float] = None,
    average_method: Optional[AverageMethod] = None,
    custom_metric_id: Optional[str] = None,
    quantile: Optional[float] = None,
    group_by_time: Optional[bool] = None,
    group_by_entity: Optional[bool] = None,
    alert_group_time_unit: Optional[PeriodType] = None,
    alert_group_time_quantity: Optional[int] = None,
) -> MonitorConfiguration:
    """Creates a monitor configuration by the given parameters."""
    if segment_identification is None:
        segment_identification = SegmentIdentification()

    monitor_type = MonitorType(monitor_type)
    detection_method = DetectionMethod(detection_method)
    severity = Severity(severity)

    preconditions = []

    if min_baseline_prediction_count is not None:
        if baseline is None:
            raise ValueError(
                "Can't specify min_baseline_prediction_count for monitors with no baseline"
            )
        preconditions.append(
            PreConditionConfiguration(
                name=PreConditionType.MIN_BASELINE_DATA_POINTS, value=min_baseline_prediction_count
            )
        )
    if min_focal_prediction_count is not None:
        preconditions.append(
            PreConditionConfiguration(
                name=PreConditionType.MIN_FOCAL_DATA_POINTS, value=min_focal_prediction_count
            )
        )

    monitor_params = _MONITOR_PARAMETERS[monitor_type][detection_method](
        percentage=percentage,
        thresholds=thresholds,
        sensitivity=sensitivity,
        testOnlyIncrease=alert_on_increase_only,
        min=min,
        max=max,
        new_values_count_threshold=new_values_count_threshold,
        new_values_ratio_threshold=new_values_ratio_threshold,
        distance=distance,
        staleness_period=staleness_period,
        baseline=baseline,
        is_embedding=is_embedding_monitor,
        metric=metric,
        k=k,
        threshold=prediction_threshold,
        prediction_class=prediction_class,
        average_method=average_method,
        custom_metric_id=custom_metric_id,
        quantile=quantile,
    )

    notifications = []
    if emails is not None:
        notifications.append({"type": "EMAIL", "emails": emails})

    if messaging is not None:
        for integration_type, integration_ids in messaging.items():
            integration_type = MessagingIntegrationType(integration_type)
            for integration_id in integration_ids:
                notifications.append(
                    {"type": integration_type.value, "integration_id": integration_id}
                )

    if monitor_params.precondition is not None:
        preconditions.append(monitor_params.precondition)

    if monitor_params.metric.type in [MetricType.HISTOGRAM, MetricType.EUCLIDEAN_DISTANCE]:
        focal.alignBinsWithBaseline = True

    return MonitorConfiguration(
        identification=Identification(
            models=ModelIdentification(id="", version=version),
            segment=segment_identification,
            raw_inputs=raw_inputs,
            features=features,
            predictions=predictions,
        ),
        metric=monitor_params.metric,
        focal=focal,
        baseline=baseline,
        preConditions=preconditions,
        logicEvaluations=[monitor_params.logic_evaluation],
        actions=[
            ActionConfiguration(
                type=ActionType.ALERT,
                severity=severity,
                alertType=monitor_params.alert_type,
                description=monitor_params.description,
                notification=notifications,
                visualization=monitor_params.visualization,
                alertGroupByTime=group_by_time,
                alertGroupByEntity=group_by_entity,
                alertGroupTimeUnit=alert_group_time_unit,
                alertGroupTimeQuantity=alert_group_time_quantity,
            )
        ],
    )


def parse_monitor_configuration(configuration: Dict) -> MonitorConfiguration:
    config = configuration["configuration"]
    identification = configuration["identification"]

    return MonitorConfiguration(
        identification=identification,
        focal=config.get("focal"),
        baseline=config.get("baseline"),
        actions=[ActionConfiguration(**action) for action in config["actions"]],
        metric=config["metric"],
        logicEvaluations=[
            LogicEvaluationConfiguration(**evaluation)
            for evaluation in config.get("logicEvaluations", [])
        ],
        preConditions=[
            PreConditionConfiguration(**precondition)
            for precondition in config.get("preConditions", [])
        ],
    )


def infer_detection_method(configuration: MonitorConfiguration) -> DetectionMethod:
    logic_evaluation = configuration.logicEvaluations[0]
    if logic_evaluation.name is LogicEvaluationType.MODEL_STALENESS:
        return DetectionMethod.ABSOLUTE
    if logic_evaluation.name is LogicEvaluationType.RANGE:
        if configuration.metric.type is not MetricType.EUCLIDEAN_DISTANCE:
            return DetectionMethod.ABSOLUTE
    if logic_evaluation.name is LogicEvaluationType.TIME_SERIES_ANOMALY:
        return DetectionMethod.ANOMALY
    if logic_evaluation.name is LogicEvaluationType.APORIA_DRIFT_SCORE or (
        logic_evaluation.name is LogicEvaluationType.RANGE
        and configuration.metric.type is MetricType.EUCLIDEAN_DISTANCE
    ):
        if configuration.actions[0].alertType in [
            AlertType.DATA_DRIFT_ANOMALY,
            AlertType.PREDICTION_DRIFT_ANOMALY,
        ]:
            return DetectionMethod.ANOMALY
        elif configuration.actions[0].alertType in [
            AlertType.DATA_DRIFT_SEGMENT_CHANGE,
            AlertType.PREDICTION_DRIFT_SEGMENT_CHANGE,
        ]:
            return DetectionMethod.COMPARED_TO_SEGMENT
        elif configuration.actions[0].alertType in [
            AlertType.DATA_DRIFT_TRAINING,
            AlertType.PREDICTION_DRIFT_TRAINING,
        ]:
            return DetectionMethod.COMPARED_TO_TRAINING
    if configuration.baseline is None:
        return DetectionMethod.ABSOLUTE
    if configuration.baseline.source is SourceType.TRAINING:
        return DetectionMethod.COMPARED_TO_TRAINING
    if configuration.baseline.skipPeriod is None:
        return DetectionMethod.COMPARED_TO_SEGMENT
    if configuration.baseline.segmentGroupId is not None:
        return DetectionMethod.COMPARED_TO_SEGMENT
    return DetectionMethod.PERCENTAGE
