import tensorflow as tf
import pandas as pd
from abc import abstractmethod
from azureml.designer.modules.recommendation.dnn.common.dataset import TransactionDataset
from azureml.designer.modules.recommendation.dnn.common.feature_builder import FeatureBuilder
from azureml.designer.modules.recommendation.dnn.common.constants import RANDOM_SEED
from azureml.studio.core.logger import common_logger


class InputFunctionBuilder:
    def __init__(self,
                 transactions: TransactionDataset,
                 user_feature_builder: FeatureBuilder,
                 item_feature_builder: FeatureBuilder,
                 batch_size,
                 epochs,
                 random_seed=RANDOM_SEED):
        self.transactions = transactions
        self.batch_size = batch_size
        self.epochs = epochs
        self.random_seed = random_seed

        self._init_features_lookup(user_feature_builder=user_feature_builder, item_feature_builder=item_feature_builder)

    def _init_features_lookup(self, user_feature_builder, item_feature_builder):
        self.user_features_lookup = user_feature_builder.build_feature_lookup(ids=self.transactions.users)
        self.item_features_lookup = item_feature_builder.build_feature_lookup(ids=self.transactions.items)

    @abstractmethod
    def get_input_fn(self):
        pass


class TrainInputFunctionBuilder(InputFunctionBuilder):
    def __init__(self,
                 transactions: TransactionDataset,
                 user_feature_builder: FeatureBuilder,
                 item_feature_builder: FeatureBuilder,
                 batch_size,
                 epochs,
                 shuffle,
                 random_seed=RANDOM_SEED):
        common_logger.debug("Init train input function builder.")
        super().__init__(transactions, user_feature_builder, item_feature_builder, batch_size, epochs, random_seed)
        if shuffle:
            self.transactions = TransactionDataset(
                df=self.transactions.df.sample(frac=1.0, random_state=self.random_seed))

    def get_input_fn(self):
        if self.transactions.row_size == 0:
            common_logger.debug("No valid samples found, return none input function.")
            return None

        user_ids = self.transactions.users
        item_ids = self.transactions.items
        ratings = self.transactions.ratings

        users = self.user_features_lookup.loc[user_ids].reset_index(drop=True)
        items = self.item_features_lookup.loc[item_ids].reset_index(drop=True)
        x_df = pd.concat([users, items], axis=1)
        y_sr = ratings.reset_index(drop=True)

        return tf.compat.v1.estimator.inputs.pandas_input_fn(x=x_df,
                                                             y=y_sr,
                                                             batch_size=self.batch_size,
                                                             num_epochs=self.epochs,
                                                             shuffle=False)


class RatingPredictionInputFunctionBuilder(InputFunctionBuilder):
    def __init__(self,
                 transactions: TransactionDataset,
                 user_feature_builder: FeatureBuilder,
                 item_feature_builder: FeatureBuilder,
                 batch_size,
                 random_seed=RANDOM_SEED):
        common_logger.debug("Init rating prediction function builder.")
        super().__init__(transactions, user_feature_builder, item_feature_builder, batch_size, 1, random_seed)

    def get_input_fn(self):
        if self.transactions.row_size == 0:
            common_logger.debug("No valid samples found, return none input function.")
            return None

        user_ids = self.transactions.users
        item_ids = self.transactions.items

        users = self.user_features_lookup.loc[user_ids].reset_index(drop=True)
        items = self.item_features_lookup.loc[item_ids].reset_index(drop=True)
        x_df = pd.concat([users, items], axis=1)

        return tf.compat.v1.estimator.inputs.pandas_input_fn(x=x_df,
                                                             y=None,
                                                             batch_size=self.batch_size,
                                                             num_epochs=self.epochs,
                                                             shuffle=False)


class RecommendationInputFunctionBuilder(InputFunctionBuilder):
    def __init__(self,
                 transactions: TransactionDataset,
                 user_feature_builder: FeatureBuilder,
                 item_feature_builder: FeatureBuilder,
                 batch_size,
                 random_seed=RANDOM_SEED):
        common_logger.debug("Init recommendation input function builder.")
        super().__init__(transactions, user_feature_builder, item_feature_builder, batch_size, 1, random_seed)
        self.user_ids = self.transactions.users.unique()
        self.item_vocab = self.item_features_lookup.index.values

    def _init_features_lookup(self, user_feature_builder, item_feature_builder):
        self.user_features_lookup = user_feature_builder.build_feature_lookup(ids=self.transactions.users)
        self.item_features_lookup = item_feature_builder.build_feature_lookup(ids=item_feature_builder.dynamic_id_vocab)

    def get_input_fn(self):
        if self.transactions.row_size == 0:
            common_logger.debug("No valid samples found, return none input function.")
            return None

        return lambda: self._dataset(self.user_features_lookup, self.item_features_lookup, self.user_ids,
                                     self.batch_size)

    @staticmethod
    def _dataset(user_features_lookup, item_features_lookup, user_ids, batch_size):
        users = user_features_lookup.loc[user_ids]
        users_dataset = tf.data.Dataset.from_tensor_slices(users.to_dict("list"))
        items_dataset = tf.data.Dataset.from_tensor_slices(item_features_lookup.to_dict("list"))

        item_num = len(item_features_lookup)
        users_dataset = users_dataset.interleave(lambda x: tf.data.Dataset.from_tensors(x).repeat(item_num),
                                                 cycle_length=1, block_length=item_num)

        user_num = len(user_ids)
        items_dataset = items_dataset.repeat(user_num)

        dataset = (tf.data.Dataset.zip((users_dataset, items_dataset)).
                   flat_map(lambda user, item: tf.data.Dataset.from_tensors({**user, **item})))
        dataset = dataset.batch(batch_size * item_num).prefetch(tf.data.experimental.AUTOTUNE)

        return dataset
