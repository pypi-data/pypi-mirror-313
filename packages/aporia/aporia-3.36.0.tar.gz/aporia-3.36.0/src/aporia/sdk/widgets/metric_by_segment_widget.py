from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel
from typing_extensions import Literal

from aporia.sdk.datasets import DatasetType
from aporia.sdk.fields import FieldGroup
from aporia.sdk.metrics import MetricType
from aporia.sdk.monitors import AverageMethod
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


class MetricBySegmentWidgetDataOptionsAnnotations(BaseModel):
    phase: Literal[DatasetType.SERVING] = DatasetType.SERVING
    metric: Union[
        MetricType, str
    ]  # If the metric is a string, it is a custom metric/code-based metric ID
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
    dataSegmentId: Optional[str] = None
    dataSegmentName: Optional[str] = None
    dataSegmentValue: Optional[Union[List[Union[int, float, str]], Union[int, float, str]]] = None
    dataSegmentBucketName: Optional[List[str]] = None

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class MetricBySegmentWidgetDataOptionsFilters(BaseModel):
    annotations: MetricBySegmentWidgetDataOptionsAnnotations
    timeframe: Optional[Union[str, FixedTimeframe]] = None


class MetricBySegmentWidgetDataOptions(BaseModel):
    display: DisplayOptions = DisplayOptions()
    filters: MetricBySegmentWidgetDataOptionsFilters


class MetricBySegmentWidget(BaseWidget):
    type: Literal[WidgetType.METRIC_BY_SEGMENT] = WidgetType.METRIC_BY_SEGMENT
    dataOptions: List[MetricBySegmentWidgetDataOptions]  # Length must be at most 2?

    @classmethod
    def create(
        cls,
        position: Tuple[int, int],
        size: Tuple[int, int],
        title: str,
        metric: MetricConfiguration,
        segment: Segment,
        segment_values: List[Any],
        version: Optional[Version] = None,
        phase: DatasetType = DatasetType.SERVING,
        timeframe: Optional[Union[str, FixedTimeframe]] = None,
    ) -> "MetricBySegmentWidget":
        fixed_values = []
        for value in segment_values:
            if value in segment.get_widget_values():
                fixed_values.append(value)
        if len(fixed_values) == 0:
            raise RuntimeError("No valid values given to segment")
        segment_values = fixed_values

        version_selection = (
            VersionSelection(id=version.id) if version is not None else VersionSelection()
        )

        return MetricBySegmentWidget(
            _internal_state={"metric": metric},
            x=position[0],
            y=position[1],
            w=size[0],
            h=size[1],
            name=title,
            dataOptions=[
                MetricBySegmentWidgetDataOptions(
                    filters=MetricBySegmentWidgetDataOptionsFilters(
                        timeframe=timeframe,
                        annotations=MetricBySegmentWidgetDataOptionsAnnotations(
                            metric=metric._get_metric(),
                            version=version_selection,
                            phase=phase,
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
                            dataSegmentId=segment.id,
                            dataSegmentName=segment.name,
                            dataSegmentValue=segment_values,
                            dataSegmentBucketName=(
                                [
                                    bucket["name"]
                                    for bucket in segment.to_widget()["buckets"]
                                    if bucket["value"] in segment_values
                                ]
                            ),
                        ),
                    )
                )
            ],
        )

    def compare(
        self,
        version: Optional[Version] = None,
        metric: Optional[MetricConfiguration] = None,
        metric_overrides: Optional[MetricOverrideConfiguration] = None,
        phase: DatasetType = DatasetType.SERVING,
        timeframe: Optional[Union[str, FixedTimeframe]] = None,
    ) -> "MetricBySegmentWidget":
        # TODO: Consider enforcing compare limits here
        original_metric: MetricConfiguration = self._internal_state["metric"]
        if metric is not None and metric_overrides is not None:
            raise ValueError("Can't provide both metric and metric_overrides.")
        if metric is not None:
            metric = metric
        elif metric_overrides is not None:
            metric = metric_overrides._apply(original_metric)
        else:
            metric = MetricOverrideConfiguration()._apply(original_metric)
        color = self.dataOptions[-1].display.color + 1
        data_segment_id = self.dataOptions[-1].filters.annotations.dataSegmentId
        data_segment_name = self.dataOptions[-1].filters.annotations.dataSegmentName
        data_segment_value = self.dataOptions[-1].filters.annotations.dataSegmentValue
        data_segment_bucket_name = self.dataOptions[-1].filters.annotations.dataSegmentBucketName

        version_selection = (
            VersionSelection(id=version.id) if version is not None else VersionSelection()
        )

        self.dataOptions.append(
            MetricBySegmentWidgetDataOptions(
                display=DisplayOptions(color=color),
                filters=MetricBySegmentWidgetDataOptionsFilters(
                    timeframe=timeframe,
                    annotations=MetricBySegmentWidgetDataOptionsAnnotations(
                        metric=metric._get_metric(),
                        version=version_selection,
                        phase=phase,
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
                        dataSegmentId=data_segment_id,
                        dataSegmentName=data_segment_name,
                        dataSegmentValue=data_segment_value,
                        dataSegmentBucketName=data_segment_bucket_name,
                    ),
                ),
            )
        )
        return self
