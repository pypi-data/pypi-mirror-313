from typing import Any, Dict, Optional, Tuple, Union

from aporia.as_code.resources.base import BaseResource, CompareStatus
from aporia.sdk.client import Client
from aporia.sdk.data_sources import DataSource as _DataSource
from aporia.sdk.data_sources import DataSourceType


class DataSource(BaseResource):
    def __init__(
        self,
        resource_name: str,
        /,
        *,
        type: Union[DataSourceType, str],
        connection_data: Dict[str, Any],
        name: Optional[str] = None,
    ):
        self.dependants = []
        self.name = resource_name
        if name is None:
            name = resource_name

        self._args = {
            "name": name,
            "data_source_type": DataSourceType(type),
            "connection_data": connection_data,
        }

    def compare(self, resource_data: Dict) -> CompareStatus:
        if all(
            [
                self._args["name"] == resource_data["name"],
                self._args["data_source_type"].value == resource_data["type"],
                # TODO: Data source configuration isn't getable
                # self._args["connection_data"] == resource_data["connection"],
            ]
        ):
            return CompareStatus.SAME
        return CompareStatus.MISMATCHED

    def setarg(self, arg_name: str, arg_value: Any):
        self._args[arg_name] = arg_value

    def create(self, client: Client) -> Tuple[str, Dict]:
        data_source = _DataSource.create(client=client, **self._args)
        return data_source.id, data_source.raw_data

    @classmethod
    def read(cls, client: Client, id: str) -> Dict:
        return _DataSource.read(client=client, id=id).raw_data

    def update(self, client: Client, id: str) -> Dict:
        data_source = _DataSource.read(client=client, id=id)
        data_source.update(**self._args)
        return data_source.raw_data

    @classmethod
    def delete(cls, client: Client, id: str):
        _DataSource.delete_by_id(client=client, id=id)

    def get_diff(self, resource_data: Dict) -> Dict:
        diffs = {}
        if self._args["name"] != resource_data["name"]:
            diffs["name"] = (resource_data["name"], self._args["name"])
        if self._args["data_source_type"].value != resource_data["type"]:
            diffs["type"] = (resource_data["type"], self._args["data_source_type"].value)
        return diffs
