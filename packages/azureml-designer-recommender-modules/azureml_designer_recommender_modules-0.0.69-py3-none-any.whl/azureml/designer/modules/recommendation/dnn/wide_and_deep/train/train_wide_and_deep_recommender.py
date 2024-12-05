from azureml.studio.internal.error import ErrorMapping, MoreThanOneRatingError, DuplicateFeatureDefinitionError, \
    InvalidDatasetError, InvalidColumnTypeError
from azureml.studio.core.data_frame_schema import ColumnTypeName
from azureml.designer.modules.recommendation.dnn.common.constants import TRANSACTIONS_RATING_COL, \
    TRANSACTIONS_USER_COL, TRANSACTIONS_ITEM_COL
from azureml.designer.modules.recommendation.dnn.common.entry_param import IntTuple, Boolean
from azureml.designer.modules.recommendation.dnn.common.dataset import TransactionDataset, FeatureDataset
from azureml.designer.modules.recommendation.dnn.common.entry_utils import params_loader
from azureml.designer.modules.recommendation.dnn.wide_and_deep.common.preprocess import preprocess_features, \
    preprocess_transactions
from azureml.designer.modules.recommendation.dnn.common.feature_builder import FeatureBuilder
from azureml.designer.modules.recommendation.dnn.wide_and_deep.common.wide_n_deep_model import WideNDeepModel, \
    WideNDeepModelHyperParams, OptimizerSelection, ActivationFnSelection
from azureml.studio.core.io.model_directory import save_model_to_directory
from azureml.studio.core.data_frame_schema import DataFrameSchema
from azureml.studio.core.io.data_frame_directory import DataFrameDirectory
from azureml.designer.modules.recommendation.dnn.model_deployment.model_deployment_handler import \
    WideAndDeepRecommendationDeploymentHandler
from azureml.studio.core.logger import TimeProfile
from azureml.designer.modules.recommendation.dnn.wide_and_deep.common.input_function_builder import \
    TrainInputFunctionBuilder


