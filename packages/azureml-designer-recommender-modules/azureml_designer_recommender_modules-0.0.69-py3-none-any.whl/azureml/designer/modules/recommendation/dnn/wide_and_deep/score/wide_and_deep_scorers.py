import numpy as np
import pandas as pd
from abc import abstractmethod
from azureml.studio.core.logger import TimeProfile, module_logger
from tensorflow.keras.preprocessing.sequence import pad_sequences
from azureml.studio.internal.error import ErrorMapping, DuplicateFeatureDefinitionError, NullOrEmptyError
from azureml.designer.modules.recommendation.dnn.common.dataset import TransactionDataset, FeatureDataset
from azureml.designer.modules.recommendation.dnn.wide_and_deep.common.wide_n_deep_model import WideNDeepModel
from azureml.designer.modules.recommendation.dnn.common.constants import TRANSACTIONS_RATING_COL
from azureml.designer.modules.recommendation.dnn.wide_and_deep.common.preprocess import preprocess_features, \
    preprocess_transactions
from azureml.designer.modules.recommendation.dnn.common.score_column_names import USER_COLUMN, ITEM_COLUMN, \
    SCORED_RATING, build_ranking_column_names, build_rated_ranking_column_names
from azureml.designer.modules.recommendation.dnn.wide_and_deep.common.input_function_builder import \
    RatingPredictionInputFunctionBuilder, RecommendationInputFunctionBuilder


class BaseWideNDeepScorer:
    input_function_builder_class = None

    def __init__(self,
                 learner: WideNDeepModel,
                 test_transactions: TransactionDataset,
                 training_transactions: TransactionDataset,
                 user_features: FeatureDataset,
                 item_features: FeatureDataset,
                 max_recommended_item_count,
                 min_recommendation_pool_size,
                 return_ratings,
                 batch_size=None):
        self.learner = learner
        self.test_transactions = test_transactions
        self.training_transactions = training_transactions
        self.user_features = user_features
        self.item_features = item_features
        self.max_recommended_item_count = max_recommended_item_count
        self.min_recommendation_pool_size = min_recommendation_pool_size
        self.return_ratings = return_ratings

        self._validate_dataset()
        self._preprocess_dataset()

        self.batch_size = batch_size if batch_size else self.learner.hyper_params.batch_size
        self.learner.update_feature_builders(user_features=self.user_features, item_features=self.item_features)
        self.input_function_builder = self.input_function_builder_class(self.test_transactions,
                                                                        self.learner.user_feature_builder,
                                                                        self.learner.item_feature_builder,
                                                                        self.batch_size,
                                                                        self.learner.random_seed)

    def _validate_dataset(self):
        ErrorMapping.verify_not_null_or_empty(x=self.learner, name=WideNDeepModel.MODEL_NAME)
        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=self.test_transactions.row_size,
                                                                    required_row_count=1,
                                                                    arg_name=self.test_transactions.name)
        self._validate_feature_dataset(self.user_features)
        self._validate_feature_dataset(self.item_features)

    def _preprocess_dataset(self):
        self.test_transactions = preprocess_transactions(self.test_transactions)
        self.user_features = preprocess_features(self.user_features) if self.user_features is not None else None
        self.item_features = preprocess_features(self.item_features) if self.item_features is not None else None
        self.training_transactions = (
            preprocess_transactions(self.training_transactions) if self.training_transactions is not None else None
        )

        self._validate_duplicated_features_dataset(self.user_features)
        self._validate_duplicated_features_dataset(self.item_features)

    def score(self):
        with TimeProfile(f"Generate predictions"):
            for predictions in self.learner.predict(input_function_builder=self.input_function_builder):
                self.collect_batch_results(predictions)

        with TimeProfile(f"Format prediction results"):
            result_df = self.format_results()

        return result_df

    @abstractmethod
    def collect_batch_results(self, predictions):
        pass

    @abstractmethod
    def format_results(self):
        pass

    @staticmethod
    def _validate_feature_dataset(dataset: FeatureDataset):
        if dataset is None:
            return

        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=dataset.row_size,
                                                                    required_row_count=1,
                                                                    arg_name=dataset.name)

    @staticmethod
    def _validate_duplicated_features_dataset(dataset: FeatureDataset):
        if dataset is None:
            return

        duplicated_names = dataset.ids[dataset.ids.duplicated()]
        if len(duplicated_names) > 0:
            ErrorMapping.throw(
                DuplicateFeatureDefinitionError(duplicated_name=duplicated_names.iloc[0], dataset=dataset.name,
                                                troubleshoot_hint='Please consider to use "Remove Duplicate Rows" '
                                                                  'module to remove duplicated features.'))


