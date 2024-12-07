# -*- coding: utf-8 -*-
import numpy
import pytest
import requests
from PIL import Image
from sklearn import datasets, svm

from fosforml import scoring_func

def _env_setup(monkeypatch):
    monkeypatch.setenv(
        "base_docker_image_name",
        "python",
    )

 

@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    _env_setup(monkeypatch)

@pytest.fixture(autouse=True)
def model_dict():
    return {
        "created_by": "10662254",
        "created_on": "2019-08-06T08:40:59.273662+00:00",
        "description": "svm classifier using sklearn",
        "flavour": "sklearn",
        "id": "c6252ff7-8928-4d43-b433-02fb67f24a3d",
        "init_script": "",
        "last_modified_by": "10662254",
        "last_modified_on": None,
        "name": "Credit_Train",
        "project_id": "1",
        "versions": [
            {
                "created_by": "10662254",
                "created_on": "2019-08-06T08:58:27.519680+00:00",
                "description": None,
                "id": "63d4ce07-ee31-4c1b-9bb1-52fb0c1901c9",
                "last_modified_by": "10662254",
                "last_modified_on": None,
                "ml_model_id": "c6252ff7-8928-4d43-b433-02fb67f24a3d",
                "object_url": None,
            }
        ],
    }


@pytest.fixture(autouse=True)
def no_deployments_model_dict():
    return {
        "created_by": "10662254",
        "created_on": "2019-08-06T08:40:59.273662+00:00",
        "description": "svm classifier using sklearn",
        "flavour": "sklearn",
        "id": "c6252ff7-8928-4d43-b433-02fb67f24a3d",
        "init_script": "",
        "last_modified_by": "10662254",
        "last_modified_on": None,
        "name": "Credit_Train",
        "project_id": "1",
        "versions": [
            {
                "created_by": "10662254",
                "created_on": "2019-08-06T08:58:27.519680+00:00",
                "description": None,
                "deployments": [],
                "id": "63d4ce07-ee31-4c1b-9bb1-52fb0c1901c9",
                "last_modified_by": "10662254",
                "last_modified_on": None,
                "ml_model_id": "c6252ff7-8928-4d43-b433-02fb67f24a3d",
                "object_url": None,
            }
        ],
    }


