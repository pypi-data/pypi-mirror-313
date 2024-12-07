# # -*- coding: utf-8 -*-
# import os
# import requests
# import shutil
# from unittest.mock import MagicMock, patch
# from uuid import uuid4

# from matplotlib import figure as matfig
# from mosaic_utils.ai.flavours.r import check_pre_installed_packages, get_r_packages

# from fosforml.api import (
#     add_artifacts,
#     add_model_version,
#     add_version,
#     apply_model_strategy,
#     build_time_metrics,
#     create_artifacts,
#     create_model,
#     create_version,
#     delete_model,
#     deploy_model,
#     ensemble_model_list,
#     generate_schema,
#     get_model_info,
#     get_model_profiling,
#     list_models,
#     load_model,
#     load_train_and_test_data,
#     promote_model,
#     register,
#     register_ensemble_model,
#     register_model,
#     stop_model,
#     store_model_profiling,
#     update_existing_model,
#     update_metadata_info,
#     update_model_details,
#     update_version_details,
#     upload_model,
#     fetch_feedback_accuracy,
#     delete_model_version,
#     create_init_script,
#     download_artifacts
# )
# from fosforml.widgets.register_model import RegisterModel
# from fosforml.widgets.registered_output import ModelDescribe
# from mosaic_utils.ai.decorators import scoring_func
# from fosforml.constants import MLModelFlavours
# from fosforml.utils import create_r_installation
# import sklearn
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn import datasets

# @patch("fosforml.api.get_headers")
# @patch("fosforml.api.register")
# @patch("fosforml.api.describe_model")
# @patch("fosforml.api.shutil.rmtree")
# def test_register_model(
#     mock_rmtree,
#     mock_describe_model,
#     mock_register,
#     mock_headers,
#     model_dict,
#     version_dict,
#     model_obj,
#     score_func,
# ):
#     # mock responses
#     mock_rmtree.return_value = ""
#     mock_describe_model.return_value = model_dict
#     mock_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}

#     # make call
#     name = "Credit_Train"
#     description = "svm classifier using sklearn"
#     flavour = "sklearn"
#     init_script = "mkdir abc"
#     response = register_model(
#         model_obj,
#         score_func,
#         name,
#         description,
#         flavour,
#         init_script=init_script,
#         schema=None,
#         y_true=None,
#         y_pred=None,
#         model_type=None,
#         datasource_name=None,
#         metadata_info=None,
#         tags=["a","b"],
#         input_type="json",
#         x_train=None,
#         y_train=None,
#         x_test=None,
#         y_test=None,
#     )
#     assert mock_register.is_called_once()


# @patch("fosforml.api.get_headers")
# @patch("requests.post")
# @patch("fosforml.api.shutil.rmtree")
# def test_upload_model(
#     mock_rmtree,
#     mock_post,sklearn
#     mock_headers,
#     model_dict,
#     version_dict,
#     model_obj,
#     score_func,
# ):
#     mock_rmtree.return_value = ""
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token dcrtuv887tyg789h-uyg"
#     }
#     mock_post.return_value.status_code = 201
#     _, artifacts_tar = create_artifacts(model_dict["flavour"], model_obj, score_func)
#     upload_model(model_dict, version_dict, artifacts_tar)

#     assert mock_headers.is_called_once()
#     assert mock_post.is_called_once()


# @patch("fosforml.api.get_headers")
# @patch("requests.put")
# @patch("fosforml.api.add_model_version")
# @patch("requests.get")
# @patch("fosforml.api.shutil.rmtree")
# def test_add_version(
#     mock_rmtree,
#     mock_get_describe_model,
#     mock_add_model,
#     mock_post_create_version,
#     mock_headers,
#     model_dict,
#     model_obj,
#     score_func,
# ):
#     mock_rmtree = ""
#     mock_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     mock_post_create_version.return_value.status_code = 201
#     mock_get_describe_model.return_value.json.return_value = model_dict
#     response = add_version(
#         model_dict,
#         model_obj,
#         score_func,
#         schema={"input": {}, "output": {}},
#         init_script="mkdir abc",
#         flavour="sklearn",
#         x_train=None,
#         y_train=None,
#         x_test=None,
#         y_test=None,
#     )

#     assert response["description"] == model_dict["description"]
#     assert mock_add_model.is_called_once()
#     assert mock_post_create_version.is_called_once()
#     assert mock_get_describe_model.is_called_once()

# @patch("requests.post")
# @patch("fosforml.api.get_headers")
# def test_add_artifacts_file(mock_headers, mock_post, image_obj):
#     mock_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     mock_post.return_value.status_code = 201
#     response = add_artifacts(
#         ml_model_id="test_model_1",
#         version_id="v1",
#         tag="Forecasting",
#         image_object=image_obj,
#         artifacts_path="/test"
#     )
#     os.unlink("/tmp/mosaic.jpg")
#     assert mock_post.is_called_once()

# @patch("requests.post")
# @patch("fosforml.api.get_headers")
# def test_add_artifacts(mock_headers, mock_post, image_obj):
#     mock_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     mock_post.return_value.status_code = 201
#     response = add_artifacts(
#         ml_model_id="test_model_1",
#         version_id="v1",
#         tag="Forecasting",
#         image_object=image_obj,
#     )
#     os.unlink("/tmp/mosaic.jpg")
#     assert mock_post.is_called_once()