class RatingPredictionScorer(BaseWideNDeepScorer):
    input_function_builder_class = RatingPredictionInputFunctionBuilder

    def __init__(self,
                 learner: WideNDeepModel,
                 test_transactions: TransactionDataset,
                 training_transactions: TransactionDataset,
                 user_features: FeatureDataset,
                 item_features: FeatureDataset,
                 max_recommended_item_count,
                 min_recommendation_pool_size,
                 return_ratings,
                 batch_size=None):
        module_logger.info("Init rating prediction scorer.")
        super().__init__(learner, test_transactions, training_transactions, user_features, item_features,
                         max_recommended_item_count, min_recommendation_pool_size, return_ratings, batch_size)
        self.predictions_buffer = []

    def _validate_dataset(self):
        super()._validate_dataset()
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=self.test_transactions.column_size,
            required_column_count=2,
            arg_name=self.test_transactions.name)

    def _preprocess_dataset(self):
        transactions_df = self.test_transactions.df.iloc[:, :TRANSACTIONS_RATING_COL]
        transactions_df = transactions_df.drop_duplicates().reset_index(drop=True)
        self.test_transactions = TransactionDataset(transactions_df, name=self.test_transactions.name)
        super()._preprocess_dataset()

    def collect_batch_results(self, predictions):
        self.predictions_buffer += list(predictions.flatten())

    def format_results(self):
        transactions_df = self.test_transactions.df
        result_df = transactions_df.rename(columns=dict(zip(transactions_df.columns, [USER_COLUMN, ITEM_COLUMN])))
        result_df[SCORED_RATING] = self.predictions_buffer
        result_df = result_df.reset_index(drop=True)

        return result_df


class RecommendationScorer(BaseWideNDeepScorer):
    PredRatingColumn = 'Predicted Rating'
    input_function_builder_class = RecommendationInputFunctionBuilder

    @abstractmethod
    def collect_batch_results(self, predictions):
        pass

    @abstractmethod
    def format_results(self):
        pass

    def _build_result_df(self, predictions_df):
        predictions_df = predictions_df.reset_index(drop=True)
        user_group = predictions_df.groupby(USER_COLUMN)
        recommended_items = user_group[ITEM_COLUMN].apply(list)
        users = recommended_items.index[:, np.newaxis]
        recommended_items = pad_sequences(recommended_items.values,
                                          dtype='object',
                                          maxlen=self.max_recommended_item_count,
                                          padding='post', value=None)
        result_arr = np.concatenate([users, recommended_items], axis=1)
        column_names = self.build_ranking_column_names(top_k=self.max_recommended_item_count)

        if self.return_ratings:
            ratings = user_group[SCORED_RATING].apply(list)
            ratings = pad_sequences(ratings.values,
                                    dtype='object',
                                    maxlen=self.max_recommended_item_count,
                                    padding='post', value=None)
            result_arr = np.concatenate([result_arr, ratings], axis=1)
            col_idx = np.zeros(2 * self.max_recommended_item_count + 1, np.int32)
            col_idx[1::2] = range(1, self.max_recommended_item_count + 1)
            col_idx[2::2] = range(self.max_recommended_item_count + 1, 2 * self.max_recommended_item_count + 1)
            result_arr = result_arr[:, col_idx]
            column_names += [f"{self.PredRatingColumn} {i}" for i in range(1, self.max_recommended_item_count + 1)]
            column_names = [column_names[i] for i in col_idx]

        result_df = pd.DataFrame(result_arr, columns=column_names)

        return result_df

    def build_ranking_column_names(self, top_k):
        return build_ranking_column_names(top_k)


