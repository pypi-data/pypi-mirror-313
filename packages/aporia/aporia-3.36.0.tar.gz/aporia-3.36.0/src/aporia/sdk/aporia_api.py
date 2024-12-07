from typing import Any, Dict, List, Optional, Union

from requests import Session

from aporia.sdk.base import BaseAporiaResource
from aporia.sdk.client import Client
from aporia.sdk.data_sources import DataSource, DataSourceType
from aporia.sdk.metrics import AporiaMetrics, MetricParameters
from aporia.sdk.models import Model, ModelColor, ModelIcon, ModelType, NoOwner


class Aporia:
    def __init__(
        self,
        token: str,
        account_name: str,
        workspace_name: str = "default-workspace",
        base_url: str = "https://platform.aporia.com",
        debug: bool = False,
        delete_on_failure: bool = False,
        requests_session: Optional[Session] = None,
    ):
        self._assert_workspace(
            base_url=base_url,
            token=token,
            account=account_name,
            workspace=workspace_name,
            requests_session=requests_session,
        )
        self.client = Client(
            base_url=f"{base_url}/api/v1/{account_name}/{workspace_name}",
            token=token,
            debug=debug,
            requests_session=requests_session,
        )
        self.metrics_client = AporiaMetrics(
            token=token,
            account_name=account_name,
            workspace_name=workspace_name,
            base_url=base_url,
            requests_session=requests_session,
        )
        self.delete_on_failure = delete_on_failure
        self._created_resources: List[BaseAporiaResource] = []

    def create_model(
        self,
        name: str,
        model_type: ModelType,
        description: Optional[str] = None,
        icon: Optional[ModelIcon] = None,
        color: Optional[ModelColor] = None,
        owner: Optional[Union[str, NoOwner]] = NoOwner(),
    ) -> Model:
        model = Model.create(
            client=self.client,
            name=name,
            model_type=model_type,
            description=description,
            icon=icon,
            color=color,
            owner=owner,
        )
        self._created_resources.append(model)
        return model

    def create_data_source(
        self,
        name: str,
        data_source_type: DataSourceType,
        connection_data: Dict[str, Any],
    ) -> DataSource:
        data_source = DataSource.create(
            client=self.client,
            name=name,
            data_source_type=data_source_type,
            connection_data=connection_data,
        )
        self._created_resources.append(data_source)
        return data_source

    def query_metrics(self, model_id: str, metrics: List[MetricParameters]) -> List:
        return self.metrics_client.query_batch(model_id=model_id, metrics=metrics)

    def get_models(self) -> List[Model]:
        models = Model.get_all(client=self.client)
        return models

    def get_data_sources(self) -> List[DataSource]:
        data_sources = DataSource.get_all(client=self.client)
        return data_sources

    def delete(self):
        for resource in self._created_resources:
            resource.delete()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            if self.delete_on_failure:
                self.delete()

    def _assert_workspace(
        self,
        base_url: str,
        token: str,
        account: str,
        workspace: str,
        requests_session: Optional[Session] = None,
    ):
        client = Client(
            base_url=base_url,
            token=token,
            requests_session=requests_session,
        )
        response = client.send_request(
            f"/v1/identity-service/accounts/{account}/workspaces/{workspace}", "GET"
        )
        client.assert_response(response)
