import pandas as pd
from azureml.studio.core.data_frame_schema import DataFrameSchema
from azureml.designer.modules.recommendation.dnn.common.constants import TRANSACTIONS_USER_COL, TRANSACTIONS_ITEM_COL, \
    FEATURES_ID_COL, TRANSACTIONS_RATING_COL
from azureml.designer.modules.recommendation.dnn.common.entry_param import EntryParam
from azureml.studio.core.io.data_frame_directory import load_data_frame_from_directory, DataFrameDirectory
from azureml.studio.core.utils.missing_value_utils import is_na


class Dataset(metaclass=EntryParam):
    def __init__(self, df: pd.DataFrame, column_attributes=None, name: str = None):
        self.df = df
        self.name = name
        if column_attributes is None:
            self.column_attributes = self.build_column_attributes()
        else:
            self.column_attributes = column_attributes

    def get_column_type(self, col_key):
        return self.column_attributes[col_key].column_type

    def get_element_type(self, col_key):
        return self.column_attributes[col_key].element_type

    def build_column_attributes(self):
        self.column_attributes = DataFrameSchema.generate_column_attributes(df=self.df)
        return self.column_attributes

    def is_all_na_column(self, col_key):
        """Determine if a column has all nan values."""
        self._validate_column_key(col_key)
        column = self.get_column(col_key)
        return is_na(column)

    def get_column(self, col_key):
        self._validate_column_key(col_key)
        if isinstance(col_key, str):
            return self.df[col_key]
        return self.df.iloc[:, col_key]

    def _validate_column_key(self, col_key):
        self.column_attributes.validate_key(col_key)

    @property
    def column_size(self):
        return self.df.shape[1]

    @property
    def row_size(self):
        return self.df.shape[0]

    @property
    def columns(self):
        return self.df.columns

    @classmethod
    def load(cls, load_from: str):
        if isinstance(load_from, str):
            dfd = load_data_frame_from_directory(load_from_dir=load_from)
            return cls(df=dfd.data, column_attributes=dfd.schema_instance.column_attributes)
        elif isinstance(load_from, DataFrameDirectory):
            return cls(df=load_from.data, column_attributes=load_from.schema_instance.column_attributes)
        else:
            raise NotImplementedError(f"Cannot load data from {load_from} of type {type(load_from)}")


class TransactionDataset(Dataset):
    """The class describes transactions for recommendation task.

    A valid transaction dataset should have at least two columns, where the first column represents user ids,
    the second column represent item ids, and an optional rating column as the last column."""

    @property
    def users(self):
        if self.column_size - 1 >= TRANSACTIONS_USER_COL:
            return self.df.iloc[:, TRANSACTIONS_USER_COL]
        else:
            return None

    @users.setter
    def users(self, users: pd.Series):
        if self.column_size - 1 >= TRANSACTIONS_USER_COL:
            self.df.iloc[:, TRANSACTIONS_USER_COL] = users
        else:
            self.df[users.name] = users

    @property
    def items(self):
        if self.column_size - 1 >= TRANSACTIONS_ITEM_COL:
            return self.df.iloc[:, TRANSACTIONS_ITEM_COL]
        else:
            return None

    @items.setter
    def items(self, items: pd.Series):
        if self.column_size - 1 >= TRANSACTIONS_ITEM_COL:
            self.df.iloc[:, TRANSACTIONS_ITEM_COL] = items
        else:
            self.df[items.name] = items

    @property
    def ratings(self):
        if self.column_size - 1 >= TRANSACTIONS_RATING_COL:
            return self.df.iloc[:, TRANSACTIONS_RATING_COL]
        else:
            return None

    @ratings.setter
    def ratings(self, ratings: pd.Series):
        if self.column_size - 1 >= TRANSACTIONS_RATING_COL:
            # if data has rating column, then set rating column values with ratings, and ignore ratings name
            self.df.iloc[:, TRANSACTIONS_RATING_COL] = ratings
        else:
            # if data doesn't have rating column, then add a rating column with ratings, as well as its name
            self.df[ratings.name] = ratings


class FeatureDataset(Dataset):
    """The class describes feature dataset for recommendation task.

    The feature column should have at least two columns, where the first column represents user/item ids, and
    the remaining columns represents all features."""

    @property
    def ids(self):
        return self.df.iloc[:, FEATURES_ID_COL]

    @ids.setter
    def ids(self, ids):
        self.df.iloc[:, FEATURES_ID_COL] = ids

    @property
    def features(self):
        return self.df.iloc[:, FEATURES_ID_COL + 1:]