class RatedItemRecommendationScorer(RecommendationScorer):
    input_function_builder_class = RatingPredictionInputFunctionBuilder

    def __init__(self,
                 learner: WideNDeepModel,
                 test_transactions: TransactionDataset,
                 training_transactions: TransactionDataset,
                 user_features: FeatureDataset,
                 item_features: FeatureDataset,
                 max_recommended_item_count,
                 min_recommendation_pool_size,
                 return_ratings,
                 batch_size=None):
        module_logger.info("Init rated items recommendation scorer.")
        super().__init__(learner, test_transactions, training_transactions, user_features, item_features,
                         max_recommended_item_count, min_recommendation_pool_size, return_ratings, batch_size)
        self.predictions_buffer = []

    def _validate_dataset(self):
        super()._validate_dataset()
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=self.test_transactions.column_size,
            required_column_count=2,
            arg_name=self.test_transactions.name)

    def _preprocess_dataset(self):
        transactions_df = self.test_transactions.df.iloc[:, :TRANSACTIONS_RATING_COL]
        transactions_df = transactions_df.drop_duplicates()
        transactions_df = transactions_df.rename(columns=dict(zip(transactions_df.columns, [USER_COLUMN, ITEM_COLUMN])))
        # remove users whose interacted items count less than min recommendation pool size
        rated_item_count = transactions_df.groupby(USER_COLUMN, as_index=False).count()
        valid_users = rated_item_count[USER_COLUMN][rated_item_count[ITEM_COLUMN] >= self.min_recommendation_pool_size]
        valid_transactions_df = transactions_df[transactions_df[USER_COLUMN].isin(valid_users)].reset_index(drop=True)

        self.test_transactions = TransactionDataset(valid_transactions_df, name=self.test_transactions.name)
        super()._preprocess_dataset()

    def collect_batch_results(self, predictions):
        self.predictions_buffer += list(predictions.flatten())

    def format_results(self):
        transactions_df = self.test_transactions.df
        predictions_df = transactions_df.rename(columns=dict(zip(transactions_df.columns, [USER_COLUMN, ITEM_COLUMN])))
        predictions_df[SCORED_RATING] = self.predictions_buffer
        predictions_df = (predictions_df.groupby(USER_COLUMN, as_index=False).
                          apply(lambda x: x.nlargest(n=self.max_recommended_item_count, columns=SCORED_RATING)))
        if predictions_df.shape[0] == 0:
            predictions_df = pd.DataFrame({}, columns=[USER_COLUMN, ITEM_COLUMN, SCORED_RATING])

        return self._build_result_df(predictions_df)

    def build_ranking_column_names(self, top_k):
        return build_rated_ranking_column_names(top_k)


