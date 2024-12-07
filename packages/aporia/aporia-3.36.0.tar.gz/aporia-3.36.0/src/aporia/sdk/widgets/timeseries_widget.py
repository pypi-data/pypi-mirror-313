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
    MetricConfiguration,
    MetricOverrideConfiguration,
    MetricParameters,
    VersionSelection,
    WidgetType,
)


class TimeSeriesWidgetDataOptionsAnnotations(BaseModel):
    phase: Literal[DatasetType.SERVING] = DatasetType.SERVING
    metric: Union[MetricType, str]
    version: Union[VersionSelection, List[VersionSelection]] = VersionSelection()
    field: Optional[Dict] = None
    fieldCategory: Optional[FieldGroup] = None
    granularity: Optional[
        str
    ] = None  # Optional[TimePeriod] = None # TODO: Find a way to implicitly convert a string to TimePeriod
    baseline: Optional[BaselineConfiguration] = None
    threshold: Optional[float] = None
    metricAtK: Optional[int] = None
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
        Union[List[Union[int, float, str]], Union[int, float, str]]
    ] = None  # For dataSegmentValue and version, just one of them is a list
    dataSegmentBucketName: Optional[
        str
    ] = None  # This appears only when dataSegmentValue is not a list

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class TimeSeriesWidgetDataOptionsFilters(BaseModel):
    annotations: TimeSeriesWidgetDataOptionsAnnotations


class TimeSeriesWidgetDataOptions(BaseModel):
    display: DisplayOptions = DisplayOptions()
    filters: TimeSeriesWidgetDataOptionsFilters


class TimeSeriesWidget(BaseWidget):
    type: Literal[WidgetType.TIME_SERIES] = WidgetType.TIME_SERIES
    dataOptions: List[TimeSeriesWidgetDataOptions]  # Length must be at most 2?

    @classmethod
    def create(
        cls,
        position: Tuple[int, int],
        size: Tuple[int, int],
        title: str,
        metric: MetricConfiguration,
        # Mutually Exclusive
        version: Optional[Version] = None,
        versions: Optional[List[Optional[Version]]] = None,
        segment: Optional[Segment] = None,
        # Mutually Exclusive
        segment_value: Optional[Any] = None,
        segment_values: Optional[List[Any]] = None,
        granularity: Optional[str] = None,
    ) -> "TimeSeriesWidget":
        if version is not None and versions is not None:
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

        return TimeSeriesWidget(
            _internal_state={"metric": metric},
            x=position[0],
            y=position[1],
            w=size[0],
            h=size[1],
            name=title,
            dataOptions=[
                TimeSeriesWidgetDataOptions(
                    filters=TimeSeriesWidgetDataOptionsFilters(
                        annotations=TimeSeriesWidgetDataOptionsAnnotations(
                            metric=metric._get_metric(),
                            version=version_selection,
                            field=metric._get_field(),
                            fieldCategory=metric._get_field_category(),
                            baseline=metric._get_baseline(),
                            threshold=metric._get_threshold(),
                            metricAtK=metric._get_k(),
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
                            granularity=granularity,
                        ),
                    )
                )
            ],
        )

    def compare(
        self,
        # Mutually Exclusive
        version: Optional[Version] = None,
        versions: Optional[List[Optional[Version]]] = None,
        metric_overrides: MetricOverrideConfiguration = MetricOverrideConfiguration(),
        segment: Optional[Segment] = None,
        # Mutually Exclusive
        segment_value: Optional[Any] = None,
        segment_values: Optional[List[Any]] = None,
    ) -> "TimeSeriesWidget":
        # TODO: Consider enforcing compare limits here
        original_metric: MetricConfiguration = self._internal_state["metric"]
        metric = metric_overrides._apply(original_metric)
        granularity = self.dataOptions[0].filters.annotations.granularity
        color = self.dataOptions[-1].display.color + 1
        if version is not None and versions is not None:
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
            TimeSeriesWidgetDataOptions(
                display=DisplayOptions(color=color),
                filters=TimeSeriesWidgetDataOptionsFilters(
                    annotations=TimeSeriesWidgetDataOptionsAnnotations(
                        metric=metric._get_metric(),
                        version=version_selection,
                        field=metric._get_field(),
                        fieldCategory=metric._get_field_category(),
                        baseline=metric._get_baseline(),
                        threshold=metric._get_threshold(),
                        metricAtK=metric._get_k(),
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
                        granularity=granularity,
                    ),
                ),
            )
        )
        return self
