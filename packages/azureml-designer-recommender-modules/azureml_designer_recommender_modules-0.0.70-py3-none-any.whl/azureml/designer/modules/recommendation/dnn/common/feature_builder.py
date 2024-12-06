import pandas as pd
import numpy as np
from azureml.studio.core.logger import common_logger
from azureml.studio.internal.error import ErrorMapping, ColumnNotFoundError, InvalidColumnTypeError
from azureml.designer.modules.recommendation.dnn.common.dataset import FeatureDataset
from azureml.studio.core.data_frame_schema import ColumnTypeName
from azureml.designer.modules.recommendation.dnn.common.utils import convert_to_str, convert_to_float
from azureml.studio.core.utils.missing_value_utils import is_na


class FeatureMeta:
    """The tool class recorded feature metas.

    Feature meta includes four fields: feature original name, feature type, values used to fill missing elements,
    and the value vocabulary for categorical feature.
    """

    def __init__(self, name, type_, fill, vocab=None):
        self.name = name
        self.type_ = type_
        self.fill = fill
        self.vocab = vocab

    def is_numeric_feature(self):
        return self.vocab is None


class FeatureBuilder:
    """The tool class helps recommenders to build training/test dataset with normalized features.

    The class has three main functionality:
    1. Record (user/item) ids vocab in id_vocab attribute. This attr is usually init during training stage and re-used
    in score stage.
    2. Record features in _features_df and _features_meta attributes. These attrs would be used to build dataset with
    features, which is usually used in hybrid recommendation.
    3. Provide update method to update features for unseen ids during training.
    """

    def __init__(self, ids: pd.Series, id_key: str, features: FeatureDataset = None, feat_key_suffix=None):
        """Init ids and features.

        This function would record ids and features values. And feature metas will also recorded, which can be checked
        in the update method.

        :param ids: represents feature identifiers with pd.Series type
        :param id_key: the key represent id feature
        :param features: FeatureDataset type, where the first column must be feature identifiers, and the remain
        columns are features
        :param feat_key_suffix: when rename features, this string will be append the new names, this param is useful
        when there will be many feature builders and to avoid duplicate feature keys
        """
        ids_df = pd.DataFrame({id_key: convert_to_str(ids).dropna().unique()})

        # _features_df and _feature_metas is used to record valid features fed to the train module. _features_df records
        # feature values, and _feature_metas records feature meta data.
        # The first column of _features_df is id column, the subsequent columns are features. Thus, if no valid
        # features, the _features_df contains only one column.
        self._features_df = None
        # If no valid features, _feature_metas will be empty.
        self._feature_metas = {}
        if features is not None:
            common_logger.info(f"Get {features.features.shape[1]} features")
            features_df = pd.DataFrame({id_key: convert_to_str(features.ids)})
            for idx, name in enumerate(features.features.columns):
                feature = features.features[name]
                column_type = features.get_column_type(name)
                # Fix bug 779240, not use original column names to avoid invalid scope name for tensorflow
                key = f"feature_{feat_key_suffix}_{idx}" if feat_key_suffix else f"feature_{idx}"

                normalized_feature = self._normalize_feature(feature=feature, column_type=column_type)
                feature_meta = self._init_feature_meta(feature=normalized_feature, column_type=column_type)
                if feature_meta is not None:
                    features_df[key] = normalized_feature
                    self.feature_metas[key] = feature_meta

            if self.feature_metas:
                self._features_df = features_df

        # set the first column of _features_df to be ids column
        if not self.feature_metas:
            self._features_df = ids_df
        else:
            self._features_df = self._features_df.append(ids_df)
            self._features_df = self._features_df.drop_duplicates(subset=[id_key])

        self.id_vocab = self._features_df.iloc[:, 0]

        common_logger.info(f"Create feature metas for {len(self.feature_metas)} features")

    def build_feature_lookup(self, ids: pd.Series):
        """Build feature lookup for the given ids.

        With ids provided, the module checks _features_df attr, and finds corresponding features for those ids.
        If _features_df is None, then only convert ids to string type and return.
        :param ids: the identifiers to built with features
        :return: pd.DataFrame, feature lookup for ids, the dataframe indexes are the given ids.
        """
        common_logger.info(f"Build {len(self.feature_metas)} features for {self.id_key} ids.")
        ids = convert_to_str(ids.dropna()).unique()
        features_df = pd.DataFrame({self.id_key: ids})

        if self._features_df is not None:
            features_df = pd.merge(features_df, self._features_df, how='left', on=[self.id_key])

        features_df = features_df.set_index(self.id_key, drop=False)
        if self.feature_metas:
            common_logger.info("Process null values for features.")
            for key, meta in self.feature_metas.items():
                feature = features_df[key]
                features_df[key] = self._fill_feature_na(feature=feature, feature_meta=meta)

        return features_df

    def update(self, features: FeatureDataset):
        """Update existing features with the new features dataset.

        The method checks the compatibility between existing features and new features dataset. Then update
        unseen identifiers features according to new features. The features for existing identifiers would not be
        updated.
        :param features: FeatureDataset, the new features dataset provided to update the existing features.
        """
        if not features:
            common_logger.info(f"Update feature metas with None features")
            return

        self._check_features(features)
        common_logger.info(f"Found {len(self.feature_metas)} features to update")
        new_features_df = features.df[[features.ids.name]].rename(columns={features.ids.name: self.id_key})
        new_features_df[self.id_key] = convert_to_str(new_features_df[self.id_key])

        for key, meta in self.feature_metas.items():
            new_features_df[key] = self._normalize_feature(feature=features.df[meta.name],
                                                           column_type=features.get_column_type(meta.name))

        new_features_df = pd.concat([self._features_df, new_features_df], axis=0)
        existed_ids = new_features_df.duplicated(subset=self.id_key, keep='first')
        new_features_df = new_features_df[~existed_ids].reset_index(drop=True)
        common_logger.info(
            f"Updated features have {len(new_features_df)} rows, and fixed id vocab has {len(self.id_vocab)} rows.")

        self._features_df = new_features_df

    def _check_features(self, features: FeatureDataset):
        """Check compatibility between recorded features and the given features.

        The two feature dataset are compatibility if:
        1. The new feature dataset contains all feature names in the old feature dataset
        2. The same feature in two dataset is of same type
        """
        if features.row_size == 0:
            return
        common_logger.info(f"Check features compatibility with existing feature metas")
        for _, feature_meta in self.feature_metas.items():
            name = feature_meta.name
            if name not in features.features:
                ErrorMapping.throw(ColumnNotFoundError(column_id=name, arg_name_missing_column=features.name))
            column_type = features.get_column_type(name)
            if features.get_column_type(name) != feature_meta.type_:
                ErrorMapping.throw(InvalidColumnTypeError(
                    col_type=column_type,
                    col_name=name,
                    reason=f'column types must be the same in training and scoring stages. Column "{name}" is '
                    f'of {feature_meta.type_} type in training',
                    troubleshoot_hint='Consider to use "Edit Metadata" module to convert column type.'))

    @staticmethod
    def _fill_feature_na(feature: pd.Series, feature_meta: FeatureMeta):
        if feature_meta.type_ == ColumnTypeName.NUMERIC:
            feature = feature.replace(to_replace=[np.inf, -np.inf], value=np.nan)
        feature = feature.fillna(feature_meta.fill)

        return feature

    @staticmethod
    def _normalize_feature(feature: pd.Series, column_type):
        if column_type in [ColumnTypeName.CATEGORICAL, ColumnTypeName.BINARY, ColumnTypeName.OBJECT,
                           ColumnTypeName.STRING]:
            new_feature = convert_to_str(column=feature)
        elif column_type == ColumnTypeName.NUMERIC:
            new_feature = convert_to_float(column=feature)
        else:
            new_feature = feature.copy()

        return new_feature

    @staticmethod
    def _init_feature_meta(feature: pd.Series, column_type):
        """Init feature meta for the feature, which is described as pd.Series type.

        The DateTime, TimeSpan and NAN type features would be ignored. And the numeric features with NAN mean
        value is also ignored."""
        if column_type in [ColumnTypeName.DATETIME, ColumnTypeName.TIMESPAN] \
                or is_na(feature):
            common_logger.info(f"Skip {column_type} type feature: {feature.name}")
            feature_meta = None
        elif column_type in [ColumnTypeName.CATEGORICAL, ColumnTypeName.BINARY, ColumnTypeName.OBJECT,
                             ColumnTypeName.STRING]:
            feature_meta = FeatureMeta(name=feature.name, type_=column_type, fill='', vocab=feature.dropna().unique())
        else:
            mean = feature.replace(to_replace=[np.inf, -np.inf], value=np.nan).mean()
            if np.isnan(mean):
                feature_meta = None
                common_logger.info(f"Skip {column_type} feature {feature.name}, the mean value is {mean}")
            else:
                feature_meta = FeatureMeta(name=feature.name, type_=column_type, fill=mean)

        return feature_meta

    @property
    def feature_metas(self):
        return self._feature_metas

    @property
    def id_key(self):
        return self.id_vocab.name

    @property
    def dynamic_id_vocab(self):
        # this dynamic id vocab is different from self.id_vocab. self.id_vocab is fixed for building the model,
        # and dynamic id vocab is deduced from features data frame, where users can add new items with features.
        return self._features_df.iloc[:, 0]
