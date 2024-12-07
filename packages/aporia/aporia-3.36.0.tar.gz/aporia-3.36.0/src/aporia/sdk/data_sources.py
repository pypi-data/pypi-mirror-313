from enum import Enum
from typing import Any, Dict, List

from aporia.sdk.base import BaseAporiaResource
from aporia.sdk.client import Client


class DataSourceType(Enum):
    APORIA_DEMO_DATA = "aporia-demo"
    DATABRICKS = "databricks"
    S3 = "s3"
    POSTGRES = "postgres"
    BIGQUERY = "bigquery"
    ATHENA = "athena"
    SNOWFLAKE = "snowflake"
    GLUE = "glue"
    REDSHIFT = "redshift"
    AZURE_BLOB_STORAGE = "azure_blob_storage"
    SNOWFLAKE_NATIVE = "snowflake_native"
    SNOWFLAKE_NATIVE_APP = "snowflake_native_app"
    GOOGLE_CLOUD_STORAGE = "google_cloud_storage"
    HIVE = "hive"
    MSSQL = "mssql"
    ORACLE = "oracle"
    UPLOAD_FILE = "upload_file"
    COMPOSITE = "composite"


class DataSource(BaseAporiaResource):
    def __init__(self, client: Client, data: Dict):
        self.client = client
        self.__update_members(data)

    def __update_members(self, data: Dict):
        self.raw_data = data
        self.id = data["id"]
        self.name = data["name"]
        self.type = DataSourceType(data["type"])

    @classmethod
    def get_all(cls, client: Client) -> List["DataSource"]:
        response = client.send_request("/data-sources", "GET")

        client.assert_response(response)

        return [cls(client=client, data=entry) for entry in response.json()]

    @classmethod
    def create(
        cls,
        client: Client,
        name: str,
        data_source_type: DataSourceType,
        connection_data: Dict[str, Any],
    ) -> "DataSource":
        existing_data_sources = cls.get_all(client=client)

        for data_source in existing_data_sources:
            if data_source.name == name:
                if data_source.type != data_source_type:
                    raise RuntimeError(
                        f"Data source {name} already exists but is of different type (expected {data_source_type.value}, received {data_source.type.value})"
                    )
                print(f"Data source {name} already exists! Using it. Check configuration")
                return data_source

        connection_data["type"] = data_source_type.value
        response = client.send_request(
            "/data-sources",
            "POST",
            {"name": name, "connection": connection_data},
        )

        client.assert_response(response)

        return cls(client=client, data=response.json())

    @classmethod
    def read(cls, client: Client, id: str) -> "DataSource":
        response = client.send_request(f"/data-sources/{id}", "GET")
        client.assert_response(response)
        return cls(client=client, data=response.json())

    def update(self, **kwargs):
        args = {}
        for k, v in kwargs.items():
            if isinstance(v, Enum):
                args[k] = v.value
            else:
                args[k] = v
        response = self.client.send_request(f"/data-sources/{self.id}", "PUT", args)
        self.client.assert_response(response)
        self.__update_members(response.json())

    def delete(self):
        response = self.client.send_request(
            f"/data-sources/{self.id}",
            "DELETE",
        )
        self.client.assert_response(response)

    @staticmethod
    def delete_by_id(client: Client, id: str):
        response = client.send_request(
            f"/data-sources/{id}",
            "DELETE",
        )
        client.assert_response(response)
