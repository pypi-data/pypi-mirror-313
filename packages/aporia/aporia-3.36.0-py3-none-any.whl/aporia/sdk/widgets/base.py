import datetime
from enum import Enum
from typing import Dict, Optional, Tuple, Union
import uuid

from pydantic import BaseModel, Field, PrivateAttr, root_validator, validator

from aporia.sdk.custom_metrics import CustomMetric
from aporia.sdk.fields import Field as SDKField
from aporia.sdk.fields import FieldGroup, FieldType
from aporia.sdk.metrics import (
    AverageMethod,
    is_aggregable_metric,
    is_code_based_metric,
    is_custom_metric,
    is_model_metric,
    MetricType,
)


class FixedTimeframe(BaseModel):
    to: datetime.datetime
    from_impl: datetime.datetime = Field(alias="from")

    @validator("to", "from_impl")
    def _validate_utc(cls, value, values):
        if value.tzinfo != datetime.timezone.utc:
            raise ValueError("Timezones must be in UTC")
        return value

    def dict(self, *args, **kwargs):
        return {"to": self.to.isoformat(), "from": self.from_impl.isoformat()}


class DisplayOptions(BaseModel):
    color: int = 0  # 1 for compare


class VersionSelection(BaseModel):
    id: str = "*"


class BaselineType(str, Enum):
    TRAINING = "training"
    RELATIVE_TIME_PERIOD = "relativeTimePeriod"


class TimeUnit(str, Enum):
    DAY = "day"
    MONTH = "month"


class BaselineConfiguration(BaseModel):
    type: BaselineType
    unit: Optional[TimeUnit] = None
    duration: Optional[int] = None

    @validator("unit")
    def _validate_unit(cls, value, values) -> Optional[TimeUnit]:
        if values["type"] == "training" and value is not None:
            raise ValueError("Unit can't be used with training baseline")
        return value

    @validator("duration")
    def _validate_duration(cls, value, values) -> Optional[int]:
        if values["type"] == "training" and value is not None:
            raise ValueError("Unit can't be used with training baseline")
        return value

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class MetricParameters(BaseModel):
    id: str


class WidgetType(str, Enum):
    TEXT = "text"
    ANOMALY_TABLE = "anomaly-table"
    DISTRIBUTION = "distribution"
    TIME_SERIES_HISTOGRAM = "time-series-histogram"
    METRIC = "metric"
    TIME_SERIES = "time-series"
    METRIC_BY_SEGMENT = "metric-by-segment"
    METRIC_CORRELATION = "metric-correlation"


class BaseWidget(BaseModel):
    i: str = Field(default_factory=lambda: str(uuid.uuid4()))
    h: int
    w: int  # Capped at 12
    x: int  # Capped at 11?
    y: int
    name: str
    type: WidgetType
    moved: bool = False
    resizable: bool = True
    dependencies: Optional[
        Dict
    ] = None  # TODO: Investigate this, and consider if you want to raise error if it has issues
    _internal_state: Dict = PrivateAttr(default_factory=dict)

    def __init__(self, **data):
        internal_state = data.pop("_internal_state", None)
        super().__init__(**data)
        if internal_state is not None:
            self._internal_state = internal_state

    @validator("x")
    def _validate_x(cls, value, values):
        if value < 0:
            raise ValueError("x must be non-negative")
        if value >= 12:
            raise ValueError("The grid's x-axis is limited at 12 cells")
        return value

    @validator("y")
    def _validate_y(cls, value, values):
        if value < 0:
            raise ValueError("y must be non-negative")
        return value

    @validator("w")
    def _validate_w(cls, value, values):
        if value <= 0:
            raise ValueError("w must be positive")
        if value > 12:
            raise ValueError("The grid's x-axis is limited at 12 cells")
        return value

    @validator("h")
    def _validate_h(cls, value, values):
        if value <= 0:
            raise ValueError("h must be positive")
        return value

    @classmethod
    def create(
        cls, position: Tuple[int, int], size: Tuple[int, int], *args, **kwargs
    ) -> "BaseWidget":
        raise NotImplementedError()

    def dict(self, *args, **kwargs):
        return {
            k: v
            for k, v in super().dict(*args, **kwargs).items()
            if v is not None and k != "_internal_state"
        }


class MetricBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True  # For CustomMetric as an object


