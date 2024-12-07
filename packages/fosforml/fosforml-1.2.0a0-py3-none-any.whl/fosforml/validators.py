# -*- coding: utf-8 -*-

""" Validators associated with Mosaic-AI-Client """
from .constants import DeployFeasibility
from .utils import get_deployment_data


def check_if_model_is_alredy_deployed(model_data, version_id, strategy="default"):
    """
    Validates if version is already deployed
    :param data:

    """
    for item in model_data["versions"]:
        if item.get("id") == version_id:
            if len(item.get("deployments")) != 0:
                if strategy == "promote":
                    for data in item.get("deployments"):
                        if (
                                data.get("deployment_info").get("deployment_type")
                                != "Default"
                        ):
                            return
                raise Exception(
                    "Version already deployed. Kindly stop that version deployment or try with another version !"
                )


def check_deployment_feasibility(model_data):
    count = 0
    deployments = list()
    for item in model_data["versions"]:
        if len(item.get("deployments")) != 0:
            for data in item.get("deployments"):
                deployments.append(
                    {
                        "deployment_id": data.get("id"),
                        "version_id": data.get("id"),
                        "deployment_type": data.get("deployment_info").get(
                            "deployment_type"
                        ),
                        "cpu_utilization": data.get("deployment_info").get(
                            "cpu_utilization"
                        ),
                        "resource_id": data.get("resource_id"),
                    }
                )
            count = count + 1
    if count == 0:
        return deployments, DeployFeasibility.default
    if count == 1:
        return deployments, DeployFeasibility.apply_strategy
    if count == 2:
        return deployments, DeployFeasibility.no_deploy


def fetch_promotion_key(deployment_type):
    if deployment_type == "AB-Testing":
        return "Confirm-AB"
    if deployment_type == "Canary":
        return "Confirm-Canary"
    if deployment_type == "PreProd":
        return "Confirm-PreProd"


def validate_details_for_deployment(model_data, version_id, strategy="default"):
    if bool(model_data):
        # Check if Model Version is already deployed
        check_if_model_is_alredy_deployed(model_data, version_id, strategy)

        # Check Deployment Feasibility
        deployments, deployment_feasibility = check_deployment_feasibility(model_data)
        if strategy == "apply_strategy":
            # Block to be executed with proper exceptions in case of Applying Strategy
            if deployment_feasibility == DeployFeasibility.apply_strategy:
                deployment_data = get_deployment_data(deployments)
                return deployment_data
            if deployment_feasibility == DeployFeasibility.default:
                raise Exception(
                    "Strategy cannot be applied to this model as there is no Model Version currently in production"
                )
            if deployment_feasibility == DeployFeasibility.no_deploy:
                raise Exception(
                    "Strategy cannot be applied to this model as there are already versions in Production and in Strategy."
                )
        if strategy == "default":
            # Block to be executed with proper exceptions in case of Default Deployment
            if deployment_feasibility == DeployFeasibility.default:
                return "Default"
            if deployment_feasibility == DeployFeasibility.no_deploy:
                raise Exception(
                    "Strategy cannot be applied to this model as there are already versions in Production and in Strategy."
                )
            if deployment_feasibility == DeployFeasibility.apply_strategy:
                raise Exception(
                    "A version is already in Production, kindly try applying a strategy or stop the existing Version and try again"
                )
        if strategy == "promote":
            # Block to be executed with proper exceptions in case of Promoting Models
            if deployment_feasibility == DeployFeasibility.default:
                raise Exception("Unable to promote as no models have been deployed.")
            if deployment_feasibility == DeployFeasibility.apply_strategy:
                raise Exception(
                    "A version in Production, kindly try applying a strategy and then try promoting the version !"
                )
            if deployment_feasibility == DeployFeasibility.no_deploy:
                deployment_data = get_deployment_data(deployments)
                promotion_key = fetch_promotion_key(
                    deployment_data.get("deployment_type")
                )
                deployment_data.update({"promotion_key": promotion_key})
                return deployment_data

    raise Exception(
        "The Model ID provided is invalid. Kindly provide a valid Model ID !"
    )


def stop_model_validations(model_data, version_id):
    if bool(model_data):
        for item in model_data["versions"]:
            if item.get("id") == version_id:
                if len(item.get("deployments")) != 0:
                    for data in item.get("deployments"):
                        deployment_id = data.get("id")
                        return deployment_id
                raise Exception("No deployment found for the specified Version ID.")
        raise Exception(
            "Kindly provide valid Version ID for the deployed models to stop !"
        )
    raise Exception(
        "The Model ID provided is invalid. Kindly provide a valid Model ID !"
    )


def validate_model_id_version_id(model_data, version_id):
    if not bool(model_data):
        raise Exception("The Model ID provided is invalid. Kindly provide a valid Model ID !")
    for item in model_data.get("versions"):
        if item.get("id") == version_id:
            return
    raise Exception("The Version ID provided is invalid. Kindly provide a valid Version ID !")

