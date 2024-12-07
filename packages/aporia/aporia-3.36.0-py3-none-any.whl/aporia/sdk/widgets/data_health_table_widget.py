from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel
from typing_extensions import Literal

from aporia.sdk.datasets import DatasetType
from aporia.sdk.segments import Segment
from aporia.sdk.versions import Version
from aporia.sdk.widgets.base import (
    BaseWidget,
    DisplayOptions,
    FixedTimeframe,
    VersionSelection,
    WidgetType,
)


class SortType(str, Enum):
    DRIFT_SCORE = "drift_score"
    MISSING_VALUES = "missing_ratio"


class SortDirection(str, Enum):
    DESCENDING = "desc"
    ASCENDING = "asc"


class DataHealthTableWidgetDataOptionsAnnotations(BaseModel):
    phase: DatasetType
    version: VersionSelection
    sortBy: SortType = SortType.DRIFT_SCORE
    sortDirection: SortDirection = SortDirection.DESCENDING
    dataSegment: Optional[Dict] = None
    dataSegmentId: Optional[str] = None
    dataSegmentName: Optional[str] = None
    dataSegmentValue: Optional[Any] = None  # Optional[Union[int, float, str]] = None
    dataSegmentBucketName: Optional[str] = None

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class DataHealthTableWidgetDataOptionsFilters(BaseModel):
    annotations: DataHealthTableWidgetDataOptionsAnnotations
    timeframe: Optional[Union[str, FixedTimeframe]] = None

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class DataHealthTableWidgetDataOptions(BaseModel):
    display: DisplayOptions = DisplayOptions()
    filters: DataHealthTableWidgetDataOptionsFilters


class DataHealthTableWidget(BaseWidget):
    type: Literal[WidgetType.ANOMALY_TABLE] = WidgetType.ANOMALY_TABLE
    dataOptions: List[DataHealthTableWidgetDataOptions]  # Length must be 2?

    @classmethod
    def create(
        cls,
        position: Tuple[int, int],
        size: Tuple[int, int],
        title: str,
        version: Version,
        timeframe: Optional[Union[str, FixedTimeframe]] = None,
        phase: DatasetType = DatasetType.SERVING,
        sort_by: SortType = SortType.DRIFT_SCORE,
        sort_direction: SortDirection = SortDirection.DESCENDING,
        segment: Optional[Segment] = None,
        segment_value: Optional[Any] = None,
    ) -> "DataHealthTableWidget":
        if (segment is None) != (segment_value is None):
            raise ValueError(
                "For using segments, both segment and segment_value arguments are needed"
            )

        version_selection = VersionSelection(id=version.id)

        return DataHealthTableWidget(
            x=position[0],
            y=position[1],
            w=size[0],
            h=size[1],
            name=title,
            dataOptions=[
                DataHealthTableWidgetDataOptions(
                    filters=DataHealthTableWidgetDataOptionsFilters(
                        timeframe=timeframe,
                        annotations=DataHealthTableWidgetDataOptionsAnnotations(
                            phase=phase,
                            version=version_selection,
                            sortBy=sort_by,
                            sortDirection=sort_direction,
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
        segment: Optional[Segment] = None,
        segment_value: Optional[Any] = None,
    ) -> "DataHealthTableWidget":
        color = self.dataOptions[-1].display.color + 1
        version = self.dataOptions[0].filters.annotations.version
        sort_by = self.dataOptions[0].filters.annotations.sortBy
        sort_direction = self.dataOptions[0].filters.annotations.sortDirection

        self.dataOptions.append(
            DataHealthTableWidgetDataOptions(
                display=DisplayOptions(color=color),
                filters=DataHealthTableWidgetDataOptionsFilters(
                    timeframe=timeframe,
                    annotations=DataHealthTableWidgetDataOptionsAnnotations(
                        phase=phase,
                        version=version,
                        sortBy=sort_by,
                        sortDirection=sort_direction,
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
