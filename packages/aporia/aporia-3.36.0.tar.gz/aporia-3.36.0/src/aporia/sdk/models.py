from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

from aporia.sdk.base import BaseAporiaResource
from aporia.sdk.client import Client
from aporia.sdk.custom_metrics import CustomMetric
from aporia.sdk.dashboards import Dashboard, DashboardConfiguration
from aporia.sdk.fields import Field
from aporia.sdk.monitors import Monitor, MonitorConfiguration, MonitorType
from aporia.sdk.segments import Segment
from aporia.sdk.versions import Version


class ModelType(Enum):
    REGRESSION = "regression"
    BINARY = "binary"
    MULTICLASS = "multiclass"
    MULTILABEL = "multi-label"
    RANKING = "ranking"


class ModelIcon(Enum):
    GENERAL = "general"
    CHURN_RETENTION = "churn-and-retention"
    CONVERSION_PREDICT = "conversion-predict"
    ANOMALY = "anomaly"
    DYNAMIC_PRICING = "dynamic-pricing"
    EMAIL_FILTERING = "email-filtering"
    DEMAND_FORECASTING = "demand-forecasting"
    LTV = "ltv"
    PERSONALIZATION = "personalization"
    FRAUD_DETECTION = "fraud-detection"
    CREDIT_RISK = "credit-risk"
    RECOMMENDATIONS = "recommendations"


class ModelColor(Enum):
    BLUE = "#3564C9"
    TURQUOISE = "#60DFE8"
    GREEN = "#A0D468"
    LIGHT_TEAL = "#39DAA3"
    PINK = "#EC87C0"
    PURPLE = "#AF72FD"
    GOLD = "#FFCE54"
    ORANGE = "#FC6E51"


class ModelAggregationPeriod(Enum):
    DAILY = "daily"
    HOURLY = "hourly"


class NoOwner:
    pass


class Model(BaseAporiaResource):
    def __init__(self, client: Client, data: Dict):
        self.client = client
        self.__update_members(data)

    def __update_members(self, data: Dict):
        self.raw_data = data
        self.id = data["id"]
        self.name = data["name"]
        self.type = ModelType(data["type"])
        self.description = data["description"]
        try:
            self.color = ModelColor(data["color"])
        except Exception:
            self.color = data["color"]
        self.icon = ModelIcon(data["icon"])
        self.owner = data["owner"]

    @classmethod
    def get_all(cls, client: Client) -> List["Model"]:
        response = client.send_request("/models", "GET")

        client.assert_response(response)

        return [cls(client=client, data=entry) for entry in response.json()]

    @classmethod
    def create(
        cls,
        client: Client,
        name: str,
        model_type: ModelType,
        description: Optional[str] = None,
        icon: Optional[ModelIcon] = None,
        color: Optional[ModelColor] = None,
        owner: Optional[Union[str, NoOwner]] = NoOwner(),
        aggregation_period: Optional[ModelAggregationPeriod] = None,
    ) -> "Model":
        """Creates a new model in Aporia, and returns a new model descriptor."""
        model_type = ModelType(model_type)

        creation_parameters = {"name": name, "type": model_type.value}

        if description is not None:
            creation_parameters["description"] = description
        if icon is not None:
            creation_parameters["icon"] = icon.value
        if color is not None:
            creation_parameters["color"] = color.value
        if not isinstance(owner, NoOwner):
            creation_parameters["owner"] = owner
        if aggregation_period is not None:
            creation_parameters["aggregation_period"] = aggregation_period.value

        response = client.send_request(
            "/models",
            "POST",
            creation_parameters,
        )

        client.assert_response(response)

        return cls(client=client, data=response.json())

    @classmethod
    def read(cls, client: Client, id: str) -> "Model":
        response = client.send_request(f"/models/{id}", "GET")
        client.assert_response(response)
        return cls(client=client, data=response.json())

    def update(self, **kwargs):
        args = {}
        for k, v in kwargs.items():
            if isinstance(v, Enum):
                args[k] = v.value
            else:
                args[k] = v
        response = self.client.send_request(f"/models/{self.id}", "PUT", args)
        self.client.assert_response(response)
        self.__update_members(response.json())

    def delete(self):
        response = self.client.send_request(f"/models/{self.id}", "DELETE")
        self.client.assert_response(response)

    @staticmethod
    def delete_by_id(client: Client, id: str):
        response = client.send_request(f"/models/{id}", "DELETE")
        client.assert_response(response)

    def create_model_version(self, name: str) -> Version:
        """Creates a new model version."""
        version = Version.create(client=self.client, name=name, model_id=self.id)
        return version

    def create_custom_metric(self, name: str, code: str) -> CustomMetric:
        metric = CustomMetric.create(client=self.client, name=name, model_id=self.id, code=code)
        return metric

    def create_segment(
        self,
        name: str,
        field_name: Optional[str] = None,
        values: Optional[Union[List[str], List[Union[float, int]]]] = None,
        terms: Optional[List[Tuple[str, str]]] = None,
    ) -> Segment:
        segment = Segment.create(
            client=self.client,
            name=name,
            model_id=self.id,
            field_name=field_name,
            values=values,
            terms=terms,
        )
        return segment

    def create_monitor(
        self,
        name: str,
        monitor_type: MonitorType,
        configuration: MonitorConfiguration,
        scheduling: Optional[str] = None,
        comment: Optional[str] = None,
        creator: Optional[str] = None,
        is_active: bool = True,
    ) -> Monitor:
        monitor = Monitor.create(
            client=self.client,
            model_id=self.id,
            name=name,
            monitor_type=monitor_type,
            scheduling=scheduling,
            configuration=configuration,
            comment=comment,
            creator=creator,
            is_active=is_active,
        )
        return monitor

    def create_dashboard(
        self,
        name: str,
        definition: DashboardConfiguration,
        description: str = "",
        owner: Optional[str] = None,
    ) -> Dashboard:
        dashboard = Dashboard.create(
            client=self.client,
            name=name,
            description=description,
            model_id=self.id,
            definition=definition,
            owner=owner,
        )
        return dashboard

    def get_versions(self) -> List[Version]:
        versions = Version.get_all(client=self.client, model_id=self.id)
        return versions

    def get_segments(self) -> List[Segment]:
        segments = Segment.get_all(client=self.client, model_id=self.id)
        return segments

    def get_custom_metrics(self) -> List[CustomMetric]:
        custom_metrics = CustomMetric.get_all(client=self.client, model_id=self.id)
        return custom_metrics

    def get_monitors(self) -> List[Monitor]:
        monitors = Monitor.get_all(client=self.client, model_id=self.id)
        return monitors

    def get_fields(self) -> List[Field]:
        fields = Field.get_model_fields(client=self.client, model_id=self.id)
        return fields

    def get_field_by_name(self, name: str) -> Field:
        for field in self.get_fields():
            if field.name == name:
                return field
        raise ValueError(f"Field '{name}' not found")

    def get_dashboards(self) -> List[Dashboard]:
        dashboards = Dashboard.get_all(client=self.client, model_id=self.id)
        return dashboards

    def _get_calculation_status(self) -> str:
        response = self.client.send_request(
            "/default_metrics/get_status",
            "POST",
            [{"model_id": self.id}],
            url_search_replace=("/api/v1/", "/v1/metrics-agency/"),
        )

        self.client.assert_response(response)

        return response.json()["statuses"][0]
