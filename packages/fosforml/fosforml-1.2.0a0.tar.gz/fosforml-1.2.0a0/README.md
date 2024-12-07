
# Fosforml

## Overview
The `fosforml` package is designed to facilitate the registration, management, and deployment of machine learning models with a focus on integration with Snowflake. It provides tools for managing datasets, model metadata, and the lifecycle of models within a Snowflake environment.

## Features
- Model Registration: Register models to the Snowflake Model registry with detailed metadata, including descriptions, types, and dependencies.
- Dataset Management: Handle datasets within Snowflake, including creation, versioning, and deletion of dataset objects.
- Metadata Management: Update model registry with descriptions and tags for better organization and retrieval.
- Snowflake Session Management: Manage Snowflake sessions for executing operations within the Snowflake environment.

## Installation
To install the `fosforml` package, ensure you have Python installed on your system and run the following command:

```shell
pip install fosforml
```

## Usage
Register a model with the Snowflake Model Registry using the `register_model` function. The function supports both Snowflake and Pandas dataframes, catering to different data handling preferences.

### Requirements
- **Snowflake DataFrame**: If you are using Snowflake as your data warehouse, you must provide a Snowflake DataFrame (`snowflake.snowpark.dataframe.DataFrame`) that includes model feature names, labels, and output column names.
  - `snowflake_df`: Training snowflake dataframe with required feature,label and prediction columns.

- **Pandas DataFrame**: For users preferring local or in-memory data processing, you must upload the following as Pandas DataFrames (`pandas.DataFrame`):
  - `x_train`: Training data with feature columns.
  - `y_train`: Training data labels.
  - `x_test`: Test data with feature columns.
  - `y_test`: Test data labels.
  - `y_pred`: Predicted labels for the test data.
  - `y_prob`: Predicted probabilities for the test data classes for classification problems.

- Numpy data arrays are not allowed as input datasets to register the model
- `dataset_name`: Name of the dataset on which the model is trained.
- `dataset_source`: Name of the source from where the dataset is pulled/created.
- `source`: Model environment name where the model is being developed (e.g., Notebook/Experiment).

### Supported Model Flavors

Currently, the framework supports the following model flavors:

- **Snowflake Models (snowflake)**: Models that are directly integrated with Snowflake, leveraging Snowflake's data processing capabilities.
- **Scikit-Learn Models (sklearn)**: Models built using the Scikit-Learn library, a widely used library for machine learning in Python.

### Registering a Model
To register a model with the `fosforml` package, you need to provide the model object, session, and other relevant details such as the model name, description, and type.

#### For Snowflake Models:

```python
from fosforml import register_model

register_model(
  model_obj=pipeline,
  session=session,
  name="MyModel",
  snowflake_df=pred_df,
  dataset_name="HR_CHURN",
  dataset_source="Dataset",
  source="Notebook",
  description="This is a Snowflake model",
  flavour="snowflake",
  model_type="classification",
  conda_dependencies=["scikit-learn==1.3.2"]
)
```

#### For Scikit-Learn Models:

```python
from fosforml import register_model

register_model(
  model_obj=model,
  session=session,
  x_train=x_train,
  y_train=y_train,
  x_test=x_test,
  y_test=y_test,
  y_pred=y_pred,
  y_prob=y_prob,
  source="Notebook",
  dataset_name="HR_CHURN",
  dataset_source="InMemory",
  name="MyModel",
  description="This is a sklearn model",
  flavour="sklearn",
  model_type="classification",
  conda_dependencies=["scikit-learn==1.3.2"]
)
```

### Snowflake Session Management
The `SnowflakeSession` class is used to manage connections to Snowflake, facilitating the execution of operations within the Snowflake environment. It provides the following features:
- `session`: To get the Snowflake session object.
- `connection_params`: To get the Snowflake connection parameters.

```python
from fosforml.model_manager.snowflakesession import get_session, get_connection_params

session = get_session()
connection_params = get_connection_params()
```

### Retrieving Model History

