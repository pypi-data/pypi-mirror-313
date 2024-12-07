from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from importlib.metadata import version as get_version
import json
import pathlib
import string
import traceback
from typing import Any, Dict, List, Optional, Tuple

from requests import Session

from aporia.as_code.resources.base import (
    BaseResource,
    CompareStatus,
    NonDeletableResourceException,
)
from aporia.as_code.resources.custom_metrics import CustomMetric
from aporia.as_code.resources.data_source import DataSource
from aporia.as_code.resources.dataset import Dataset
from aporia.as_code.resources.model import Model
from aporia.as_code.resources.monitor import Monitor
from aporia.as_code.resources.segment import Segment
from aporia.as_code.resources.version import Version
from aporia.sdk.aporia_api import Aporia
from aporia.sdk.aporia_api import BaseAporiaResource as SDKBaseAporiaResource
from aporia.sdk.client import Client, EntityNotFoundException
from aporia.sdk.custom_metrics import CustomMetric as SDKCustomMetric
from aporia.sdk.datasets import Dataset as SDKDataset
from aporia.sdk.metrics import MetricType
from aporia.sdk.models import Model as SDKModel
from aporia.sdk.models import ModelColor
from aporia.sdk.monitors import (
    ActionType,
    infer_detection_method,
    LogicEvaluationType,
    MessagingIntegrationType,
)
from aporia.sdk.monitors import Monitor as SDKMonitor
from aporia.sdk.monitors import (
    MonitorType,
    parse_monitor_configuration,
    PreConditionType,
)
from aporia.sdk.segments import Segment as SDKSegment
from aporia.sdk.versions import Version as SDKVersion

sdk_version = get_version("aporia")


class StackAction(Enum):
    CREATE = "create"
    DELETE = "delete"
    PREVIEW = "preview"
    REFRESH = "refresh"
    DIFF = "diff"


class ResourceStatus(Enum):
    CREATED = "created"  # Found in config file
    MISSING = "missing"  # Not found in config file, create
    DEPRECATED = "deprecated"  # Found in config file, definition changed
    # TODO: Support that
    # UNWANTED = "unwanted"  # Found in config file, not in resources


@dataclass
class Resource:
    resource: BaseResource
    depth: int
    status: ResourceStatus
    id: Optional[str] = None


RESOURCE_TYPE_TO_RESOURCE_CLASS = {
    CustomMetric.__name__: CustomMetric,
    DataSource.__name__: DataSource,
    Dataset.__name__: Dataset,
    Model.__name__: Model,
    Monitor.__name__: Monitor,
    Segment.__name__: Segment,
    Version.__name__: Version,
}


