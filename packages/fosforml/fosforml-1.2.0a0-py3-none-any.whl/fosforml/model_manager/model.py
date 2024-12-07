
import pandas as pd
import json
from fosforml.constants import SnowflakeTables
from datetime import datetime
import xgboost as xgb

class ModelObject:
    def __init__(self, model,model_type,snowflake_model=True):
        self.model_type = model_type
        self.model_obj = model
        self.model = model
        self.snowflake_model = snowflake_model
    
    def get_model_artifacts(self, session, snowflake_df, x_test, y_test, x_train, y_train, y_pred, y_prob):
        model_artifacts = {}
        new_model_object = self.get_model_object()
        model_artifacts['model_obj'] = new_model_object
        model_artifacts['hyper_parameters'] = self.get_hyper_parameters(new_model_object)
        model_artifacts['final_df'] = self.get_final_df(session, snowflake_df, x_test, y_test, x_train, y_train, y_pred, y_prob)
        return model_artifacts
    
    def get_hyper_parameters(self,new_model_object):
        if hasattr(new_model_object, 'get_params'):
            hyper_parameters = new_model_object.get_params()
        elif isinstance(new_model_object, xgb.core.Booster):
            hyper_parameters = new_model_object.attributes()
        updated_hp = {key:eval(str(f'"{value}"')) if not value==None else value for (key,value) in hyper_parameters.items()} if hyper_parameters else {}
        return updated_hp

    def get_model_object(self):

        ## To get the model object from pipeline
        if str(type(self.model_obj)).find("pipeline") >= 1 :
            ## returing the last step of the model pipeline
            last_step_index = len(self.model_obj.steps) - 1
            return self.get_model(self.model_obj.steps[last_step_index][1])
        
        return self.get_model(self.model_obj)
    
    def get_model(self,model):
        ## To get the model object snowflake xgboost
        if all([
                str(type(model)).find("snowflake") > 1,
                str(type(model)).find("xgboost") > 1
            ]):
            return model.to_xgboost()
        
        ## ## To get the model object snowflake lightgbm
        elif all([
                str(type(model)).find("snowflake") > 1,
                str(type(model)).find("lightgbm") > 1
            ]):
            return model.to_lightgbm()
                        
        ## To get the model object from default snowflake model
        elif str(type(model)).find("snowflake") > 1 :
            return model.to_sklearn()

        else:
            ## Default model object
            return model


    def get_final_df(self, session, snowflake_df, x_test, y_test, x_train, y_train, y_pred, y_prob):
        if self.snowflake_model:
            return snowflake_df
        else:
            no_rows = x_test.shape[0] ; final_pandas_dataframe = None
            if y_prob is None or self.model_type == "regression":
                final_pandas_dataframe = pd.concat([x_test.reset_index(drop=True).iloc[:no_rows,:],
                                                    y_test.reset_index(drop=True).squeeze(),
                                                    y_pred.reset_index(drop=True).squeeze()
                                                    ],axis=1)
            elif isinstance(y_prob, pd.DataFrame):
                final_pandas_dataframe = pd.concat([x_test.reset_index(drop=True).iloc[:no_rows,:],
                                                    y_test.reset_index(drop=True).squeeze(),
                                                    y_pred.reset_index(drop=True).squeeze(),
                                                    y_prob.reset_index(drop=True).squeeze()
                                                    ],axis=1)

            final_pandas_dataframe_columns = final_pandas_dataframe.columns.to_list()
            return session.create_dataframe(final_pandas_dataframe,schema=final_pandas_dataframe_columns)

    

def is_table_exists(session,MODEL_MONITOR):
    query = f"""
    SHOW TABLES LIKE '{MODEL_MONITOR}';
    """
    result = session.sql(query).collect()
    return len(result) > 0

def create_model_monitor_table(session):
    sf_user = session.get_current_user().replace('"','')
    # sf_user = session.sql(f"SHOW SERVICES LIKE '{service_name}'").collect()[0]['owner']
    MODEL_MONITOR = SnowflakeTables.MODEL_MONITOR_TABLE + sf_user
    if not is_table_exists(session,MODEL_MONITOR):
        '''
        create drift table if not exists
        with OBJECT_ID | PROJECT_ID | MODEL_NAME | VERSION_NAME | OBJECT_TYPE | OBJECT_DATA | CREATED_AT | CREATED_BY
        '''
        query = f"""
            CREATE TABLE IF NOT EXISTS {MODEL_MONITOR} (
                OBJECT_ID STRING PRIMARY KEY DEFAULT UUID_STRING(),
                RUN_ID STRING,
                PROJECT_ID STRING,
                MODEL_NAME STRING,
                VERSION_NAME STRING,
                OBJECT_TYPE STRING,
                OBJECT_DATA VARIANT,
                CREATED_AT TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP(),
                CREATED_BY STRING
            );
        """
        session.sql(query).collect()
        print("created drift table")

def save_build_time_metrics(session,
                            model_details,
                            model_metadata:dict):
    
    ## create table if not exists
    create_model_monitor_table(session)

    sf_user = session.get_current_user().replace('"','')
    # sf_user = session.sql(f"SHOW SERVICES LIKE '{service_name}'").collect()[0]['owner']
    MODEL_MONITOR = SnowflakeTables.MODEL_MONITOR_TABLE + sf_user
    query = f"""
            INSERT INTO {MODEL_MONITOR} 
                (RUN_ID, PROJECT_ID, MODEL_NAME, VERSION_NAME, OBJECT_TYPE, OBJECT_DATA, CREATED_AT, CREATED_BY)
            SELECT 
                '{model_metadata['run_id']}' AS RUN_ID,
                '{model_metadata['project_id']}' AS PROJECT_ID,
                '{model_metadata["model_name"]}' AS MODEL_NAME,
                '{model_metadata["version_name"]}' AS VERSION_NAME,
                '{model_metadata["object_type"]}' AS OBJECT_TYPE,
                parse_json('""" + json.dumps(model_details).replace('\\"','') + f"""') AS OBJECT_DATA,
                '{datetime.now().isoformat()}' AS CREATED_AT,
                '{model_metadata["created_by"]}' AS CREATED_BY;
"""
    ## commiting the query
    session.sql(query).collect()