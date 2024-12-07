import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel
from requests import Session

from aporia.sdk.client import Client
from aporia.sdk.datasets import DatasetType


class MetricType(str, Enum):
    COUNT = "count"
    MEAN = "mean"
    MEAN_LENGTH = "mean_length"
    MIN = "min"
    MEDIAN = "median"
    MIN_LENGTH = "min_length"
    MAX = "max"
    MAX_LENGTH = "max_length"
    SUM = "sum"
    MISSING_COUNT = "missing_count"
    MISSING_RATIO = "missing_ratio"
    TP_COUNT = "tp_count"
    TN_COUNT = "tn_count"
    FP_COUNT = "fp_count"
    FN_COUNT = "fn_count"
    ACCURACY = "accuracy"
    RECALL = "recall"
    PRECISION = "precision"
    AUC_ROC = "auc_roc"
    F1 = "f1"
    MSE = "mse"
    RMSE = "rmse"
    MAE = "mae"
    ACCURACY_AT_K = "accuracy_at_k"
    PRECISION_AT_K = "precision_at_k"
    RECALL_AT_K = "recall_at_k"
    MAP_AT_K = "map_at_k"
    MRR_AT_K = "mrr_at_k"
    NDCG_AT_K = "ndcg_at_k"
    JS_DISTANCE = "js_distance"
    KS_DISTANCE = "ks_distance"
    HELLINGER_DISTANCE = "hellinger_distance"
    EUCLIDEAN_DISTANCE = "euclidean_distance"
    PSI = "psi"
    ACCURACY_PER_CLASS = "accuracy_per_class"
    PRECISION_PER_CLASS = "precision_per_class"
    RECALL_PER_CLASS = "recall_per_class"
    F1_PER_CLASS = "f1_per_class"
    TP_COUNT_PER_CLASS = "tp_count_per_class"
    TN_COUNT_PER_CLASS = "tn_count_per_class"
    FP_COUNT_PER_CLASS = "fp_count_per_class"
    FN_COUNT_PER_CLASS = "fn_count_per_class"
    QUANTILE = "quantile"
    MAPE="mape"
    # Non-aggregable metrics
    AUUC = "auuc"
    # None-Dashboard metrics
    LAST_VERSION_CREATION = "last_version_creation"
    HISTOGRAM = "histogram"
    VALUE_COUNT = "value_count"
    MIN_MAX = "min_max"
    UNIQUE_VALUES = "unique_values"
    MISSING = "missing"
    # Custom metrics
    CUSTOM_METRIC = "custom_metric"
    CODE = "code"


class AverageMethod(str, Enum):
    MICRO = "micro"
    MACRO = "macro"
    WEIGHTED = "weighted"


def is_model_metric(metric: MetricType) -> bool:
    return metric is MetricType.COUNT


def is_custom_metric(metric: MetricType) -> bool:
    return metric is MetricType.CUSTOM_METRIC


def is_code_based_metric(metric: MetricType) -> bool:
    return metric is MetricType.CODE


def is_aggregable_metric(metric: MetricType) -> bool:
    return not (metric is MetricType.CODE or metric is MetricType.AUUC)


class TimeRange(BaseModel):
    start: datetime.datetime
    end: datetime.datetime  # "2023-05-12T00:00:00.000000+00:00"

    def serialize(self):
        return {
            "start": self.start.isoformat(timespec="microseconds") + "+00:00",
            "end": self.end.isoformat(timespec="microseconds") + "+00:00",
        }


class MetricSegment(BaseModel):
    id: str
    value: str  # TODO: Test with numeric auto segments

    def serialize(self) -> Dict:
        return {"id": self.id, "value": self.value}


class MetricDataset(BaseModel):
    dataset_type: DatasetType = DatasetType.SERVING
    time_range: Optional[TimeRange] = None
    model_version: Optional[str] = None
    segment: Optional[MetricSegment] = None

    def serialize(self) -> Dict:
        return {
            "dataset_type": self.dataset_type.value,
            "time_range": self.time_range.serialize() if self.time_range is not None else None,
            "model_version": self.model_version,
            "segment": self.segment.serialize() if self.segment is not None else None,
        }


class MetricResponse(BaseModel):
    id: str
    value: Any
    error: Optional[Union[Dict, List, str]]
    segment: Optional[MetricSegment]


