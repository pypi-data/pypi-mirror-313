import logging
from typing import Tuple, List
from sklearn.metrics import root_mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.model_selection import TimeSeriesSplit
from lightgbm import early_stopping, log_evaluation
import numpy as np
import pandas as pd

# Setting up logging for the entire file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logging_sales_prediction_kaggle.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()


class ModelValidator:

    """
    Class for validating and training machine learning models using
    time-series cross-validation.

    This class provides functionality to:
        - Split the dataset into training and validation sets based on
        time-series cross-validation with either expanding or sliding windows.
        - Train and evaluate models across multiple folds, calculating RMSE
        for both training and validation sets.
        - Retrain the model on the combined training and validation data, and
        make predictions on the test set.

    Attributes:
        - df: pd.DataFrame - Combined dataset containing both train and test
        data after feature generation.
        - model: The scikit-learn model (e.g., LinearRegression, LGBM, XGBoost,
        CatBoost).
        - model_name: Accepted short model name (e.g. lr, lgbm, xgboost,
        catboost).
        - n_splits: int - The number of splits for the time-series
        cross-validation.
        - test_size: int - The size of each validation set.
        - fill_na: bool - Indicates whether NaN values should be filled
        with -1.
        - validation_type: str - Type of time-series validation ('expanding'
        or 'sliding').
        - last_fold_only: bool, whether to use the last fold only.
        - early_stopping : bool, whether to apply early stopping if supported
        by the model.
        - early_stopping_rounds: num of early_stopping_rounds.
        - cat_features: list of categorical features (for CatBoost and LGBM).

    Methods:
        - get_train_df: Extracts the train set from the combined dataset.
        - get_test_df: Extracts the test set from the combined dataset.
        - get_train_val_indices: Returns indices for train and validation sets
        based on unique periods (e.g., date_block_num).
        - train_and_validate: Performs training and validation across multiple
        folds, tracking RMSE for both train and validation sets.
        - final_training_and_evaluation: Retrains the model on all training
        data and makes predictions for the test set, saving the results in a
        submission file.

    Returns:
        - None
    """

    def __init__(self, df: pd.DataFrame, model, model_name: str,
                 n_splits: int = 3,
                 test_size: int = 1, fill_na: bool = False,
                 validation_type: str = 'expanding',
                 last_fold_only: bool = False,
                 early_stopping: bool = False,
                 early_stopping_rounds: int = None,
                 cat_features=None) -> None:
        """
        df: pd.DataFrame, Combined dataset containing both train and test data
        after feature
        generation.
        model: The scikit-learn model (e.g., LinearRegression, LGBM, XGBoost,
        CatBoost).
        model_name: str, Accepted short model name (e.g. lr, lgbm, xgboost,
        catboost)
        n_splits: The number of splits for the time-series cross-validation.
        fill_na : Indicates whether to fill NaNs: if True, fills NaNs with -1.
        validation_type : Type of time-series validation ('expanding' or
        'sliding').
        last_fold_only: bool, whether to use the last fold only.
        early_stopping : bool, whether to apply early stopping if supported by
        the model.
        early_stopping_rounds: num of early_stopping_rounds.
        cat_features: list of categorical features (for CatBoost and LGBM).
        """
        self.df = df
        self.model = model
        self.model_name = model_name
        self.n_splits = n_splits
        self.test_size = test_size
        self.fill_na = fill_na
        self.validation_type = validation_type
        self.last_fold_only = last_fold_only
        self.early_stopping = early_stopping
        self.early_stopping_rounds = early_stopping_rounds
        self.cat_features = cat_features

    def get_train_df(self) -> pd.DataFrame:
        """Extracts the train set from the combined dataset."""
        train_df = self.df[self.df['set'] == 'train'].drop(columns='set')
        return train_df

    def get_test_df(self) -> pd.DataFrame:
        """Extracts the test set from the combined dataset"""
        test_df = self.df[self.df['set'] == 'test'].drop(columns='set')
        return test_df

    def __get_train_val_indices(self, unique_periods: np.ndarray) -> (
            List[Tuple[np.ndarray, np.ndarray]]):
        """
        Returns indices for the training and validation sets for the selected
        validation type.

        Args:
        - unique_periods : unique values ​​of periods 'date_block_num' from the
        - training dataset (1-34).
        """
        tscv = TimeSeriesSplit(n_splits=self.n_splits,
                               test_size=self.test_size)
        indices = []

        for i, (train_index, val_index) in enumerate(
            tscv.split(unique_periods)
        ):
            if self.validation_type == 'expanding':
                indices.append((train_index, val_index))

            elif self.validation_type == 'sliding':
                # the last n_splits of data are used for validation
                indices.append(
                    (train_index[-(len(train_index)-i):], val_index)
                )

        return indices

    def __train_model(self, X_train: pd.DataFrame, y_train: pd.Series,
                      X_val: pd.DataFrame = None, y_val: pd.Series = None):
        """
        Configure model training parameters based on its name.

        This method prepares the necessary parameters for training the model,
        if we need early stopping, and categorical feature handling. It does
        not directly perform training but sets up all configurations required
        for the `fit` method of the model.

        Args:
        - X_train: pd.DataFrame, training features.
        - y_train: pd.Series, target values for the training set.
        - X_val: pd.DataFrame, validation features. Defaults=None.
        - y_val: pd.Series, target values for the validation set.
        Defaults=None.
        """
        fit_params = {
            'X': X_train,
            'y': y_train,
        }
        if self.early_stopping:
            if 'xgboost' == self.model_name:
                fit_params['eval_set'] = [(X_train, y_train), (X_val, y_val)]
            elif 'lgbm' == self.model_name:
                fit_params['eval_set'] = [(X_train, y_train), (X_val, y_val)]
                fit_params['eval_names'] = ["Train", "Validation"]
                fit_params['eval_metric'] = 'rmse'
                callbacks = []
                callbacks.append(
                    early_stopping(self.early_stopping_rounds, verbose=True)
                )
                callbacks.append(log_evaluation())
                fit_params['callbacks'] = callbacks
            elif 'catboost' == self.model_name:
                fit_params['eval_set'] = [(X_val, y_val)]
                fit_params['early_stopping_rounds'] = (
                    self.early_stopping_rounds
                )
                fit_params['use_best_model'] = True

        if self.cat_features is not None:
            if 'catboost' == self.model_name:
                fit_params['cat_features'] = self.cat_features
            elif 'lgbm' == self.model_name:
                fit_params['categorical_feature'] = self.cat_features

        self.model.fit(**fit_params)

    def train_and_validate(self, train_df: pd.DataFrame,
                           target_col: str) -> Tuple[
                               pd.Series, pd.Series,
                               pd.DataFrame]:
        """
        This method splits the provided dataset into multiple training and
        validation folds based on unique time periods. For each fold the model
        is trained, and predictions are made. The RMSE metric is calculated
        for both the training and validation sets.

        Args:
        - train_df : DataFrame, training dataset which will be split into
        training and validation sets.
        - target_col : str, column name with the target variable.
        """
        unique_periods = train_df['date_block_num'].unique()
        indices = self.__get_train_val_indices(unique_periods)

        # If last_fold_only=True, then use only the last fold
        folds_to_use = [indices[-1]] if self.last_fold_only else indices
        rmses_train, rmses_val = [], []
        y_val_last, y_pred_val_last, X_val_last = None, None, None

        for fold, (train_index, val_index) in enumerate(folds_to_use):

            train_periods = unique_periods[train_index]
            val_periods = unique_periods[val_index]

            train_fold_df = (
                train_df[train_df['date_block_num'].isin(train_periods)]
            )
            val_fold_df = (
                train_df[train_df['date_block_num'].isin(val_periods)]
            )

            # Log train and validation periods
            logger.info(
                f"Fold {fold + 1}: "
                f"Training periods: {train_periods} "
                f"Validation periods: {val_periods}"
            )

            # Splitting X and y
            X_train, y_train = train_fold_df.drop(
                columns=[target_col]
            ), train_fold_df[target_col]

            X_val, y_val = val_fold_df.drop(
                columns=[target_col]
            ), val_fold_df[target_col]

            if self.fill_na:
                X_train = X_train.fillna(-1)
                X_val = X_val.fillna(-1)

            # Log sizes of train and validation sets
            logger.info(
                f"Fold {fold + 1}: Training set size: {len(X_train)}, "
                f"Validation set size: {len(X_val)}"
            )

            # Model training
            self.__train_model(X_train, y_train, X_val, y_val)

            # Making predictions
            y_pred_train = self.model.predict(X_train)
            y_pred_val = self.model.predict(X_val)

            # Calculating RMSE metric
            rmse_train = root_mean_squared_error(y_train, y_pred_train)
            rmses_train.append(rmse_train)

            rmse_val = root_mean_squared_error(y_val, y_pred_val)
            rmses_val.append(rmse_val)

            logger.info(
                f'Fold {fold + 1}: RMSE for train fold: {rmse_train}'
                f'for validation fold: {rmse_val}'
                f' - Model: {self.model_name}'
            )

            # Store predictions and actuals val values
            y_val_last, y_pred_val_last, X_val_last = y_val, y_pred_val, X_val

        if self.last_fold_only == False:
            logger.info(
                f'Average train RMSE across folds: {np.mean(rmses_train)},'
                f'Average val RMSE across folds: {np.mean(rmses_val)}'
                f' - Model: {self.model_name}'
            )

        return y_val_last, y_pred_val_last, X_val_last

    def final_training_and_evaluation(self, train_df: pd.DataFrame,
                                      test_df: pd.DataFrame,
                                      target_col: str) -> pd.DataFrame:

        """
        Perform final training, and generate a submission file.

        This method retrains the model using the combined training and
        validation dataset, calculate RMSE metric for this combined set,
        and makes predictions for the test dataset. The predictions are
        saved to a submission file.

        Args:
        - train_df: pd.DataFrame, combined training and validation dataset.
        - test_df: pd.DataFrame, test dataset.
        - target_col: str, column name with the target variable.
        - submission_path: str, path to the file (CSV) where predictions will
        be saved.
        """

        X_train_val, y_train_val = train_df.drop(
            columns=[target_col]
        ), train_df[target_col]
        X_test = test_df.drop(columns=[target_col])

        if self.fill_na:
            X_train_val = X_train_val.fillna(-1)
            X_test = X_test.fillna(-1)

        # Retraining on the combined set
        self.__train_model(X_train_val, y_train_val)

        # Making predictions
        y_pred_train_val = self.model.predict(X_train_val)

        submission = pd.DataFrame(
            self.model.predict(X_test), columns=['item_cnt_month']
        )
        submission.reset_index(inplace=True)
        submission.columns = ['ID', 'item_cnt_month']
        # submission = self.model.predict(X_test)

        # Calculating RMSE metric
        rmse_train_val = root_mean_squared_error(y_train_val, y_pred_train_val)
        logger.info(f'RMSE for train_val: {rmse_train_val}'
                    f' - Model: {self.model_name}'
                    )

        return submission
