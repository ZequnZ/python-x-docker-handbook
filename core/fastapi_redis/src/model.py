import json
import os
from datetime import datetime

import numpy as np
import pandas as pd
from joblib import dump, load
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

from data import session_data_preprocessing, venue_data_preprocessing


def metrics_computation(
    label: pd.Series, prediction: np.ndarray, probability: np.ndarray
) -> tuple[float, float, float, float]:
    """Compute the evaluation metrics of the model

    Args:
        label (pd.Series): label of the test set
        prediction (np.ndarray): Predicted class
        probability (np.ndarray): Predicted probability

    Returns:
        tuple[float, float, float, float]: roc_auc, precision, recall, f1
    """
    roc_auc = roc_auc_score(label, probability)
    precision = precision_score(label, prediction)
    recall = recall_score(label, prediction)
    f1 = f1_score(label, prediction)
    return roc_auc, precision, recall, f1


class Model:
    def __init__(self):
        self.model_version: str = "1.0"
        self.model: LogisticRegression = LogisticRegression()

    def model_loading(self, model_directory: str) -> None:
        """Load the model artifact from given directory

        Args:
            model_directory (str): model artifact directory
        """
        self.model = load(os.path.join("registry", model_directory, "model.joblib"))

    def model_training(self, session_data_path: str, venue_data_path: str):
        """Train the model using given session and venue data

        Args:
            session_data_path (str): path of the session data file
            venue_data_path (str): path of the venue data file
        """
        # Obtain dataset
        dataset = self.feature_preprocessing(session_data_path, venue_data_path)

        # Split the dataset into training and validation set
        # -> 70% training, 30% validation
        trn, val = train_test_split(
            dataset, stratify=dataset["purchased"], test_size=0.3, random_state=42
        )
        # Obtain labels
        trn_label, val_label = trn.pop("purchased"), val.pop("purchased")

        # Model training
        self.model = LogisticRegression()
        self.model.fit(trn, trn_label)

        # Getting evaluation metric from training and validation set
        trn_pred = self.model.predict(trn)
        trn_prob = self.model.predict_proba(trn)[:, 1]
        trn_metrics = metrics_computation(trn_label, trn_pred, trn_prob)

        val_pred = self.model.predict(val)
        val_prob = self.model.predict_proba(val)[:, 1]
        val_metrics = metrics_computation(val_label, val_pred, val_prob)

        # String of current date & time: used as postfix
        postfix = datetime.now().strftime("%d%m%y_%H%M%S")

        # Create a folder to save model artifact and metrics
        self.model_saving_path = f"registry/model_{self.model_version}_{postfix}"
        os.mkdir(self.model_saving_path)

        # Training & validation set should be saved as well in work
        # Save model artifact
        dump(self.model, os.path.join(self.model_saving_path, "model.joblib"))
        # Save model evaluation metrics
        self.save_model_metrics(postfix, trn_metrics, val_metrics)

    def save_model_metrics(
        self,
        postfix: str,
        trn_metrics: tuple[float, float, float, float],
        val_metrics: tuple[float, float, float, float],
    ) -> None:
        """Save the evaluation metrics into a json file

        Args:
            postfix (str): postfix of the model: representing the timestamp
            trn_metrics (tuple[float, float, float, float]):
                evaluation metrics of the training set
            val_metrics (tuple[float, float, float, float]):
                evaluation metrics of the validation set
        """
        model_metrics_json = {
            "Model_version": self.model_version,
            "Model postfix": postfix,
            "Metrics on training set": {
                "roc-auc": trn_metrics[0],
                "precision": trn_metrics[1],
                "recall": trn_metrics[2],
                "f1": trn_metrics[3],
            },
            "Metrics on validation set": {
                "roc-auc": val_metrics[0],
                "precision": val_metrics[1],
                "recall": val_metrics[2],
                "f1": val_metrics[3],
            },
        }

        # Save the metrics into a json file
        with open(
            os.path.join(self.model_saving_path, "model_metrics.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(model_metrics_json, f, ensure_ascii=False, indent=4)

    def model_prediction(self, test_data: pd.DataFrame) -> list[float]:
        """Run the model on given test data and return the probability

        Args:
            test_data (pd.DataFrame): test data contains feature columns only

        Returns:
            list[float]: predicted probability from the model
        """
        return self.model.predict_proba(test_data)[:, 1].tolist()

    def feature_preprocessing(
        self, session_data_path: str, venue_data_path: str
    ) -> pd.DataFrame:
        """Preprocess the session and venue data and return a dataset for model training

        Args:
            session_data_path (str): path of the session data file
            venue_data_path (str): path of the venue data file

        Returns:
            pd.DataFrame: dataset contains feature columns only for model training
        """
        # Load data into dataframe
        session_df = pd.read_csv(session_data_path)
        venue_df = pd.read_csv(venue_data_path)

        session_df = session_data_preprocessing(session_df)
        venue_df = venue_data_preprocessing(venue_df)

        # Merge data from session and venue, based on venue_id
        dataset = pd.merge(session_df, venue_df, how="left", on="venue_id")
        dataset.reset_index(drop=True, inplace=True)

        # Drop columns that won't be used as features for model training
        dataset.drop(
            [
                "session_id",
                "has_seen_venue_in_this_session",
                "position_in_list",
                "venue_id",
            ],
            axis=1,
            inplace=True,
        )

        return dataset


if __name__ == "__main__":
    m = Model()
    m.model_training(os.getenv("SESSION_DATA_PATH"), os.getenv("VENUE_DATA_PATH"))