class QueryResponse(BaseModel):
    metrics: List[MetricResponse]
    time_range: Optional[TimeRange] = None


class MetricParameters(BaseModel):
    dataset: MetricDataset
    # Metric identifier
    name: str
    # Parameters
    column: Optional[str] = None
    k: Optional[int] = None
    threshold: Optional[float] = None
    custom_metric_id: Optional[str] = None
    baseline: Optional[MetricDataset] = None
    value: Optional[Any] = None


class MetricError(Exception):
    def __init__(self, error, parameters: MetricParameters):
        super().__init__(error)
        self.parameters = parameters


class AporiaMetrics:
    def __init__(
        self,
        token: str,
        account_name: str,
        base_url: str = "https://platform.aporia.com",
        workspace_name: str = "default-workspace",
        requests_session: Optional[Session] = None,
    ) -> Dict:
        self.client = Client(
            base_url=f"{base_url}/api/v1/{account_name}/{workspace_name}",
            token=token,
            requests_session=requests_session,
        )

    def query(
        self,
        # Dataset identifiers
        model_id: str,
        dataset: MetricDataset,
        # Metric identifier
        metric_name: str,
        baseline: Optional[MetricDataset] = None,
        # Parameters
        column: Optional[str] = None,
        k: Optional[int] = None,
        threshold: Optional[float] = None,
        custom_metric_id: Optional[str] = None,
    ):
        metric_parameters = {}
        if column is not None:
            metric_parameters["column"] = column
        if k is not None:
            metric_parameters["k"] = k
        if threshold is not None:
            metric_parameters["threshold"] = threshold
        if custom_metric_id is not None:
            metric_parameters["id"] = custom_metric_id

        metric_datasets = {"data": dataset.serialize()}
        if baseline is not None:
            metric_datasets["baseline"] = baseline.serialize()

        response = self.client.send_request(
            "/query",
            method="POST",
            data={
                "model_id": model_id,
                "metrics": [
                    {
                        "id": "0",
                        "metric": metric_name,
                        "parameters": metric_parameters,
                        "datasets": metric_datasets,
                    }
                ],
            },
            url_search_replace=("/api/v1/", "/v1/metrics-reducer/"),
        )
        self.client.assert_response(response)

        result = [QueryResponse(**entry) for entry in response.json()]

        if result[0].metrics[0].error is not None:
            raise Exception(f"Error occured: {result[0].metrics[0].error}")
        return result[0].metrics[0].value

    def query_batch(self, model_id: str, metrics: List[MetricParameters]) -> List:
        metric_requests = []
        for i, metric in enumerate(metrics):
            metric_parameters = {}
            if metric.column is not None:
                metric_parameters["column"] = metric.column
            if metric.k is not None:
                metric_parameters["k"] = metric.k
            if metric.threshold is not None:
                metric_parameters["threshold"] = metric.threshold
            if metric.quantile is not None:
                metric_parameters["quantile"] = metric.quantile
            if metric.custom_metric_id is not None:
                metric_parameters["id"] = metric.custom_metric_id
            if metric.value is not None:
                metric_parameters["value"] = metric.value

            metric_datasets = {"data": metric.dataset.serialize()}
            if metric.baseline is not None:
                metric_datasets["baseline"] = metric.baseline.serialize()
            metric_requests.append(
                {
                    "id": str(i),
                    "metric": metric.name,
                    "parameters": metric_parameters,
                    "datasets": metric_datasets,
                }
            )

        response = self.client.send_request(
            "/query",
            method="POST",
            data={
                "model_id": model_id,
                "metrics": metric_requests,
            },
            url_search_replace=("/api/v1/", "/v1/metrics-reducer/"),
        )
        self.client.assert_response(response)

        result = [QueryResponse(**entry) for entry in response.json()]

        # Restore order, because different timeframes may change order
        metric_results = {}
        for entry in result:
            for metric in entry.metrics:
                metric_index = int(metric.id)
                if metric.error is not None:
                    metric_results[metric_index] = MetricError(
                        error=metric.error, parameters=metrics[metric_index]
                    )
                else:
                    metric_results[metric_index] = metric.value

        return [metric_results[i] for i in range(len(metric_results))]
