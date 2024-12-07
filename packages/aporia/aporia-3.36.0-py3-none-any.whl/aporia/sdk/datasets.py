from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from aporia.sdk.base import BaseAporiaResource
from aporia.sdk.client import Client
from aporia.sdk.data_sources import DataSource
from aporia.sdk.fields import FieldType


class DatasetType(str, Enum):
    SERVING = "serving"
    TRAINING = "training"


class FieldSchema(BaseModel):
    name: str
    type: FieldType
    properties: Optional[Dict[str, Any]] = None


class SortOrder(Enum):
    ASCENDING = "ascending"
    DESCENDING = "descending"


class DatasetSchema(BaseModel):
    # Null id and timestamp allowed for training
    id_column: Optional[str]
    timestamp_column: Optional[str]
    order_by_column: Optional[str] = None
    group_by_column: Optional[str] = None
    group_order_sort: Optional[SortOrder] = None
    raw_inputs: List[FieldSchema]
    features: List[FieldSchema]
    predictions: List[FieldSchema]
    actuals: List[FieldSchema]


class Dataset(BaseAporiaResource):
    def __init__(self, client: Client, data: Dict):
        self.client = client
        self.__update_members(data)

    def __update_members(self, data: Dict):
        self.raw_data = data
        self.id = data["id"]

    @classmethod
    def get_all(cls, client: Client, model_version_id: Optional[str] = None) -> List["Dataset"]:
        response = client.send_request(
            f"/datasets{'' if model_version_id is None else f'?model_version_id={model_version_id}'}",
            "GET",
        )

        client.assert_response(response)

        return [cls(client=client, data=entry) for entry in response.json()]

    @classmethod
    def create(
        cls,
        client: Client,
        model_id: str,
        version_id: str,
        dataset_type: DatasetType,
        connection_data: Dict[str, Any],
        schema: DatasetSchema,
        data_source: Optional[DataSource] = None,
        data_source_id: Optional[str] = None,
    ) -> "Dataset":
        dataset_type = DatasetType(dataset_type)

        group_keys = {}

        if schema.group_by_column is not None:
            group_keys["group_by_column"] = schema.group_by_column
        if schema.order_by_column is not None:
            group_keys["order_by_column"] = schema.order_by_column
        if schema.group_order_sort is not None:
            group_keys["group_order_sort"] = schema.group_order_sort.value

        response = client.send_request(
            "/datasets",
            "POST",
            {
                "stage": dataset_type.value,
                "model_version_id": version_id,
                "model_id": model_id,
                "data_source_id": data_source.id if data_source_id is None else data_source_id,
                "config": connection_data,
                "schema": {
                    "id_column": schema.id_column,
                    "timestamp_column": schema.timestamp_column,
                    **group_keys,
                    "raw_inputs": [
                        {"name": raw_input.name, "type": raw_input.type.value}
                        for raw_input in schema.raw_inputs
                    ],
                    "features": [
                        {"name": feature.name, "type": feature.type.value}
                        for feature in schema.features
                    ],
                    "predictions": [
                        {"name": prediction.name, "type": prediction.type.value}
                        for prediction in schema.predictions
                    ],
                    "actuals": [
                        {
                            "name": actual.name,
                            "type": actual.type.value,
                            "properties": actual.properties,
                        }
                        for actual in schema.actuals
                    ],
                },
            },
        )

        client.assert_response(response)

        return cls(client=client, data=response.json())

    @classmethod
    def read(cls, client: Client, id: str) -> "Dataset":
        response = client.send_request(f"/datasets/{id}", "GET")
        client.assert_response(response)
        return cls(client=client, data=response.json())

    def update(
        self,
        # dataset_type: DatasetType | None = None,
        connection_data: Optional[Dict[str, Any]] = None,
        schema: Optional[DatasetSchema] = None,
        data_source: Optional[DataSource] = None,
        data_source_id: Optional[str] = None,
        **kwargs,
    ):
        # dataset_type = DatasetType(dataset_type)

        args = {}
        # if dataset_type is not None:
        #     args["stage"] = dataset_type.value
        if data_source_id is not None or data_source is not None:
            args["data_source_id"] = data_source.id if data_source_id is None else data_source_id
        if connection_data is not None:
            args["config"] = connection_data
        # if schema is not None:
        #     args["schema"] = {
        #         "id_column": schema.id_column,
        #         "timestamp_column": schema.timestamp_column,
        #         "raw_inputs": [
        #             {"name": raw_input.name, "type": raw_input.type.value}
        #             for raw_input in schema.raw_inputs
        #         ],
        #         "features": [
        #             {"name": feature.name, "type": feature.type.value}
        #             for feature in schema.features
        #         ],
        #         "predictions": [
        #             {"name": prediction.name, "type": prediction.type.value}
        #             for prediction in schema.predictions
        #         ],
        #         "actuals": [
        #             {
        #                 "name": actual.name,
        #                 "type": actual.type.value,
        #                 "properties": actual.properties,
        #             }
        #             for actual in schema.actuals
        #         ],
        #     }
        if schema is not None:
            if schema.id_column is not None:
                args["id_column"] = schema.id_column
            if schema.timestamp_column is not None:
                args["timestamp_column"] = schema.timestamp_column

        # response = self.client.send_request(
        #     f"/datasets/{self.id}",
        #     "PUT",
        #     args,
        # )
        response = self.client.send_request(
            f"/datasets/{self.id}/change-query",
            "PUT",
            args,
            url_search_replace=("/api/v1/", "/v1/crud-service/"),
        )
        self.client.assert_response(response)
        # self.__update_members(response.json())
        data = response.json()
        self.raw_data["config"] = data["config"]
        self.raw_data["schema"]["id_column"] = data["id_column"]
        self.raw_data["schema"]["timestamp_column"] = data["timestamp_column"]
        self.raw_data["data_source_id"] = data["data_source_id"]

    def delete(self):
        response = self.client.send_request(f"/datasets/{self.id}", "DELETE")
        self.client.assert_response(response)

    @staticmethod
    def delete_by_id(client: Client, id: str):
        response = client.send_request(f"/datasets/{id}", "DELETE")
        client.assert_response(response)
