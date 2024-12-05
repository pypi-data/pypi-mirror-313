import os
import tempfile

import pandas as pd

from azureml.studio.common.error import ErrorMapping, FailedToEvaluateScriptError
from azureml.studio.common.utils.inspectutils import assert_obj_has_attribute, assert_obj_has_method
from azureml.studio.core.logger import module_logger, TimeProfile
from azureml.studio.core.utils.strutils import generate_random_string, profile_column_names
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.attributes import ScriptParameter, UntrainedLearnerOutputPort, ModuleMeta
from azureml.studio.modulehost.custom_module_utils import CustomModuleUtils
from azureml.studio.modulehost.module_reflector import BaseModule, module_entry
from azureml.studio.modules.ml.common.base_learner import BaseLearner
from azureml.studio.modules.ml.common.base_learner_setting import BaseLearnerSetting

PYTHON_MODEL_SAMPLE = """
# The script MUST define a class named AzureMLModel.
# This class MUST at least define the following three methods: "__init__", "train" and "predict".
# The signatures (method and argument names) of all these methods MUST be exactly the same as the following example.

# Please do not install extra packages such as "pip install xgboost" in this script,
# otherwise errors will be raised when reading models in down-stream modules.

import pandas as pd
from sklearn.linear_model import LogisticRegression


class AzureMLModel:
    # The __init__ method is only invoked in module "Create Python Model",
    # and will not be invoked again in the following modules "Train Model" and "Score Model".
    # The attributes defined in the __init__ method are preserved and usable in the train and predict method.
    def __init__(self):
        # self.model must be assigned
        self.model = LogisticRegression()
        self.feature_column_names = list()

    # Train model
    #   Param<df_train>: a pandas.DataFrame
    #   Param<df_label>: a pandas.Series
    def train(self, df_train, df_label):
        # self.feature_column_names records the column names used for training.
        # It is recommended to set this attribute before training so that the
        # feature columns used in predict and train methods have the same names.
        self.feature_column_names = df_train.columns.tolist()
        self.model.fit(df_train, df_label)

    # Predict results
    #   Param<df>: a pandas.DataFrame
    #   Must return a pandas.DataFrame
    def predict(self, df):
        # The feature columns used for prediction MUST have the same names as the ones for training.
        # The name of score column ("Scored Labels" in this case) MUST be different from any other
        # columns in input data.
        return pd.DataFrame({'Scored Labels': self.model.predict(df[self.feature_column_names])})
"""
SCRIPT_LANGUAGE = 'Python'
CUSTOM_MODEL_CLASS_NAME = 'AzureMLModel'
TRAIN_METHOD_NAME = 'train'
TRAIN_METHOD_ARGUMENTS = ['self', 'df_train', 'df_label']
PREDICT_METHOD_NAME = 'predict'
PREDICT_METHOD_ARGUMENTS = ['self', 'df']


