import pandas as pd
import numpy as np
from itertools import product
pd.set_option('display.max_columns', 300)


class DataPreparation:
    """
    Class to prepare a combined dataset including both train and test data.

    This class provides functionality to:
        - Processes training data after DQL and EDA steps. It includes target
        value clipping, dataset expansion using a Cartesian product, and base
        feature selection.
        - Processes test data by assigning the `date_block_num` value equal 34
        and merges it
        with the preprocessed train data.
        - Optimizes data types based on feature values to reduce memory usage.

    Attributes:
        - train_df: pd.DataFrame - train data after DQL and EDA steps
        - test_df: pd.DataFrame - initial test data

    Methods:
        - preprocess_train_data - Prepares a training dataset, adds missing
        combinations of stores and products.
        - combine_data - Combines the training and test datasets into one
        common DataFrame
        - optimize_dtypes - Optimizes data types to save memory
        - prepare - Runs all stages of data preparation.

    Returns:
        - combined_df: pd.DataFrame
    """

    def __init__(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> None:
        self.train_df = train_df
        self.test_df = test_df
        self.combined_df = None

    def __preprocess_train_data(self) -> None:
        """
        Prepares a training dataset, adds missing combinations of stores
        and products.
        """

        self.train_df['item_cnt_month'] = np.clip(
            self.train_df['item_cnt_month'], None, 22
        )

        self.train_df['item_price_log'] = np.log1p(self.train_df['item_price'])
        self.train_df['item_revenue_log'] = np.log1p(self.train_df['revenue'])

        # Generate a Cartesian product of date_block_num, shop_id, item_id
        monthly_train_df_full = []
        for date_block in self.train_df['date_block_num'].unique():
            shops = (
                self.train_df
                .loc[self.train_df['date_block_num'] == date_block, 'shop_id']
                .unique()
            )
            items = (
                self.train_df
                .loc[self.train_df['date_block_num'] == date_block, 'item_id']
                .unique()
            )
            monthly_train_df_full.append(
                np.array(list(product([date_block], shops, items)))
            )

        idx_features = ['date_block_num', 'shop_id', 'item_id']
        self.train_full_df = pd.DataFrame(
            np.vstack(monthly_train_df_full), columns=idx_features
        )

        # Connect with basic features and existing values
        base_features = (
            self.train_df[['date_block_num', 'shop_id',
                           'item_id', 'item_price', 'item_price_log',
                           'item_cnt_month', 'transactions_cnt_month',
                           'item_revenue_log']]
        )

        self.train_full_df = (
            self.train_full_df
            .merge(base_features, on=idx_features, how='left')
        )
        self.train_full_df['item_cnt_month'] = (
            self.train_full_df['item_cnt_month'].fillna(0)
        )

    def __combine_data(self) -> None:
        """Combines the training and test datasets into one common DataFrame"""

        self.test_df['date_block_num'] = 34
        self.train_full_df['set'] = 'train'
        self.test_df['set'] = 'test'

        self.combined_df = pd.concat(
            [self.train_full_df, self.test_df], sort=False
        ).reset_index(drop=True)

    def __optimize_dtypes(self) -> None:
        """Optimizes data types to save memory."""

        self.combined_df['date_block_num'] = (
            self.combined_df['date_block_num'].astype('int8')
        )
        self.combined_df['shop_id'] = (
            self.combined_df['shop_id'].astype('int8')
        )
        self.combined_df['item_id'] = (
            self.combined_df['item_id'].astype('int16')
            )
        self.combined_df['item_price'] = (
            self.combined_df['item_price'].astype('float32')
        )
        self.combined_df['item_price_log'] = (
            self.combined_df['item_price_log'].astype('float32')
        )
        self.combined_df['item_cnt_month'] = (
            self.combined_df['item_cnt_month'].astype('float32')
        )
        self.combined_df['transactions_cnt_month'] = (
            self.combined_df['transactions_cnt_month'].astype('float32')
        )
        self.combined_df['item_revenue_log'] = (
            self.combined_df['item_revenue_log'].astype('float32')
        )

    def prepare(self) -> pd.DataFrame:
        """Runs all stages of data preparation."""

        self.__preprocess_train_data()
        self.__combine_data()
        self.__optimize_dtypes()
        return self.combined_df
