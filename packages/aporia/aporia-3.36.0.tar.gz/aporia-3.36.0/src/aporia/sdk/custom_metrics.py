from typing import Dict, List, Optional

from aporia.sdk.base import BaseAporiaResource
from aporia.sdk.client import Client


class CustomMetric(BaseAporiaResource):
    def __init__(self, client: Client, data: Dict):
        self.client = client
        self.__update_members(data)

    def __update_members(self, data: Dict):
        self.id = data["id"]
        self.name = data["name"]
        self.raw_data = data

    @classmethod
    def get_all(cls, client: Client, model_id: Optional[str] = None) -> List["CustomMetric"]:
        response = client.send_request(
            f"/metrics/custom-metrics{'' if model_id is None else f'?model_id={model_id}'}", "GET"
        )

        client.assert_response(response)

        return [cls(client=client, data=entry) for entry in response.json()]

    @classmethod
    def create(
        cls,
        client: Client,
        name: str,
        model_id: str,
        code: str,
    ) -> "CustomMetric":
        response = client.send_request(
            "/metrics/custom-metrics",
            "POST",
            {"name": name, "model_id": model_id, "code": code},
        )

        client.assert_response(response)

        return cls(client=client, data=response.json())

    @classmethod
    def read(cls, client: Client, id: str) -> "CustomMetric":
        response = client.send_request(f"/metrics/custom-metrics/{id}", "GET")
        client.assert_response(response)
        return cls(client=client, data=response.json())

    def update(self, **kwargs):
        response = self.client.send_request(
            f"/metrics/custom-metrics/{self.id}",
            "PUT",
            {"syntax": "aporia", **kwargs},
            url_search_replace=("/api/v1/", "/v1/crud-service/"),
        )
        self.client.assert_response(response)
        self.__update_members(response.json())

    def delete(self):
        response = self.client.send_request(f"/metrics/custom-metrics/{self.id}", "DELETE")
        self.client.assert_response(response)

    @staticmethod
    def delete_by_id(client: Client, id: str):
        response = client.send_request(f"/metrics/custom-metrics/{id}", "DELETE")
        client.assert_response(response)