class MetricConfiguration(MetricBaseModel):
    metric: MetricType
    field: Optional[SDKField] = None
    custom_metric: Optional[CustomMetric] = None
    average: Optional[AverageMethod] = None
    threshold: Optional[float] = None
    k: Optional[int] = None
    class_name: Optional[str] = None
    baseline: Optional[BaselineConfiguration] = None
    quantile: Optional[float] = None

    def _get_metric(self) -> Union[MetricType, str]:
        if self.metric is MetricType.CUSTOM_METRIC:
            return self.custom_metric.id
        if self.metric is MetricType.CODE:
            raise NotImplementedError("Code-based metrics currently not supported")
        return self.metric

    def _get_field(self) -> Optional[Dict]:
        if self.field is not None:
            return self.field.to_widget()
        return None

    def _get_field_category(self) -> Optional[FieldGroup]:
        if self.field is not None:
            return self.field.group
        return None

    def _get_parameters(self) -> Optional[MetricParameters]:
        if self.custom_metric is not None:
            return MetricParameters(id=self.custom_metric.id)
        return None

    def _get_average(self) -> Optional[AverageMethod]:
        return self.average

    def _get_threshold(self) -> Optional[float]:
        return self.threshold

    def _get_k(self) -> Optional[int]:
        return self.k
    
    def _get_quantile(self) -> Optional[float]:
        return self.quantile

    def _get_class(self) -> Optional[str]:
        return self.class_name

    def _get_baseline(self) -> Optional[BaselineConfiguration]:
        return self.baseline

    def _is_model_metric(self) -> bool:
        return is_model_metric(self.metric)

    def _is_aggregable_metric(self) -> bool:
        return is_aggregable_metric(self.metric)

    def _is_custom_metric(self) -> bool:
        return is_custom_metric(self.metric)

    def _is_code_based_metric(self) -> bool:
        return is_code_based_metric(self.metric)

    @validator("threshold")
    def _validate_threshold(cls, value, values):
        if value is not None:
            if value < 0 or value > 1:
                raise ValueError("Threshold must be between 0 and 1, inclusive")
            value = round(value, 2)
        return value

    @validator("k")
    def _validate_k(cls, value, values):
        if value is not None:
            if not (1 <= value <= 12):
                raise ValueError("K must be between 1 and 12, inclusive")
        return value

    @root_validator()
    def _validate_metric_parameters(cls, values):
        value = values["metric"]
        if value is MetricType.CUSTOM_METRIC and values["custom_metric"] is None:
            raise ValueError("Must provide `custom_metric` parameter")

        if value is MetricType.CODE:
            # TODO: Add support when code-based metrics are added to the SDK as an object
            raise NotImplementedError(
                "Code-based metrics are currently not supported through the SDK"
            )

        if (
            value not in [MetricType.COUNT, MetricType.CUSTOM_METRIC, MetricType.CODE]
            and values["field"] is None
        ):
            raise ValueError("Must provide `field` parameter")

        if (
            value
            in [
                MetricType.ACCURACY_AT_K,
                MetricType.PRECISION_AT_K,
                MetricType.RECALL_AT_K,
                MetricType.MAP_AT_K,
                MetricType.MRR_AT_K,
                MetricType.NDCG_AT_K,
            ]
            and values["k"] is None
        ):
            raise ValueError("Must provide `k` parameter` for ranking metrics")

        if (
            value
            in [
                MetricType.JS_DISTANCE,
                MetricType.KS_DISTANCE,
                MetricType.HELLINGER_DISTANCE,
                MetricType.EUCLIDEAN_DISTANCE,
                MetricType.PSI,
            ]
            and values["baseline"] is None
        ):
            raise ValueError("Must provide `baseline` parameter for drift metrics")

        if (
            value
            in [
                MetricType.ACCURACY_PER_CLASS,
                MetricType.PRECISION_PER_CLASS,
                MetricType.RECALL_PER_CLASS,
                MetricType.F1_PER_CLASS,
                MetricType.TP_COUNT_PER_CLASS,
                MetricType.TN_COUNT_PER_CLASS,
                MetricType.FP_COUNT_PER_CLASS,
                MetricType.FN_COUNT_PER_CLASS,
            ]
            and values["class_name"] is None
        ):
            raise ValueError("Must provide `class_name` parameter for multiclass per-class metrics")

        if value in [
            MetricType.TP_COUNT,
            MetricType.TN_COUNT,
            MetricType.FP_COUNT,
            MetricType.FN_COUNT,
            MetricType.ACCURACY,
            MetricType.RECALL,
            MetricType.PRECISION,
            MetricType.F1,
        ]:
            # This was previously validated
            field: SDKField = values["field"]
            if field.type is FieldType.NUMERIC and values["threshold"] is None:
                raise ValueError(
                    "Must provide `threshold` parameter for numeric confusion-matrix metrics"
                )

            if (
                value
                in [
                    MetricType.RECALL,
                    MetricType.PRECISION,
                    MetricType.F1,
                ]
                and field.type is FieldType.CATEGORICAL
                and values["class_name"] is None
            ):
                raise ValueError(
                    "Must provide `average` parameter for multiclass confusion-matrix metrics"
                )

        return values


class MetricOverrideConfiguration(BaseModel):
    field: Optional[SDKField] = None
    average: Optional[AverageMethod] = None
    threshold: Optional[float] = None
    k: Optional[int] = None
    class_name: Optional[str] = None
    baseline: Optional[BaselineConfiguration] = None
    quantile: Optional[float] = None

    def _apply(self, original_metric: MetricConfiguration) -> MetricConfiguration:
        return MetricConfiguration(
            metric=original_metric.metric,
            field=self.field or original_metric.field,
            custom_metric=original_metric.custom_metric,
            average=self.average or original_metric.average,
            threshold=self.threshold or original_metric.threshold,
            k=self.k or original_metric.k,
            class_name=self.class_name or original_metric.class_name,
            baseline=self.baseline or original_metric.baseline,
            quantile=self.quantile or original_metric.quantile,
        )