class Stack:
    def __init__(
        self,
        token: str,
        account: str,
        workspace: str = "default-workspace",
        base_url: str = "https://platform.aporia.com",
        requests_session: Optional[Session] = None,
    ):
        self._resources: OrderedDict[str, Resource] = OrderedDict()
        self._output = None
        self._base_url = base_url
        self._client = Client(
            base_url=f"{base_url}/api/v1/{account}/{workspace}",
            token=token,
            requests_session=requests_session,
        )
        self._delete_resources: OrderedDict[str, BaseResource] = OrderedDict()
        self._aporia_api = Aporia(
            token=token,
            account_name=account,
            workspace_name=workspace,
            base_url=base_url,
            requests_session=requests_session,
        )

    def add(self, resource: BaseResource, depth=0, prefix=None):
        unique_id = (prefix or "") + resource.name

        if unique_id in self._resources.keys():
            raise Exception(f"Found duplicate resource name: {unique_id}")

        self._resources[unique_id] = Resource(
            resource=resource, depth=depth, status=ResourceStatus.MISSING
        )
        if hasattr(resource, "sub_resources"):
            for sub_resource, _ in resource.sub_resources:
                self.add(
                    sub_resource,
                    depth=depth + 1,
                    prefix=f"{prefix or ''}{resource.name}/",
                )

    def _call_argsetters(self, resource, resource_data):
        if hasattr(resource, "sub_resources"):
            sub_resources = resource.sub_resources
            for sub_resource, argsetter in sub_resources:
                argsetter(resource_data, sub_resource)
        if hasattr(resource, "dependants"):
            dependants = resource.dependants
            for sub_resource, argsetter in dependants:
                argsetter(resource_data, sub_resource)

    def _preview(self, delete: bool = False):
        if delete:
            RESOURCE_STATUS_TO_PREVIEW_ACTION = {
                ResourceStatus.CREATED: "delete",
                ResourceStatus.MISSING: "create",
                ResourceStatus.DEPRECATED: "delete",
            }
            for resource_entry in self._resources.values():
                if resource_entry.status is ResourceStatus.MISSING:
                    continue
                print(
                    f"|-{'----' * resource_entry.depth}{resource_entry.resource.name} - {RESOURCE_STATUS_TO_PREVIEW_ACTION[resource_entry.status]}"
                )
        else:
            RESOURCE_STATUS_TO_PREVIEW_ACTION = {
                ResourceStatus.CREATED: "pass",
                ResourceStatus.MISSING: "create",
                ResourceStatus.DEPRECATED: "update",
            }
            for resource_entry in self._resources.values():
                print(
                    f"|-{'----' * resource_entry.depth}{resource_entry.resource.name} - {RESOURCE_STATUS_TO_PREVIEW_ACTION[resource_entry.status]}"
                )
        if len(self._delete_resources) > 0:
            print("Removed resources:")
        for unique_id in self._delete_resources.keys():
            resource_parts = unique_id.split("/")
            depth = len(resource_parts) - 1
            name = resource_parts[-1]
            print(f"|-{'----' * depth}{name} - delete")

    def _get_diff_config(self, output_format: str = "print"):
        diffs = {}
        for unique_id, resource_entry in self._resources.items():
            if resource_entry.status is not ResourceStatus.DEPRECATED:
                continue
            resource_data = self._output[unique_id]
            resource_diff = resource_entry.resource.get_diff(resource_data=resource_data)
            diffs[unique_id] = {}
            for config_name, (old, new) in resource_diff.items():
                diffs[unique_id][config_name] = {"old": old, "new": new}
        if output_format == "json":
            print(json.dumps(diffs))
        elif output_format == "print":
            for unique_id, diffed_configs in diffs.items():
                print(f"Resource '{unique_id}' changed. Changes:")
                for config_name, config_diffs in diffed_configs.items():
                    print(
                        f"    Configuration '{config_name}' changed.\n        Old: {config_diffs['old']}\n        New: {config_diffs['new']}"
                    )

    def __pop_deleted_sub_resources(self, non_deleteable_resources: List[str], unique_id):
        resource_entry = self._resources[unique_id]
        if hasattr(resource_entry.resource, "sub_resources"):
            for resource, _ in resource_entry.resource.sub_resources:
                sub_resource_unique_id = f"{unique_id}/{resource.name}"
                if sub_resource_unique_id in non_deleteable_resources:
                    self.__pop_deleted_sub_resources(
                        non_deleteable_resources=non_deleteable_resources,
                        unique_id=sub_resource_unique_id,
                    )
                    self._output.pop(sub_resource_unique_id)
                elif sub_resource_unique_id in self._output.keys():
                    raise RuntimeError(
                        f"Resource deletion missed for {sub_resource_unique_id}. Stack potentially corrupted."
                    )

    def _create(self, debug: bool = False) -> Tuple[Dict, Optional[Exception]]:
        output = self._output or {}
        error = None
        try:
            # Create/update resources
            for (
                unique_id,
                resource_entry,
            ) in self._resources.items():
                if resource_entry.status is ResourceStatus.CREATED:
                    continue
                if hasattr(resource_entry.resource, "deferred_load"):
                    resource_entry.resource.deferred_load(self._client, resource_entry.resource)

                if resource_entry.status is ResourceStatus.MISSING:
                    if debug:
                        print(f"Attempting to create: {unique_id}")
                    _, resource_data = resource_entry.resource.create(client=self._client)
                elif resource_entry.status is ResourceStatus.DEPRECATED:
                    resource_data = resource_entry.resource.update(
                        client=self._client, id=self._output[unique_id]["id"]
                    )
                else:
                    raise Exception("Unexpected resource status")
                self._call_argsetters(resource_entry.resource, resource_data)
                output[unique_id] = resource_data
                output[unique_id]["_resource_type"] = type(resource_entry.resource).__name__
                resource_entry.status = ResourceStatus.CREATED

            # Delete resources
            non_deleteable_resources = []
            for unique_id, resource_class in list(self._delete_resources.items())[::-1]:
                resource_data = self._output[unique_id]
                if debug:
                    print(f"Attempting to delete: {unique_id}")
                try:
                    resource_class.delete(client=self._client, id=resource_data["id"])
                except NonDeletableResourceException:
                    non_deleteable_resources.append(unique_id)
                    continue
                for non_deleteable_resource in [*non_deleteable_resources]:
                    if non_deleteable_resource.startswith(f"{unique_id}/"):
                        self._output.pop(non_deleteable_resource)
                        non_deleteable_resources.remove(non_deleteable_resource)
                self._output.pop(unique_id)
        except Exception as e:
            error = e

        return output, error

    def _destroy(self):
        # Read from storage
        # Destroy all resources
        # TODO: Consider adding all this logic into _create, just with setting resource.action to delete
        error = None
        if self._output is None:
            raise Exception("Stack not created")
        try:
            non_deleteable_resources = []
            for unique_id, resource_entry in list(self._resources.items())[::-1]:
                if unique_id in self._output.keys():
                    resource_data = self._output[unique_id]
                    try:
                        resource_entry.resource.delete(client=self._client, id=resource_data["id"])
                    except NonDeletableResourceException:
                        non_deleteable_resources.append(unique_id)
                        continue
                    self.__pop_deleted_sub_resources(non_deleteable_resources, unique_id)
                    self._output.pop(unique_id)
            for unique_id, resource_class in list(self._delete_resources.items())[::-1]:
                resource_data = self._output[unique_id]
                try:
                    resource_class.delete(client=self._client, id=resource_data["id"])
                except NonDeletableResourceException:
                    non_deleteable_resources.append(unique_id)
                    continue
                self.__pop_deleted_sub_resources(non_deleteable_resources, unique_id)
                self._output.pop(unique_id)
        except Exception as e:
            error = e

        return error

    def _diff(self):
        for unique_id, resource_entry in self._resources.items():
            if unique_id in self._output.keys():
                # Resource already exists. Call argsetters
                # TODO: Add support for edit
                resource_data = self._output[unique_id]
                self._call_argsetters(resource_entry.resource, resource_data)
                compare_status = self._resources[unique_id].resource.compare(
                    resource_data=resource_data
                )
                if compare_status is CompareStatus.SAME:
                    self._resources[unique_id].status = ResourceStatus.CREATED
                elif compare_status is CompareStatus.UPDATEABLE:
                    self._resources[unique_id].status = ResourceStatus.DEPRECATED
                else:
                    raise Exception(
                        f"Configuration for {unique_id} was edited but can't be updated!"
                    )
                continue

        for unique_id, resource_data in self._output.items():
            if unique_id not in self._resources.keys():
                self._delete_resources[unique_id] = RESOURCE_TYPE_TO_RESOURCE_CLASS[
                    resource_data["_resource_type"]
                ]

    def __resource_name_to_python_name(self, name: str) -> str:
        result = "".join(
            [c if c in (string.ascii_letters + string.digits + "_") else "_" for c in name]
        ).lower()
        if result[0] in string.digits:
            result = f"_{result}"
        return result

    def __create_python_representation(
        self,
        resource: SDKBaseAporiaResource,
        index: int,
        version_id_to_object: Optional[Dict[str, str]] = None,
        segment_id_to_object: Optional[Dict[str, str]] = None,
        custom_metric_id_to_object: Optional[Dict[str, str]] = None,
    ) -> Tuple[str, str]:
        if isinstance(resource, SDKSegment):
            code = f"""{self.__resource_name_to_python_name(resource.name)} = aporia.Segment(
    "{resource.name}",
"""
            if resource.raw_data["field_name"] is not None:
                code += f"""\tfield="{resource.raw_data["field_name"]}",\n"""
                code += f"""\tvalues={resource.raw_data["values"]}\n"""
            else:
                code += f"""\tterms={resource.raw_data["terms_values"]}\t"""
            code += ")"
            return code, self.__resource_name_to_python_name(resource.name)
        elif isinstance(resource, SDKCustomMetric):
            return (
                f'''{self.__resource_name_to_python_name(resource.name)} = aporia.CustomMetric(
    "{resource.name}",
    code="""{resource.raw_data["code"]}""",
)''',
                self.__resource_name_to_python_name(resource.name),
            )
        elif isinstance(resource, SDKDataset):
            schema = resource.raw_data["schema"]
            raw_inputs = {
                raw_input["name"]: raw_input["type"] for raw_input in schema["raw_inputs"]
            }
            features = {feature["name"]: feature["type"] for feature in schema["features"]}
            predictions = {
                prediction["name"]: prediction["type"] for prediction in schema["predictions"]
            }
            actuals = {actual["name"]: actual["type"] for actual in schema["actuals"]}
            actual_mappings = {
                actual["name"]: actual["properties"]["prediction"] for actual in schema["actuals"]
            }
            code = f"""{resource.raw_data["stage"]}_dataset_{index} = aporia.Dataset(
    "{resource.raw_data["stage"]}",
    type="{resource.raw_data["stage"]}",
    data_source_id="{resource.raw_data["data_source_id"]}",
    connection_data={resource.raw_data["config"]},
"""
            if schema["id_column"] is not None:
                code += f"""\tid_column="{schema['id_column']}",\n"""
            if schema["timestamp_column"] is not None:
                code += f"""\ttimestamp_column="{schema['timestamp_column']}",\n"""
            if len(raw_inputs) > 0:
                code += f"\traw_inputs={raw_inputs},\n"
            if len(features) > 0:
                code += f"\tfeatures={features},\n"
            if len(predictions) > 0:
                code += f"\tpredictions={predictions},\n"
            if len(actuals) > 0:
                code += f"\tactuals={actuals},\n"
            if len(actual_mappings) > 0:
                code += f"\tactual_mappings={actual_mappings},\n"
            code += ")"
            return code, f'{resource.raw_data["stage"]}_dataset_{index}'
        elif isinstance(resource, SDKVersion):
            code = f"""{self.__resource_name_to_python_name(resource.name)} = aporia.Version(
    "{resource.name}",
"""
            if resource.raw_data["serving_dataset"] is not None:
                code += f"\tserving=serving_dataset_{index},\n"
            if resource.raw_data["training_dataset"] is not None:
                code += f"\ttraining=training_dataset_{index},\n"
            code += ")"
            return code, self.__resource_name_to_python_name(resource.name)
        elif isinstance(resource, SDKMonitor):
            parsed_config = parse_monitor_configuration(resource.raw_data["configuration"])
            detection_method = infer_detection_method(parsed_config)
            code = f"""{self.__resource_name_to_python_name(resource.name)} = aporia.Monitor(\n"""
            code += f'\t"{resource.name}",\n'
            code += f"\tmonitor_type=aporia.MonitorType.{resource.type.name},\n"
            code += f"\tdetection_method=aporia.DetectionMethod.{detection_method.name},\n"

            if parsed_config.metric.type == MetricType.EUCLIDEAN_DISTANCE:
                code += "\tis_embedding_monitor=True,\n"

            # Identification configuration
            if parsed_config.identification.raw_inputs is not None:
                raw_inputs = parsed_config.identification.raw_inputs
                raw_inputs_array = (
                    f"""[{', '.join(f'"{raw_input}"' for raw_input in raw_inputs)}]"""
                )
                code += f"\traw_inputs={raw_inputs_array},\n"
            if parsed_config.identification.features is not None:
                features = parsed_config.identification.features
                features_array = f"""[{', '.join(f'"{feature}"' for feature in features)}]"""
                code += f"\tfeatures={features_array},\n"
            if parsed_config.identification.predictions is not None:
                predictions = parsed_config.identification.predictions
                predictions_array = (
                    f"""[{', '.join(f'"{prediction}"' for prediction in predictions)}]"""
                )
                code += f"\tpredictions={predictions_array},\n"
            if parsed_config.identification.models.version is not None:
                version_id = parsed_config.identification.models.version
                if version_id in (version_id_to_object or {}):
                    code += f"\tversion={version_id_to_object[version_id]},\n"
                else:
                    code += f'\tversion_id="{version_id}",\n'

            if parsed_config.identification.segment.group is not None:
                segment_id = parsed_config.identification.segment.group
                if segment_id in (segment_id_to_object or {}):
                    code += f"\tsegment={segment_id_to_object[segment_id]},\n"
                else:
                    code += f'\tsegment_id="{segment_id}",\n'

            if parsed_config.identification.segment.value is not None:
                segment_value = parsed_config.identification.segment.value
                if isinstance(segment_value, str):
                    segment_value = f'"{segment_value}"'
                code += f"\tsegment_value={segment_value},\n"

            # Dataset configuration:
            code += f"\tfocal=aporia.FocalConfiguration(**{parsed_config.focal.to_dict()}),\n"
            if parsed_config.baseline is not None:
                code += f"\tbaseline=aporia.BaselineConfiguration(**{parsed_config.baseline.to_dict()}),\n"

            # Metric Configuration
            if resource.type in [
                MonitorType.PERFORMANCE_DEGRADATION,
                MonitorType.METRIC_CHANGE,
            ]:
                code += f"\tmetric=aporia.MetricType.{parsed_config.metric.type.name},\n"
            metric_config = parsed_config.metric
            if metric_config.id is not None:
                custom_metric_id = metric_config.id
                if custom_metric_id in (custom_metric_id_to_object or {}):
                    code += f"\tcustom_metric={custom_metric_id_to_object[custom_metric_id]},\n"
                else:
                    code += f'\tcustom_metric_id="{custom_metric_id}",\n'
            if metric_config.average is not None:
                code += f"\taverage_method=aporia.AverageMethod.{metric_config.average.name},\n"
            if metric_config.metricAtK is not None:
                code += f"\tk={metric_config.metricAtK},\n"
            if metric_config.quantile is not None:
                code += f"\tquantile={metric_config.quantile},\n"
            if metric_config.threshold is not None:
                code += f"\tprediction_threshold={metric_config.threshold},\n"
            if metric_config.metricPerClass is not None:
                prediction_class = metric_config.metricPerClass
                if isinstance(prediction_class, str):
                    prediction_class = f'"{prediction_class}"'
                code += f"\tprediction_class={prediction_class},\n"

            # Logic Evaluation Configuration
            # TODO: Support multiple logic evaluations, if needed
            logic_evaluation_configuration = parsed_config.logicEvaluations[0]
            added_percentage = False
            use_percentage = False
            use_staleness = False
            if logic_evaluation_configuration.name is LogicEvaluationType.RATIO:
                use_percentage = True
            if logic_evaluation_configuration.name is LogicEvaluationType.MODEL_STALENESS:
                use_staleness = True
            if logic_evaluation_configuration.min is not None:
                if use_percentage:
                    if not added_percentage:
                        code += f"\tpercentage={(1-logic_evaluation_configuration.min)*100},\n"
                        added_percentage = True
                else:
                    code += f"\tmin={logic_evaluation_configuration.min},\n"
            if logic_evaluation_configuration.max is not None:
                if use_percentage:
                    if not added_percentage:
                        code += f"\tpercentage={(logic_evaluation_configuration.max-1)*100},\n"
                        added_percentage = True
                elif use_staleness:
                    code += (
                        f'\tstaleness_period="{logic_evaluation_configuration.max.to_string()}",\n'
                    )
                else:
                    code += f"\tmax={logic_evaluation_configuration.max},\n"
            if logic_evaluation_configuration.sensitivity is not None:
                code += f"\tsensitivity={logic_evaluation_configuration.sensitivity},\n"
            if logic_evaluation_configuration.testOnlyIncrease is not None:
                code += (
                    f"\talert_on_increase_only={logic_evaluation_configuration.testOnlyIncrease},\n"
                )
            if logic_evaluation_configuration.thresholds is not None:
                code += f"\tthresholds=aporia.ThresholdConfiguration(**{logic_evaluation_configuration.thresholds.to_dict()}),\n"
            if logic_evaluation_configuration.distance is not None:
                code += f"\tdistance={logic_evaluation_configuration.distance},\n"
            if logic_evaluation_configuration.new_values_count_threshold is not None:
                code += f"\tnew_values_count_threshold={logic_evaluation_configuration.new_values_count_threshold},\n"
            if logic_evaluation_configuration.new_values_ratio_threshold is not None:
                code += f"\tnew_values_ratio_threshold={logic_evaluation_configuration.new_values_ratio_threshold},\n"

            # Alert configuration
            added_alert = False
            for action in parsed_config.actions:
                if action.type is ActionType.ALERT:
                    if not added_alert:
                        emails = []
                        messaging = {}
                        code += f"\tseverity=aporia.Severity.{action.severity.name},\n"
                        for notification in action.notification:
                            if notification["type"] == "EMAIL":
                                emails.extend(notification["emails"])
                            else:
                                integration_type = (
                                    f"{MessagingIntegrationType(notification['type']).value}"
                                )
                                if integration_type not in messaging.keys():
                                    messaging[integration_type] = []
                                messaging[integration_type].append(notification["integration_id"])
                        if len(emails) > 0:
                            code += f"\temails={emails},\n"
                        if len(messaging) > 0:
                            code += f"\tmessaging={messaging},\n"
                        added_alert = True
                        if action.alertGroupByEntity is not None:
                            code += f"\talertGroupByEntity={action.alertGroupByEntity},\n"
                        if action.alertGroupByTime is not None:
                            code += f"\talertGroupByTime={action.alertGroupByTime},\n"
                        if action.alertGroupTimeQuantity is not None:
                            code += f"\talertGroupTimeQuantity={action.alertGroupTimeQuantity},\n"
                        if action.alertGroupTimeUnit is not None:
                            code += f"\talertGroupTimeUnit={action.alertGroupTimeUnit},\n"

            # Precondition Configuration
            added_min = False
            added_min_focal_datapoints = False
            added_min_baseline_datapoints = False
            for precondition in parsed_config.preConditions or []:
                if precondition.name is PreConditionType.FOCAL_DATA_VALUE_IN_RANGE:
                    if not added_min:
                        code += f"\tmin={precondition.min},\n"
                        added_min = True
                if precondition.name is PreConditionType.MIN_FOCAL_DATA_POINTS:
                    if not added_min_focal_datapoints:
                        code += f"\tmin_focal_prediction_count={precondition.value},\n"
                        added_min_focal_datapoints = True
                if precondition.name is PreConditionType.MIN_BASELINE_DATA_POINTS:
                    if not added_min_baseline_datapoints:
                        code += f"\tmin_baseline_prediction_count={precondition.value},\n"
                        added_min_baseline_datapoints = True

            code += ")"
            return code, self.__resource_name_to_python_name(resource.name)
        elif isinstance(resource, SDKModel):
            return (
                f"""{self.__resource_name_to_python_name(resource.name)} = aporia.Model(
    "{resource.name}",
    type=aporia.ModelType.{resource.type.name},
    icon=aporia.ModelIcon.{resource.icon.name},
    color={f'aporia.ModelColor.{resource.color.name}' if isinstance(resource.color, ModelColor) else f'"{resource.color}"'},
    versions=[],
    segments=[],
    custom_metrics=[],
    monitors=[],
)""",
                self.__resource_name_to_python_name(resource.name),
            )
        raise TypeError(f"Unsupported type: {type(resource).__name__})")

    def __create_model_code(
        self,
        model: SDKModel,
        versions: List[Tuple[SDKVersion, List[SDKDataset]]],
        segments: List[SDKSegment],
        custom_metrics: List[SDKCustomMetric],
        monitors: List[SDKMonitor],
    ) -> Tuple[str, str]:
        model_code, model_name = self.__create_python_representation(model, 0)
        model_versions = []
        model_segments = []
        model_custom_metrics = []
        model_monitors = []
        versions_code = []
        segments_code = []
        custom_metrics_code = []
        monitors_code = []
        version_id_to_object = {}
        segment_id_to_object = {}
        custom_metric_id_to_object = {}
        for index, (version, datasets) in enumerate(versions):
            datasets_code = [
                self.__create_python_representation(dataset, index=index)[0] for dataset in datasets
            ]
            version_code, version_name = self.__create_python_representation(version, index=index)
            version_id_to_object[version.id] = version_name
            full_version_code = "\n".join([*datasets_code, version_code])
            versions_code.append(full_version_code)
            model_versions.append(version_name)
        for index, segment in enumerate(segments):
            segment_code, segment_name = self.__create_python_representation(segment, index=index)
            segment_id_to_object[segment.id] = segment_name
            segments_code.append(segment_code)
            model_segments.append(segment_name)
        for index, custom_metric in enumerate(custom_metrics):
            custom_metric_code, custom_metric_name = self.__create_python_representation(
                custom_metric, index=index
            )
            custom_metric_id_to_object[custom_metric.id] = custom_metric_name
            custom_metrics_code.append(custom_metric_code)
            model_custom_metrics.append(custom_metric_name)
        for index, monitor in enumerate(monitors):
            monitor_code, monitor_name = self.__create_python_representation(
                monitor,
                index=index,
                version_id_to_object=version_id_to_object,
                segment_id_to_object=segment_id_to_object,
                custom_metric_id_to_object=custom_metric_id_to_object,
            )
            monitors_code.append(monitor_code)
            model_monitors.append(monitor_name)

        model_code = model_code.replace("versions=[]", f"versions=[{', '.join(model_versions)}]")
        model_code = model_code.replace("segments=[]", f"segments=[{', '.join(model_segments)}]")
        model_code = model_code.replace(
            "custom_metrics=[]", f"custom_metrics=[{', '.join(model_custom_metrics)}]"
        )
        model_code = model_code.replace("monitors=[]", f"monitors=[{', '.join(model_monitors)}]")

        # Hack to allow newlines in f-string expressions
        newline = "\n"
        full_code = """import aporia.as_code as aporia
"""
        full_code += f"""
# Creating Model {model.name}
"""
        if len(versions) > 0:
            full_code += f"""
## Define Versions
{newline.join(versions_code)}
"""
        if len(segments) > 0:
            full_code += f"""
## Define Segments
{newline.join(segments_code)}
"""

        if len(custom_metrics) > 0:
            full_code += f"""
## Define Custom Metrics
{newline.join(custom_metrics_code)}
"""

        if len(monitors) > 0:
            full_code += f"""
## Define Monitors
{newline.join(monitors_code)}
"""

        full_code += "## Creating model\n"
        full_code += model_code

        full_code += f"""

def add_model(stack: aporia.Stack):
    stack.add({model_name})
"""

        return full_code, model_name

    def __create_resource_entry(
        self, resource: SDKBaseAporiaResource, parent_unique_id: Optional[str] = None
    ) -> Tuple[str, Dict]:
        data = deepcopy(resource.raw_data)
        data["_resource_type"] = type(resource).__name__
        if isinstance(resource, SDKDataset):
            resource_name = resource.raw_data["stage"]
        else:
            resource_name = resource.name
        name = f"{parent_unique_id + '/' if parent_unique_id is not None else ''}{resource_name.replace('/', '-')}"
        return (name, data)

    def __iterate_model(
        self, model: SDKModel, index: int
    ) -> Tuple[Dict[str, Dict[str, Any]], str, str]:
        resources = OrderedDict()
        model_name, data = self.__create_resource_entry(resource=model)
        resources[model_name] = data

        model_versions = []
        for version in model.get_versions():
            datasets = version.get_datasets()
            model_versions.append((version, datasets))
        model_segments = model.get_segments()
        model_custom_metrics = model.get_custom_metrics()
        model_monitors = model.get_monitors()

        # Add versions
        for version, datasets in model_versions:
            version_name, data = self.__create_resource_entry(
                resource=version, parent_unique_id=model_name
            )
            resources[version_name] = data
            # Add datasets
            for dataset in datasets:
                dataset_name, data = self.__create_resource_entry(
                    resource=dataset, parent_unique_id=version_name
                )
                resources[dataset_name] = data

        # Add segments
        for segment in model_segments:
            segment_name, data = self.__create_resource_entry(
                resource=segment, parent_unique_id=model_name
            )
            resources[segment_name] = data

        # Add custom metrics
        for custom_metric in model_custom_metrics:
            custom_metric_name, data = self.__create_resource_entry(
                resource=custom_metric, parent_unique_id=model_name
            )
            resources[custom_metric_name] = data

        # Add custom metrics
        for monitor in model_monitors:
            monitor_name, data = self.__create_resource_entry(
                resource=monitor, parent_unique_id=model_name
            )
            resources[monitor_name] = data

        model_code, model_name = self.__create_model_code(
            model=model,
            versions=model_versions,
            segments=model_segments,
            custom_metrics=model_custom_metrics,
            monitors=model_monitors,
        )

        return resources, model_code, model_name

    def _import(self, output_directory: str, model_names: Optional[List[str]]):
        # data_sources = self._aporia_api.get_data_sources()
        models = self._aporia_api.get_models()
        resources = OrderedDict()
        output_path = pathlib.Path(output_directory)
        output_path.mkdir(parents=True, exist_ok=True)

        models_code = {}

        for index, model in enumerate(models):
            if model_names is not None and model.name not in model_names:
                continue
            model_resources, model_code, model_name = self.__iterate_model(model=model, index=index)
            for name, data in model_resources.items():
                if name in resources.keys():
                    raise NameError(f"Resource {name} found duplicate!")
                resources[name] = data
            models_code[model_name] = model_code

        code = [
            "import os",
            "import aporia.as_code as aporia\n",
            "",
            'account = os.environ["APORIA_ACCOUNT"]',
            'workspace = os.environ["APORIA_WORKSPACE"]',
            'token = os.environ["APORIA_TOKEN"]',
            "",
            "stack = aporia.Stack(",
            "    account=account,",
            "    workspace=workspace,",
            "    token=token,",
            f'    base_url="{self._base_url}"',
            ")",
            "",
        ]

        code.append("\n# Registering Models")
        for model_name, model_code in models_code.items():
            with open(output_path / f"{model_name}.py", "w") as model_file:
                model_file.write(model_code)
                code.append(f"import {model_name}")
                code.append(f"{model_name}.add_model(stack)")

        code.append("\n# Applying Stack")
        code.append('stack.apply(config_path="stack.json", action="create", rollback=False)\n')

        with open(output_path / "stack.json", "w") as json_file:
            json_file.write(json.dumps(resources))

        with open(output_path / "main.py", "w") as python_file:
            python_file.write("\n".join(code))

    def _refresh_config(self):
        new_config = {}
        for unique_id, resource in self._output.items():
            resource_type = resource["_resource_type"]
            resource_name = f"{resource_type}/{unique_id.split('/')[-1]}"
            print("Refreshing resource: {:80.80s}".format(resource_name), end="\r")
            try:
                new_config[unique_id] = RESOURCE_TYPE_TO_RESOURCE_CLASS[resource_type].read(
                    client=self._client, id=resource["id"]
                )
                new_config[unique_id]["_resource_type"] = resource_type
            except EntityNotFoundException:
                print(f"{resource_type} - {unique_id} not found, removing from config")
            except Exception as e:
                print(f"issue refreshing data for: {resource_type} - {unique_id}")
                raise e
        print("Refresh complete" + (100 * " "))
        self._output = new_config

    def apply(
        self,
        action: StackAction = StackAction.CREATE,
        skip_preview: bool = False,
        yes: bool = False,
        rollback=True,  # BUG: Deletes all resources always
        yes_rollback=False,
        config_path: Optional[str] = None,
        debug: Optional[bool] = False,
        diff_format: str = "print",
    ):
        action = StackAction(action)
        # TODO: Read config_path, and apply diffs. Then write to config_path
        if config_path is not None:
            try:
                with open(config_path, "r") as f:
                    stack_data = json.loads(f.read())
                    if "version" in stack_data and type(stack_data["version"]) is str:
                        stack_version = stack_data["version"]
                        self._output = stack_data["resources"]
                    else:
                        stack_version = "0"
                        self._output = stack_data
                    if sdk_version < stack_version:
                        raise Exception(
                            "SDK version is older than config version, please update aporia SDK (pip install --upgrade aporia)"
                        )
                    self._diff()
            except FileNotFoundError:
                # It's OK if the file wasn't found. It's probably the first run
                pass

        if action is StackAction.CREATE:
            if not skip_preview:
                self._preview()
            if not yes:
                if input("Do create? [Y/N] ").lower().strip() not in ["y"]:
                    print("Cancelling...")
                    return
            self._output, error = self._create(debug=debug)

            if error is not None:
                if debug:
                    traceback.print_exception(error, tb=error.__traceback__, value=error)
                else:
                    print(error)
                if rollback:
                    if not yes_rollback:
                        if input("Delete created resources? [Y/N] ").lower().strip() in ["y"]:
                            print("Deleting...")
                            error = self._destroy()
                            if error is not None:
                                if debug:
                                    traceback.print_exception(
                                        error, tb=error.__traceback__, value=error
                                    )
                                else:
                                    print(error)
        elif action is StackAction.PREVIEW:
            self._preview()
            return
        elif action is StackAction.DELETE:
            if not skip_preview:
                self._preview(delete=True)
            # TODO: Change the way you use ResourceAction to support deletes, edits etc all at once, and previews for all
            if not yes:
                if input("Do delete? [Y/N] ").lower().strip() not in ["y"]:
                    print("Cancelling...")
                    return
            error = self._destroy()
            if error is not None:
                if debug:
                    traceback.print_exception(error, tb=error.__traceback__, value=error)
                else:
                    print(error)
        elif action is StackAction.DIFF:
            self._get_diff_config(output_format=diff_format)
            return
        elif action is StackAction.REFRESH:
            self._refresh_config()
        else:
            raise ValueError("Unknown action")

        if config_path is not None:
            with open(config_path, "w") as f:
                f.write(json.dumps({"version": sdk_version, "resources": self._output}))

    def get_resource_id(self, unique_id: str) -> str:
        return self._output[unique_id]["id"]