# @patch("fosforml.api.get_headers")
# @patch("requests.post")
# def test_store_model_profiling(mock_post, mock_headers):
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token dcrtuv887tyg789h-uyg"
#     }
#     mock_post.return_value.status_code = 201
#     response = store_model_profiling("ds_source_system", "v1", "test_model_1", 123)
#     # self.assertEqual(response, 201)
#     return response


# @patch("fosforml.api.get_headers")
# @patch("requests.get")
# def test_get_model_profiling(mock_post, mock_headers):
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token dcrtuv887tyg789h-uyg"
#     }
#     mock_post.return_value.json.return_value = {"column_name": "id"}
#     response = get_model_profiling("ds_source_system", "id", "v2", "test_model")
#     assert response["column_name"] == "id"


# @patch("fosforml.api.get_headers")
# @patch("requests.get")
# def test_list_model(mock_get, mock_headers, model_dict):
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token dcrtuv887tyg789h-uyg"
#     }

#     mock_get.return_value.json.return_value = [model_dict]

#     models = list_models()
#     assert len(models) == 1
#     assert models[0]["flavour"] == "sklearn"


# @patch("fosforml.api.get_headers")
# @patch("requests.delete")
# def test_delete_model(mock_delete, mock_headers, model_dict):
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token dcrtuv887tyg789h-uyg"
#     }
#     mock_delete.return_value.status_code = 204
#     response = delete_model(model_dict["id"])
#     assert response is None


# @patch("fosforml.utils.read_jwt")
# @patch("requests.post")
# def test_deploy_model(mock_deploy, mock_read_jwt):
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     mock_deploy.return_value.json.return_value = {}
#     model_id = str(uuid4())
#     version_id = str(uuid4())
#     resource_id = str(uuid4())
#     deploy_model(model_id, version_id, resource_id)

#     assert mock_read_jwt.is_called_once()
#     assert mock_deploy.is_called_once()


# @patch("fosforml.utils.read_jwt")
# @patch("requests.put")
# def test_apply_model_strategy(mock_deploy, mock_read_jwt):
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     mock_deploy.return_value.json.return_value = {}
#     mock_deploy.return_value.status_code = 201
#     model_id = str(uuid4())
#     version_id = str(uuid4())
#     apply_model_strategy(model_id, version_id, "AB-Testing")
#     assert mock_read_jwt.is_called_once()
#     assert mock_deploy.is_called_once()


# @patch("fosforml.api.get_headers")
# @patch("requests.get")
# @patch("fosforml.api.extract_tar")
# @patch("fosforml.api.get_flavour_handler")
# @patch("fosforml.api.pickle_loads")
# def test_load_model(mock_pkl, mock_model_handler, mock_tar, mock_obj, mock_headers):
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token dcrtuv887tyg789h-uyg"
#     }
#     mock_obj.return_value.content = b"test"
#     mock_tar.return_value = "blank"
#     mock_model_handler.return_value.model_handler = "sklearn"
#     mock_pkl.return_value = "blank"
#     model_id = str(uuid4())
#     version_id = str(uuid4())
#     model = load_model(model_id, version_id)
#     assert mock_obj.is_called_once()
#     return model


# def test_register_model_metadata_exception(model_obj, score_func):
#     # make call
#     name = "Credit_Train"
#     description = "svm classifier using sklearn"
#     flavour = "sklearn"
#     metadata = "wrong definition"
#     try:
#         response = register_model(
#             model_obj, score_func, name, description, flavour, metadata_info=metadata
#         )
#     except Exception as ex:
#         if type(ex) == "TypeError":
#             assert True


# @patch("fosforml.api.get_headers")
# @patch("fosforml.api.describe_model")
# def test_register_model_schema_exception(
#     mock_describe_model, mock_headers, model_obj, score_func
# ):
#     # make call
#     name = "Credit_Train"
#     description = "svm classifier using sklearn"
#     flavour = "sklearn"
#     schema = "wrong definition"
#     try:
#         response = register_model(
#             model_obj, score_func, name, description, flavour, schema
#         )
#     except Exception as ex:
#         if type(ex) == "TypeError":
#             assert True


# def test_check_pre_installed_packages():
#     packages = check_pre_installed_packages(["a"], ["b"], ["1"])
#     assert len(packages) == 1

# @patch("fosforml.api.get_headers")
# @patch("requests.put")
# def test_update_metadata_info(mock_put, mock_headers):
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token dcrtuv887tyg789h-uyg"
#     }
#     mock_put.return_value.status_code = 200
#     response = update_metadata_info("123", "456", {"test": 90})
#     assert response.status_code == 200


# @patch("fosforml.api.get_headers")
# @patch("fosforml.api.describe_model")
# @patch("fosforml.api.register")
# @patch("fosforml.api.create_artifacts")
# @patch("fosforml.api.store_model_profiling")
# def test_validation_expai(
#     mock_store_model_profiling,
#     mock_create_artifacts,
#     mock_register,
#     mock_describe_model,
#     mock_headers,
#     model_dict,
# ):
#     mock_describe_model.return_value = model_dict
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token eyJ0eXAiOiJKV1QiLCJhbGcs5zM1MoLs"
#     }
#     import tempfile

#     temp_dir = tempfile.mkdtemp()
#     mock_create_artifacts.return_value = temp_dir, "tests/test_files/ml_model.tar.gz"
#     name = "Credit_Train"
#     description = "svm classifier using sklearn"
#     flavour = "sklearn"
#     init_script = "mkdir abc"
#     response = register_model(
#         name=name,
#         description=description,
#         flavour=flavour,
#         model_obj="1",
#         scoring_func="1",
#         init_script=init_script,
#         schema=None,
#         y_true=None,
#         y_pred=None,
#         model_type=None,
#         datasource_name=None,
#         metadata_info=None,
#         input_type="json",
#         explain_ai="True",
#         kyd=True,
#     )
#     assert mock_create_artifacts.is_called_once()
#     assert mock_register.is_called_once()

