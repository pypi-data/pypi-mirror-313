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


class MetricCorrelationWidgetDataOptionsAnnotations(BaseModel):
    phase: Literal[DatasetType.SERVING] = DatasetType.SERVING
    version: Union[VersionSelection, List[VersionSelection]] = VersionSelection()
    dataSegmentId: Optional[str] = None
    dataSegmentName: Optional[str] = None
    dataSegmentValue: Optional[
        Union[List[Union[int, float, str]], Union[int, float, str]]
    ] = None  # For dataSegmentValue and version, just one of them is a list
    dataSegmentBucketName: Optional[
        str
    ] = None  # This appears only when dataSegmentValue is not a list
    # X axis
    xAxisMetric: Union[
        MetricType, str
    ]  # If the metric is a string, it is a custom metric/code-based metric ID
    isXAxisModelMetric: bool = False
    isXAxisCustomMetric: bool = False
    isXAxisCodeBasedMetric: bool = False
    isXAxisAggregableMetric: bool = True
    xAxisField: Optional[Dict] = None
    xAxisFieldCategory: Optional[FieldGroup] = None
    xAxisAverage: Optional[AverageMethod] = None
    xAxisMetricPerClass: Optional[str] = None
    xAxisMetricBaseline: Optional[BaselineConfiguration] = None
    xAxisThreshold: Optional[float] = None
    xAxisMetricAtK: Optional[int] = None
    xAxisQuantile: Optional[float] = None
    xAxisParameters: Optional[MetricParameters] = None
    # Y axis
    yAxisMetric: Union[
        MetricType, str
    ]  # If the metric is a string, it is a custom metric/code-based metric ID
    isYAxisModelMetric: bool = False
    isYAxisCustomMetric: bool = False
    isYAxisCodeBasedMetric: bool = False
    isYAxisAggregableMetric: bool = True
    yAxisField: Optional[Dict] = None
    yAxisFieldCategory: Optional[FieldGroup] = None
    yAxisAverage: Optional[AverageMethod] = None
    yAxisMetricPerClass: Optional[str] = None
    yAxisMetricBaseline: Optional[BaselineConfiguration] = None
    yAxisThreshold: Optional[float] = None
    yAxisMetricAtK: Optional[int] = None
    yAxisQuantile: Optional[float] = None
    yAxisParameters: Optional[MetricParameters] = None

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class MetricCorrelationWidgetDataOptionsFilters(BaseModel):
    annotations: MetricCorrelationWidgetDataOptionsAnnotations
    timeframe: Optional[Union[str, FixedTimeframe]] = None


class MetricCorrelationWidgetDataOptions(BaseModel):
    display: DisplayOptions = DisplayOptions()
    filters: MetricCorrelationWidgetDataOptionsFilters


