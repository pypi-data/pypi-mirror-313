from typing import List, Tuple

from pydantic import BaseModel, validator
from typing_extensions import Literal

from aporia.sdk.widgets.base import BaseWidget, DisplayOptions, WidgetType


class TextWidgetDataOptionsAnnotations(BaseModel):
    text: str
    fontSize: int

    @validator("fontSize")
    def _validate_font_size(cls, value, values):
        if value > 32 or value < 8:
            raise ValueError("Font size must be in the range [8,32]")
        return value


class TextWidgetDataOptionsFilters(BaseModel):
    annotations: TextWidgetDataOptionsAnnotations


class TextWidgetDataOptions(BaseModel):
    display: DisplayOptions = DisplayOptions()
    filters: TextWidgetDataOptionsFilters


class TextWidget(BaseWidget):
    name: str = "Text Widget"
    type: Literal[WidgetType.TEXT] = WidgetType.TEXT
    dataOptions: List[TextWidgetDataOptions]  # Length must be 1?

    @classmethod
    def create(
        cls, position: Tuple[int, int], size: Tuple[int, int], text: str, font: int = 24
    ) -> "TextWidget":
        return TextWidget(
            x=position[0],
            y=position[1],
            w=size[0],
            h=size[1],
            dataOptions=[
                TextWidgetDataOptions(
                    filters=TextWidgetDataOptionsFilters(
                        annotations=TextWidgetDataOptionsAnnotations(text=text, fontSize=font)
                    )
                )
            ],
        )