# @patch("fosforml.api.get_headers")
# @patch("requests.put")
# def test_update_model_details(mock_put, mock_headers):
#     model_id = str(uuid4())
#     flavour = "sklearn"
#     mock_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     mock_put.return_value.status_code = 200
#     response = update_model_details(model_id, flavour)
#     assert response == 200


# @patch("fosforml.api.get_headers")
# @patch("requests.put")
# def test_update_version_details(mock_put, mock_headers):
#     model_id = str(uuid4())
#     version_id = str(uuid4())
#     flavour = "sklearn"
#     mock_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     mock_put.return_value.status_code = 200
#     response = update_version_details(model_id, version_id, flavour)
#     assert response == 200


# @patch("fosforml.api.get_headers")
# @patch("fosforml.api.update_model_details")
# @patch("fosforml.api.update_version_details")
# @patch("fosforml.api.upload_model")
# @patch("fosforml.api.describe_model")
# @patch("fosforml.api.shutil.rmtree")
# def test_update_existing_model(
#     mock_rmtree,
#     mock_describe_model,
#     mock_upload_model,
#     mock_update_version_details,
#     mock_update_model_details,
#     mock_headers,
#     model_dict,
#     version_dict,
#     model_obj,
#     score_func,
# ):
#     # mock responses
#     mock_rmtree.return_value = ""
#     mock_update_version_details.return_value.status_code = 200
#     mock_update_model_details.return_value.status_code = 200
#     mock_describe_model.return_value = model_dict
#     mock_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     flavour = "sklearn"
#     init_script = "mkdir abc"
#     response = update_existing_model(
#         model_dict["id"],
#         model_dict["versions"][0]["id"],
#         model_obj,
#         score_func,
#         flavour,
#         init_script=init_script,
#         schema=None,
#         datasource_name=None,
#     )
#     assert mock_upload_model.is_called_once()


# @patch("fosforml.api.get_headers")
# @patch("fosforml.api.describe_model")
# @patch("fosforml.api.add_model_version")
# @patch("fosforml.api.create_artifacts")
# @patch("fosforml.api.store_model_profiling")
# def test_validation_add_version_expai(
#     mock_store_model_profiling,
#     mock_create_artifacts,
#     mock_add_version,
#     mock_describe_model,
#     mock_headers,
#     model_dict,
# ):
#     mock_describe_model.return_value = model_dict
#     mock_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     import tempfile

#     temp_dir = tempfile.mkdtemp()
#     mock_create_artifacts.return_value = temp_dir, "tests/test_files/ml_model.tar.gz"
#     flavour = "sklearn"
#     init_script = "mkdir abc"
#     ml_model = {
#         "description": "svm classifier using sklearn",
#         "flavour": "sklearn",
#         "id": "cd7dacda-2e63-4a9e-b0a0-4a5fc8788a7b",
#         "last_modified_by": "pratiksha.shinde@lntinfotech.com",
#         "last_modified_on": "2020-05-20T14:04:28+00:00",
#         "name": "expai_test",
#         "project_id": "1",
#         "type": "model",
#         "versions": [
#             {
#                 "created_by": "pratiksha.shinde@lntinfotech.com",
#                 "created_on": "2020-05-20T14:04:36+00:00",
#                 "id": "cfd4e887-777a-4bb4-84c3-b11557b19600",
#                 "init_script": init_script,
#                 "input_type": "json",
#                 "last_modified_by": "pratiksha.shinde@lntinfotech.com",
#                 "last_modified_on": "2020-05-20T14:04:39+00:00",
#                 "metadata_info": None,
#                 "ml_model_id": "cd7dacda-2e63-4a9e-b0a0-4a5fc8788a7b",
#             }
#         ],
#     }

#     response = add_version(
#         ml_model=ml_model,
#         flavour=flavour,
#         ml_model_obj="1",
#         scoring_func="1",
#         init_script=init_script,
#         schema=None,
#         y_true=None,
#         y_pred=None,
#         model_type=None,
#         datasource_name=None,
#         metadata_info=None,
#         input_type="json",
#         explain_ai="True",
#     )
#     assert response["flavour"] == "sklearn"
#     assert mock_create_artifacts.is_called_once()
#     assert mock_add_version.is_called_once()


# @patch("fosforml.api.get_headers")
# @patch("requests.post")
# def test_register(mock_post, mock_headers, model_dict):
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token eyJ0eXAiOiJKV1QiLCJhbGcs5zM1MoLs"
#     }
#     mock_post.return_value.status_code = 200
#     mock_post.return_value.json.return_value = model_dict
#     model = register(
#         "Credit_Train",
#         "svm classifier using sklearn",
#         "sklearn",
#         init_script="mkdir abc",
#         model_display=True,
#         source=None,
#         schema=None,
#         datasource_name=None,
#         metadata_info=None,
#         input_type="json",
#         target_names={"target": "quality"},
#         model_class=None,
#         tar_file="tests/test_files/ml_model.tar.gz",
#         tags="user_tag",
#     )
#     assert model["name"] == "Credit_Train"
#     assert mock_post.is_called_once()


