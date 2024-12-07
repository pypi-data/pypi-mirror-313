from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel
from typing_extensions import Literal

from aporia.sdk.datasets import DatasetType
from aporia.sdk.fields import Field as SDKField
from aporia.sdk.fields import FieldGroup
from aporia.sdk.segments import Segment
from aporia.sdk.versions import Version
from aporia.sdk.widgets.base import BaseWidget, DisplayOptions, VersionSelection, WidgetType


class HistogramOverTimeWidgetDataOptionsAnnotations(BaseModel):
    field: Dict
    phase: Literal[DatasetType.SERVING] = DatasetType.SERVING
    version: VersionSelection = VersionSelection()
    fieldCategory: FieldGroup
    granularity: Optional[str] = None
    dataSegment: Optional[Dict] = None
    dataSegmentId: Optional[str] = None
    dataSegmentName: Optional[str] = None
    dataSegmentValue: Optional[Any] = None  # Optional[Union[int, float, str]] = None
    dataSegmentBucketName: Optional[str] = None

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class HistogramOverTimeWidgetDataOptionsFilters(BaseModel):
    annotations: HistogramOverTimeWidgetDataOptionsAnnotations


class HistogramOverTimeWidgetDataOptions(BaseModel):
    display: DisplayOptions = DisplayOptions()
    filters: HistogramOverTimeWidgetDataOptionsFilters


class HistogramOverTimeWidget(BaseWidget):
    type: Literal[WidgetType.TIME_SERIES_HISTOGRAM] = WidgetType.TIME_SERIES_HISTOGRAM
    dataOptions: List[HistogramOverTimeWidgetDataOptions]  # Length must be at most 2?

    @classmethod
    def create(
        cls,
        position: Tuple[int, int],
        size: Tuple[int, int],
        title: str,
        field: SDKField,
        version: Optional[Version] = None,
        segment: Optional[Segment] = None,
        segment_value: Optional[Any] = None,
        granularity: Optional[str] = None,
    ) -> "HistogramOverTimeWidget":
        if (segment is None) != (segment_value is None):
            raise ValueError(
                "For using segments, both segment and segment_value arguments are needed"
            )

        version_selection = (
            VersionSelection(id=version.id) if version is not None else VersionSelection()
        )

        return HistogramOverTimeWidget(
            x=position[0],
            y=position[1],
            w=size[0],
            h=size[1],
            name=title,
            dataOptions=[
                HistogramOverTimeWidgetDataOptions(
                    filters=HistogramOverTimeWidgetDataOptionsFilters(
                        annotations=HistogramOverTimeWidgetDataOptionsAnnotations(
                            version=version_selection,
                            field=field.to_widget(),
                            granularity=granularity,
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
