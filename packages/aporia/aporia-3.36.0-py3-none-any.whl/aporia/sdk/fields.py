import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from aporia.sdk.client import Client


class FieldType(str, Enum):
    BOOLEAN = "boolean"
    NUMERIC = "numeric"
    DATETIME = "datetime"
    CATEGORICAL = "categorical"
    TEXT = "text"
    ARRAY = "array"
    EMBEDDING = "embedding"
    IMAGE_URL = "image_url"
    NUMERIC_ARRAY = "numeric_array"


class FieldGroup(str, Enum):
    RAW_INPUTS = "raw_inputs"
    FEATURES = "features"
    PREDICTIONS = "predictions"
    ACTUALS = "actuals"


class Field(BaseModel):
    id: str
    name: str
    model_id: str
    type: FieldType
    group: FieldGroup
    properties: Optional[Dict[str, Any]] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_widget(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "modelId": self.model_id,
            "type": self.type.value,
            "category": self.group.value,
            "properties": self.properties,
            "displayName": self.name,
        }

    @classmethod
    def get_model_fields(cls, client: Client, model_id: str) -> List["Field"]:
        response = client.send_request(
            "/fields",
            "GET",
            params={"model_id": model_id},
            url_search_replace=("/api/v1/", "/v1/crud-service/"),
        )
        client.assert_response(response)
        return [cls(**field) for field in response.json()]
