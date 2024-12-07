from http import HTTPStatus
from typing import Any, Dict, Optional, Tuple

from aporia.as_code.resources.base import BaseResource, CompareStatus, NonDeletableResourceException
from aporia.as_code.resources.dataset import Dataset
from aporia.sdk.client import BackendRuntimeError, Client
from aporia.sdk.versions import Version as _Version


class Version(BaseResource):
    def __init__(
        self,
        resource_name: str,
        /,
        *,
        name: Optional[str] = None,
        serving: Optional[Dataset] = None,
        training: Optional[Dataset] = None,
        active: bool = True,
    ):
        self.name = resource_name
        self.active = active
        self.dependants = []
        self.sub_resources = []
        if name is None:
            name = resource_name

        self._args = {"name": name, "is_active": active}

        def apply_args(data, dataset):
            dataset.setarg("version_id", data["id"])
            dataset.setarg("model_id", data["model_id"])

        if serving is not None:
            self.sub_resources.append((serving, apply_args))
        if training is not None:
            self.sub_resources.append((training, apply_args))

    def compare(self, resource_data: Dict) -> CompareStatus:
        if all([self._args[k] == resource_data[k] for k in self._args.keys()]):
            return CompareStatus.SAME
        return CompareStatus.UPDATEABLE

    def setarg(self, arg_name: str, arg_value: Any):
        self._args[arg_name] = arg_value

    def create(self, client: Client) -> Tuple[str, Dict]:
        version = _Version.create(client=client, **self._args)
        return version.id, version.raw_data

    @classmethod
    def read(cls, client: Client, id: str) -> Dict:
        return _Version.read(client=client, id=id).raw_data

    def update(self, client: Client, id: str) -> Dict:
        version = _Version.read(client=client, id=id)
        version.update(**self._args)
        return version.raw_data

    @classmethod
    def delete(cls, client: Client, id: str):
        try:
            _Version.delete_by_id(client=client, id=id)
        except BackendRuntimeError as e:
            if (
                e.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value
                and type(e.body) is dict
                and e.body.get("detail", {}).get("type") == "last_version"
            ):
                raise NonDeletableResourceException()
            raise e

    def get_diff(self, resource_data: Dict) -> Dict:
        diffs = {}
        for k in self._args.keys():
            if self._args[k] != resource_data[k]:
                diffs[k] = (resource_data[k], self._args[k])
        return diffs
