import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder


class FeatureExtractor:
    """
    Class to generate features to a combined dataset.

    This class generates a variety of features to enhance model performance,
    including:
        - descriptive features: (e.g. item_category_id, city, shop_type,
        shop_cluster_umap, shop_cluster_pca)
        from dict based on csv files (items, and train dataset after EDA)
        - One-hot encoded features (item_category_id).
        - TF-IDF encoded features (shop_type).
        - Binary features (e.g. is_moscow, is_december)
        - Time-based features (e.g., months_since_last_sale,
        months_since_first_sale).
        - Lag features, including lagged item_cnt_month and item_price

    Attributes:
        - combined_df: pd.DataFrame - train data and test data
        - df_for_mapping: pd.DataFrame - dataset after EDA

    Methods:
        - add_category_features: Adds item_category_id to combined_df from
        dict based on csv file (items.csv).
        - add_city_and_shop_features: Adds city, shop_type, shop_cluster_umap,
        shop_cluster_pca from.
        dict based on csv file (train dataset after EDA).
        - add_tfidf_encoding: Adds TF-IDF encoding for a given column(for
        item_category_name_short).
        - add_one_hot_encoding: Adds One Hot Encoding for a given column (for
        shop_type).
        - add_binary_features: Adds binary features such as 'is_moscow'.
        - add_months_since_last_sale: Adds the 'months_since_last_sale'
        feature.
        - add_months_since_first_sale: Adds the 'months_since_first_sale'
        feature.
        - add_months_since_shop_first_sale: Adds the
        'months_since_shop_first_sale' feature.
        - add_lagged_features_and_growth_rates: Adds lagged features and
        growth rates for the specified target column.
        - add_agg_lagged_features: Adds lagged features for specified
        aggregated features over given lag periods.
        - add_rolling_lagged_features: Adds lagged features with rolling
        average


    Returns:
        - combined_df: pd.DataFrame - combined df with new features
    """

    def __init__(self, combined_df: pd.DataFrame, items: pd.DataFrame,
                 df_for_mapping: pd.DataFrame) -> None:

        self.combined_df = combined_df
        self.items = items
        self.df_for_mapping = df_for_mapping

    def _add_category_features(self) -> None:
        """
        Adds item_category_id to combined_df from dict based on csv file
        (items.csv)
        """

        item_category_mapping = (
            self.items.set_index('item_id')['item_category_id'].to_dict()
        )

        self.combined_df['item_category_id'] = (
            self.combined_df['item_id'].map(item_category_mapping)
            .astype('int8')
        )

    def _add_city_and_shop_features(self) -> None:
        """
        Adds city, shop_type, shop_cluster_umap, shop_cluster_pca from
        dict based on csv file (train dataset after EDA)
        """

        features_for_mapping = ['city', 'shop_type', 'shop_cluster_umap',
                                'shop_cluster_pca']
        for i in features_for_mapping:
            mapping = self.df_for_mapping.set_index('shop_id')[i].to_dict()
            self.combined_df[f'{i}'] = self.combined_df['shop_id'].map(mapping)
            if self.combined_df[f'{i}'].dtype == 'int64':
                self.combined_df[f'{i}'] = (
                    self.combined_df[f'{i}'].astype('int8')
                )

        mapping = (
            self.df_for_mapping
            .set_index('item_category_id')['item_category_name_short']
            .to_dict()
        )

        self.combined_df['item_category_name_short'] = (
            self.combined_df['item_category_id']
            .map(mapping)
        )

    def _add_tfidf_encoding(self, column: str) -> None:
        """
        Adds TF-IDF encoding for a given column (for item_category_name_short).
        """

        # Apply TF-IDF encoding
        vectorizer = TfidfVectorizer()
        encoded = pd.DataFrame(
            vectorizer.fit_transform(self.combined_df[column]).toarray(),
            columns=[
                f"tfidf_{col}" for col in vectorizer.get_feature_names_out()
                ]
        ).astype('float16')

        # Add encoded columns to combined_df
        self.combined_df = pd.concat(
            [self.combined_df.reset_index(drop=True), encoded], axis=1
        )

    def _add_one_hot_encoding(self, column: str) -> None:
        """Adds One Hot Encoding for a given column (for shop_type)."""

        # Apply OneHot encoding
        ohe_encoder = OneHotEncoder(sparse_output=False)
        ohe_encoded = pd.DataFrame(
            ohe_encoder.fit_transform(self.combined_df[[column]]),
            columns=[
                f"ohe_{col.lower()}" for col in ohe_encoder.categories_[0]
                ]
            ).astype('int8')

        # Updating indexes and add encoded columns to combined_df
        ohe_encoded.index = self.combined_df.index
        self.combined_df = pd.concat(
            [self.combined_df, ohe_encoded], axis=1
        )

    def _add_months_since_last_sale(self) -> None:
        """Adds 'months_since_last_sale' feature."""

        self.combined_df['sale_period'] = np.where(
            self.combined_df['item_cnt_month'] > 0,
            self.combined_df['date_block_num'], np.nan
        )

        self.combined_df['sale_period'] = (
            self.combined_df
            .groupby(['shop_id', 'item_id'])['sale_period']
            .ffill()
            .astype('float32')
        )

        self.combined_df['previous_sale_period'] = (
            self.combined_df
            .groupby(['shop_id', 'item_id'])['sale_period']
            .shift(1)
        )

        self.combined_df['months_since_last_sale'] = (
            self.combined_df['date_block_num'] -
            self.combined_df['previous_sale_period']
        )

        # Remove auxiliary column
        self.combined_df = self.combined_df.drop(
            columns=['sale_period', 'previous_sale_period']
        )

    def _add_months_since_first_sale(self) -> None:
        """Adds the 'months_since_first_sale' feature."""

        # find the minimum (first) period when item was sold
        self.combined_df['global_item_first_sale_date'] = (
            self.combined_df[self.combined_df['item_cnt_month'] > 0]
            .groupby('item_id')['date_block_num'].transform('min')
        )

        self.combined_df['global_item_first_sale_date'] = (
            self.combined_df
            .groupby(['item_id'])['global_item_first_sale_date']
            .ffill().astype('float32')
        )

        self.combined_df['global_item_first_sale_date'] = (
            self.combined_df
            .groupby(['item_id'])['global_item_first_sale_date']
            .bfill().astype('float32')
        )        

        self.combined_df['months_since_first_sale'] = (
            self.combined_df['date_block_num'] -
            self.combined_df['global_item_first_sale_date']
        )

        # Remove auxiliary column
        self.combined_df = self.combined_df.drop(
            columns=['global_item_first_sale_date']
        )

    def _add_months_since_shop_first_sale(self) -> None:
        """Adds the 'months_since_shop_first_sale' feature."""

        # find the first period when the first sale was made in the store
        self.combined_df['global_shop_first_sale_date'] = (
            self.combined_df[self.combined_df['item_cnt_month'] > 0]
            .groupby('shop_id')['date_block_num'].transform('min')
        )

        self.combined_df['global_shop_first_sale_date'] = (
            self.combined_df.groupby('shop_id')['global_shop_first_sale_date']
            .ffill().bfill().astype('float32')
        )

        self.combined_df['months_since_shop_first_sale'] = (
            self.combined_df['date_block_num'] -
            self.combined_df['global_shop_first_sale_date']
        )

        # Remove auxiliary column
        self.combined_df = self.combined_df.drop(
            columns=['global_shop_first_sale_date']
        )

    def _add_lagged_features_and_growth_rates(self, target_column: str,
                                              lag_periods: list[int] =
                                              [1, 3, 12]) -> None:
        """
        Adds lagged features and growth rates for the specified target column.
        target_column: Name of the column for which need to calculate lagged
        features.
        lag_periods: List of lag periods to calculate.
        """

        # Calculate lag values
        for lag in lag_periods:
            # Creating a copy with an incremental period
            df_lagged = self.combined_df[
                ['date_block_num', 'shop_id', 'item_id'] + [target_column]
            ].copy()
            df_lagged['date_block_num'] += lag

            # Merging a dataset with a lagged variable
            self.combined_df = self.combined_df.merge(
                df_lagged,
                on=['date_block_num', 'shop_id', 'item_id'],
                how='left',
                suffixes=('', f'_lag_{lag}')
            )

            lagged_target_column = f'{target_column}_lag_{lag}'

            # Calculating a growth rate
            if lag == lag_periods[0]:
                # Relative change of feature
                relative_change_name = f'{target_column}_growth_rate'
                self.combined_df[relative_change_name] = (
                    (self.combined_df[target_column] -
                    self.combined_df[lagged_target_column]) /
                    self.combined_df[lagged_target_column]
                )

                # Replace inf values with 1 in the relative change column
                self.combined_df[relative_change_name] = (
                    self.combined_df[relative_change_name].replace(
                        [np.inf, -np.inf], 1
                    )
                )

                df_lagged = self.combined_df[
                    ['date_block_num', 'shop_id', 'item_id'] +
                    [relative_change_name]
                ].copy()
                df_lagged['date_block_num'] += lag

                self.combined_df = self.combined_df.merge(
                    df_lagged,
                    on=['date_block_num', 'shop_id', 'item_id'],
                    how='left',
                    suffixes=('', f'_lag_{lag}')
                )            

                # Remove auxiliary column
                self.combined_df = self.combined_df.drop(
                    columns=[relative_change_name]
                )

    def _add_agg_lagged_features(self, group_columns: list[str],
                                 target_column: str,
                                 lag_periods: list[int] = [1, 3, 12]) -> None:
        """
        Adds lagged features for specified aggregated features over given lag
        periods.
        group_columns: List of columns to group by (e.g., ['item_id']).
        target_column: Column to aggregate (e.g., 'item_cnt_month').
        lag_periods: List of lag periods to apply. Default is [1, 3, 12].
        """

        # Сalculate the average values
        agg_feature_name = f'avg_{target_column}_by_' + '_'.join(group_columns)
        avg_feature = (
            self.combined_df
            .groupby(['date_block_num'] + group_columns)[target_column].mean()
            .reset_index().rename(columns={target_column: agg_feature_name})
        )

        self.combined_df = (self.combined_df.merge(
            avg_feature, on=['date_block_num'] + group_columns, how='left')
        )

        # Calculate lag values
        for lag in lag_periods:
            # Creating a copy with an incremental period
            df_lagged = self.combined_df[
                ['date_block_num', 'shop_id', 'item_id'] +
                [agg_feature_name]
            ].copy()
            df_lagged['date_block_num'] += lag

            # Merging a dataset with a lagged variable
            self.combined_df = self.combined_df.merge(
                df_lagged,
                on=['date_block_num', 'shop_id', 'item_id'],
                how='left',
                suffixes=('', f'_lag_{lag}')
            )

        # Remove auxiliary column
        self.combined_df = self.combined_df.drop(columns=[agg_feature_name])

    def _add_rolling_lagged_features(self,
                                     target_column: str, window: int = 3,
                                     min_periods: int = 1) -> None:
        """
        Adds lagged features with rolling average.
        target column: Column to calculate rolling average (e.g.,
        'item_cnt_month').
        window: size of rolling window.
        min_periods: start period to calculate rolling values.
        """

        # Сalculate the rolling average values
        rolling_avg_name = f'rolling_{target_column}_w{window}'
        self.combined_df[rolling_avg_name] = (
            self.combined_df
            .groupby(['shop_id', 'item_id'])[target_column]
            .transform(lambda x: x.rolling(
                window=window, min_periods=min_periods).mean()
            )
            .astype('float32')
        )

        # Creating a copy with an incremental period
        df_lagged = self.combined_df[
            ['date_block_num', 'shop_id', 'item_id'] +
            [rolling_avg_name]
        ].copy()
        df_lagged['date_block_num'] += 1

        # Merging a dataset with a lagged variable
        self.combined_df = self.combined_df.merge(
            df_lagged,
            on=['date_block_num', 'shop_id', 'item_id'],
            how='left',
            suffixes=('', f'_lag_{1}')
        )

        # Remove auxiliary column
        self.combined_df = self.combined_df.drop(columns=[rolling_avg_name])

    def _add_binary_features(self) -> None:
        """Adds binary features such as 'is_moscow'."""

        self.combined_df['is_moscow'] = (
            self.combined_df['city']
            .apply(lambda x: 1 if x == 'Москва' else 0)
            .astype('int8')
        )

        # self.combined_df = self.combined_df.drop(columns='city')

    def transform(self) -> pd.DataFrame:
        """Runs all stages of adding features"""

        self._add_category_features()
        self._add_city_and_shop_features()
        self._add_tfidf_encoding('item_category_name_short')
        self._add_one_hot_encoding('shop_type')
        self._add_binary_features()
        self._add_months_since_last_sale()
        self._add_months_since_first_sale()
        self._add_months_since_shop_first_sale()

        self._add_lagged_features_and_growth_rates(
            target_column='item_cnt_month', lag_periods=[1, 3, 12]
        )
        self._add_lagged_features_and_growth_rates(
            target_column='transactions_cnt_month', lag_periods=[1, 3, 12]
        )
        self._add_lagged_features_and_growth_rates(
            target_column='item_revenue_log', lag_periods=[1, 3, 12]
        )
        self._add_lagged_features_and_growth_rates(
            target_column='item_price_log', lag_periods=[1]
        )
        self._add_agg_lagged_features(
            group_columns=['shop_id', 'item_category_id'],
            target_column='item_cnt_month',
            lag_periods=[1, 3, 12]
        )
        self._add_agg_lagged_features(
            group_columns=['city', 'item_id'],
            target_column='item_cnt_month',
            lag_periods=[1, 3, 12]
        )
        self._add_agg_lagged_features(
            group_columns=['item_id'],
            target_column='item_cnt_month',
            lag_periods=[1, 3, 12]
        )

        self._add_agg_lagged_features(
            group_columns=['shop_id', 'item_category_id'],
            target_column='item_price_log',
            lag_periods=[1]
        )

        self._add_rolling_lagged_features(
            target_column='item_cnt_month',
            window=3, min_periods=1

        )

        return self.combined_df
