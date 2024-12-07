from snowflake.ml.dataset import Dataset
import pandas as pd
import snowflake,json

class DatasetManager:
    def __init__(self,
                 model_name,
                 version_name,
                 session,
                 connection_params
                ):
        self.model_name = model_name
        self.version_name = version_name
        self.connection_params = connection_params
        self.datasets_obj = self.get_or_create_dataset_object(model_name,version_name,session)
    
    def get_or_create_dataset_object(self,model_name,version_name,session):
        datasets_obj = Dataset(session=session,
                                database=self.connection_params['database'],
                                schema =self.connection_params['schema'],
                                name=f"{model_name}_{version_name}"
                                )
        try:
            datasets_obj.create(session=session,name=f"{model_name}_{version_name}")
        except Exception as e:
            datasets_obj.load(session=session,name=f"{model_name}_{version_name}")
        
        return datasets_obj
    
    def upload_datasets(self,session,datasets: dict):
        try:
            existings_versions = self.datasets_obj.list_versions()
            if len(existings_versions) > 0:
                for version_name in existings_versions:
                    self.datasets_obj.delete_version(version_name=version_name)
            
            datasets = {k:v for k,v in datasets.items() if v is not None}

            for dataset_name, dataset in datasets.items():
                snowpark_dataset = self.get_snowpark_dataset(session,dataset)
                purpose = self.get_dataset_purpose(dataset_name)
                self.datasets_obj.create_version(version=dataset_name,
                                                 input_dataframe=snowpark_dataset,
                                                 comment=json.dumps(
                                                            {
                                                                "purpose": purpose,
                                                                "dataset_type": "Table"
                                                            }
                                                        ))
                
            return True,f"Successfully uploaded {self.model_name} datasets."
        except Exception as e:
            return False,f"model dataset upload failed, error: {str(e)}"
        
    def remove_datasets(self):
        try:
            self.datasets_obj.delete()
            return True,f"Successfully removed {self.model_name} datasets."
        except Exception as e:
            raise Exception(e)
    
    def read_dataset(self,dataset_name,to_pandas=True):
        try:
            if to_pandas:
                return self.datasets_obj.select_version(version=dataset_name).read.to_pandas()
            return self.datasets_obj.select_version(version=dataset_name).read.to_snowpark_dataframe()
        except Exception as e:
            raise Exception(f"Failed to get dataset {dataset_name}. {str(e)}")
    
    def list_datasets(self):
        try:
            return self.datasets_obj.list_versions()
        except Exception as e:
            raise Exception(f"Failed to list datasets. {str(e)}")
    
    @staticmethod
    def get_dataset_purpose(dataset_name):
        if "x_train" in dataset_name.lower():
            return "Training"
        elif "y_train" in dataset_name.lower():
            return "Training"
        elif "x_test" in dataset_name.lower():
            return "Inference"
        elif "y_test" in dataset_name.lower():
            return "Inference"
        elif "y_pred" in dataset_name.lower():
            return "Validation"
        elif "prob" in dataset_name.lower():
            return "Validation"
        else:
            return "Training"        
        
    def get_snowpark_dataset(self,session,dataset):
        if isinstance(dataset,snowflake.snowpark.dataframe.DataFrame):
            return dataset
        elif isinstance(dataset,pd.DataFrame):
            return session.create_dataframe(dataset)
        
        elif isinstance(dataset,pd.Series):
            return session.create_dataframe(dataset.to_frame())
        else:
            raise Exception("Invalid dataset type to save .")  

class Metadata:
    def __init__(self, model_registry):
        self.model_registry = model_registry

    def update_model_registry(self,
                              model_name,
                              model_description,
                              model_tags,
                              session
                              ):
        try:
            model = self.model_registry.get_model(model_name=model_name)
            model.description = model_description
            self.set_model_tags(session,
                                model,
                                model_name,
                                tags=model_tags)
            
            return f"Updated model metadata for {model_name}."
        except Exception as e:
            print(f"error:{str(e)}")
            return False

    def set_model_tags(self,
                       session,
                       model,
                       model_name,
                       tags={}):
        try:
            for tag_name,tag_value in tags.items():
                session.sql(f"create tag if not exists {tag_name}").collect()
                model.set_tag(
                            tag_name = tag_name,
                            tag_value = tag_value
                            )
        except Exception as e:
            print(f"Failed to set tags for model {model_name}.")
            print(e)
            # pass
            # raise Exception(f"Failed to set tags for model {model_name}")
        

    

