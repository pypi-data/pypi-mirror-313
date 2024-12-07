from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from aporia.as_code.resources.base import BaseResource, CompareStatus
from aporia.as_code.resources.custom_metrics import CustomMetric
from aporia.as_code.resources.monitor import Monitor
from aporia.as_code.resources.segment import Segment
from aporia.as_code.resources.version import Version
from aporia.sdk.client import Client
from aporia.sdk.models import Model as _Model
from aporia.sdk.models import ModelAggregationPeriod, ModelColor, ModelIcon, ModelType, NoOwner


class Model(BaseResource):
    def __init__(
        self,
        resource_name: str,
        /,
        *,
        # Model args
        type: Union[ModelType, str],
        name: Optional[str] = None,
        description: Optional[str] = None,
        icon: Optional[ModelIcon] = None,
        color: Optional[ModelColor] = None,
        owner: Optional[Union[str, NoOwner]] = NoOwner(),
        aggregation_period: Optional[Union[ModelAggregationPeriod, str]] = None,
        # Model sub-resources
        versions: Optional[List[Version]] = None,
        segments: Optional[List[Segment]] = None,
        custom_metrics: Optional[List[CustomMetric]] = None,
        monitors: Optional[List[Monitor]] = None,
    ):
        self.sub_resources = []
        self.name = resource_name
        if name is None:
            name = resource_name

        type = ModelType(type)
        self._args = {"name": name, "model_type": type}

        if description is not None:
            self._args["description"] = description
        if icon is not None:
            icon = ModelIcon(icon)
            self._args["icon"] = icon
        if color is not None:
            color = ModelColor(color)
            self._args["color"] = color
        if not isinstance(owner, NoOwner):
            self._args["owner"] = owner
        if aggregation_period is not None:
            self._args["aggregation_period"] = ModelAggregationPeriod(aggregation_period)

        for version in versions or []:
            self.sub_resources.append(
                (version, lambda data, version: version.setarg("model_id", data["id"]))
            )
        for segment in segments or []:
            self.sub_resources.append(
                (segment, lambda data, segment: segment.setarg("model_id", data["id"]))
            )
        for custom_metric in custom_metrics or []:
            self.sub_resources.append(
                (
                    custom_metric,
                    lambda data, custom_metric: custom_metric.setarg("model_id", data["id"]),
                )
            )
        for monitor in monitors or []:
            self.sub_resources.append(
                (monitor, lambda data, monitor: monitor.setarg("model_id", data["id"]))
            )

    def compare(self, resource_data: Dict) -> CompareStatus:
        checks = [
            self._args["name"] == resource_data["name"],
            self._args["model_type"].value == resource_data["type"],
        ]
        for k in ["description", "icon", "color", "owner"]:
            if k in self._args:
                if isinstance(self._args[k], Enum):
                    checks.append(self._args[k].value == resource_data[k])
                else:
                    checks.append(self._args[k] == resource_data[k])
        if all(checks):
            return CompareStatus.SAME
        return CompareStatus.UPDATEABLE

    def setarg(self, arg_name: str, arg_value: Any):
        self._args[arg_name] = arg_value

    def create(self, client: Client) -> Tuple[str, Dict]:
        model = _Model.create(client=client, **self._args)
        return model.id, model.raw_data

    @classmethod
    def read(cls, client: Client, id: str) -> Dict:
        return _Model.read(client=client, id=id).raw_data

    def update(self, client: Client, id: str) -> Dict:
        model = _Model.read(client=client, id=id)
        model.update(**self._args)
        return model.raw_data

    @classmethod
    def delete(cls, client: Client, id: str):
        _Model.delete_by_id(client=client, id=id)

    def get_diff(self, resource_data: Dict) -> Dict:
        diffs = {}
        if self._args["name"] != resource_data["name"]:
            diffs["name"] = (resource_data["name"], self._args["name"])
        if self._args["model_type"].value != resource_data["type"]:
            diffs["model_type"] = (resource_data["type"], self._args["model_type"])
        for k in ["description", "icon", "color", "owner"]:
            if k in self._args:
                if isinstance(self._args[k], Enum):
                    if self._args[k].value != resource_data[k]:
                        diffs[k] = (resource_data[k], self._args[k].value)
                else:
                    if self._args[k] != resource_data[k]:
                        diffs[k] = (resource_data[k], self._args[k])
        return diffs
