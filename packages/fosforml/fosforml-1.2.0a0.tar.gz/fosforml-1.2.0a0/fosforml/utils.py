import os,re
from .exceptions import ConfigError
from .constants import Headers, Client
from .constants import ModelFlavours
import snowflake
import pandas as pd

def generate_model_name(name,source):
    """
    Get model name from the given name
    Experiment Models --- Experiment_<project id(please replace '-' with '_'>_FDC_<experiment_name>
    NOtebooks Models ---  Model_<project id(please replace '-' with '_'>_FDC_<model_name>
    """

    projectID = os.getenv("PROJECT_ID").upper().replace("-","_")

    if name is None:
        return False, "Model name is required"
    
    if not source or source.upper() == "NOTEBOOK":
        return True,f"MODEL_{projectID}_FDC_{name.upper()}"
    
    if source.upper() == "EXPERIMENT":
        from fosforml.constants import UserConfigs
        if UserConfigs.run_id in os.environ or UserConfigs.run_id.upper() in os.environ:
            run_id = os.getenv(UserConfigs.run_id, os.getenv(UserConfigs.run_id.upper()))
            return True, f"EXPERIMENT_{projectID}_FDC_{name.upper()}_{run_id}"
        else:
            print("RUN_ID is not found in environment variables")
            return False, f"EXPERIMENT_{projectID}_FDC_{name.upper()}"
    
    return False, "Invalid source, please enter the value of 'source' as 'notebook' or 'experiment'"

def get_sf_dataset_columns_names(model_obj):
    """
    Get feature columns, target column and prediction columns for snowflake dataframes using snowflake model object
    """

    temp_model = model_obj.steps[0][1] if str(type(model_obj)).find("pipeline") >= 1 else model_obj
    feature_names = temp_model.input_cols
    target_name = temp_model.label_cols
    prediction_column = temp_model.output_cols
    
    return feature_names, target_name, prediction_column

def read_jwt():
    config_file = os.path.expanduser(Client.config_file)
    if os.path.exists(config_file):
        with open(config_file) as f:
            jwt = f.read().strip("\n")
        return jwt
    elif os.getenv("TOKEN"):
        jwt = os.getenv("TOKEN")
        return jwt
    raise ConfigError


def get_headers():
    jwt = read_jwt()
    return {
        Headers.authorization: f"Token {jwt}",
        Headers.x_project_id: os.environ.get("PROJECT_ID"),
    }


def validate_dataset(dataset):
    if dataset is not None and not isinstance(dataset, (pd.DataFrame, pd.Series, snowflake.snowpark.dataframe.DataFrame)):
        raise ValueError("Dataset must be a DataFrame or Series")

def validate_column_names(df):
    pattern = r'^("[^"]*"|[A-Za-z_][A-Za-z_\d$]*)$'
    if isinstance(df,snowflake.snowpark.dataframe.DataFrame):
        for col in df.columns:
            if not re.match(pattern, col):
                raise ValueError(f"Column name '{col}' is invalid. Column names must start with a letter or underscore and contain only letters, numbers, underscores and $ signs.")
            
    elif isinstance(df, pd.DataFrame):
        for col in df.columns.to_list():
            if not re.match(pattern, col):
                raise ValueError(f"Column name '{col}' is invalid. Column names must start with a letter or underscore and contain only letters, numbers, underscores and $ signs.")
        
    elif isinstance(df,pd.Series):
        if not re.match(pattern, df.name):
            raise ValueError(f"Column name '{df.name}' is invalid. Column names must start with a letter or underscore and contain only letters, numbers, underscores and $ signs.")
    
    else:
        raise ValueError(f"Input must be a DataFrame or Series")

def validate_connection_configs(connection_configs):
    if connection_configs and not isinstance(connection_configs, dict):
        raise ValueError("Connection configs must be a dictionary")

def validate_model_name(name):
    pattern = r'^[A-Za-z_][A-Za-z_\d$]*$'
    if not re.match(pattern, name):
        raise ValueError(f"Model name '{name}' is invalid. Model names must start with a letter or underscore and contain only letters, numbers, underscores and $ signs.")
    