@pytest.fixture(autouse=True)
def deployment_model_dict_deployed():
    return {
        "created_by": "mosaic.ai",
        "created_on": "2020-01-28T09:37:58+00:00",
        "deploymentstatus": True,
        "description": "svm classifier using sklearn",
        "flavour": "sklearn",
        "id": "45c7e7db-5674-4878-bd40-59c38a9521f2",
        "last_modified_by": "mosaic.ai",
        "last_modified_on": "2020-01-28T09:37:58+00:00",
        "name": "TestingGiven",
        "project_id": "1",
        "type": "model",
        "versions": [
            {
                "created_by": "mosaic.ai",
                "created_on": "2020-01-28T09:39:53+00:00",
                "datasource_name": None,
                "deploy_info": None,
                "deployments": [
                    {
                        "created_by": "mosaic.ai",
                        "created_on": "2020-08-25T17:59:12+00:00",
                        "deployment_info": {
                            "configmap_name": "jwt-dp-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                            "cpu_utilization": "75",
                            "deployment_name": "dp-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                            "deployment_type": "Default",
                            "host_name": "ratanboddu.com/testingartinofucksgiven/45c7e7db-5674-4878-bd40-59c38a9521f2",
                            "hpa_name": "hpa-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                            "ingress_name": "ing-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                            "init_configmap_name": "script-dp-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                            "labels": {},
                            "service_name": "svc-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                            "strategy_deployment_id": "46f7a0b7-94ab-483e-aee1-9d39242441cd",
                            "strategy_version_id": "28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                        },
                        "deployment_status": "DEPLOYED",
                        "id": "19430fc7-89e7-4e78-be2f-3fd5b01c81a6",
                        "last_modified_by": "mosaic.ai",
                        "last_modified_on": "2020-08-26T09:29:53+00:00",
                        "ml_model_id": "45c7e7db-5674-4878-bd40-59c38a9521f2",
                        "name": "dp-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                        "resource": {
                            "cpu_limit": "500m",
                            "cpu_request": "50m",
                            "gpu": "",
                            "gpu_type": None,
                            "id": "b0d93c79-b4f0-46c0-8a54-e41abbaa5583",
                            "max_replicas": "3",
                            "min_replicas": "1",
                            "name": "Micro",
                            "ram_limit": "300Mi",
                            "ram_request": "50Mi",
                        },
                        "resource_id": "b0d93c79-b4f0-46c0-8a54-e41abbaa5583",
                        "version_id": "28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                    }
                ],
                "description": None,
                "docker_image_url": "registry.lti-aiq.in:443/mosaic-ai-logistics/mosaic-ai-serving:1.0.0-52280",
                "id": "28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                "init_script": '"pip install absl-py==0.9.0 appdirs==1.4.3 appnope==0.1.0 aspy.yaml==1.3.0 astor==0.8.1 attrs==19.3.0 backcall==0.1.0 black==19.10b0 bleach==3.1.0 blis==0.4.1 cachetools==4.0.0 certifi==2019.11.28 cffi==1.13.2 cfgv==2.0.1 chardet==3.0.4 Click==7.0 cloudpickle==1.2.1 coverage==5.0.2 cymem==2.0.3 decorator==4.4.1 defusedxml==0.6.0 entrypoints==0.3 gast==0.3.2 google-auth==1.10.0 google-pasta==0.1.8 grpcio==1.26.0 h5py==2.10.0 identify==1.4.9 idna==2.8 importanize==0.7.0 importlib-metadata==1.3.0 importlib-resources==1.0.2 ipykernel==5.1.3 ipython==7.11.1 ipython-genutils==0.2.0 ipywidgets==7.5.1 jedi==0.15.2 Jinja2==2.10.3 joblib==0.14.1 jsonschema==3.2.0 jupyter==1.0.0 jupyter-client==5.3.4 jupyter-console==6.0.0 jupyter-core==4.6.1 Keras==2.3.1 Keras-Applications==1.0.8 Keras-Preprocessing==1.1.0 kubernetes==9.0.0 Markdown==3.1.1 MarkupSafe==1.1.1 mistune==0.8.4 more-itertools==8.0.2 murmurhash==1.0.2 nbconvert==5.6.1 nbformat==5.0.3 nodeenv==1.3.4 notebook==6.0.2 numpy==1.17.0 oauthlib==3.1.0 packaging==20.0 pandas==0.25.1 pandocfilters==1.4.2 parso==0.5.2 pathlib2==2.3.5 pathspec==0.7.0 pexpect==4.7.0 pickleshare==0.7.5 Pillow==7.0.0 pip==19.3.1 plac==1.1.3 pluggy==0.13.1 pre-commit==1.21.0 preshed==3.0.2 prometheus-client==0.7.1 prompt-toolkit==2.0.10 protobuf==3.11.2 ptyprocess==0.6.0 py==1.8.1 py4j==0.10.4 pyasn1==0.4.8 pyasn1-modules==0.2.8 pycparser==2.19 Pygments==2.5.2 pyparsing==2.4.6 pyrsistent==0.15.7 pyspark==2.1.2 pytest==5.3.2 pytest-cov==2.8.1 python-dateutil==2.8.1 pytz==2019.3 PyYAML==5.1.2 pyzmq==18.1.1 qtconsole==4.6.0 regex==2020.1.8 requests==2.22.0 requests-oauthlib==1.3.0 rpy2==3.2.0 rsa==4.0 scikit-learn==0.21.3 scipy==1.4.1 Send2Trash==1.5.0 setuptools==44.0.0 simplegeneric==0.8.1 six==1.13.0 sklearn==0.0 spacy==2.2.2 srsly==1.0.1 tensorboard==1.14.0 tensorflow==1.14.0 tensorflow-estimator==1.14.0 termcolor==1.1.0 terminado==0.8.3 testpath==0.4.4 thinc==7.3.1 toml==0.10.0 torch==1.2.0 torchvision==0.4.0 tornado==6.0.3 tqdm==4.41.1 traitlets==4.3.3 typed-ast==1.4.0 tzlocal==2.0.0 urllib3==1.25.7 virtualenv==16.7.9 wasabi==0.6.0 wcwidth==0.1.8 webencodings==0.5.1 websocket-client==0.57.0 Werkzeug==0.16.0 wheel==0.33.6 widgetsnbextension==3.5.1 wrapt==1.11.2 zipp==0.6.0 \\nmkdir abc"',
                "input_type": "json",
                "last_modified_by": "mosaic.ai",
                "last_modified_on": "2020-01-28T09:39:54+00:00",
                "metadata_info": None,
                "ml_model_id": "45c7e7db-5674-4878-bd40-59c38a9521f2",
                "model_class": None,
                "model_info": None,
                "object_url": "45c7e7db-5674-4878-bd40-59c38a9521f2/28617a40-64b7-4dfc-a0d1-35eef9f2c558/ml_model.tar.gz",
                "profiling": [],
                "schema": None,
                "status": "active",
                "target_names": None,
                "version_no": 2,
            },
            {
                "created_by": "mosaic.ai",
                "created_on": "2020-01-28T09:37:58+00:00",
                "datasource_name": None,
                "deploy_info": None,
                "deployments": [
                    {
                        "created_by": "mosaic.ai",
                        "created_on": "2020-08-26T09:29:51+00:00",
                        "deployment_info": {
                            "configmap_name": "jwt-dp-4250de43-ea10-4c92-881a-d01907f24b5b",
                            "cpu_utilization": "75",
                            "deployment_name": "dp-4250de43-ea10-4c92-881a-d01907f24b5b",
                            "deployment_type": "PreProd",
                            "host_name": "mosaic.dev.lti-mosaic.com/testingartinofucksgiven/45c7e7db-5674-4878-bd40-59c38a9521f2",
                            "hpa_name": "hpa-4250de43-ea10-4c92-881a-d01907f24b5b",
                            "ingress_name": "ing-4250de43-ea10-4c92-881a-d01907f24b5b",
                            "init_configmap_name": "script-dp-4250de43-ea10-4c92-881a-d01907f24b5b",
                            "labels": {},
                            "service_name": "svc-4250de43-ea10-4c92-881a-d01907f24b5b",
                            "strategy_deployment_id": "19430fc7-89e7-4e78-be2f-3fd5b01c81a6",
                            "strategy_version_id": "4250de43-ea10-4c92-881a-d01907f24b5b",
                        },
                        "deployment_status": "DEPLOYING",
                        "id": "46f7a0b7-94ab-483e-aee1-9d39242441cd",
                        "last_modified_by": "mosaic.ai",
                        "last_modified_on": "2020-08-26T09:29:53+00:00",
                        "ml_model_id": "45c7e7db-5674-4878-bd40-59c38a9521f2",
                        "name": None,
                        "resource": {
                            "cpu_limit": "1",
                            "cpu_request": "50m",
                            "gpu": "",
                            "gpu_type": None,
                            "id": "844991ca-5d3f-4ddd-b9bf-34c9b78125f0",
                            "max_replicas": "3",
                            "min_replicas": "1",
                            "name": "default",
                            "ram_limit": "800Mi",
                            "ram_request": "50Mi",
                        },
                        "resource_id": "844991ca-5d3f-4ddd-b9bf-34c9b78125f0",
                        "version_id": "4250de43-ea10-4c92-881a-d01907f24b5b",
                    }
                ],
                "id": "4250de43-ea10-4c92-881a-d01907f24b5b",
                "ml_model_id": "45c7e7db-5674-4878-bd40-59c38a9521f2",
            },
        ],
    }


@pytest.fixture(autouse=True)
def deployment_model_dict_deployed_VA():
    return {
        "created_by": "mosaic.ai",
        "created_on": "2020-01-28T09:37:58+00:00",
        "deploymentstatus": True,
        "description": "svm classifier using sklearn",
        "flavour": "sklearn",
        "id": "45c7e7db-5674-4878-bd40-59c38a9521f2",
        "last_modified_by": "mosaic.ai",
        "last_modified_on": "2020-01-28T09:37:58+00:00",
        "name": "TestingGiven",
        "project_id": "1",
        "type": "model",
        "versions": [
            {
                "created_by": "mosaic.ai",
                "created_on": "2020-01-28T09:39:53+00:00",
                "datasource_name": None,
                "deploy_info": None,
                "deployments": [
                    {
                        "created_by": "mosaic.ai",
                        "created_on": "2020-08-25T17:59:12+00:00",
                        "deployment_info": {
                            "configmap_name": "jwt-dp-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                            "cpu_utilization": "75",
                            "deployment_name": "dp-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                            "deployment_type": "Default",
                            "host_name": "ratanboddu.com/testingartinofucksgiven/45c7e7db-5674-4878-bd40-59c38a9521f2",
                            "hpa_name": "hpa-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                            "ingress_name": "ing-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                            "init_configmap_name": "script-dp-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                            "labels": {},
                            "service_name": "svc-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                            "strategy_deployment_id": "46f7a0b7-94ab-483e-aee1-9d39242441cd",
                            "strategy_version_id": "28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                        },
                        "deployment_status": "DEPLOYED",
                        "id": "19430fc7-89e7-4e78-be2f-3fd5b01c81a6",
                        "last_modified_by": "mosaic.ai",
                        "last_modified_on": "2020-08-26T09:29:53+00:00",
                        "ml_model_id": "45c7e7db-5674-4878-bd40-59c38a9521f2",
                        "name": "dp-28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                        "resource": {
                            "cpu_limit": "500m",
                            "cpu_request": "50m",
                            "gpu": "",
                            "gpu_type": None,
                            "id": "b0d93c79-b4f0-46c0-8a54-e41abbaa5583",
                            "max_replicas": "3",
                            "min_replicas": "1",
                            "name": "Micro",
                            "ram_limit": "300Mi",
                            "ram_request": "50Mi",
                        },
                        "resource_id": "b0d93c79-b4f0-46c0-8a54-e41abbaa5583",
                        "version_id": "28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                    }
                ],
                "description": None,
                "docker_image_url": "registry.lti-aiq.in:443/mosaic-ai-logistics/mosaic-ai-serving:1.0.0-52280",
                "id": "28617a40-64b7-4dfc-a0d1-35eef9f2c558",
                "init_script": '"pip install absl-py==0.9.0 appdirs==1.4.3 appnope==0.1.0 aspy.yaml==1.3.0 astor==0.8.1 attrs==19.3.0 backcall==0.1.0 black==19.10b0 bleach==3.1.0 blis==0.4.1 cachetools==4.0.0 certifi==2019.11.28 cffi==1.13.2 cfgv==2.0.1 chardet==3.0.4 Click==7.0 cloudpickle==1.2.1 coverage==5.0.2 cymem==2.0.3 decorator==4.4.1 defusedxml==0.6.0 entrypoints==0.3 gast==0.3.2 google-auth==1.10.0 google-pasta==0.1.8 grpcio==1.26.0 h5py==2.10.0 identify==1.4.9 idna==2.8 importanize==0.7.0 importlib-metadata==1.3.0 importlib-resources==1.0.2 ipykernel==5.1.3 ipython==7.11.1 ipython-genutils==0.2.0 ipywidgets==7.5.1 jedi==0.15.2 Jinja2==2.10.3 joblib==0.14.1 jsonschema==3.2.0 jupyter==1.0.0 jupyter-client==5.3.4 jupyter-console==6.0.0 jupyter-core==4.6.1 Keras==2.3.1 Keras-Applications==1.0.8 Keras-Preprocessing==1.1.0 kubernetes==9.0.0 Markdown==3.1.1 MarkupSafe==1.1.1 mistune==0.8.4 more-itertools==8.0.2 murmurhash==1.0.2 nbconvert==5.6.1 nbformat==5.0.3 nodeenv==1.3.4 notebook==6.0.2 numpy==1.17.0 oauthlib==3.1.0 packaging==20.0 pandas==0.25.1 pandocfilters==1.4.2 parso==0.5.2 pathlib2==2.3.5 pathspec==0.7.0 pexpect==4.7.0 pickleshare==0.7.5 Pillow==7.0.0 pip==19.3.1 plac==1.1.3 pluggy==0.13.1 pre-commit==1.21.0 preshed==3.0.2 prometheus-client==0.7.1 prompt-toolkit==2.0.10 protobuf==3.11.2 ptyprocess==0.6.0 py==1.8.1 py4j==0.10.4 pyasn1==0.4.8 pyasn1-modules==0.2.8 pycparser==2.19 Pygments==2.5.2 pyparsing==2.4.6 pyrsistent==0.15.7 pyspark==2.1.2 pytest==5.3.2 pytest-cov==2.8.1 python-dateutil==2.8.1 pytz==2019.3 PyYAML==5.1.2 pyzmq==18.1.1 qtconsole==4.6.0 regex==2020.1.8 requests==2.22.0 requests-oauthlib==1.3.0 rpy2==3.2.0 rsa==4.0 scikit-learn==0.21.3 scipy==1.4.1 Send2Trash==1.5.0 setuptools==44.0.0 simplegeneric==0.8.1 six==1.13.0 sklearn==0.0 spacy==2.2.2 srsly==1.0.1 tensorboard==1.14.0 tensorflow==1.14.0 tensorflow-estimator==1.14.0 termcolor==1.1.0 terminado==0.8.3 testpath==0.4.4 thinc==7.3.1 toml==0.10.0 torch==1.2.0 torchvision==0.4.0 tornado==6.0.3 tqdm==4.41.1 traitlets==4.3.3 typed-ast==1.4.0 tzlocal==2.0.0 urllib3==1.25.7 virtualenv==16.7.9 wasabi==0.6.0 wcwidth==0.1.8 webencodings==0.5.1 websocket-client==0.57.0 Werkzeug==0.16.0 wheel==0.33.6 widgetsnbextension==3.5.1 wrapt==1.11.2 zipp==0.6.0 \\nmkdir abc"',
                "input_type": "json",
                "last_modified_by": "mosaic.ai",
                "last_modified_on": "2020-01-28T09:39:54+00:00",
                "metadata_info": None,
                "ml_model_id": "45c7e7db-5674-4878-bd40-59c38a9521f2",
                "model_class": None,
                "model_info": None,
                "object_url": "45c7e7db-5674-4878-bd40-59c38a9521f2/28617a40-64b7-4dfc-a0d1-35eef9f2c558/ml_model.tar.gz",
                "profiling": [],
                "schema": None,
                "status": "active",
                "target_names": None,
                "version_no": 2,
            },
            {
                "created_by": "mosaic.ai",
                "created_on": "2020-01-28T09:37:58+00:00",
                "datasource_name": None,
                "deploy_info": None,
                "deployments": [],
                "id": "4250de43-ea10-4c92-881a-d01907f24b5b",
                "ml_model_id": "45c7e7db-5674-4878-bd40-59c38a9521f2",
            },
        ],
    }


@pytest.fixture(autouse=True)
def deployment_model_dict_deployed_None():
    return {
        "created_by": "mosaic.ai",
        "created_on": "2020-01-28T09:37:58+00:00",
        "deploymentstatus": True,
        "description": "svm classifier using sklearn",
        "flavour": "sklearn",
        "id": "45c7e7db-5674-4878-bd40-59c38a9521f2",
        "last_modified_by": "mosaic.ai",
        "last_modified_on": "2020-01-28T09:37:58+00:00",
        "name": "TestingGiven",
        "project_id": "1",
        "type": "model",
        "versions": [
            {
                "created_by": "mosaic.ai",
                "created_on": "2020-01-28T09:37:58+00:00",
                "datasource_name": None,
                "deploy_info": None,
                "deployments": [],
                "id": "4250de43-ea10-4c92-881a-d01907f24b5b",
                "ml_model_id": "45c7e7db-5674-4878-bd40-59c38a9521f2",
            }
        ],
    }


@pytest.fixture(autouse=True)
def version_dict():
    return {
        "created_by": "10662254",
        "created_on": "2019-08-06T08:58:27.519680+00:00",
        "description": None,
        "id": "63d4ce07-ee31-4c1b-9bb1-52fb0c1901c9",
        "last_modified_by": "10662254",
        "last_modified_on": None,
        "ml_model_id": "c6252ff7-8928-4d43-b433-02fb67f24a3d",
        "object_url": None,
    }


@pytest.fixture(autouse=True)
def score_func():
    @scoring_func
    def score_func1(model, request):
        payload = request.json["payload"]
        data_list = payload
        data_array = numpy.asarray(data_list)
        prediction = model.predict(data_array)
        return prediction.tolist()

    return score_func1


@pytest.fixture(autouse=True)
def model_obj():
    digits = datasets.load_digits()

    clf = svm.SVC(gamma=0.001, C=100.0)
    clf.fit(digits.data[:-1], digits.target[:-1])
    return clf


@pytest.fixture(autouse=True)
def image_obj():
    image = Image.new(mode="RGB", size=(200, 200))
    image.save("/tmp/mosaic.jpg")
    image_object = Image.open("/tmp/mosaic.jpg")
    return image_object


@pytest.fixture(autouse=True)
def req_payload():
    req = requests.Request()
    req.json = {
        "payload": [
            [
                0.0,
                0.0,
                10.0,
                14.0,
                8.0,
                1.0,
                0.0,
                0.0,
                0.0,
                2.0,
                16.0,
                14.0,
                6.0,
                1.0,
                0.0,
                0.0,
                0.0,
                0.0,
                15.0,
                15.0,
                8.0,
                15.0,
                0.0,
                0.0,
                0.0,
                0.0,
                5.0,
                16.0,
                16.0,
                10.0,
                0.0,
                0.0,
                0.0,
                0.0,
                12.0,
                15.0,
                15.0,
                12.0,
                0.0,
                0.0,
                0.0,
                4.0,
                16.0,
                6.0,
                4.0,
                16.0,
                6.0,
                0.0,
                0.0,
                8.0,
                16.0,
                10.0,
                8.0,
                16.0,
                8.0,
                0.0,
                0.0,
                1.0,
                8.0,
                12.0,
                14.0,
                12.0,
                1.0,
                0.0,
            ]
        ]
    }
    return req.json


@pytest.fixture(autouse=True)
def model_ensemble_dict():
    return [
        {
            "model_id": "bbeb53ea-fa18-496b-bb4a-a6bd44b6508b",
            "version_id": "3878ea9e-8617-4b69-831b-2d36238e79d3",
            "name": "breastCancer_ensemble",
            "flavour": "sklearn",
        },
        {
            "model_id": "8a7c7a02-6a58-4e4d-ae93-db9c4c998fe7",
            "version_id": "7a909086-7ec8-4a8c-8efe-76e675852458",
            "name": "sklearn_ensemble",
            "flavour": "sklearn",
        },
    ]