class CustomModelProxy(BaseLearner):

    def __new__(cls, custom_model_cls_script: str, module_name=None):
        obj = super().__new__(cls)

        module = cls._load_script_to_module(custom_model_cls_script, module_name)
        obj.custom_model_cls = cls._load_custom_model_cls(module)

        # Record the custom_model_cls_script and module_name for __getnewargs__
        obj.custom_model_cls_script = custom_model_cls_script
        obj.module_name = module.__name__

        if module_name is None:
            module_logger.info(f"First time create {cls} instance.")
        else:
            module_logger.info(f"Create {cls} instance during reading pickle file.")

        return obj

    def __init__(self, *args, **kwargs):
        # CustomModelProxy initialization must only have one argument,
        # eg.: CustomModelProxy(custom_model_cls_script),
        # CustomModelProxy(custom_model_cls_script, module_name) is forbidden
        if len(args) + len(kwargs) != 1:
            raise ValueError(
                "__init__ function of class CustomModelProxy must have one argument")

        self.custom_model = self._initialize_and_validate_custom_model()
        super().__init__(setting=BaseLearnerSetting())

    def init_model(self):
        # To implement the abstract method init_model of BaseLearner
        pass

    def __getnewargs__(self):
        # pylint: disable=no-member
        return self.custom_model_cls_script, self.module_name

    def _initialize_and_validate_custom_model(self):
        # pylint: disable=no-member
        try:
            custom_model = self.custom_model_cls()
            self._validate_custom_model(custom_model)
        except BaseException as ex:
            ErrorMapping.rethrow(ex, FailedToEvaluateScriptError(
                script_language=SCRIPT_LANGUAGE,
                message=f"Got exception when initializing custom model: '{ErrorMapping.get_exception_message(ex)}'."
            ))
        return custom_model

    def generate_score_column_meta(self, predict_df):
        """Build score_column_names dict

        Map column name to column name
        :return: built score column names dict
        """
        score_columns = {x: x for x in predict_df.columns.tolist()}
        module_logger.info("Custom Defined Module Scored Columns are: ")
        module_logger.info(
            f'There are {len(score_columns.keys())} score columns: '
            f'"{profile_column_names(list(score_columns.keys()))}"')
        return score_columns

    def preprocess_training_data(self, data_table, fit=True):
        df = data_table.data_frame
        # This will return a new data frame
        df = df.reset_index(drop=True)
        df = self._clean_training_data(df)

        # Record label/feature columns
        self._record_feature_column_names(data_table)

        # split df_train with df_label, does not perform normalization
        df_label = df[self.label_column_name]
        df_train = df.drop(self.label_column_name, axis=1)
        return df_train, df_label

    def train(self, data_table, label_column_selection):
        """
        :param data_table: input training data
        :param label_column_selection: label column selection
        :return: None
        """
        self.collect_label_column_name(data_table, label_column_selection)
        self.check_label_column(data_table=data_table)
        # This will return a new data frame
        df = data_table.data_frame
        df = df.reset_index(drop=True)
        df = self._clean_training_data(df)

        df_train, df_label = self.preprocess_training_data(data_table=data_table)

        # Invoke user-defined train method
        try:
            with TimeProfile('Train model'):
                self.custom_model.train(df_train, df_label)
        except BaseException as ex:
            ErrorMapping.rethrow(ex, FailedToEvaluateScriptError(
                script_language=SCRIPT_LANGUAGE,
                message=f"Error occurred when invoking user-defined {TRAIN_METHOD_NAME} method: "
                f"'{ErrorMapping.get_exception_message(ex)}'."
            ))

        # Tag the trained model
        self._is_trained = True

    def predict(self, test_data_df: pd.DataFrame):
        """
        :param test_data_df: input testing data
        :return: predicted data
        """

        try:
            with TimeProfile('Predict model'):
                predict_results = self.custom_model.predict(test_data_df)
                if not isinstance(predict_results, pd.DataFrame):
                    raise ValueError("prediction results must be a pandas DataFrame")

                # Verify if columns names of predict_results are all string
                ErrorMapping.verify_column_names_are_string(predict_results.columns)
                # Fix bug 771390: predict function generates scored results rows not match with test data
                if predict_results.shape[0] != test_data_df.shape[0]:
                    raise ValueError(f"rows number not match: Scored result has {predict_results.shape[0]} rows, "
                                     f"while input test data has {test_data_df.shape[0]} rows")

        except BaseException as ex:
            ErrorMapping.rethrow(ex, FailedToEvaluateScriptError(
                script_language=SCRIPT_LANGUAGE,
                message=f"Error occurred when invoking user-defined {PREDICT_METHOD_NAME} method: "
                        f"'{ErrorMapping.get_exception_message(ex)}'."
            ))

        return predict_results

    @staticmethod
    def _load_script_to_module(custom_model_cls_script: str, module_name: str = None):
        with tempfile.TemporaryDirectory() as temp_dir_name:
            if module_name is None:
                module_name = generate_random_string()

            # Prepare python script
            module_logger.info("Prepare python script")
            script_file = f"{module_name}.py"

            # Add current temporary directory into sys.path
            module_logger.info("Add current temporary directory into sys.path")
            CustomModuleUtils.add_directory_to_sys_path(temp_dir_name)

            with open(os.path.join(temp_dir_name, script_file), "w") as text_file:
                text_file.write(custom_model_cls_script)

            module_logger.info(f"Import custom module {module_name}")
            try:
                custom_module = __import__(module_name)
            except BaseException as ex:
                ErrorMapping.rethrow(ex, FailedToEvaluateScriptError(
                    script_language=SCRIPT_LANGUAGE,
                    message=f"Got exception when importing script: '{ErrorMapping.get_exception_message(ex)}'."
                ))

        return custom_module

    @staticmethod
    def _load_custom_model_cls(custom_module):

        try:
            if hasattr(custom_module, CUSTOM_MODEL_CLASS_NAME):
                module_logger.info('Get custom model class')
                custom_model_cls = getattr(custom_module, CUSTOM_MODEL_CLASS_NAME)
            else:
                raise ValueError(f"{CUSTOM_MODEL_CLASS_NAME} is not found")

        except BaseException as ex:
            ErrorMapping.rethrow(ex, FailedToEvaluateScriptError(
                script_language=SCRIPT_LANGUAGE,
                message=ErrorMapping.get_exception_message(ex)
            ))

        return custom_model_cls

    @staticmethod
    def _validate_custom_model(custom_model):
        # custom module must define "model" attribute
        assert_obj_has_attribute(obj=custom_model, attr_name='model')

        # custom module must define "train" and "predict" methods
        assert_obj_has_method(obj=custom_model,
                              method_name=TRAIN_METHOD_NAME,
                              method_args=TRAIN_METHOD_ARGUMENTS)
        assert_obj_has_method(obj=custom_model,
                              method_name=PREDICT_METHOD_NAME,
                              method_args=PREDICT_METHOD_ARGUMENTS)

        # __getstate__ method is invoked when dumping model with pickle. Make sure it worked.
        if hasattr(custom_model, "__getstate__"):
            custom_model.__getstate__()


class CreatePythonModelModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Create Python Model",
        description="Creates Python model using custom script.",
        category="Python Language",
        version="1.0",
        owner="Microsoft Corporation",
        family_id="a5b1e9d2-5c54-11e9-8647-d663bd873d93",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            python_stream_reader: ScriptParameter(
                name="Python Script",
                friendly_name="Python script",
                description="The Python script to execute",
                script_name="script.py",
                default_value=PYTHON_MODEL_SAMPLE
            )
    ) -> (
            UntrainedLearnerOutputPort(
                name="Untrained model",
                friendly_name="Untrained model",
                description="A untrained custom python model",
            ),
    ):
        input_values = locals()
        return CreatePythonModelModule._run_impl(**input_values)

    @classmethod
    def _run_impl(
            cls,
            python_stream_reader: str,
    ):
        custom_model_proxy = CustomModelProxy(python_stream_reader)

        return custom_model_proxy,