# @patch("fosforml.api.get_headers")
# @patch("requests.put")
# def test_add_model(mock_put, mock_headers, model_dict):
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token eyJ0eXAiOiJKV1QiLCJhbGcs5zM1MoLs"
#     }
#     mock_put.return_value.status_code = 200
#     mock_put.return_value.json.return_value = model_dict
#     model_version = add_model_version(
#         model_dict,
#         schema=None,
#         metadata_info=None,
#         init_script="mkdir abc",
#         flavour="sklearn",
#         datasource_name=None,
#         input_type="json",
#         target_names={"target": "quality"},
#         model_class=None,
#         tar_file="tests/test_files/ml_model.tar.gz",
#     )
#     assert model_version["name"] == "Credit_Train"
#     assert mock_put.is_called_once()


# def test_generate_schema(score_func, model_obj, req_payload):
#     import requests

#     req = requests.Request()
#     schema = generate_schema(score_func, (model_obj, req), req_payload)
#     return schema


# @patch("fosforml.api.get_headers")
# @patch("fosforml.api.ensemble_model_list")
# @patch("fosforml.api.register")
# @patch("fosforml.api.describe_model")
# @patch("fosforml.api.create_artifacts")
# def test_register_ensemble_model(
#     mock_artifacts,
#     mock_describe_model,
#     mock_register,
#     mock_get_version,
#     mock_headers,
#     model_dict,
#     model_ensemble_dict,
#     score_func,
# ):
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token eyJ0eXAiOiJKV1QiLCJhbGcs5zM1MoLs"
#     }
#     mock_describe_model.return_value = model_dict
#     mock_artifacts.return_value = ("artifacts_dir", "artifacts_tar")
#     version_list = []
#     mock_get_version.return_value.status_code = 200
#     mock_get_version.return_value.json.return_value = model_ensemble_dict
#     register_ensemble_model(
#         name="TestEnsemble",
#         description="Testing",
#         version_list=version_list,
#         scoring_func=score_func,
#     )
#     assert mock_register.is_called_once()


# @patch("fosforml.api.get_headers")
# @patch("fosforml.api.ensemble_model_list")
# def test_register_ensemble_model_with_exception(
#     mock_get_version, mock_headers, model_dict, model_ensemble_dict, score_func
# ):
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token eyJ0eXAiOiJKV1QiLCJhbGcs5zM1MoLs"
#     }
#     mock_get_version.side_effect = MagicMock(side_effect=Exception)
#     version_list = []
#     mock_get_version.return_value.status_code = 200
#     mock_get_version.return_value.json.return_value = model_ensemble_dict
#     try:
#         response = register_ensemble_model(
#             name="TestEnsemble",
#             description="Testing",
#             version_list=version_list,
#             scoring_func=score_func,
#         )
#     except Exception as ex:
#         assert True


# @patch("fosforml.api.get_headers")
# @patch("fosforml.api.describe_model")
# @patch("fosforml.api.register")
# @patch("fosforml.api.metrics_stats")
# @patch("fosforml.api.store_model_profiling")
# @patch("fosforml.api.missing_param")
# @patch("fosforml.api.shutil.rmtree")
# def test_validation_metrics(
#     mock_rmtree,
#     mock_missing_param,
#     mock_store_model_profiling,
#     mock_metrics_stats,
#     mock_register,
#     mock_describe_model,
#     mock_headers,
#     model_dict,
# ):
#     mock_rmtree.return_value = ""
#     mock_describe_model.return_value = model_dict
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token eyJ0eXAiOiJKV1QiLCJhbGcs5zM1MoLs"
#     }
#     mock_missing_param.return_value = None
#     name = "Credit_Train"
#     description = "svm classifier using sklearn"
#     flavour = "sklearn"
#     init_script = "mkdir abc"
#     response = register_model(
#         name=name,
#         description=description,
#         flavour=flavour,
#         model_obj="1",
#         scoring_func="1",
#         init_script=init_script,
#         schema=None,
#         y_true=None,
#         y_pred=None,
#         model_type="classification",
#         datasource_name=None,
#         metadata_info=None,
#         input_type="json",
#         explain_ai="True",
#     )
#     assert mock_metrics_stats.is_called_once()
#     assert mock_register.is_called_once()


# @patch("fosforml.api.get_headers")
# @patch("requests.post")
# def test_create_model(mock_post, mock_headers, model_dict):
#     # mock responses
#     mock_post.return_value.status_code = 201
#     mock_post.return_value.json.return_value = model_dict
#     mock_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}

#     # make call
#     name = "Credit_Train"
#     description = "svm classifier using sklearn"
#     flavour = "sklearn"
#     tags = "user_tag"
#     response = create_model(name, description, flavour, tags)
#     assert response["flavour"] == "sklearn"


# @patch("fosforml.api.get_headers")
# @patch("requests.post")
# def test_create_version(mock_post, mock_headers, model_dict):
#     # mock responses
#     mock_post.return_value.status_code = 201
#     mock_post.return_value.json.return_value = model_dict
#     mock_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}

#     flavour = "sklearn"
#     init_script = "mkdir abc"

#     import json

#     response = create_version(
#         ml_model=model_dict,
#         schema=test_generate_schema,
#         metadata_info=None,
#         user_init_script=init_script,
#         flavour=flavour,
#         model_class=json.dumps(model_dict),
#     )
#     assert response["flavour"] == "sklearn"


