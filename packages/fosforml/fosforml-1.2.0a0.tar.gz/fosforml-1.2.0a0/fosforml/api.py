# -*- coding: utf-8 -*-
from .model_manager import ModelRegistry
from fosforml.constants import ModelFlavours
from fosforml.utils import generate_model_name, validate_datasets_for_sf, validate_privileges
import sys
import warnings
warnings.filterwarnings("ignore")

def register_model(
    model_obj,
    session,
    name,
    description,
    dataset_name=None,
    dataset_source=None,
    scoring_func=None,
    flavour=None,
    model_type=None,
    snowflake_df=None,
    conda_dependencies=[],
    x_train=None,
    y_train=None,
    x_test=None,
    y_test=None,
    y_pred=None,
    y_prob=None,
    prediction_column=None,
    target_column=None,
    metadata=None,
    source=None,
    connection_configs=None,
    **kwargs
):
    """
    Register model to the Snowflake Model Registry

    Args:
        model_obj (object): The model object to be registered.
        session (snowflake.snowpark.session.Session): The Snowflake session object.
        scoring_func (function): The function to be used for scoring the model.
        name (str): The name of the model.
        description (str): The description of the model.
        snowflake_df (snowflake.snowpark.dataframe.DataFrame): The Snowflake DataFrame object. which should container prediction columns,feature columns and target column.
        flavour (str): The flavour of the model, e.g., keras, pytorch, tensorflow, etc.
        y_true (array, optional): The true labels of the model's predictions. Shape: [n_samples].
        y_pred (array, optional): The predicted labels of the model. Shape: [n_samples].
        prob (array-like, optional): The predicted probabilities of the model. Shape: (n_samples,).
        model_type (str, optional): The type of the model, e.g., classification, regression, etc.
        conda_dependencies (list, optional): The Conda dependencies required by the model.
        x_train (numpy array, optional): The training data of the model with feature columns.
        x_test (numpy array, optional): The test data of the model with feature columns.
        y_train (numpy array, optional): The training data of the model with target column.
        y_test (numpy array, optional): The test data of the model with target column.
        source (str, optional): The source of the Notebook,Experment, e.g., AutoML, etc.
        pretty_output (bool, optional): If True, returns a widget after registration; else, returns a dictionary.
        metadata (dict, optional): Metadata information about the version.

    Keyword Args:
        explicit_x_train (pd.DataFrame or np.ndarray, optional): Explicit x_train clean raw data.
            If provided, the following algorithms will automatically use it for their executions:
            - Know Your Data: explicit_x_train is used for extraction of knowledge. x_train is still used internally.
        explicit_x_test (pd.DataFrame or np.ndarray, optional): Explicit x_test clean raw data.
            If provided, the following algorithms will automatically use it for their executions:
            - Know Your Data: explicit_x_test is used for extraction of knowledge. x_test is still used internally.
        explicit_feature_names (list, optional): Feature names for the explicit provided data.
        source (str, optional): Value will be "automl" if the model is registered from AutoML; else, None.
        model_display (bool, optional): If True, display the model on the model list.

    Returns:
        The response from the model registry.

    Raises:
        ValueError: If the session object is invalid.

    """
    # validate session and privileges
    session_status,session_response = validate_privileges(session)
    if session_status is False:
        return session_response
    connection_configs = {'database': session.get_current_database(),'schema': session.get_current_schema()}
    
    # validate model flavour
    allowed_flavours = ModelFlavours.allowed_flavours()
    if flavour is None:
        return False,f"Model flavour is required, please provide the value of 'flavour' as one of the following: {allowed_flavours}"
    if flavour not in allowed_flavours:
        return False,f"Invalid model flavour, please provide the value of 'flavour' as one of the following: {allowed_flavours}"
    
    # validate model object
    if model_obj is None:
        return False,"Model object is required, please provide the model object to be registered."
    if flavour not in str(type(model_obj)):
        return False,f"Invalid model object, model flavour and model object type mismatch. Expected {flavour} model object."
    
    # validate datasets
    is_invalid_dfs,validation_response = validate_datasets_for_sf(model_obj,name,model_type,flavour,snowflake_df,
                                                       x_train,y_train,x_test,
                                                       y_test,y_pred,y_prob,dataset_name,dataset_source,
                                                       prediction_column)
    if is_invalid_dfs is False:
        return validation_response

    status,model_name = generate_model_name(
        name=name,
        source=source
    )
    if not status:
        return model_name

    # register model
    model_registry = ModelRegistry(session=session,connection_params=connection_configs)
    reg_status,response = model_registry.register_model(
        model=model_obj,
        score=None,
        model_name=model_name,
        dataset_name=dataset_name,
        dataset_source=dataset_source,
        conda_dependencies=conda_dependencies,
        description=description,
        model_flavour=flavour,
        model_type=model_type,
        sf_input_dataframe=snowflake_df,
        x_train=x_train,
        y_train=y_train,
        x_test=x_test,
        y_test=y_test,
        y_pred=y_pred,
        prob=y_prob,
        prediction_column=prediction_column,
        target_column=target_column,
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}",
        source=source,
        metadata=metadata
    )

    return response
