from typing import Any, Dict, Optional, Tuple

from aporia.as_code.resources.base import BaseResource, CompareStatus
from aporia.sdk.client import Client
from aporia.sdk.custom_metrics import CustomMetric as _CustomMetric


class CustomMetric(BaseResource):
    def __init__(self, resource_name: str, /, *, code: str, name: Optional[str] = None):
        self.name = resource_name
        self.dependants = []
        if name is None:
            name = resource_name

        self._args = {"name": name, "code": code}

    def compare(self, resource_data: Dict) -> CompareStatus:
        if all([self._args[k] == resource_data[k] for k in self._args.keys()]):
            return CompareStatus.SAME
        return CompareStatus.UPDATEABLE

    def setarg(self, arg_name: str, arg_value: Any):
        self._args[arg_name] = arg_value

    def create(self, client: Client) -> Tuple[str, Dict]:
        custom_metric = _CustomMetric.create(client=client, **self._args)
        return custom_metric.id, custom_metric.raw_data

    @classmethod
    def read(cls, client: Client, id: str) -> Dict:
        return _CustomMetric.read(client=client, id=id).raw_data

    def update(self, client: Client, id: str) -> Dict:
        custom_metric = _CustomMetric.read(client=client, id=id)
        custom_metric.update(**self._args)
        return custom_metric.raw_data

    @classmethod
    def delete(cls, client: Client, id: str):
        _CustomMetric.delete_by_id(client=client, id=id)

    def get_diff(self, resource_data: Dict) -> Dict:
        diffs = {}
        for k in self._args.keys():
            if self._args[k] != resource_data[k]:
                diffs[k] = (resource_data[k], self._args[k])
        return diffs
