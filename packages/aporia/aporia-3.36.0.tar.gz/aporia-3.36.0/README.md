# Aporia Python SDK

Aporia's Python SDK is a powerful tool designed to streamline ML monitoring and observability. 

Define your models, monitors, dashboards, segments, custom metrics, and other ML Observability resources *as code*, just like in Terraform or Pulumi. The SDK also enables you to query metrics from Aporia to integrate with other platforms.

## Key Features

 * **ML Monitoring as Code:** Make it easier to manage and track changes by managing your models, dashboards, segments, and other ML Observability resources as code.
 * **CI/CD Integration:** Integrate with your CI/CD pipeline to automatically monitor all your models with Aporia.
 * **Query Metrics:** Fetch metrics directly from Aporia's platform to inform decisions or to use in other applications.
 * **Data Source Integration:** You can define and integrate multiple types of data sources, like S3, Snowflake, Glue Data Catalog, Databricks, and others. This allows your models to leverage a wide range of data for training and inference.
 * **Pythonic Interface:** Use the familiar Python programming paradigm to interact with Aporia.


## Installation

You can install the Aporia SDK using pip:

```bash
pip install aporia
```

## Quickstart

### Define models as code

```python
import datetime
import os

from aporia import Aporia, MetricDataset, MetricParameters, TimeRange
import aporia.as_code as aporia

aporia_token = os.environ["APORIA_TOKEN"]
aporia_account = os.environ["APORIA_ACCOUNT"]
aporia_workspace = os.environ["APORIA_WORKSPACE"]

stack = aporia.Stack(
    token=aporia_token,
    account=aporia_account,
    workspace=aporia_workspace,
)

# Your model definition code goes here

stack.apply(yes=True, rollback=False, config_path="config.json")
```

### Query Metrics using the SDK

This example shows how you can use the Aporia SDK to query metrics from a model:

```python
from datetime import datetime
from aporia import (
    Aporia,
    MetricDataset,
    MetricParameters,
    TimeRange,
    DatasetType,
)

aporia_token = os.environ["APORIA_TOKEN"]
aporia_account = os.environ["APORIA_ACCOUNT"]
aporia_workspace = os.environ["APORIA_WORKSPACE"]

aporia_client = Aporia(
    token=aporia_token,
    account_name=aporia_account,
    workspace_name=aporia_workspace,
)

last_week_dataset = MetricDataset(
    dataset_type=DatasetType.SERVING,
    time_range=TimeRange(
        start=datetime.now() - datetime.timedelta(days=7),
        end=datetime.now(),
    ),
)

metrics = aporia_client.query_metrics(
    model_id=model_id,
    metrics=[
        MetricParameters(
            dataset=MetricDataset(dataset_type=DatasetType.SERVING),
            name="count",
        ),
    ],
)

print(f"The model had {metrics[0]} predictions last week")
```

Refer to the official Aporia documentation for detailed information on how to use the SDK.

## Development
This package uses Poetry for dependency management. To install dependencies, use:

```bash
poetry install
```