class TrainWideAndDeepRecommenderModule:
    @staticmethod
    def _validate_feature_dataset(dataset: FeatureDataset):
        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=dataset.row_size,
                                                                    required_row_count=1,
                                                                    arg_name=dataset.name)

    @staticmethod
    def _validate_datasets(transactions: TransactionDataset, user_features: FeatureDataset = None,
                           item_features: FeatureDataset = None):
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(curr_column_count=transactions.column_size,
                                                                       required_column_count=3,
                                                                       arg_name=transactions.name)
        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=transactions.row_size,
                                                                    required_row_count=1,
                                                                    arg_name=transactions.name)
        rating_column_type = transactions.get_column_type(TRANSACTIONS_RATING_COL)
        if rating_column_type != ColumnTypeName.NUMERIC:
            ErrorMapping.throw(InvalidColumnTypeError(
                col_type=rating_column_type,
                col_name=transactions.ratings.name,
                reason=f"rating column in {transactions.name} dataset must be {ColumnTypeName.NUMERIC} type",
                troubleshoot_hint=''))

        if user_features is not None:
            TrainWideAndDeepRecommenderModule._validate_feature_dataset(user_features)
        if item_features is not None:
            TrainWideAndDeepRecommenderModule._validate_feature_dataset(item_features)

    @staticmethod
    def _preprocess(transactions: TransactionDataset, user_features: FeatureDataset, item_features: FeatureDataset):
        # preprocess transactions data
        transactions = preprocess_transactions(transactions)

        # preprocess user features
        user_features = preprocess_features(user_features) if user_features is not None else None
        item_features = preprocess_features(item_features) if item_features is not None else None
        TrainWideAndDeepRecommenderModule._validate_preprocessed_dataset(transactions, user_features=user_features,
                                                                         item_features=item_features)
        return transactions, user_features, item_features

    @staticmethod
    def _validate_preprocessed_dataset(transactions: TransactionDataset, user_features: FeatureDataset,
                                       item_features: FeatureDataset):
        if transactions.row_size <= 0:
            ErrorMapping.throw(
                InvalidDatasetError(dataset1=transactions.name, reason=f"dataset does not have any valid samples"))
        duplicated_pairs = transactions.df[
            transactions.df.duplicated(subset=transactions.columns[[TRANSACTIONS_USER_COL, TRANSACTIONS_ITEM_COL]])]
        if len(duplicated_pairs) > 0:
            duplicated_user = duplicated_pairs.iloc[0, TRANSACTIONS_USER_COL]
            duplicated_item = duplicated_pairs.iloc[0, TRANSACTIONS_ITEM_COL]
            ErrorMapping.throw(
                MoreThanOneRatingError(user=duplicated_user, item=duplicated_item, dataset=transactions.name))
        TrainWideAndDeepRecommenderModule._validate_duplicated_features_dataset(user_features)
        TrainWideAndDeepRecommenderModule._validate_duplicated_features_dataset(item_features)

    @staticmethod
    def _validate_duplicated_features_dataset(features: FeatureDataset):
        if features is None:
            return

        duplicated_names = features.ids[features.ids.duplicated()]
        if len(duplicated_names) > 0:
            ErrorMapping.throw(DuplicateFeatureDefinitionError(
                duplicated_name=duplicated_names.iloc[0], dataset=features.name,
                troubleshoot_hint='Please consider to use "Remove Duplicate Rows" '
                                  'module to remove duplicated features.'))

    @staticmethod
    def set_inputs_name(transactions: TransactionDataset, user_features: FeatureDataset = None,
                        item_features: FeatureDataset = None):
        _TRANSACTIONS_NAME = "Training dataset of user-item-rating triples"
        _USER_FEATURES_NAME = "User features"
        _ITEM_FEATURES_NAME = "Item features"
        if transactions is not None:
            transactions.name = _TRANSACTIONS_NAME
        else:
            ErrorMapping.verify_not_null_or_empty(x=transactions, name=_TRANSACTIONS_NAME)
        if user_features is not None:
            user_features.name = _USER_FEATURES_NAME
        if item_features is not None:
            item_features.name = _ITEM_FEATURES_NAME

    @params_loader
    def run(self,
            training_dataset_of_user_item_rating_triples: TransactionDataset,
            user_features: FeatureDataset,
            item_features: FeatureDataset,
            epochs: int,
            batch_size: int,
            wide_part_optimizer: OptimizerSelection,
            wide_optimizer_learning_rate: float,
            crossed_feature_dimension: int,
            deep_part_optimizer: OptimizerSelection,
            deep_optimizer_learning_rate: float,
            user_embedding_dimension: int,
            item_embedding_dimension: int,
            categorical_features_embedding_dimension: int,
            hidden_units: IntTuple,
            activation_function: ActivationFnSelection,
            dropout: float,
            batch_normalization: Boolean,
            trained_wide_and_deep_recommendation_model: str):
        self.set_inputs_name(training_dataset_of_user_item_rating_triples, user_features=user_features,
                             item_features=item_features)
        self._validate_datasets(training_dataset_of_user_item_rating_triples, user_features=user_features,
                                item_features=item_features)
        self._preprocess(training_dataset_of_user_item_rating_triples, user_features=user_features,
                         item_features=item_features)

        hyper_params = WideNDeepModelHyperParams(epochs=epochs,
                                                 batch_size=batch_size,
                                                 wide_optimizer=wide_part_optimizer,
                                                 wide_lr=wide_optimizer_learning_rate,
                                                 deep_optimizer=deep_part_optimizer,
                                                 deep_lr=deep_optimizer_learning_rate,
                                                 hidden_units=hidden_units,
                                                 activation_fn=activation_function,
                                                 dropout=dropout,
                                                 batch_norm=batch_normalization,
                                                 crossed_dim=crossed_feature_dimension,
                                                 user_dim=user_embedding_dimension,
                                                 item_dim=item_embedding_dimension,
                                                 embed_dim=categorical_features_embedding_dimension)
        user_feature_builder = FeatureBuilder(ids=training_dataset_of_user_item_rating_triples.users,
                                              id_key="User",
                                              features=user_features, feat_key_suffix='user_feature')
        item_feature_builder = FeatureBuilder(ids=training_dataset_of_user_item_rating_triples.items,
                                              id_key="Item",
                                              features=item_features, feat_key_suffix='item_feature')
        model = WideNDeepModel(hyper_params=hyper_params, save_dir=None, user_feature_builder=user_feature_builder,
                               item_feature_builder=item_feature_builder)
        input_function_builder = TrainInputFunctionBuilder(transactions=training_dataset_of_user_item_rating_triples,
                                                           user_feature_builder=user_feature_builder,
                                                           item_feature_builder=item_feature_builder,
                                                           batch_size=hyper_params.batch_size,
                                                           epochs=hyper_params.epochs,
                                                           shuffle=True,
                                                           random_seed=model.random_seed)
        model.train(input_function_builder)
        # trained_wide_and_deep_recommendation_model is trained model output path, and the variable name is
        # defined according to the module spec

        with TimeProfile("Create deployment handler and inject schema and sample."):
            schema = DataFrameSchema(training_dataset_of_user_item_rating_triples.column_attributes)
            dfd = DataFrameDirectory(training_dataset_of_user_item_rating_triples.df, schema)
            deployment_handler = WideAndDeepRecommendationDeploymentHandler()
            deployment_handler.sample_data = dfd.get_samples()
            deployment_handler.data_schema = schema.to_dict()

        save_model_to_directory(
            save_to=trained_wide_and_deep_recommendation_model,
            model=model,
            model_deployment_handler=deployment_handler)