# @patch("fosforml.api.get_headers")
# @patch("requests.get")
# def test_build_time_metrics(mock_get, mock_headers):
#     """
#     This function is used as test case for  build time metrics function
#     :param mock_get:
#     :param mock_headers:
#     :return:
#     """
#     mock_get.return_value.status_code = 201
#     mock_get.return_value.json.return_value = [{"metric_value": {"accuracy": 1.0}}]
#     mock_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     response = build_time_metrics("1", "details_metrics")
#     assert response["accuracy"] == 1.0


# @patch("fosforml.api.get_headers")
# @patch("requests.post")
# def test_build_time_metrics_exception(mock_get, mock_headers):
#     """
#     This function is used as test case for  build time metrics function
#     :param mock_get:
#     :param mock_headers:
#     :return:
#     """
#     mock_get.return_value.status_code = 201
#     mock_get.return_value.json.return_value = [{"metric_value": {"accuracy": 1.0}}]
#     mock_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     response = build_time_metrics("1", "details_metrics")
#     assert response == {}


# @patch("fosforml.api.get_headers")
# @patch("requests.get")
# @patch("fosforml.api.extract_tar")
# @patch("fosforml.api.pickle_loads")
# def test_load_training_and_test_data(mock_pkl, mock_tar, mock_obj, mock_headers):
#     mock_headers.return_value.json.return_value = {
#         "Authorization": "Token dcrtuv887tyg789h-uyg"
#     }
#     mock_obj.return_value.content = b"test"
#     mock_tar.return_value = "blank"
#     mock_pkl.return_value = "blank"
#     model_id = str(uuid4())
#     version_id = str(uuid4())
#     model = load_train_and_test_data(model_id, version_id)
#     assert mock_obj.is_called_once()
#     return model


# @patch("fosforml.api.get_headers")
# @patch("requests.get")
# def test_ensemble_model_list(mock_get, mock_get_headers):
#     """
#     This function is used as test case for ensemble model list function
#     :param mock_get:
#     :param mock_get_headers:
#     :return:
#     """
#     mock_get.return_value.status_code = 200
#     mock_get.return_value.json.return_value = [
#         {
#             "id": 1,
#             "ml_model_id": "1",
#             "name": "value",
#             "flavour": "sklearn",
#             "init_script": "mkdir abc",
#             "description": "value",
#             "version_no": "1",
#         }
#     ]
#     mock_get_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     response = ensemble_model_list(["1"])
#     assert len(response) == 1


# @patch("fosforml.api.describe_model")
# @patch("fosforml.utils.read_jwt")
# @patch("requests.post")
# def test_invalid_model_id(mock_deploy, mock_read_jwt, mock_describe_model):
#     mock_describe_model.return_value = {}
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     mock_deploy.return_value.json.return_value = {}
#     model_id = str(uuid4())
#     version_id = str(uuid4())
#     resource_id = str(uuid4())
#     response = deploy_model(model_id, version_id, resource_id)

#     assert mock_read_jwt.is_called_once()
#     assert mock_deploy.is_called_once()
#     assert (
#         response
#         == "The Model ID provided is invalid. Kindly provide a valid Model ID !"
#     )


# @patch("fosforml.api.describe_model")
# @patch("fosforml.utils.read_jwt")
# @patch("requests.post")
# def test_version_already_deployed(
#     mock_deploy, mock_read_jwt, mock_describe_model, deployment_model_dict_deployed
# ):
#     mock_describe_model.return_value = deployment_model_dict_deployed
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     mock_deploy.return_value.json.return_value = {}
#     model_id = "45c7e7db-5674-4878-bd40-59c38a9521f2"
#     version_id = "28617a40-64b7-4dfc-a0d1-35eef9f2c558"
#     resource_id = "b0d93c79-b4f0-46c0-8a54-e41abbaa5583"
#     response = deploy_model(model_id, version_id, resource_id)

#     assert mock_read_jwt.is_called_once()
#     assert mock_deploy.is_called_once()
#     assert (
#         response
#         == "Version already deployed. Kindly stop that version deployment or try with another version !"
#     )


# @patch("fosforml.api.describe_model")
# @patch("fosforml.utils.read_jwt")
# @patch("requests.post")
# def test_version_already_deployed_apply_strategy(
#     mock_deploy, mock_read_jwt, mock_describe_model, deployment_model_dict_deployed
# ):
#     mock_describe_model.return_value = deployment_model_dict_deployed
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     mock_deploy.return_value.json.return_value = {}
#     model_id = "45c7e7db-5674-4878-bd40-59c38a9521f2"
#     version_id = "28617a40-64b7-4dfc-a0d1-35eef9f2c558"
#     response = apply_model_strategy(model_id, version_id)

#     assert mock_read_jwt.is_called_once()
#     assert mock_deploy.is_called_once()
#     assert (
#         response
#         == "Version already deployed. Kindly stop that version deployment or try with another version !"
#     )


# @patch("fosforml.api.describe_model")
# @patch("fosforml.utils.read_jwt")
# @patch("requests.post")
# def test_version_already_deployed_apply_strategy_VA(
#     mock_deploy, mock_read_jwt, mock_describe_model, deployment_model_dict_deployed_VA
# ):
#     mock_describe_model.return_value = deployment_model_dict_deployed_VA
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     mock_deploy.return_value.json.return_value = {}
#     model_id = "45c7e7db-5674-4878-bd40-59c38a9521f2"
#     version_id = "4250de43-ea10-4c92-881a-d01907f24b5b"
#     response = apply_model_strategy(model_id, version_id)

#     assert mock_read_jwt.is_called_once()
#     assert mock_deploy.is_called_once()