class UnratedItemRecommendationScorer(RecommendationScorer):
    def __init__(self,
                 learner: WideNDeepModel,
                 test_transactions: TransactionDataset,
                 training_transactions: TransactionDataset,
                 user_features: FeatureDataset,
                 item_features: FeatureDataset,
                 max_recommended_item_count,
                 min_recommendation_pool_size,
                 return_ratings,
                 batch_size=None):
        module_logger.info("Init unrated items recommendation scorer.")
        super().__init__(learner, test_transactions, training_transactions, user_features, item_features,
                         max_recommended_item_count, min_recommendation_pool_size, return_ratings, batch_size)
        self.predictions_buffer = pd.DataFrame({}, columns=[USER_COLUMN, ITEM_COLUMN, SCORED_RATING])
        self.finished_user_counter = 0

    def _validate_dataset(self):
        super()._validate_dataset()
        if self.training_transactions is None:
            ErrorMapping.throw(NullOrEmptyError(
                name="Training data",
                troubleshoot_hint='Reason: "From Unrated Items" recommendation task '
                                  'needs to filter out rated items in the training data. Consider to connect training '
                                  'dataset to the "Training data" port.'))
        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=self.training_transactions.row_size,
                                                                    required_row_count=1,
                                                                    arg_name=self.training_transactions.name)
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=self.training_transactions.column_size,
            required_column_count=2,
            arg_name=self.training_transactions.name)
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=self.test_transactions.column_size,
            required_column_count=1,
            arg_name=self.test_transactions.name)

    def _preprocess_dataset(self):
        test_transactions_df = pd.DataFrame({USER_COLUMN: self.test_transactions.users.unique()})
        self.test_transactions = TransactionDataset(test_transactions_df, name=self.test_transactions.name)

        training_transactions_df = self.training_transactions.df.iloc[:, :TRANSACTIONS_RATING_COL]
        training_transactions_df = training_transactions_df.rename(
            columns=dict(zip(training_transactions_df.columns, [USER_COLUMN, ITEM_COLUMN])))
        training_transactions_df = training_transactions_df.drop_duplicates().reset_index(drop=True)
        self.training_transactions = TransactionDataset(training_transactions_df)

        super()._preprocess_dataset()
        self.user_to_rated_items = self.training_transactions.df.set_index(USER_COLUMN)
        self.user_to_rated_items[SCORED_RATING] = None
        self.seen_users = self.user_to_rated_items.index.unique()

    def collect_batch_results(self, predictions):
        predictions = predictions.flatten()
        item_count = len(self.input_function_builder.item_vocab)
        user_count = len(predictions) // item_count
        # remove rated items
        user_ids = self.input_function_builder.user_ids[
                   self.finished_user_counter:self.finished_user_counter + user_count]
        seen_user_ids = self.seen_users.intersection(user_ids)
        # In some cases, the index name may missing after call ".loc[]" operation.
        # So need to set the index name explicitly.
        rated_items = self.user_to_rated_items.loc[seen_user_ids]
        rated_items.index.name = USER_COLUMN
        rated_items = rated_items.reset_index()

        predictions_df = pd.DataFrame({
            USER_COLUMN: np.repeat(user_ids, repeats=item_count),
            ITEM_COLUMN: np.tile(self.input_function_builder.item_vocab, reps=len(user_ids)),
            SCORED_RATING: predictions})
        predictions_df = predictions_df.append(rated_items).drop_duplicates(subset=[USER_COLUMN, ITEM_COLUMN],
                                                                            keep=False)

        predictions_df = (predictions_df.groupby(USER_COLUMN, as_index=False).
                          apply(lambda x: x.nlargest(n=self.max_recommended_item_count, columns=SCORED_RATING)))
        self.predictions_buffer = self.predictions_buffer.append(predictions_df)
        self.finished_user_counter += user_count

    def format_results(self):
        return self._build_result_df(self.predictions_buffer)


class AllItemRecommendationScorer(RecommendationScorer):
    def __init__(self,
                 learner: WideNDeepModel,
                 test_transactions: TransactionDataset,
                 training_transactions: TransactionDataset,
                 user_features: FeatureDataset,
                 item_features: FeatureDataset,
                 max_recommended_item_count,
                 min_recommendation_pool_size,
                 return_ratings,
                 batch_size=None):
        module_logger.info("Init all items recommendation scorer.")
        super().__init__(learner, test_transactions, training_transactions, user_features, item_features,
                         max_recommended_item_count, min_recommendation_pool_size, return_ratings, batch_size)
        self.predictions_buffer = pd.DataFrame({}, columns=[USER_COLUMN, ITEM_COLUMN, SCORED_RATING])
        self.finished_user_counter = 0

    def _validate_dataset(self):
        super()._validate_dataset()
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=self.test_transactions.column_size,
            required_column_count=1,
            arg_name=self.test_transactions.name)

    def _preprocess_dataset(self):
        test_transactions_df = pd.DataFrame({USER_COLUMN: self.test_transactions.users.unique()})
        self.test_transactions = TransactionDataset(test_transactions_df, name=self.test_transactions.name)
        super()._preprocess_dataset()

    def collect_batch_results(self, predictions):
        predictions = predictions.flatten()
        item_count = len(self.input_function_builder.item_vocab)
        user_count = len(predictions) // item_count

        user_ids = self.input_function_builder.user_ids[
                   self.finished_user_counter:self.finished_user_counter + user_count]
        predictions_df = pd.DataFrame({
            USER_COLUMN: np.repeat(user_ids, repeats=item_count),
            ITEM_COLUMN: np.tile(self.input_function_builder.item_vocab, reps=len(user_ids)),
            SCORED_RATING: predictions})

        predictions_df = (predictions_df.groupby(USER_COLUMN, as_index=False).
                          apply(lambda x: x.nlargest(n=self.max_recommended_item_count, columns=SCORED_RATING)))
        self.predictions_buffer = self.predictions_buffer.append(predictions_df)
        self.finished_user_counter += user_count

    def format_results(self):
        return self._build_result_df(self.predictions_buffer)
