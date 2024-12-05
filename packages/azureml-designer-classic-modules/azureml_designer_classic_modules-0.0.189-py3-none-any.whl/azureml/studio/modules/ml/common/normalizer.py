import numpy as np
import pandas as pd
import scipy
from pandas.core.dtypes.common import is_categorical_dtype, is_numeric_dtype, is_integer_dtype, is_extension_array_dtype
from scipy.sparse import csr_matrix

import azureml.studio.common.datatable.data_type_conversion as data_type_conversion
import azureml.studio.common.utils.datetimeutils as datetimeutils
from azureml.studio.common.error import ErrorMapping, TooFewFeatureColumnsInDatasetError
from azureml.studio.core.logger import module_logger, time_profile
from azureml.studio.core.utils.strutils import profile_column_names
from azureml.studio.modulehost.constants import ElementTypeName
from azureml.studio.modules.datatransform.common.named_encoder import NamedMinMaxEncoder, NamedOneHotEncoder, \
    NamedLabelEncoder


class Normalizer:
    """
    NOTICE: the input df: pd.DataFrame would be changed in this class
    """

    def __init__(self):
        self.label_column_encoders = {}
        self.str_feature_column_encoders = {}
        self.numeric_feature_column_encoders = {}
        self.label_column_name = None

    @property
    def feature_columns_categorized_by_type(self):
        return tuple((set(self.str_feature_column_encoders.keys()),
                      set(self.numeric_feature_column_encoders.keys())))

    def build(self, df: pd.DataFrame, feature_columns, label_column_name, normalize_number=True, encode_label=True):

        def _is_category(series):
            return is_categorical_dtype(series.dtype)

        def _is_number(series):
            if (not is_categorical_dtype(series.dtype)) and is_numeric_dtype(series):
                return True
            return False

        def _is_date_data(series):
            return datetimeutils.is_datetime_dtype(series) or datetimeutils.is_timespan_dtype(series)

        module_logger.info(f"Building Normalizer - found Label column={label_column_name}"
                           f" with encode_label={encode_label}")
        # when task type is regression, label column will passed as None
        if label_column_name is not None:
            self.label_column_name = label_column_name
            if encode_label:
                self.label_column_encoders[label_column_name] = NamedLabelEncoder(label_column_name)

        module_logger.info(f"Building normalizer - found {len(feature_columns)} feature columns"
                           f" with normalize_number={normalize_number}")
        module_logger.debug(
            f'Building normalizer - found feature columns: "{profile_column_names(feature_columns)}".')

        for column in feature_columns:
            if _is_date_data(df[column]):
                module_logger.info(
                    f"Convert date column '{column}' to nanoseconds, then treat it as numeric feature column.")
                df[column] = datetimeutils.convert_to_ns(df[column])
                self.numeric_feature_column_encoders[column] = NamedMinMaxEncoder(column) if normalize_number else None
            elif _is_category(df[column]):
                self.str_feature_column_encoders[column] = NamedOneHotEncoder(column)
            elif not _is_number(df[column]):
                self.str_feature_column_encoders[column] = NamedOneHotEncoder(column)
            else:
                self.numeric_feature_column_encoders[column] = NamedMinMaxEncoder(column) if normalize_number else None

        module_logger.info(f"Building normalizer - found {len(self.numeric_feature_column_encoders)} "
                           f"numeric feature columns and {len(self.str_feature_column_encoders)} "
                           f"string feature columns to be encoded")
        module_logger.debug(f'Building normalizer - found numeric feature columns to be encoded:'
                            f' "{profile_column_names(list(self.numeric_feature_column_encoders.keys()))}".')
        module_logger.debug(f'Building normalizer - found string feature columns to be encoded:'
                            f' "{profile_column_names(list(self.str_feature_column_encoders.keys()))}".')
        if len(self.numeric_feature_column_encoders) + len(self.str_feature_column_encoders) == 0:
            module_logger.warning(f"==Get Empty Valid Training Feature==")
            ErrorMapping.throw(TooFewFeatureColumnsInDatasetError(required_columns_count=1))

    def fit(self, df: pd.DataFrame):
        if self.label_column_encoders:
            self._fit_label_column_encoders(df)

        if self.str_feature_column_encoders:
            self._fit_str_feature_column_encoders(df)

        if self.numeric_feature_column_encoders:
            self._fit_numeric_feature_column_encoders(df)

    @time_profile
    def _fit_label_column_encoders(self, df: pd.DataFrame):
        for column_name in self.label_column_encoders:
            if is_categorical_dtype(df[column_name]):
                df[column_name] = data_type_conversion.convert_column_by_element_type(df[column_name],
                                                                                      ElementTypeName.UNCATEGORY)
            if is_integer_dtype(df[column_name]) and is_extension_array_dtype(df[column_name]):
                df[column_name] = df[column_name].astype(np.int64)
            self.label_column_encoders[column_name].fit(df[column_name])
        module_logger.info(f"Successfully fit {len(self.label_column_encoders)} label column encoders.")

    @time_profile
    def _fit_str_feature_column_encoders(self, df: pd.DataFrame):
        for column_name in self.str_feature_column_encoders:
            series = df[column_name]
            self.str_feature_column_encoders[column_name].fit(series)
        module_logger.info(f"Successfully fit {len(self.str_feature_column_encoders)} string feature column encoders.")

    @time_profile
    def _fit_numeric_feature_column_encoders(self, df: pd.DataFrame):
        for column_name in self.numeric_feature_column_encoders:
            if self.numeric_feature_column_encoders[column_name] is not None:
                self.numeric_feature_column_encoders[column_name].fit(df[column_name])
        module_logger.info(f"Successfully fit {len(self.numeric_feature_column_encoders)} numeric feature"
                           f" column encoders.")

    def transform(self, df: pd.DataFrame, df_transform_column_list=None):
        if df_transform_column_list is None:
            module_logger.debug("df_transform_column_list is empty, will use full column list instead.")
            df_transform_column_list = df.columns.tolist()

        module_logger.info(f'Start to execute normalizer.transform with column_list: '
                           f'"{profile_column_names(df_transform_column_list)}".')

        encoder_keys = \
            self.label_column_encoders.keys() | \
            self.str_feature_column_encoders.keys() | \
            self.numeric_feature_column_encoders.keys()

        cols_has_encoder = [col for col in df_transform_column_list if col in encoder_keys]
        module_logger.info(f"Columns of input DataFrame: {len(df.columns.tolist())}")
        module_logger.info(f"Columns to be transformed: {len(df_transform_column_list)}")
        module_logger.info(f"Columns to be encoded: {len(cols_has_encoder)}")
        if not cols_has_encoder or np.array_equal(cols_has_encoder, list(self.label_column_encoders.keys())):
            ErrorMapping.throw(TooFewFeatureColumnsInDatasetError(required_columns_count=1))

        label = None
        if self.label_column_name:
            module_logger.info(f"Transform with label column {self.label_column_name}.")
            if self.label_column_name in df.columns:
                label = self._transform_label_column(df)

        str_features = []
        str_encoder_column_names = [col for col in cols_has_encoder if col in self.str_feature_column_encoders.keys()]
        if str_encoder_column_names:
            # str encoder columns would be dropped in place
            str_features = self._transform_str_feature_columns(df)

        num_features = self._transform_numeric_feature_columns(df)

        train_set_list = []
        use_sparse_matrix = False
        if str_features:
            # the default output type of hstack is coo_matrix, which is not subscriptable, so we use "csr", which means
            # Compressed Sparse Row matrix, as the output format instead. More details can be found here:
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html
            csr_str_cols = scipy.sparse.hstack(str_features, format='csr')
            train_set_list.append(csr_str_cols)
            use_sparse_matrix = True

        if num_features.size != 0:
            if use_sparse_matrix:
                csr_cols_without_encode = csr_matrix(num_features)
                train_set_list.append(csr_cols_without_encode)
            else:
                train_set_list.append(num_features)

        if not train_set_list:
            ErrorMapping.throw(TooFewFeatureColumnsInDatasetError(required_columns_count=1))
        if len(train_set_list) == 1:
            module_logger.info(f"Construct train set complete.")
            return train_set_list[0], label
        else:
            train_set_list.reverse()
            if use_sparse_matrix:
                module_logger.info(f"Construct train set with Sparse structure.")
                # the default output type of hstack is coo_matrix, which is not subscriptable, so we use "csr" as the
                # output format instead.
                return scipy.sparse.hstack(train_set_list, format='csr'), label
            else:
                module_logger.info(f"Construct train set with Dense structure.")
                return pd.concat(train_set_list, axis=1), label

    def _transform_label_column(self, df: pd.DataFrame):
        series = df[self.label_column_name]
        if self.label_column_name in self.label_column_encoders:
            if is_categorical_dtype(series.dtype):
                series = data_type_conversion.convert_column_by_element_type(series, ElementTypeName.UNCATEGORY)
            return self.label_column_encoders[self.label_column_name].transform(series)
        else:
            return series

    @time_profile
    def _transform_str_feature_columns(self, df: pd.DataFrame):
        str_features = []
        for column_name in self.str_feature_column_encoders.keys():
            series = df[column_name]
            str_features.append(self.str_feature_column_encoders[column_name].transform(series))

        module_logger.info(f"Successfully encoded {len(str_features)} string feature columns.")
        generated_str_cols_count = sum(m.shape[1] if len(m.shape) > 1 else 1 for m in str_features)
        module_logger.info(f"After transformation, {generated_str_cols_count} string feature column are generated")
        return str_features

    @time_profile
    def _transform_numeric_feature_columns(self, df: pd.DataFrame):
        num_features = np.zeros((df.shape[0], len(self.numeric_feature_column_encoders.keys())), dtype=np.float)
        column_index = 0
        for column_name in self.numeric_feature_column_encoders.keys():
            series = df[column_name]
            if self.numeric_feature_column_encoders[column_name] is not None:
                ret = self.numeric_feature_column_encoders[column_name].transform(series)
            else:
                ret = series.values
            ret = np.nan_to_num(ret)
            num_features[:, column_index] = ret
            column_index += 1
        module_logger.info(
            f"Successfully encoded {len(self.numeric_feature_column_encoders)} numeric feature columns.")
        return num_features

    def fit_transform(self, df: pd.DataFrame):
        self.fit(df)
        return self.transform(df)

    def inverse_transform(self, array, label_column):
        return self.label_column_encoders[label_column].inverse_transform(array)
