from enum import Enum
from typing import Dict, List, Optional

from aporia.sdk.base import BaseAporiaResource
from aporia.sdk.client import Client


class MessagingIntegrationType(Enum):
    SLACK = "SLACK"
    WEBHOOK = "WEBHOOK"
    TEAMS = "TEAMS"
    DATADOG = "DATADOG"
    CISCO = "CISCO"


class MessagingIntegration(BaseAporiaResource):
    def __init__(self, client: Client, data: Dict):
        self.client = client
        self.__update_members(data)

    def __update_members(self, data: Dict):
        self.raw_data = data
        self.id = data["id"]
        self.type = MessagingIntegrationType(data["type"])

    @classmethod
    def get_all(
        cls, client: Client, integration_type: Optional[MessagingIntegrationType] = None
    ) -> List["MessagingIntegration"]:
        response = client.send_request(
            f"/integrate/query{'' if integration_type is None else f'/{integration_type.value}'}",
            "GET",
            url_search_replace=("/api/v1/", "/v1/messaging-service/"),
        )

        client.assert_response(response)

        return [cls(client=client, data=entry) for entry in response.json()]

    @classmethod
    def create(cls, client: Client, name: str, model_id: str) -> "MessagingIntegration":
        raise NotImplementedError()

    @classmethod
    def read(cls, client: Client, id: str) -> "MessagingIntegration":
        integrations = cls.get_all(client=client)
        filtered_integrations = [
            integration for integration in integrations if integration.id == id
        ]
        if len(filtered_integrations) == 0:
            raise RuntimeError(f"Integration with ID {id} not found")
        return filtered_integrations[0]

    def update(self, **kwargs):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    @staticmethod
    def delete_by_id(client: Client, id: str):
        raise NotImplementedError()
