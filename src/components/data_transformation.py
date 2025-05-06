import sys
import numpy as np 
import pandas as pd 
import os

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging
from src.utils import save_obj

class DataTransformationConfig():
    preprocessor_obj_file_path=os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_obj(self): #Responsible for Data Transformation
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns =[
                "gender",
                "race_ethnicity",
                "lunch",
                "parental_level_of_education",
                "test_preparation_course",
            ]

            num_pipeline = Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler(with_mean=False))
                ]
            )

            cat_pipeline = Pipeline(
                    steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("ohe", OneHotEncoder(handle_unknown='ignore'))  # No scaler here (optional)
                        ]
            )

            logging.info("Standard Scaling for Numerical values Complete")

            logging.info("Categorical Columns encoding Complete")

            preprocessor= ColumnTransformer(
                [
                    ("num_pipelines", num_pipeline, numerical_columns),
                    ("cat_pipelines", cat_pipeline, categorical_columns)
                ]
            )
            
            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read Train and Test Data Complete")

            logging.info("Obtaining Preprocessing Object")

            preprocessing_obj = self.get_data_transformer_obj()

            target_col_name = "math_score"
            numerical_columns =  ["writing_score", "reading_score"]

            input_feature_train = train_df.drop(columns=[target_col_name], axis=1)
            target_feature_train = train_df[target_col_name]

            
            input_feature_test = test_df.drop(columns=[target_col_name], axis=1)
            target_feature_test = test_df[target_col_name]

            logging.info(
                f"Applying Preprocessing Object on Training and Testing data"

            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train)]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test)]

            logging.info(f"Saved Preprocessing Object.")

            save_obj(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj= preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e, sys)