The `ModelRegistry` class provides functionalities to interact with the history of machine learning models stored in your environment. By utilizing this class, you can retrieve list of all models and their respective versions. This feature is particularly useful for tracking model evolution and managing model versions effectively.

#### Initializing ModelRegistry

To begin, you need to initialize the `ModelRegistry` class with an active session and connection parameters. These parameters are essential for establishing a connection to your data storage environment, where your models and their metadata are stored.

```python
from fosforml.model_manager import ModelRegistry

registry = ModelRegistry(
    session=session,
    connection_params=connection_params
)
```

#### Listing All Models
To obtain a list of all models stored in your environment, use the `list_models` method. This method returns a list of model names, providing a quick overview of the models you have.

```
model_list = registry.list_models()
print("Models:", model_list)
```

#### To list model versions
For more detailed insights into a specific model's evolution, The list_model_versions method can be used. By specifying a model's name, you can retrieve a list of all versions associated with that model. This allows for easy tracking of model updates and iterations

```
versions_list = registry.list_model_versions(model_name='YourModelName')
print("Versions_list:",versions_list)
```

### Managing Datasets with DatasetManager

The `DatasetManager` class is designed to facilitate the management of datasets associated with machine learning models in Snowflake. It allows for the creation, uploading, listing, deletion, and retrieval of datasets in a structured manner.

#### Initializing DatasetManager

To use `DatasetManager`, you need to initialize it with the model name, version, session, and connection parameters. The session and connection parameters ensure that `DatasetManager` can interact with the Snowflake environment where your datasets and models are stored.

```python
from fosforml.model_manager import DatasetManager

dataset_manager = DatasetManager(
    model_name="YourModelName",
    version_name="v1",
    session=session,
    connection_params=connection_params
)
```
### Upload datasets to a specific model version
To upload datasets to a specific model version, use the following code:

```python
dataset_manager.upload_datasets(session=session, datasets={"x_train": snowflake_train_dataframe_,
                                                           "x_test": snowflake_test_dataframe_},
                                                            ...
                                                           )
```

#### Listing Datasets
To list all datasets associated with a specific model and version, use the `list_datasets` method. This method returns a list of dataset names that have been uploaded and registered under the specified model and version.

```python
datasets = dataset_manager.list_datasets()
print("Available datasets:", datasets)
```

#### Reading Datasets
The `DatasetManager` provides a method to read datasets: `read_dataset`. This method allows you to retrieve datasets either as Pandas DataFrames or as native Snowflake query results, depending on the `to_pandas` parameter.

##### To read as a Pandas DataFrame
To read a dataset as a Pandas DataFrame, set `to_pandas=True` as shown below:

```python
dataset_df = dataset_manager.read_dataset(dataset_name="x_train", to_pandas=True)
print(dataset_df.head())
```

##### To read as a Snowflake DataFrame
To read a dataset as a Snowflake DataFrame, set `to_pandas=False` as shown below:

```python
dataset_result = dataset_manager.read_dataset(dataset_name="x_train", to_pandas=False)
print(dataset_result.show())
```

### Delete datasets
To delete datasets associated with a specific model version, use the following code:

```python
dataset_manager.remove_datasets()
```

## Dependencies
- pandas
- snowflake-ml-python
- requests

Ensure these dependencies are installed in your environment to use the `fosforml` package effectively.

For issues and contributions, please refer to the project's [GitHub repository](https://gitlab.fosfor.com/fosfor-decision-cloud/intelligence/refract-sdk/-/tree/main/fosforml?ref_type=heads).

## Additional Resources
For further assistance and examples on how to register models using [`fosforml`](https://gitlab.fosfor.com/fosfor-decision-cloud/intelligence/refract-sdk/-/tree/main/fosforml/examples?ref_type=heads), please refer to the `example` folder in the project repository. This folder contains Jupyter notebooks that provide step-by-step guidance on model registration and other operations.

Visit [www.fosfor.com](https://www.fosfor.com) for more information.