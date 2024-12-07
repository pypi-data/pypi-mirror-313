from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel
from typing_extensions import Literal

from aporia.sdk.datasets import DatasetType
from aporia.sdk.fields import FieldGroup
from aporia.sdk.metrics import AverageMethod, MetricType
from aporia.sdk.segments import Segment
from aporia.sdk.versions import Version
from aporia.sdk.widgets.base import (
    BaselineConfiguration,
    BaseWidget,
    DisplayOptions,
    FixedTimeframe,
    MetricConfiguration,
    MetricOverrideConfiguration,
    MetricParameters,
    VersionSelection,
    WidgetType,
)


class MetricWidgetDataOptionsAnnotations(BaseModel):
    phase: DatasetType
    metric: Union[MetricType, str]
    version: VersionSelection = VersionSelection()
    field: Optional[Dict] = None
    fieldCategory: Optional[FieldGroup] = None
    baseline: Optional[BaselineConfiguration] = None
    threshold: Optional[float] = None
    metricAtK: Optional[int] = None
    quantile: Optional[float] = None
    metricPerClass: Optional[str] = None
    average: Optional[AverageMethod] = None
    parameters: Optional[MetricParameters] = None
    isModelMetric: bool = True
    isCustomMetric: bool = False
    isAggregableMetric: bool = True
    isCodeBasedMetric: bool = False
    dataSegment: Optional[Dict] = None
    dataSegmentId: Optional[str] = None
    dataSegmentName: Optional[str] = None
    dataSegmentValue: Optional[
        Any
    ] = None  # TODO: For some reason, this is casting numerics to strings. Changed "Union[int, float, str]" to "Any"
    dataSegmentBucketName: Optional[str] = None

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class MetricWidgetDataOptionsFilters(BaseModel):
    annotations: MetricWidgetDataOptionsAnnotations
    timeframe: Optional[Union[str, FixedTimeframe]] = None

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class MetricWidgetDataOptions(BaseModel):
    display: DisplayOptions = DisplayOptions()
    filters: MetricWidgetDataOptionsFilters


class MetricWidget(BaseWidget):
    type: Literal[WidgetType.METRIC] = WidgetType.METRIC
    dataOptions: List[MetricWidgetDataOptions]  # Length must be at most 2?

    @classmethod
    def create(
        cls,
        position: Tuple[int, int],
        size: Tuple[int, int],
        title: str,
        metric: MetricConfiguration,
        timeframe: Optional[Union[str, FixedTimeframe]] = None,
        phase: DatasetType = DatasetType.SERVING,
        version: Optional[Version] = None,
        segment: Optional[Segment] = None,
        segment_value: Optional[Any] = None,
    ) -> "MetricWidget":
        if (segment is None) != (segment_value is None):
            raise ValueError(
                "For using segments, both segment and segment_value arguments are needed"
            )

        version_selection = (
            VersionSelection(id=version.id) if version is not None else VersionSelection()
        )

        return MetricWidget(
            _internal_state={"metric": metric},
            x=position[0],
            y=position[1],
            w=size[0],
            h=size[1],
            name=title,
            dataOptions=[
                MetricWidgetDataOptions(
                    filters=MetricWidgetDataOptionsFilters(
                        timeframe=timeframe,
                        annotations=MetricWidgetDataOptionsAnnotations(
                            phase=phase,
                            metric=metric._get_metric(),
                            version=version_selection,
                            field=metric._get_field(),
                            fieldCategory=metric._get_field_category(),
                            baseline=metric.baseline,
                            threshold=metric.threshold,
                            metricAtK=metric.k,
                            quantile=metric.quantile,
                            metricPerClass=metric.class_name,
                            average=metric.average,
                            parameters=metric._get_parameters(),
                            isModelMetric=metric._is_model_metric(),
                            isCustomMetric=metric._is_custom_metric(),
                            isAggregableMetric=metric._is_aggregable_metric(),
                            isCodeBasedMetric=metric._is_code_based_metric(),
                            dataSegment=segment.to_widget() if segment is not None else None,
                            dataSegmentId=segment.id if segment is not None else None,
                            dataSegmentName=segment.name if segment is not None else None,
                            dataSegmentValue=segment_value if segment is not None else None,
                            dataSegmentBucketName=(
                                [
                                    bucket["name"]
                                    for bucket in segment.to_widget()["buckets"]
                                    if bucket["value"] == segment_value
                                ][0]
                                if segment is not None
                                else None
                            ),
                        ),
                    )
                )
            ],
        )

    def compare(
        self,
        phase: DatasetType = DatasetType.SERVING,
        version: Optional[Version] = None,
        timeframe: Optional[Union[str, FixedTimeframe]] = None,
        metric_overrides: MetricOverrideConfiguration = MetricOverrideConfiguration(),
        segment: Optional[Segment] = None,
        segment_value: Optional[Any] = None,
    ) -> "MetricWidget":
        # TODO: Consider enforcing compare limits here
        original_metric: MetricConfiguration = self._internal_state["metric"]
        metric = metric_overrides._apply(original_metric)
        color = self.dataOptions[-1].display.color + 1

        version_selection = (
            VersionSelection(id=version.id) if version is not None else VersionSelection()
        )

        self.dataOptions.append(
            MetricWidgetDataOptions(
                display=DisplayOptions(color=color),
                filters=MetricWidgetDataOptionsFilters(
                    timeframe=timeframe,
                    annotations=MetricWidgetDataOptionsAnnotations(
                        phase=phase,
                        metric=metric._get_metric(),
                        version=version_selection,
                        field=metric._get_field(),
                        fieldCategory=metric._get_field_category(),
                        baseline=metric._get_baseline(),
                        threshold=metric._get_threshold(),
                        metricAtK=metric._get_k(),
                        quantile=metric._get_quantile(),
                        metricPerClass=metric._get_class(),
                        average=metric._get_average(),
                        parameters=metric._get_parameters(),
                        isModelMetric=metric._is_model_metric(),
                        isCustomMetric=metric._is_custom_metric(),
                        isAggregableMetric=metric._is_aggregable_metric(),
                        isCodeBasedMetric=metric._is_code_based_metric(),
                        dataSegment=segment.to_widget() if segment is not None else None,
                        dataSegmentId=segment.id if segment is not None else None,
                        dataSegmentName=segment.name if segment is not None else None,
                        dataSegmentValue=segment_value if segment is not None else None,
                        dataSegmentBucketName=(
                            [
                                bucket["name"]
                                for bucket in segment.to_widget()["buckets"]
                                if bucket["value"] == segment_value
                            ][0]
                            if segment is not None
                            else None
                        ),
                    ),
                ),
            ),
        )
        return self
