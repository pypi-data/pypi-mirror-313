# -*- coding: utf-8 -*-
import os
connection_manager_url = os.getenv("CONNECTION_MANAGER_BASE_URL", "http://fdc-project-manager:80/project-manager")
from typing import Final

class ModelFlavours:
    snowflake_model_flavour = "snowflake"
    sklearn_model_flavour = "sklearn"
    xgboost_model_flavour = "xgboost"
    
    @classmethod
    def allowed_flavours(cls):
        return [value for key, value in vars(cls).items() if not key.startswith('__') and not callable(value)][:-1]

class SnowflakeTables:
    MODEL_MONITOR_TABLE: Final = 'FDC_MODEL_MONITORING_'
    ALERT_TABLE: Final = 'FDC_MODEL_ALERTS_'

class UserConfigs:
    repo_key = "repo_details"
    connection_details = "connection_details"
    run_id = "RUN_ID"
    project_id = "PROJECT_ID"
    experimet_name = "experiment_name"
    token_file = "/snowflake/session/token"

class MosaicAI:
    server = os.getenv("MOSAIC_AI_SERVER", "http://localhost:5000/registry/api")
    kyd_setting = "/v1/ml-model/{}/version/{}/kyd/settings"

class NotebooksAPI:
    notebooks_api_server_url = os.getenv("NOTEBOOKS_API_SERVER", "http://notebooks-api.insight.svc.cluster.local:5000/notebooks/api")
    git_repo = os.getenv("GIT_REPO", "/v1/git-repo")


class RPYPackage:
    r_url = os.getenv("R_PACKAGE_REPO", "http://cran.us.r-project.org")
    py_url = os.getenv("PYPI_PACKAGE_REPO", "https://pypi.org/simple")
    conda_url = os.getenv("CONDA_PACKAGE_REPO", "https://repo.anaconda.com/pkgs/main/")
    override_channel_value = (
        "override-channels"
        if os.getenv("ARTIFACTORY") and os.getenv("ARTIFACTORY").lower() == "true"
        else ""
    )


class MLModelV1:
    c = "/v1/ml-model/register"
    u = "/v1/ml-model/add-version"
    lc = "/v1/ml-model"
    rud = "/v1/ml-model/{ml_model_id}"
    rud_model_name = "/v1/ml-model/{ml_model_id}?ml_model_name={ml_model_name}"
    rud_model_name1 = (
        "/v1/ml-model/{ml_model_id}?ml_model_name={ml_model_name}&type={model_type}"
    )


class MLModelResource:
    r = "/v1/ml-model/resource"


class MLModelVersionV1:
    lc = "/v1/ml-model/{ml_model_id}/version"
    rud = "/v1/ml-model/{ml_model_id}/version/{version_id}"
    upload = "/v1/ml-model/{ml_model_id}/version/{version_id}/upload"
    download = "/v1/ml-model/{ml_model_id}/version/{version_id}/download"
    build_time_metrics = "/v1/ml-model/metrics/{version_id}/{tag}"
    delete = "/v1/ml-model/{ml_model_id}/version/{version_id}"


class MLModelMetricsV1:
    lc = "/v1/ml-model/metrics"
    rud = "/v1/ml-model/metrics/{version_id}/{tag}"


class MLModelArtifactsV1:
    add_artifacts_url = "/v1/ml-model/add-artifacts"
    download_artifacts_url = "/v1/model/request-logger/download"


class MLModelDeployV1:
    c = "/v1/ml-model/{ml_model_id}/deploy"
    ud = "/v1/ml-model/{ml_model_id}/deploy/{deployment_id}"


class Client:
    config_file = "~/.mosaic.ai"


class Headers:
    authorization = "Authorization"
    x_project_id = "X-Project-Id"


class Artifacts:
    model = "model.tar.gz"


class MLModelFlavours:
    keras = "keras"
    sklearn = "sklearn"
    pytorch = "pytorch"
    tensorflow = "tensorflow"
    pyspark = "pyspark"
    spacy = "spacy"
    r = "r"
    ensemble = "ensemble"
    xgboost = "xgboost"


class MLModelProfiling:
    l = "/v1/profiling/datasource/{datasource_name}/column-name/{column_name}/version/{version_id}/ml-model/{ml_model_id}"
    c = "/v1/profiling"


class MLModelType:
    classification = "classification"
    regression = "regression"


class MosaicPipPackages:
    client = "mosaic-ai-client"
    automl = "Mosaic-Auto-Ml"
    common_utils = "mosaic-common-utils"
    connector = "mosaic-connector-python"
    visual_client = "mosaic-visual-client"


class CRANPackageList:
    pre_installed_packages = [
        "base",
        "boot",
        "class",
        "cluster",
        "codetools",
        "compiler",
        "datasets",
        "evaluate",
        "foreign",
        "graphics",
        "grDevices",
        "grid",
        "IRkernel",
        "KernSmooth",
        "lattice",
        "MASS",
        "Matrix",
        "methods",
        "mgcv",
        "mosaicrml",
        "nlme",
        "nnet",
        "parallel",
        "pbdZMQ",
        "compareDF",
        "rpart",
        "spatial",
        "splines",
        "stats",
        "stats4",
        "survival",
        "tcltk",
        "tools",
        "utils",
    ]


class MLModelVersionMetadataInfo:
    u = "/v1/ml-model/{ml_model_id}/version/{version_id}/metadata"
    l = "/v1/ml-model/model-meta/{ml_model_id}/version/{version_id}"


class MLModelVersionListing:
    l = "/v1/ml-model/version/list"


class DeployFeasibility:
    default = "default_deploy"
    apply_strategy = "strategy_deploy"
    no_deploy = "no_deploy"


class MLModelVersionFeedback:
    r = "/v1/ml-model/metrics/version/{version_id}/model-feedback"


class MLKYDDataStoreV1:
    kyd = "/v1/ml-model/{ml_model_id}/version/{version_id}/kyd"


class KYDValidations:
    IS_DATA_SUPPORTED = "Supported Data Format"
    UNSUPPORTED_DATA_ERROR = "Know Your Data Does Not Support {} Data Formats"

    IS_SHAPE_CORRECT = "Number of Records Mismatch Validation"

    VALIDATION_FAILED = "KYD Cannot Be Executed Due To Validation Errors."


class KYDExecutorLabels(KYDValidations):
    SUPPORTED_FORMATS = ["NUMPY", "PANDAS"]
    PUBLISHED = "Know Your Data for /{}/{}/ Published"
    PUBLISHED_FAIL = "Unable to publish Know Your Data for /{}/{}/"
    CHUNK_SIZE = 200


class SparkDistributed:
    executor_pod_image = os.getenv("executor_pod_image")
    executor_request_cpu = os.getenv("executor_request_cpu")
    executor_request_memory = os.getenv("executor_request_memory")
    executor_limit_cpu = os.getenv("executor_limit_cpu")
    executor_limit_memory = os.getenv("executor_limit_memory")
    number_of_executors = os.getenv("number_of_executors")
    executor_service_name = os.getenv("pod_name")
    pvc_name = os.getenv("pvc_name")
    project_id = os.getenv("PROJECT_ID")
    user_id = os.getenv("userId")
    minio_data_bucket = os.getenv("MINIO_DATA_BUCKET")
    namespace = os.getenv("NAMESPACE")
    is_job_run = os.getenv("is_job_run")
    PYTHONPATH = os.getenv("PYTHONPATH")