# @patch("fosforml.api.describe_model")
# @patch("fosforml.utils.read_jwt")
# @patch("requests.post")
# def test_version_already_deployed_promote_model(
#     mock_deploy, mock_read_jwt, mock_describe_model, deployment_model_dict_deployed
# ):
#     mock_describe_model.return_value = deployment_model_dict_deployed
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     mock_deploy.return_value.json.return_value = {}
#     model_id = "45c7e7db-5674-4878-bd40-59c38a9521f2"
#     version_id = "4250de43-ea10-4c92-881a-d01907f24b5b"
#     response = promote_model(model_id, version_id)

#     assert mock_read_jwt.is_called_once()
#     assert mock_deploy.is_called_once()


# @patch("fosforml.api.describe_model")
# @patch("fosforml.utils.read_jwt")
# @patch("requests.delete")
# def test_stop_model(
#     mock_delete, mock_read_jwt, mock_describe_model, deployment_model_dict_deployed_VA
# ):
#     mock_describe_model.return_value = deployment_model_dict_deployed_VA
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     model_id = "45c7e7db-5674-4878-bd40-59c38a9521f2"
#     version_id = "28617a40-64b7-4dfc-a0d1-35eef9f2c558"
#     stop_model(model_id, version_id)

#     assert mock_delete.is_called_once()
#     assert mock_read_jwt.is_called_once()


# @patch("fosforml.api.describe_model")
# @patch("fosforml.utils.read_jwt")
# @patch("requests.post")
# def test_version_already_deployed_promote_fail(
#     mock_deploy, mock_read_jwt, mock_describe_model, deployment_model_dict_deployed_None
# ):
#     mock_describe_model.return_value = deployment_model_dict_deployed_None
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     mock_deploy.return_value.json.return_value = {}
#     model_id = "45c7e7db-5674-4878-bd40-59c38a9521f2"
#     version_id = "4250de43-ea10-4c92-881a-d01907f24b5b"
#     response = promote_model(model_id, version_id)

#     assert mock_read_jwt.is_called_once()
#     assert mock_deploy.is_called_once()


# @patch("fosforml.api.describe_model")
# @patch("fosforml.utils.read_jwt")
# @patch("requests.post")
# def test_version_already_deployed_promote_again(
#     mock_deploy, mock_read_jwt, mock_describe_model, deployment_model_dict_deployed
# ):
#     mock_describe_model.return_value = deployment_model_dict_deployed
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     mock_deploy.return_value.json.return_value = {}
#     model_id = "45c7e7db-5674-4878-bd40-59c38a9521f2"
#     version_id = "14250de43-ea10-4c92-881a-d01907f24b5b"
#     response = promote_model(model_id, version_id)

#     assert mock_read_jwt.is_called_once()
#     assert mock_deploy.is_called_once()


# @patch("fosforml.api.describe_model")
# @patch("fosforml.utils.read_jwt")
# @patch("requests.delete")
# def test_stop_model_invalid_model_id(mock_delete, mock_read_jwt, mock_describe_model):
#     mock_describe_model.return_value = {}
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     model_id = "45c7e7db-5674-4878-bd40-59c38a9521f2"
#     version_id = "28617a40-64b7-4dfc-a0d1-35eef9f2c558"
#     stop_model(model_id, version_id)

#     assert mock_delete.is_called_once()
#     assert mock_read_jwt.is_called_once()


# @patch("fosforml.api.describe_model")
# @patch("fosforml.utils.read_jwt")
# @patch("requests.delete")
# def test_stop_model_invalid_version_id(
#     mock_delete, mock_read_jwt, mock_describe_model, deployment_model_dict_deployed_VA
# ):
#     mock_describe_model.return_value = deployment_model_dict_deployed_VA
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     model_id = "45c7e7db-5674-4878-bd40-59c38a9521f2"
#     version_id = "12345"
#     stop_model(model_id, version_id)

#     assert mock_delete.is_called_once()
#     assert mock_read_jwt.is_called_once()


# @patch("fosforml.api.describe_model")
# @patch("fosforml.utils.read_jwt")
# @patch("requests.post")
# def test_version_already_deployed_apply_strategy_fail_default(
#     mock_deploy, mock_read_jwt, mock_describe_model, no_deployments_model_dict
# ):
#     mock_describe_model.return_value = no_deployments_model_dict
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     mock_deploy.return_value.json.return_value = {}
#     model_id = "45c7e7db-5674-4878-bd40-59c38a9521f2"
#     version_id = "28617a40-64b7-4dfc-a0d1-35eef9f2c558"
#     response = deploy_model(model_id, version_id)

#     assert mock_read_jwt.is_called_once()
#     assert mock_deploy.is_called_once()


# @patch("fosforml.api.describe_model")
# @patch("fosforml.utils.read_jwt")
# @patch("requests.post")
# def test_version_already_deployed_apply_strategy_fail_no_deploy(
#     mock_deploy, mock_read_jwt, mock_describe_model, deployment_model_dict_deployed
# ):
#     mock_describe_model.return_value = deployment_model_dict_deployed
#     mock_read_jwt.return_value = "dcrtuv887tyg789h-uyg"
#     mock_deploy.return_value.json.return_value = {}
#     model_id = "45c7e7db-5674-4878-bd40-59c38a9521f2"
#     version_id = "28617a40-64b7-4dfc-a0d1-35eef9f2c558"
#     response = deploy_model(model_id, version_id)

#     assert mock_read_jwt.is_called_once()
#     assert mock_deploy.is_called_once()


