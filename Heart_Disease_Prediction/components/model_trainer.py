import os
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

from Heart_Disease_Prediction.exception.exception import HeartDiasesException
from Heart_Disease_Prediction.logging.logging import logging
from Heart_Disease_Prediction.entity.config_entity import ModelTrainerConfig
from Heart_Disease_Prediction.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from Heart_Disease_Prediction.utils.main_utils.utils import (
    load_numpy_array_data, save_object,load_object


)
from Heart_Disease_Prediction.utils.main_utils.utils import evaluate_models

from Heart_Disease_Prediction.utils.ml_utils.metric.classification_metric import get_classification_score
from Heart_Disease_Prediction.utils.ml_utils.model.estimator import NetworkModel



class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, model_trainer_config: ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise HeartDiasesException(e, sys)

    def train_model(self, x_train, y_train, x_test, y_test) -> ModelTrainerArtifact:
        try:
            models = {
                "LogisticRegression": LogisticRegression(),
                "RandomForest": RandomForestClassifier(),
                "GradientBoosting": GradientBoostingClassifier(),
                "AdaBoost": AdaBoostClassifier(),
                "DecisionTree": DecisionTreeClassifier()
            }

            params = {
                "LogisticRegression": {
                    "penalty": ['l1', 'l2'],
                    "C": [0.01, 0.1, 1, 10],
                    "solver": ['liblinear'],
                    "max_iter": [100, 200, 500]
                },
                "DecisionTree": {
                    "criterion": ["gini", "entropy"],
                    "max_depth": [3, 5, 10, None],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4]
                },
                "RandomForest": {
                    "n_estimators": [50, 100, 200],
                    "max_depth": [5, 10, None],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4],
                    "bootstrap": [True, False]
                },
                "AdaBoost": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 1.0]
                },
                "GradientBoosting": {
                    "n_estimators": [100, 150, 200],
                    "learning_rate": [0.01, 0.1, 0.2],
                    "max_depth": [3, 5, 7],
                    "subsample": [0.8, 1.0]
                }
            }

            model_report: dict = evaluate_models(
                x_train=x_train,
                y_train=y_train,
                x_test=x_test,
                y_test=y_test,
                models=models,
                params=params
            )

            best_score = max(sorted(model_report.values()))


            best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_score)]
            best_model = models[best_model_name]

            logging.info(f"Best model: {best_model_name} with score {model_report[best_model_name]}")

            # Re-train the best model on full training data
            # best_model.fit(x_train, y_train)

            y_train_pred = best_model.predict(x_train)
            classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)

            y_test_pred = best_model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

            preprocessor = load_object(file_path=self.data_transformation_artifact.data_transformation_object_dir)

            model_dir_path = os.path.dirname(self.model_trainer_config.model_trainer_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
            save_object(self.model_trainer_config.model_trainer_model_file_path, obj=network_model)
            save_object("final_model/model.pkl", best_model)  # Optional

            model_trainer_artifact = ModelTrainerArtifact(
                model_trained_file=self.model_trainer_config.model_trainer_model_file_path,
                    # model_trainer_trained_accurayc:ClassificationMetric
    # model_trainer_tested_accuracy
                model_trainer_trained_accurayc=classification_train_metric,
                model_trainer_tested_accuracy=classification_test_metric
            )

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise HeartDiasesException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.data_transformation_train_file
            test_file_path = self.data_transformation_artifact.data_transformation_test_file

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            logging.info(f"Training arr is :{train_arr.shape}")

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )


            return self.train_model(x_train, y_train, x_test, y_test)

        except Exception as e:
            raise HeartDiasesException(e, sys)
