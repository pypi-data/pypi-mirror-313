from typing import Any, Dict, List, Optional, Tuple, Union

from aporia.as_code.resources.base import BaseResource, CompareStatus
from aporia.sdk.client import Client
from aporia.sdk.segments import Segment as _Segment


class Segment(BaseResource):
    def __init__(
        self,
        resource_name: str,
        /,
        *,
        name: Optional[str] = None,
        field: Optional[str] = None,
        values: Optional[Union[List[str], List[Union[float, int]]]] = None,
        terms: Optional[List[Tuple[str, str]]] = None,
        is_global_filter: Optional[bool] = None,
    ):
        self.name = resource_name
        self.dependants = []
        if name is None:
            name = resource_name

        self._args = {"name": name}

        if is_global_filter is not None:
            self._args["is_global_filter"] = is_global_filter

        if field is not None:
            if values is None:
                raise Exception("Must supply values for automatic segment")
            self._args["field_name"] = field
            self._args["values"] = values
        elif terms is not None:
            if values is not None:
                raise Exception("For custom segments, only specify the terms parameter")
            self._args["terms"] = terms
        else:
            raise Exception("Supply either field+values or terms")

    def compare(self, resource_data: Dict) -> CompareStatus:
        values = self._args.get("values", [])
        resource_field_name = resource_data.get("field_name")
        # Old stacks might have the field data stored in an outdated format (due to API change)
        if resource_field_name is None:
            resource_field_data = resource_data.get("field", {})
            resource_field_name = (resource_field_data or {}).get("name")

        if "terms" in self._args.keys():
            values = [term[1] for term in self._args["terms"]]
        extended_data = resource_data.get("extended_data")
        is_custom_segment = (
            extended_data.get("is_custom_segment")
            if extended_data
            else "terms" in self._args.keys()
        )

        # Old stacks might not have the global filter field.
        resource_is_global_filter = resource_data.get("is_global_filter")
        if resource_is_global_filter is None:
            resource_is_global_filter = False
        args_is_global_filter = self._args.get("is_global_filter")

        if all(
            [
                # In case it's a custom segment - we compare the terms.
                (not is_custom_segment)
                or (self._args.get("terms") == resource_data["terms_values"]),
                self._args.get("field_name") == resource_field_name,
                values == resource_data["values"],
                self._args["name"] == resource_data["name"],
                # If someone added the global filter field explicilty,
                # we should check if it requires updating.
                (args_is_global_filter is None) or args_is_global_filter == resource_is_global_filter,
            ]
        ):
            return CompareStatus.SAME
        else:
            return CompareStatus.UPDATEABLE

    def setarg(self, arg_name: str, arg_value: Any):
        self._args[arg_name] = arg_value

    def create(self, client: Client) -> Tuple[str, Dict]:
        # When creating a resource, if someone didn't set the global filter attribute
        # Set it to False by default.
        if self._args.get("is_global_filter") is None:
            self._args["is_global_filter"] = False

        segment = _Segment.create(client=client, **self._args)
        saved_data = segment.raw_data.copy()
        saved_data["extended_data"] = segment.get_extended_data()

        return segment.id, saved_data

    @classmethod
    def read(cls, client: Client, id: str) -> Dict:
        segment = _Segment.read(client=client, id=id)
        read_data = segment.raw_data.copy()
        read_data["extended_data"] = segment.get_extended_data()
        return read_data

    def update(self, client: Client, id: str) -> Dict:
        segment = _Segment.read(client=client, id=id)
        segment.update(**self._args)
        return segment.raw_data

    @classmethod
    def delete(cls, client: Client, id: str):
        _Segment.delete_by_id(client=client, id=id)

    def get_diff(self, resource_data: Dict) -> Dict:
        diffs = {}
        if self._args["name"] != resource_data["name"]:
            diffs["name"] = (resource_data["name"], self._args["name"])
        return diffs