def validate_datasets_for_sf(model_obj,name,model_type,flavour, snowflake_df, x_train, y_train, 
                             x_test, y_test, y_pred, prob, dataset_name, dataset_source,prediction_column):
        
    try:
        if not name:
            raise ValueError("Model name is required, please provide the value for 'name'")
        
        validate_model_name(name)

        if not model_type:
            raise ValueError("Model type is required, please provide the value for 'model_type' as 'classification' or 'regression'")
        
        if not dataset_name:
            raise ValueError("Dataset name is required, please provide the value for 'dataset_name'")
        
        if not dataset_source:
            raise ValueError("Dataset source is required, please provide the value for 'dataset_source'")
    
        if flavour == ModelFlavours.snowflake_model_flavour:
            if snowflake_df is None:
                raise ValueError("snowflake dataframe is required for flavour 'snowflake' with prediction columns,feature columns and target column")
            if not isinstance(snowflake_df, snowflake.snowpark.dataframe.DataFrame):
                raise ValueError("input dataframe must be a snowflake DataFrame")
            
            validate_column_names(snowflake_df)
            feature_names, target_name, prediction_col  = get_sf_dataset_columns_names(model_obj)
            
            if not set(feature_names).issubset(snowflake_df.columns):
                raise ValueError(f"Feature columns {feature_names} not found in snowflake dataframe")
            
            if not set(target_name).issubset(snowflake_df.columns):
                raise ValueError(f"Target column {target_name} not found in snowflake dataframe")
            
            if not prediction_col and prediction_column is None:
                raise ValueError("Prediction column is required for snowflake model, please provide the value for 'prediction_column'")
            
            if prediction_col and not set(prediction_col).issubset(snowflake_df.columns):
                raise ValueError(f"Prediction column {prediction_col} not found in snowflake dataframe")
            
            return True, "Snowflake Model datasets are validated successfully."

        else:
            if x_train is None or not isinstance(x_train, (pd.DataFrame)):
                raise ValueError("please provide 'x_train' as a pandas dataFrame")
            validate_column_names(x_train)

            if y_train is None or not isinstance(y_train, (pd.DataFrame, pd.Series)):
                raise ValueError("please provide 'y_train' as a pandas dataframe or series")
            validate_column_names(y_train)

            if x_test is None or not isinstance(x_test, (pd.DataFrame)):
                raise ValueError("please provide 'x_test' as a pandas dataFrame")
            validate_column_names(x_test)

            if y_test is None or not isinstance(y_test, (pd.DataFrame, pd.Series)):
                raise ValueError("please provide 'y_test' as a pandas dataframe or series")
            validate_column_names(y_test)

            if y_pred is None or not isinstance(y_pred, (pd.DataFrame, pd.Series)):
                raise ValueError("please provide 'y_pred' as a pandas dataframe or series")
            validate_y_pred(y_pred, y_test, y_train, model_type)
            validate_column_names(y_pred)

            if prob is not None and not isinstance(prob, (pd.DataFrame)):
                raise ValueError("please provide 'prob' as a pandas dataframe class probabilities for each class ")
            
            if prob is not None:
                validate_column_names(prob)
            
            return True, "Sklearn Model datasets are validated successfully."
        
    except Exception as e:
        return False,f"error, invalid inputs : {repr(e)}"


def get_clean_col(col):
    '''
    Get the column name without quotes
    '''
    match_string = re.match(r"(['\"]+)(.*)\1", col)
    if match_string:
        return match_string.group(2)
    return col

def load_model_artifacts(session,
                        model_type, 
                        model_obj,
                        snowflake_model=True,
                        snowflake_df=None,
                        x_test=None,
                        y_test=None,
                        x_train=None,
                        y_train=None,
                        y_pred=None,
                        y_prob=None,
                         ):
    """
    Load the model object from given snowflake model object
    """
    from fosforml.model_manager import ModelObject
    model_instance = ModelObject(model_obj,
                                model_type,
                                snowflake_model)
    return model_instance.get_model_artifacts(
            session=session,
            snowflake_df=snowflake_df,
            x_test=x_test,
            y_test=y_test,
            x_train=x_train,
            y_train=y_train,
            y_pred=y_pred,
            y_prob=y_prob
        )

def validate_privileges(session):
    if not session or not isinstance(session,snowflake.snowpark.session.Session):
        return False,"Invalid session object."
    database = session.get_current_database().replace('"','')
    schema = session.get_current_schema().replace('"','')
    role = session.get_current_role().replace('"','')
    validation_query = '''select privilege_type
                          from {0}.information_schema.object_privileges
                          where object_type = 'SCHEMA' and object_name = '{1}' and grantee = '{2}';'''.format(database,
                                                                                                              schema,
                                                                                                              role)
    out = session.sql(validation_query).to_pandas()
    prvilege_set = set(out['PRIVILEGE_TYPE'])
    ownner_set = {'OWNERSHIP'}
    valid_set = {'CREATE MODEL','CREATE STAGE','CREATE DATASET','USAGE','CREATE PROCEDURE','CREATE FUNCTION'}
    if ownner_set.issubset(prvilege_set):
        return True, "User has owner privileges to create model in snowflake"
    elif valid_set.issubset(prvilege_set):
        return True, "User has required privileges to create model in snowflake"
    else:
        return False, "User does not have required privileges to create model in snowflake"
    

def validate_y_pred(y_pred, y_test, y_train, model_type):
    try:
        y_test, y_pred, y_train = [
            data.squeeze() if isinstance(data, pd.DataFrame) else data
            for data in [y_test, y_pred, y_train]
        ]
        if not all(isinstance(y, pd.Series) for y in [y_test, y_pred, y_train]):
            raise AttributeError
        if model_type.lower() == "classification":
            y_test_unique = set(y_test.unique())
            y_pred_unique = set(y_pred.unique())
            y_train_unique = set(y_train.unique())
            is_subset = y_pred_unique.issubset(y_train_unique.union(y_test_unique))
            if not is_subset:
                raise ValueError("y_pred contains values that are not present in y_test or y_train")
    except AttributeError:
        raise ValueError("y_pred, y_test and y_train must be pandas series or single column dataframe")