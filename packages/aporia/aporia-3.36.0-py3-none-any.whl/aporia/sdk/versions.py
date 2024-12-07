from typing import Any, Dict, List, Optional

from aporia.sdk.base import BaseAporiaResource
from aporia.sdk.client import Client
from aporia.sdk.data_sources import DataSource
from aporia.sdk.datasets import Dataset, DatasetSchema, DatasetType


class Version(BaseAporiaResource):
    def __init__(self, client: Client, data: Dict):
        self.client = client
        self.__update_members(data)

    def __update_members(self, data: Dict):
        self.raw_data = data
        self.id = data["id"]
        self.name = data["name"]
        self.model_id = data["model_id"]
        self.is_active = data["is_active"]

    @classmethod
    def get_all(cls, client: Client, model_id: Optional[str] = None) -> List["Version"]:
        response = client.send_request(
            f"/model-versions{'' if model_id is None else f'?model_id={model_id}'}", "GET"
        )

        client.assert_response(response)

        return [cls(client=client, data=entry) for entry in response.json()]

    @classmethod
    def create(cls, client: Client, name: str, model_id: str, is_active: bool = True) -> "Version":
        existing_versions = cls.get_all(client=client, model_id=model_id)

        for version in existing_versions:
            if version.name == name:
                print(f"Version {name} already exists! Using it. Check datasets")
                return version

        response = client.send_request(
            "/model-versions",
            "POST",
            {"name": name, "model_id": model_id},
        )

        client.assert_response(response)

        if not is_active:
            response = client.send_request(
                f"/model-versions/{response.json()['id']}", "PUT", {"is_active": is_active}
            )
            client.assert_response(response)

        return cls(client=client, data=response.json())

    def create_dataset(
        self,
        dataset_type: DatasetType,
        data_source: DataSource,
        connection_data: Dict[str, Any],
        schema: DatasetSchema,
    ) -> Dataset:
        """Creates a new dataset."""
        dataset = Dataset.create(
            client=self.client,
            model_id=self.model_id,
            version_id=self.id,
            dataset_type=dataset_type,
            data_source=data_source,
            connection_data=connection_data,
            schema=schema,
        )
        return dataset

    @classmethod
    def read(cls, client: Client, id: str) -> "Version":
        response = client.send_request(f"/model-versions/{id}", "GET")
        client.assert_response(response)
        return cls(client=client, data=response.json())

    def update(self, **kwargs):
        response = self.client.send_request(
            f"/model-versions/{self.id}",
            "PUT",
            kwargs,
        )
        self.client.assert_response(response)
        self.__update_members(response.json())

    def delete(self):
        response = self.client.send_request(f"/model-versions/{self.id}", "DELETE")
        self.client.assert_response(response)

    @staticmethod
    def delete_by_id(client: Client, id: str):
        response = client.send_request(f"/model-versions/{id}", "DELETE")
        client.assert_response(response)

    def get_datasets(self) -> List[Dataset]:
        datasets = Dataset.get_all(client=self.client, model_version_id=self.id)
        return datasets
