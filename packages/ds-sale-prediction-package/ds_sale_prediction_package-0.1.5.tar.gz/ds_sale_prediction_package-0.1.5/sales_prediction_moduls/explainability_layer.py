import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap


class ExplainabilityLayer:
    """
    Class for explaining the results of model predictions through various
    plots.

    Attributes:
        - model: Trained scikit-learn model object (e.g., LinearRegression,
        LGBM, XGBoost, CatBoost).
        - model_name: str, Accepted short model name (e.g. lr, lgbm, xgboost,
        catboost)
        - X_val: pd.DataFrame, Validational dataset with features values
        - y_val: pd.Series, True target values of validational dataset
        - y_pred_val: pd.Series, Predicted target values of validational
        dataset
        - val_df_for_analysis: pd.DataFrame, Dataset for analysis containing
        true and predicted values with errors (generated once).

    Methods:
        - create_val_df_for_analysis: Create validational dataset with true and
        predicted target values and errors of predictions.
        - plots_feature_importance: Plots the importance of features in
        selected prediction model.
        - plots_prediction_errors: Plots histogram of prediction errors, and
        scatter plot of true target values vs average predictions for each
        target value
        - plots_prediction_errors_by_feature: Plots the prediction errors
        grouped by a specified feature.
        - shap_summary_plot: Plots a SHAP summary plot showing feature impacts
        on predictions.
        - shap_waterfall_plot: Plots a SHAP waterfall plot for a selected
        prediction.

    Returns:
        - None
    """
    def __init__(self, model, model_name: str,
                 X_val: pd.DataFrame, y_val: pd.Series,
                 y_pred_val: pd.Series):

        self.model = model
        self.model_name = model_name
        self.X_val = X_val
        self.y_val = y_val
        self.y_pred_val = y_pred_val
        self.val_df_for_analysis = None

    def create_val_df_for_analysis(self) -> pd.DataFrame:
        """
        Create validational dataset with true and predicted target values and
        errors of predictions.
        """

        self.val_df_for_analysis = self.X_val
        self.val_df_for_analysis['item_cnt_month_true'] = self.y_val
        self.val_df_for_analysis['item_cnt_month_pred'] = self.y_pred_val
        self.val_df_for_analysis['errors'] = self.y_val - self.y_pred_val
        self.val_df_for_analysis['errors_abs'] = (
            self.val_df_for_analysis['errors'].abs()
        )

        return self.val_df_for_analysis

    def plots_feature_importance(self, figsize: tuple=(7, 10)) -> None:

        """
        Plots the importance of features in selected prediction model.

        Args:
        - figsize : tuple, the size of the figure in inches (width, height). 
        """
        feature_names = self.X_val.columns.to_list()
        importances = self.model.feature_importances_

        sorted_indices = np.argsort(importances)[::-1]
        sorted_features = [feature_names[i] for i in sorted_indices]
        sorted_importances = importances[sorted_indices]

        plt.figure(figsize=figsize)
        plt.barh(sorted_features, sorted_importances, color='#3a4ebf')
        plt.xlabel('Feature Importance')
        plt.ylabel('Feature')
        plt.title('Feature Importance (Sorted)')
        plt.gca().invert_yaxis()  # To keep the most important features on top
        plt.show()

    def plots_prediction_errors(self, figsize: tuple=(13, 3)) -> None:

        """
        Plots histogram of prediction errors, and scatter plot of true target
        values vs average predictions for each target value
        
        Args:
        - figsize : tuple, the size of the figure in inches (width, height). 
        """

        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=figsize)

        axes[0].hist(
            self.val_df_for_analysis['errors'], bins=40, alpha=0.9,
            color='#3a4ebf'
        )
        axes[0].set_xlabel('Error: y_true - y_pred')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('Prediction Error Distribution')

        grouped_data = (
            self.val_df_for_analysis.groupby('item_cnt_month_true')
            ['item_cnt_month_pred'].mean().reset_index()
        )

        sns.regplot(
            x=grouped_data['item_cnt_month_true'],
            y=grouped_data['item_cnt_month_pred'],
            color='#3a4ebf', scatter_kws={'alpha': 0.9}, ax=axes[1]
        )
        axes[1].set_xlabel("True item_cnt_month(Grouped)")
        axes[1].set_ylabel("Mean Predicted item_cnt_month")
        axes[1].set_title("Mean Predicted vs True item_cnt_month")

        plt.show()

    def plots_prediction_errors_by_feature(self, grouping_variable: str,
                                           kind_of_plot: str = 'line',
                                           figsize: tuple=(13, 3)) -> None:
        """
        Plots the prediction errors grouped by a specified feature.

        Args:
        - grouping_variable: str, feature name that used for grouping the data
        - kind_of_plot (line or bar). Default = 'line'
        - figsize : tuple, the size of the figure in inches (width, height). 
        """

        (
            self.val_df_for_analysis
            .groupby(grouping_variable)['errors_abs']
            .mean().plot(kind=kind_of_plot, figsize=figsize,
                         title=f'Error by {grouping_variable}')
        )
        plt.show()

    def shap_summary_plot(self) -> None:

        """
        Plots a SHAP summary plot showing feature impacts on predictions.
        """
        explainer = shap.TreeExplainer(self.model)

        # Calculate SHAP values
        shap_values = explainer.shap_values(
            self.val_df_for_analysis.iloc[:, :-4]
        )

        shap.summary_plot(shap_values, self.val_df_for_analysis.iloc[:, :-4])

    def shap_waterfall_plot(self, row_index: int) -> None:

        """
        Plots a SHAP waterfall plot for a selected prediction.

        Args:
        - row_index: int, id of selected sample
        """

        explainer = shap.TreeExplainer(self.model)

        row_data = self.val_df_for_analysis.iloc[:, :-4].loc[[row_index]]
        row_array = row_data.iloc[0].values

        # Calculate SHAP values
        shap_values = explainer.shap_values(row_data)

        shap.waterfall_plot(shap.Explanation(
            values=shap_values[0],
            base_values=explainer.expected_value,
            data=row_array,
            feature_names=row_data.columns),
            max_display=50)
