from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel
from typing_extensions import Literal

from aporia.sdk.datasets import DatasetType
from aporia.sdk.fields import Field as SDKField
from aporia.sdk.fields import FieldGroup
from aporia.sdk.segments import Segment
from aporia.sdk.versions import Version
from aporia.sdk.widgets.base import (
    BaseWidget,
    DisplayOptions,
    FixedTimeframe,
    VersionSelection,
    WidgetType,
)


class DistributionWidgetDataOptionsAnnotations(BaseModel):
    field: Dict
    phase: DatasetType
    version: VersionSelection = VersionSelection()
    fieldCategory: FieldGroup
    dataSegment: Optional[Dict] = None
    dataSegmentId: Optional[str] = None
    dataSegmentName: Optional[str] = None
    dataSegmentValue: Optional[Any] = None  # Optional[Union[int, float, str]] = None
    dataSegmentBucketName: Optional[str] = None

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class DistributionWidgetDataOptionsFilters(BaseModel):
    annotations: DistributionWidgetDataOptionsAnnotations
    timeframe: Optional[Union[str, FixedTimeframe]] = None

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class DistributionWidgetDataOptions(BaseModel):
    display: DisplayOptions = DisplayOptions()
    filters: DistributionWidgetDataOptionsFilters


class DistributionWidget(BaseWidget):
    type: Literal[WidgetType.DISTRIBUTION] = WidgetType.DISTRIBUTION
    dataOptions: List[DistributionWidgetDataOptions]  # Length must be at most 2?

    @classmethod
    def create(
        cls,
        position: Tuple[int, int],
        size: Tuple[int, int],
        title: str,
        field: SDKField,
        timeframe: Optional[Union[str, FixedTimeframe]] = None,
        phase: DatasetType = DatasetType.SERVING,
        version: Optional[Version] = None,
        segment: Optional[Segment] = None,
        segment_value: Optional[Any] = None,
    ) -> "DistributionWidget":
        if (segment is None) != (segment_value is None):
            raise ValueError(
                "For using segments, both segment and segment_value arguments are needed"
            )

        version_selection = (
            VersionSelection(id=version.id) if version is not None else VersionSelection()
        )

        return DistributionWidget(
            x=position[0],
            y=position[1],
            w=size[0],
            h=size[1],
            name=title,
            dataOptions=[
                DistributionWidgetDataOptions(
                    filters=DistributionWidgetDataOptionsFilters(
                        timeframe=timeframe,
                        annotations=DistributionWidgetDataOptionsAnnotations(
                            phase=phase,
                            version=version_selection,
                            field=field.to_widget(),
                            fieldCategory=field.group,
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
        timeframe: Optional[Union[str, FixedTimeframe]] = None,
        phase: DatasetType = DatasetType.SERVING,
        version: Optional[Version] = None,
        segment: Optional[Segment] = None,
        segment_value: Optional[Any] = None,
    ) -> "DistributionWidget":
        color = self.dataOptions[-1].display.color + 1
        field = self.dataOptions[0].filters.annotations.field
        field_category = self.dataOptions[0].filters.annotations.fieldCategory

        version_selection = (
            VersionSelection(id=version.id) if version is not None else VersionSelection()
        )

        self.dataOptions.append(
            DistributionWidgetDataOptions(
                display=DisplayOptions(color=color),
                filters=DistributionWidgetDataOptionsFilters(
                    timeframe=timeframe,
                    annotations=DistributionWidgetDataOptionsAnnotations(
                        phase=phase,
                        version=version_selection,
                        field=field,
                        fieldCategory=field_category,
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