# @patch("fosforml.api.get_headers")
# @patch("requests.get")
# def test_get_model_info(mock_get, mock_get_headers):
#     """
#     This function is used as test case for ensemble model list function
#     :param mock_get:
#     :param mock_get_headers:
#     :return:
#     """
#     mock_get.return_value.status_code = 200
#     mock_get.return_value.json.return_value = {
#         "id": "1122",
#         "versions": [
#             {
#                 "id": "1",
#                 "deployments": [{"deployment_info": {"deployment_type": "PreProd"}}],
#             },
#             {"id": "2", "deployments": []},
#             {
#                 "id": "3",
#                 "deployments": [{"deployment_info": {"deployment_type": "Default"}}],
#             },
#         ],
#     }
#     mock_get_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     response = get_model_info(model_name="Test")
#     assert response != {}


# @patch("fosforml.api.get_headers")
# @patch("requests.get")
# def test_fetch_feedback_accuracy(mock_get, mock_get_headers):
#     """
#     This function is used as test case for fetch feedback accuracy function
#     :param mock_get:
#     :param mock_get_headers:
#     :return:
#     """
#     mock_get.return_value.status_code = 200
#     mock_get.return_value.json.return_value = [
#         {"date": "2020-09-04", "feedback_accuracy": 0.25}
#     ]
#     mock_get_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     response = fetch_feedback_accuracy("12345")
#     assert response != []


# @patch("fosforml.api.get_headers")
# @patch("requests.delete")
# @patch("fosforml.api.describe_model")
# def test_fetch_feedback_accuracy(
#     model_describe_model, mock_delete, mock_get_headers, no_deployments_model_dict
# ):
#     """
#     This function is used as test case for deleting model version
#     :param model_describe_model:
#     :param mock_delete:
#     :param mock_get_headers:
#     :param no_deployments_model_dict:
#     :return:
#     """
#     mock_delete.return_value.status_code = 204
#     model_describe_model.return_value = no_deployments_model_dict
#     mock_get_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     response = delete_model_version(
#         "c6252ff7-8928-4d43-b433-02fb67f24a3d", "63d4ce07-ee31-4c1b-9bb1-52fb0c1901c9"
#     )
#     assert mock_delete.is_called_once()
#     assert response == "Version deleted successfully !"


# @patch("fosforml.api.get_headers")
# @patch("requests.delete")
# @patch("fosforml.api.describe_model")
# def test_fetch_feedback_accuracy_fail(
#     model_describe_model, mock_delete, mock_get_headers, no_deployments_model_dict
# ):
#     """
#     This function is used as test case for deleting model version
#     :param model_describe_model:
#     :param mock_delete:
#     :param mock_get_headers:
#     :param no_deployments_model_dict:
#     :return:
#     """
#     mock_delete.return_value.status_code = 500
#     model_describe_model.return_value = no_deployments_model_dict
#     mock_get_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     response = delete_model_version(
#         "c6252ff7-8928-4d43-b433-02fb67f24a3d", "63d4ce07-ee31-4c1b-9bb1-52fb0c1901c9"
#     )
#     assert mock_delete.is_called_once()
#     assert response == "Failed to delete Version ! Kindly try again !"


# @patch("fosforml.api.get_headers")
# @patch("requests.delete")
# @patch("fosforml.api.describe_model")
# def test_fetch_feedback_accuracy_incorrect_model_id(
#     model_describe_model, mock_delete, mock_get_headers, no_deployments_model_dict
# ):
#     """
#     This function is used as test case for deleting model version
#     :param model_describe_model:
#     :param mock_delete:
#     :param mock_get_headers:
#     :param no_deployments_model_dict:
#     :return:
#     """
#     mock_delete.return_value.status_code = 500
#     model_describe_model.return_value = {}
#     mock_get_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     response = delete_model_version(
#         "c6252ff7-8928-4d43-b433-02fb67f24a3d", "63d4ce07-ee31-4c1b-9bb1-52fb0c1901c9"
#     )
#     assert mock_delete.is_called_once()
#     assert (
#         response
#         == "The Model ID provided is invalid. Kindly provide a valid Model ID !"
#     )


# @patch("fosforml.api.get_headers")
# @patch("requests.delete")
# @patch("fosforml.api.describe_model")
# def test_fetch_feedback_accuracy_incorrect_model_id(
#     model_describe_model, mock_delete, mock_get_headers, no_deployments_model_dict
# ):
#     """
#     This function is used as test case for deleting model version
#     :param model_describe_model:
#     :param mock_delete:
#     :param mock_get_headers:
#     :param no_deployments_model_dict:
#     :return:
#     """
#     mock_delete.return_value.status_code = 500
#     model_describe_model.return_value = no_deployments_model_dict
#     mock_get_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     response = delete_model_version(
#         "c6252ff7-8928-4d43-b433-02fb67f24a3d", "63d4ce07-ee31-4c1b-9bb1-52fb0c1901c911"
#     )
#     assert mock_delete.is_called_once()
#     assert (
#         response
#         == "The Version ID provided is invalid. Kindly provide a valid Version ID !"
#     )

# def test_create_r_installation():
#     response = create_r_installation("pip install test_package")
#     assert isinstance(response, str)


# def test_create_init_script():
#     response = create_init_script("mkdir abc", "r")
#     assert isinstance(response, str)