class MetricCorrelationWidget(BaseWidget):
    type: Literal[WidgetType.METRIC_CORRELATION] = WidgetType.METRIC_CORRELATION
    dataOptions: List[MetricCorrelationWidgetDataOptions]  # Length must be at most 2?

    @classmethod
    def create(
        cls,
        position: Tuple[int, int],
        size: Tuple[int, int],
        title: str,
        x_axis_metric: MetricConfiguration,
        y_axis_metric: MetricConfiguration,
        phase: DatasetType = DatasetType.SERVING,
        timeframe: Optional[Union[str, FixedTimeframe]] = None,
        # Mutually Exclusive
        version: Optional[Version] = None,
        versions: Optional[List[Optional[Version]]] = None,
        segment: Optional[Segment] = None,
        # Mutually Exclusive
        segment_value: Optional[Any] = None,
        segment_values: Optional[List[Any]] = None,
    ) -> "MetricCorrelationWidget":
        if version and versions:
            raise ValueError("Can't use both version and versions arguments")

        if segment_value is not None and segment_values is not None:
            raise ValueError("Can't use both segment_value and segment_values arguments")

        if segment is not None and segment_value is None and segment_values is None:
            if versions:
                raise ValueError(
                    "When using multiple versions and a segment, must specify segment_value"
                )
            segment_values = segment.values

        if segment_values is not None and versions is not None:
            raise ValueError("Can't pass segment_values when using multiple versions")

        if versions is None and segment is not None and segment_value is not None:
            segment_values = [segment_value]
            segment_value = None

        if (segment is None) != (segment_value is None and segment_values is None):
            raise ValueError(
                "For using segments, both segment and segment_value/segment_values arguments are needed"
            )

        if segment_values is not None:
            fixed_values = []
            for value in segment_values:
                if value in segment.get_widget_values():
                    fixed_values.append(value)
            if len(fixed_values) == 0:
                raise RuntimeError("No valid values given to segment")
            segment_values = fixed_values

        if version is None and versions is None:
            version_selection = VersionSelection()
        elif version is not None:
            version_selection = VersionSelection(id=version.id)
        else:
            version_selection = [
                VersionSelection(id=version.id) if version is not None else VersionSelection()
                for version in versions
            ]

        return MetricCorrelationWidget(
            _internal_state={"x_metric": x_axis_metric, "y_metric": y_axis_metric},
            x=position[0],
            y=position[1],
            w=size[0],
            h=size[1],
            name=title,
            dataOptions=[
                MetricCorrelationWidgetDataOptions(
                    filters=MetricCorrelationWidgetDataOptionsFilters(
                        timeframe=timeframe,
                        annotations=MetricCorrelationWidgetDataOptionsAnnotations(
                            phase=phase,
                            version=version_selection,
                            # X axis
                            xAxisMetric=x_axis_metric._get_metric(),
                            xAxisField=x_axis_metric._get_field(),
                            xAxisFieldCategory=x_axis_metric._get_field_category(),
                            xAxisMetricBaseline=x_axis_metric._get_baseline(),
                            xAxisThreshold=x_axis_metric._get_threshold(),
                            xAxisMetricAtK=x_axis_metric._get_k(),
                            xAxisQuantile=x_axis_metric._get_quantile(),
                            xAxisMetricPerClass=x_axis_metric._get_class(),
                            xAxisAverage=x_axis_metric._get_average(),
                            xAxisParameters=x_axis_metric._get_parameters(),
                            isXAxisAggregableMetric=x_axis_metric._is_aggregable_metric(),
                            isXAxisModelMetric=x_axis_metric._is_model_metric(),
                            isXAxisCustomMetric=x_axis_metric._is_custom_metric(),
                            isXAxisCodeBasedMetric=x_axis_metric._is_code_based_metric(),
                            # Y axis
                            yAxisMetric=y_axis_metric._get_metric(),
                            yAxisField=y_axis_metric._get_field(),
                            yAxisFieldCategory=y_axis_metric._get_field_category(),
                            yAxisMetricBaseline=y_axis_metric._get_baseline(),
                            yAxisThreshold=y_axis_metric._get_threshold(),
                            yAxisMetricAtK=y_axis_metric._get_k(),
                            yAxisQuantile=y_axis_metric._get_quantile(),
                            yAxisMetricPerClass=y_axis_metric._get_class(),
                            yAxisAverage=y_axis_metric._get_average(),
                            yAxisParameters=y_axis_metric._get_parameters(),
                            isYAxisAggregableMetric=y_axis_metric._is_aggregable_metric(),
                            isYAxisModelMetric=y_axis_metric._is_model_metric(),
                            isYAxisCustomMetric=y_axis_metric._is_custom_metric(),
                            isYAxisCodeBasedMetric=y_axis_metric._is_code_based_metric(),
                            # Segment
                            dataSegmentId=segment.id if segment is not None else None,
                            dataSegmentName=segment.name if segment is not None else None,
                            dataSegmentValue=(
                                (segment_value or segment_values) if segment is not None else None
                            ),
                            dataSegmentBucketName=(
                                [
                                    bucket["name"]
                                    for bucket in segment.to_widget()["buckets"]
                                    if bucket["value"] == segment_value
                                ][0]
                                if segment is not None and segment_value is not None
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
        timeframe: Optional[Union[str, FixedTimeframe]] = None,
        x_axis_metric_overrides: MetricOverrideConfiguration = MetricOverrideConfiguration(),
        y_axis_metric_overrides: MetricOverrideConfiguration = MetricOverrideConfiguration(),
        # Mutually Exclusive
        version: Optional[Version] = None,
        versions: Optional[List[Optional[Version]]] = None,
        segment: Optional[Segment] = None,
        # Mutually Exclusive
        segment_value: Optional[Any] = None,
        segment_values: Optional[List[Any]] = None,
    ) -> "MetricCorrelationWidget":
        # TODO: Consider enforcing compare limits here
        original_x_axis_metric: MetricConfiguration = self._internal_state["x_metric"]
        x_axis_metric = x_axis_metric_overrides._apply(original_x_axis_metric)
        original_y_axis_metric: MetricConfiguration = self._internal_state["y_metric"]
        y_axis_metric = y_axis_metric_overrides._apply(original_y_axis_metric)
        color = self.dataOptions[-1].display.color + 1

        if version and versions:
            raise ValueError("Can't use both version and versions arguments")

        if segment_value is not None and segment_values is not None:
            raise ValueError("Can't use both segment_value and segment_values arguments")

        if segment is not None and segment_value is None and segment_values is None:
            if versions:
                raise ValueError(
                    "When using multiple versions and a segment, must specify segment_value"
                )
            segment_values = segment.values

        if segment_values is not None and versions is not None:
            raise ValueError("Can't pass segment_values when using multiple versions")

        if versions is None and segment is not None and segment_value is not None:
            segment_values = [segment_value]
            segment_value = None

        if (segment is None) != (segment_value is None and segment_values is None):
            raise ValueError(
                "For using segments, both segment and segment_value/segment_values arguments are needed"
            )

        if segment_values is not None:
            fixed_values = []
            for value in segment_values:
                if value in segment.get_widget_values():
                    fixed_values.append(value)
            if len(fixed_values) == 0:
                raise RuntimeError("No valid values given to segment")
            segment_values = fixed_values

        if version is None and versions is None:
            version_selection = VersionSelection()
        elif version is not None:
            version_selection = VersionSelection(id=version.id)
        else:
            version_selection = [
                VersionSelection(id=version.id) if version is not None else VersionSelection()
                for version in versions
            ]

        self.dataOptions.append(
            MetricCorrelationWidgetDataOptions(
                display=DisplayOptions(color=color),
                filters=MetricCorrelationWidgetDataOptionsFilters(
                    timeframe=timeframe,
                    annotations=MetricCorrelationWidgetDataOptionsAnnotations(
                        phase=phase,
                        version=version_selection,
                        # X axis
                        xAxisMetric=x_axis_metric._get_metric(),
                        xAxisField=x_axis_metric._get_field(),
                        xAxisFieldCategory=x_axis_metric._get_field_category(),
                        xAxisMetricBaseline=x_axis_metric._get_baseline(),
                        xAxisThreshold=x_axis_metric._get_threshold(),
                        xAxisMetricAtK=x_axis_metric._get_k(),
                        xAxisQuantile=x_axis_metric._get_quantile(),
                        xAxisMetricPerClass=x_axis_metric._get_class(),
                        xAxisAverage=x_axis_metric._get_average(),
                        xAxisParameters=x_axis_metric._get_parameters(),
                        isXAxisAggregableMetric=x_axis_metric._is_aggregable_metric(),
                        isXAxisModelMetric=x_axis_metric._is_model_metric(),
                        isXAxisCustomMetric=x_axis_metric._is_custom_metric(),
                        isXAxisCodeBasedMetric=x_axis_metric._is_code_based_metric(),
                        # Y axis
                        yAxisMetric=y_axis_metric._get_metric(),
                        yAxisField=y_axis_metric._get_field(),
                        yAxisFieldCategory=y_axis_metric._get_field_category(),
                        yAxisMetricBaseline=y_axis_metric._get_baseline(),
                        yAxisThreshold=y_axis_metric._get_threshold(),
                        yAxisMetricAtK=y_axis_metric._get_k(),
                        yAxisQuantile=y_axis_metric._get_quantile(),
                        yAxisMetricPerClass=y_axis_metric._get_class(),
                        yAxisAverage=y_axis_metric._get_average(),
                        yAxisParameters=y_axis_metric._get_parameters(),
                        isYAxisAggregableMetric=y_axis_metric._is_aggregable_metric(),
                        isYAxisModelMetric=y_axis_metric._is_model_metric(),
                        isYAxisCustomMetric=y_axis_metric._is_custom_metric(),
                        isYAxisCodeBasedMetric=y_axis_metric._is_code_based_metric(),
                        # Segment
                        dataSegmentId=segment.id if segment is not None else None,
                        dataSegmentName=segment.name if segment is not None else None,
                        dataSegmentValue=(
                            (segment_value or segment_values) if segment is not None else None
                        ),
                        dataSegmentBucketName=(
                            [
                                bucket["name"]
                                for bucket in segment.to_widget()["buckets"]
                                if bucket["value"] == segment_value
                            ][0]
                            if segment is not None and segment_value is not None
                            else None
                        ),
                    ),
                ),
            )
        )
        return self
