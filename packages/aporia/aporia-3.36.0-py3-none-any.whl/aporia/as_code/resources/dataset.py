import json
from typing import Any, Dict, Optional, Tuple, Union

from aporia.as_code.resources.base import BaseResource, CompareStatus
from aporia.as_code.resources.data_source import DataSource
from aporia.sdk.client import Client
from aporia.sdk.data_sources import DataSource as _DataSource
from aporia.sdk.datasets import Dataset as _Dataset
from aporia.sdk.datasets import DatasetSchema, DatasetType, FieldSchema, FieldType, SortOrder


class Dataset(BaseResource):
    def __init__(
        self,
        resource_name: str,
        /,
        *,
        type: Union[DatasetType, str],
        connection_data: Dict[str, Any],
        id_column: Optional[str] = None,
        timestamp_column: Optional[str] = None,
        order_by_column: Optional[str] = None,
        group_by_column: Optional[str] = None,
        group_order_sort: Optional[Union[SortOrder, str]] = None,
        raw_inputs: Optional[Dict[str, Union[FieldType, str]]] = None,
        features: Optional[Dict[str, Union[FieldType, str]]] = None,
        predictions: Optional[Dict[str, Union[FieldType, str]]] = None,
        actuals: Optional[Dict[str, Union[FieldType, str]]] = None,
        actual_mappings: Optional[Dict[str, str]] = None,
        data_source_name: Optional[str] = None,
        data_source_id: Optional[str] = None,
        data_source: Optional[DataSource] = None,
    ):
        self.name = resource_name
        type = DatasetType(type)

        schema = DatasetSchema(
            id_column=id_column,
            timestamp_column=timestamp_column,
            group_by_column=group_by_column,
            order_by_column=order_by_column,
            group_order_sort=SortOrder(group_order_sort) if group_order_sort is not None else None,
            raw_inputs=(
                [FieldSchema(name=name, type=FieldType(type)) for name, type in raw_inputs.items()]
                if raw_inputs is not None
                else []
            ),
            features=(
                [FieldSchema(name=name, type=FieldType(type)) for name, type in features.items()]
                if features is not None
                else []
            ),
            predictions=(
                [FieldSchema(name=name, type=FieldType(type)) for name, type in predictions.items()]
                if predictions is not None
                else []
            ),
            actuals=(
                [
                    FieldSchema(
                        name=name,
                        type=FieldType(type),
                        properties={"prediction": actual_mappings[name]},
                    )
                    for name, type in actuals.items()
                ]
                if actuals is not None
                else []
            ),
        )

        if data_source_id is None and data_source_name is None and data_source is None:
            raise ValueError("Must supply data source")

        if 1 != sum(
            [
                1
                for data_source_identifier in [
                    data_source,
                    data_source_id,
                    data_source_name,
                ]
                if data_source_identifier is not None
            ]
        ):
            raise ValueError("Must supply only one method to find data source")

        self._args = {
            "dataset_type": type,
            "connection_data": connection_data,
            "schema": schema,
        }

        if data_source is not None:
            data_source.dependants.append(
                (
                    self,
                    lambda data, dataset: dataset.setarg("data_source_id", data["id"]),
                )
            )
        elif data_source_id is not None:
            self._args["data_source_id"] = data_source_id
        else:

            def deferred_load(client: Client, resource: BaseResource):
                data_sources = _DataSource.get_all(client)
                same_named_data_sources = [
                    data_source
                    for data_source in data_sources
                    if data_source.name == data_source_name
                ]
                if len(same_named_data_sources) != 1:
                    raise Exception(
                        f"Found {len(same_named_data_sources)} data sources named {data_source_name}"
                    )
                data_source = same_named_data_sources[0]
                resource.setarg("data_source_id", data_source.id)

            self.deferred_load = deferred_load

    def _compare_schema(self, aporia_schema: Dict, compare_metadata: bool = True) -> bool:
        schema: DatasetSchema = self._args["schema"]

        raw_inputs = {
            raw_input.name: json.loads(raw_input.json()) for raw_input in schema.raw_inputs or []
        }
        features = {feature.name: json.loads(feature.json()) for feature in schema.features or []}
        predictions = {
            prediction.name: json.loads(prediction.json())
            for prediction in schema.predictions or []
        }
        actuals = {actual.name: json.loads(actual.json()) for actual in schema.actuals or []}

        schema_raw_inputs = {
            raw_input["name"]: raw_input for raw_input in aporia_schema["raw_inputs"] or []
        }
        schema_features = {feature["name"]: feature for feature in aporia_schema["features"] or []}
        schema_predictions = {
            prediction["name"]: prediction for prediction in aporia_schema["predictions"] or []
        }
        schema_actuals = {actual["name"]: actual for actual in aporia_schema["actuals"] or []}

        checks = [
            (schema.id_column == aporia_schema["id_column"]) if compare_metadata else True,
            (
                (schema.timestamp_column == aporia_schema["timestamp_column"])
                if compare_metadata
                else True
            ),
            raw_inputs == schema_raw_inputs,
            features == schema_features,
            predictions == schema_predictions,
            actuals == schema_actuals,
        ]

        return all(checks)

    def compare(self, resource_data: Dict) -> CompareStatus:
        if all(
            [
                self._args["dataset_type"].value == resource_data["stage"],
                self._args["connection_data"] == resource_data["config"],
                self._compare_schema(resource_data["schema"]),
                # TODO: Find a way to validate data source
                self._args["version_id"] == resource_data["model_version_id"],
            ]
        ):
            return CompareStatus.SAME
        elif any(
            [
                self._args["dataset_type"].value != resource_data["stage"],
                not self._compare_schema(resource_data["schema"], compare_metadata=False),
                self._args["version_id"] != resource_data["model_version_id"],
            ]
        ):
            return CompareStatus.MISMATCHED
        else:
            return CompareStatus.UPDATEABLE

    def setarg(self, arg_name: str, arg_value: Any):
        self._args[arg_name] = arg_value

    def create(self, client: Client) -> Tuple[str, Dict]:
        dataset = _Dataset.create(client=client, **self._args)
        return dataset.id, dataset.raw_data

    @classmethod
    def read(cls, client: Client, id: str) -> Dict:
        return _Dataset.read(client=client, id=id).raw_data

    def update(self, client: Client, id: str) -> Dict:
        dataset = _Dataset.read(client=client, id=id)
        dataset.update(**self._args)
        return dataset.raw_data

    @classmethod
    def delete(cls, client: Client, id: str):
        _Dataset.delete_by_id(client=client, id=id)

    def get_diff(self, resource_data: Dict) -> Dict:
        diffs = {}
        if self._args["connection_data"] != resource_data["config"]:
            diffs["connection_data"] = (resource_data["config"], self._args["connection_data"])
        return diffs