# def test_check_if_model_is_alredy_deployed(deployment_model_dict_deployed):
#     from fosforml.validators import check_if_model_is_alredy_deployed
#     response = check_if_model_is_alredy_deployed(deployment_model_dict_deployed,
#                                                  "4250de43-ea10-4c92-881a-d01907f24b5b",
#                                                  "promote")
#     assert not response

# @patch("fosforml.api.get_headers")
# @patch("requests.post")
# def test_download_artifacts(mock_post,mock_get_headers):
#     mock_post.return_value == 403
#     mock_get_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     tempdir, files_list = download_artifacts()
#     assert not tempdir
#     assert not files_list


# @patch("fosforml.api.get_headers")
# @patch("requests.get")
# def test_fetch_model_resources(mock_get,mock_get_headers):
#     mock_get.status_code = 403
#     mock_get_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     from fosforml.api import fetch_model_resources
#     response = fetch_model_resources()
#     assert response


# def test_widget_model_registration():
#     widget_instance_check = RegisterModel()
#     assert isinstance(widget_instance_check, RegisterModel)
#     assert callable(widget_instance_check.run)
#     widget_instance_check.run()


# @patch("requests.get")
# @patch("requests.post")
# @patch("fosforml.api.metrics_stats")
# @patch("fosforml.api.get_headers")
# @patch("fosforml.api.register")
# @patch("fosforml.api.describe_model")
# def test_widget_model_describe(
#     describe_mocked,
#     mock_register,
#     mock_headers,
#     mock_metrics_stats,
#     mock_post,
#     mock_get,
# ):

#     mock_headers.return_value = {"Authorization": "Token dcrtuv887tyg789h-uyg"}
#     data_ = {
#         "created_by": "shivam.chaurasia@lntinfotech.com",
#         "created_on": "2021-02-04T04:13:34+00:00",
#         "deploymentstatus": False,
#         "description": "iris_classfication_1",
#         "flavour": "sklearn",
#         "id": "b9c6789b-602e-4f4d-8ae7-a29dd2d50baa",
#         "last_modified_by": "shivam.chaurasia@lntinfotech.com",
#         "last_modified_on": "2021-02-04T04:13:34+00:00",
#         "model_display": True,
#         "name": "test",
#         "project_id": "8617bbea-6e50-42c4-a61d-16e2d661d735",
#         "source": "",
#         "tags": None,
#         "type": "model",
#         "versions": [
#             {
#                 "created_by": "shivam.chaurasia@lntinfotech.com",
#                 "created_on": "2021-02-04T04:13:34+00:00",
#                 "datasource_name": "",
#                 "dependent_model": None,
#                 "deploy_info": None,
#                 "deployments": [],
#                 "description": None,
#                 "docker_image_url": "registry.lti-aiq.in:443/mosaic-ai-logistics/mosaic-ai-serving:1.0.0-07122021",
#                 "gpu_docker_image_url": "registry.lti-aiq.in:443/mosaic-ai-logistics/mosaic-ai-serving:gpu-1.0.0-07122021",
#                 "id": "186414ed-215f-4aec-af4e-994205691b43",
#                 "init_script": '"pip install --user absl-py==0.11.0\\n pip install --user alembic==1.4.3"',
#                 "input_type": "json",
#                 "last_modified_by": "shivam.chaurasia@lntinfotech.com",
#                 "last_modified_on": "2021-02-04T04:13:34+00:00",
#                 "metadata_info": None,
#                 "ml_model_id": "b9c6789b-602e-4f4d-8ae7-a29dd2d50baa",
#                 "model_class": {"base_estimator": "estimator"},
#                 "model_info": {
#                     "deep_learning_model": False,
#                     "expai": False,
#                     "feature_type_inferenced": True,
#                     "features_name": [
#                         "sepal length (cm)",
#                         "sepal width (cm)",
#                         "petal length (cm)",
#                         "petal width (cm)",
#                     ],
#                     "features_type": {
#                         "category": [],
#                         "datetime": [],
#                         "excluded": ["actual_truth_values", "predicted_truth_values"],
#                         "num_cat": [],
#                         "numeric": [
#                             "sepal length (cm)",
#                             "petal width (cm)",
#                             "sepal width (cm)",
#                             "petal length (cm)",
#                         ],
#                         "text": [],
#                         "type_undetected": [],
#                     },
#                     "kyd": True,
#                     "mode": "classification",
#                     "number_of_features": 4,
#                     "number_of_targets": 3,
#                     "targets_mapping": {
#                         "mapping_value": None,
#                         "target_names": ["setosa", "versicolor", "virginica"],
#                     },
#                     "temp_dir": "",
#                 },
#                 "object_url": "b9c6789b-602e-4f4d-8ae7-a29dd2d50baa/186414ed-215f-4aec-af4e-994205691b43/ml_model.tar.gz",
#                 "profiling": [],
#                 "schema": {},
#                 "status": "active",
#                 "target_names": {"target": ["setosa", "versicolor", "virginica"]},
#                 "version_no": 1,
#             }
#         ],
#     }
#     describe_mocked.return_value = data_

#     widget_instance_check = ModelDescribe("b9c6789b-602e-4f4d-8ae7-a29dd2d50baa")
#     assert isinstance(widget_instance_check, ModelDescribe)
#     assert callable(widget_instance_check.view)
#     widget_instance_check.view(load_data=False, use_data=data_)
#     widget_instance_check.model_info_dashboard(None)
#     widget_instance_check.model_class_dashboard("Test")
#     widget_instance_check.deploy_info_dashboard(
#         {"deploy_info": "Test", "deployments": []}
#     )


