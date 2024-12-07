# -*- coding: utf-8 -*-

from typing import Any
import os,requests,json
from fosforml.constants import connection_manager_url, UserConfigs
from snowflake.snowpark import Session
import snowflake

class snowflakesession:
    def __init__(self):
        self.connection_params = {}
        self.session = None
        self._connection_details()

    def _get_login_token(self):
        if os.path.isfile(UserConfigs.token_file):
            with open(UserConfigs.token_file, 'r') as f:
                return f.read()
        return None
    
    def _connection_details(self):
        try:
            if not self.connection_params and os.path.isfile(UserConfigs.token_file) and UserConfigs.connection_details in os.environ :
                connection_info = json.loads(os.environ.get(UserConfigs.connection_details))
                self.connection_params = {
                    'host': os.getenv('SNOWFLAKE_HOST'),
                    'port': os.getenv('SNOWFLAKE_PORT'),
                    'protocol': "https",
                    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
                    'authenticator': "oauth",
                    'token': self._get_login_token(),
                    'warehouse': connection_info.get('warehouse', os.getenv('SNOWFLAKE_WAREHOUSE')),
                    'database': os.getenv('SNOWFLAKE_DATABASE'),
                    'schema': os.getenv('SNOWFLAKE_SCHEMA'),
                    'client_session_keep_alive': True
                }
                ## snowflake session creation                
                connection = snowflake.connector.connect(**self.connection_params)
                self.session = Session.builder.configs({"connection": connection}).create()

            elif not self.connection_params and UserConfigs.connection_details in os.environ :
                connection_info = os.environ.get(UserConfigs.connection_details)
                self.connection_params = json.loads(connection_info.replace("\\", ""))

            elif not self.connection_params and  not "connection_details" in os.environ and not os.environ.get(UserConfigs.experimet_name, None):
                project_id = os.getenv(UserConfigs.project_id)

                if not project_id:
                    raise ValueError(f"{UserConfigs.project_id} not set")
                
                if not connection_manager_url:
                    raise ValueError("CONNECTION_MANAGER_BASE_URL not set")
                
                url = f"{connection_manager_url}/connections/api/ConnectionManager/v1/allConnections?projectId={project_id}"

                connection_details = requests.get(url, verify=False).json()[0]["connectionDetails"]

                region = connection_details['region'] if connection_details["cloudPlatform"] is None \
                                else connection_details['region'] + "." + connection_details["cloudPlatform"]
                
                account = connection_details['accountName'] if region is None \
                    else connection_details['accountName'] + "." + region
                
                self.connection_params = {
                    'account':account,
                    "user": connection_details["dbUserName"],
                    "password": connection_details["dbPassword"],
                    "database": connection_details["defaultDb"],
                    "schema": connection_details["defaultSchema"],
                    "warehouse": connection_details["wareHouse"],
                    "role": connection_details["role"],
                }
            else:
                self.connection_params = {}
                # raise ValueError("Invalid connection details")

        except Exception as e:
            raise Exception(f"Failed to get connection details. {str(e)}")
        
    def get_session(self):
        if not self.session:
            try:
                connection_parameters = self.validate_connection_params(self.connection_params)
                ## snowflake session creation
                self.session = Session.builder.configs(connection_parameters).create()
            except Exception as e:
                print(f"Failed to create snowflake session. {str(e)}")
                return None
            
        return self.session
    
    @staticmethod
    def validate_connection_params(connection_params):
        if not connection_params["account"]:
            raise ValueError("Account name is required")
        if not connection_params["user"]:
            raise ValueError("Username is required")
        if not connection_params["password"]:
            raise ValueError("Password is required")
        if not connection_params["database"]:
            raise ValueError("Database is required")
        if not connection_params["schema"]:
            raise ValueError("Schema is required")
        if not connection_params["warehouse"]: 
            raise ValueError("Warehouse is required")
        if not connection_params["role"]:
            raise ValueError("Role is required")
        
        return connection_params
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if not self.session:
            return self.get_session()
        
        return self.session

    def __enter__(self):
        if not self.session:
            return self.get_session()
        return self.session
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            raise Exception(exc_type, exc_value, traceback)
        
        if self.session:
            self.session.close()

    def execute(self, query):
        pass

    def close(self):
        pass


def get_session():
    try:
        session_obj = snowflakesession()
        return session_obj.get_session()
    except Exception as msg:
        return f"Failed to create snowflake session. {msg}"
    


def get_connection_params():
    try:
        session_obj = snowflakesession()
        return session_obj.connection_params
    except Exception as msg:
        raise Exception(f"Failed to get connection parameters. {msg}")