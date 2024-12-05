import inspect
import os
import traceback
import tempfile
from typing import Union

import pandas as pd
import numpy as np

from azureml.studio.modulehost.attributes import ItemInfo, ModuleMeta, DataTableInputPort, ZipInputPort, \
    ScriptParameter, ModeParameter, DataTableOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import FailedToEvaluateScriptError, ErrorMapping
from azureml.studio.core.logger import TimeProfile, module_logger
from azureml.studio.common.types import AutoEnum
from azureml.studio.core.utils.fileutils import ensure_folder, ExecuteInDirectory
from azureml.studio.core.utils.strutils import generate_random_string, add_suffix_number_to_avoid_repetition
from azureml.studio.common.zip_wrapper import ZipFileWrapper
from azureml.studio.modulehost.custom_module_utils import CustomModuleUtils
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule


class ExecutePyScriptPyVer(AutoEnum):
    Anaconda20Python277: ItemInfo(name="Anaconda 2.0/Python 2.7.7", friendly_name="Anaconda 2.0/Python 2.7.7") = ()
    Anaconda40Python2711: ItemInfo(name="Anaconda 4.0/Python 2.7.11", friendly_name="Anaconda 4.0/Python 2.7.11") = ()
    Anaconda40Python35: ItemInfo(name="Anaconda 4.0/Python 3.5", friendly_name="Anaconda 4.0/Python 3.5") = ()


PYTHON_SCRIPT_SAMPLE = """
# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# imports up here can be used to
import pandas as pd

# The entry point function MUST have two input arguments.
# If the input port is not connected, the corresponding
# dataframe argument will be None.
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(dataframe1 = None, dataframe2 = None):

    # Execution logic goes here
    print(f'Input pandas.DataFrame #1: {dataframe1}')

    # If a zip file is connected to the third input port,
    # it is unzipped under "./Script Bundle". This directory is added
    # to sys.path. Therefore, if your zip file contains a Python file
    # mymodule.py you can import it using:
    # import mymodule

    # Return value must be of a sequence of pandas.DataFrame
    # E.g.
    #   -  Single return value: return dataframe1,
    #   -  Two return values: return dataframe1, dataframe2
    return dataframe1,

"""
BASE_COLUMN_NAME_FOR_RETURNED_DATA_FRAME = 'column'
SCRIPT_FILE_PREFIX = "user_script"


class ExecutePythonScriptModule(BaseModule):
    SCRIPT_LANGUAGE = "Python"
    SCRIPT_ENTRY = "azureml_main"

    @staticmethod
    @module_entry(ModuleMeta(
        name="Execute Python Script",
        description="Executes a Python script from an Azure Machine Learning designer pipeline.",
        category="Python Language",
        version="1.1",
        owner="Microsoft Corporation",
        family_id="CDB56F95-7F4C-404D-BDE7-5BB972E6F232",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            dataset1: DataTableInputPort(
                name="Dataset1",
                friendly_name="Dataset1",
                is_optional=True,
                description="Input dataset 1",
            ),
            dataset2: DataTableInputPort(
                name="Dataset2",
                friendly_name="Dataset2",
                is_optional=True,
                description="Input dataset 2",
            ),
            bundle_file: ZipInputPort(
                name="Script Bundle",
                friendly_name="Script bundle",
                is_optional=True,
                description="Zip file containing custom resources",
            ),
            python_stream_reader: ScriptParameter(
                name="Python Script",
                friendly_name="Python script",
                description="The Python script to execute",
                script_name="script.py",
                default_value=PYTHON_SCRIPT_SAMPLE
            ),
            py_lib_version: ModeParameter(
                ExecutePyScriptPyVer,
                name="Python Version",
                friendly_name="Python Version",
                description="Specify the version of Python that the script will be run against.",
                default_value=ExecutePyScriptPyVer.Anaconda40Python2711,
                release_state=ReleaseState.Alpha,
            )
    ) -> (
            DataTableOutputPort(
                name="Result Dataset",
                friendly_name="Result dataset",
                description="Output Dataset",
            ),
            DataTableOutputPort(
                name="Python Device",
                friendly_name="Result dataset2",
                description="Output Dataset2",
            ),
    ):
        input_values = locals()
        return _run_impl(**input_values)


def _run_impl(
        dataset1: DataTable = None,
        dataset2: DataTable = None,
        bundle_file: ZipFileWrapper = None,
        python_stream_reader: str = None,
        py_lib_version: ExecutePyScriptPyVer = ExecutePyScriptPyVer.Anaconda40Python2711
):
    # This variable will be set when error occurs during executing python script.
    # Once set, this error will be raised in the finally clause.
    # This gurantees errors occurred in executing python script will be raised, not masked by errors
    # in tempfile.TemporaryDirectory.
    executing_script_error = None
    try:
        with tempfile.TemporaryDirectory() as temp_dir_name:
            script_file_basename = f"{SCRIPT_FILE_PREFIX}_{generate_random_string()}"

            # Prepare python script
            module_logger.info('Prepare python script')
            script_file = f"{script_file_basename}.py"
            with open(os.path.join(temp_dir_name, script_file), "w") as text_file:
                text_file.write(python_stream_reader)

            # Check and extract bundle zip file to path ./Script Bundle
            module_logger.info('Check and extract bundle zip file to path ./Script Bundle')
            extract_to_path = os.path.join(temp_dir_name, 'Script Bundle')
            ensure_folder(extract_to_path)

            if bundle_file:
                bundle_file.extractall(extract_to_path)

            # Add current temporary directory into sys.path
            module_logger.info('Add current temporary directory into sys.path')
            CustomModuleUtils.add_directory_to_sys_path(temp_dir_name)
            CustomModuleUtils.add_directory_to_sys_path(extract_to_path)

            try:
                # Invoke script function
                module_logger.info('Check and convert DataTable to DataFrame')
                script_function = getattr(__import__(script_file_basename), ExecutePythonScriptModule.SCRIPT_ENTRY)
                df1 = _check_and_convert_to_data_frame(dataset1)
                df2 = _check_and_convert_to_data_frame(dataset2)

                with TimeProfile('Execute python script'):
                    with ExecuteInDirectory(temp_dir_name, is_directory=True):
                        arg_count = len(inspect.signature(script_function).parameters)
                        if arg_count == 0:
                            results = script_function()
                        elif arg_count == 1:
                            results = script_function(df1)
                        else:
                            results = script_function(df1, df2)

                with TimeProfile('Wrap output DataFrame to DataTable'):
                    if results is not None:
                        if isinstance(results, tuple):
                            result_table1 = _check_and_convert_to_data_table(results[0])
                            if len(results) > 1:
                                result_table2 = _check_and_convert_to_data_table(results[1])
                            else:
                                result_table2 = DataTable()
                            return result_table1, result_table2
                        else:
                            result_table1 = _check_and_convert_to_data_table(results)
                            return result_table1, DataTable()
                    else:
                        return DataTable(), DataTable()
            except BaseException as ex:
                error_line_number = _get_error_line_number(ex, ExecutePythonScriptModule.SCRIPT_ENTRY)
                if error_line_number is not None:
                    error_message = f"Got exception when invoking script at line {error_line_number} in function " \
                        f"{ExecutePythonScriptModule.SCRIPT_ENTRY}: " \
                        f"'{ErrorMapping.get_exception_message(ex, show_exception_name=True)}'."
                else:
                    error_message = "Got exception when invoking script: " \
                        f"'{ErrorMapping.get_exception_message(ex, show_exception_name=True)}'."
                executing_script_error = FailedToEvaluateScriptError(
                    ExecutePythonScriptModule.SCRIPT_LANGUAGE,
                    error_message
                )
    except OSError as ex:
        # In some corner cases, temporarily created directory fails to be deleted after executing python script.
        # Such error will not be raised.
        module_logger.warning(f'Failed to delete temporarily-created folder due to {ex}.')
    finally:
        # This gurantees errors occurred in executing python script will be raised, not masked by errors
        # in tempfile.TemporaryDirectory.
        if executing_script_error:
            ErrorMapping.throw(executing_script_error)


def _check_and_convert_to_data_frame(table):
    if table is not None:
        return table.data_frame
    else:
        return None


def _check_and_convert_to_data_table(result):
    if result is not None:
        if not isinstance(result, pd.DataFrame):
            result = _convert_return_value_to_data_frame(result)

        # Convert column names to string
        result.rename(mapper=str, axis='columns', inplace=True)

        _rename_column_name_if_duplicated(result)
        # Verify if all column names are string
        ErrorMapping.verify_column_names_are_string(result.columns)
        return DataTable(result)
    else:
        return DataTable()


def _rename_column_name_if_duplicated(df: pd.DataFrame):
    new_column_name_lst = []
    for i, name in enumerate(df.columns):
        if name not in new_column_name_lst:
            new_column_name_lst.append(name)
        else:
            new_name = add_suffix_number_to_avoid_repetition(name, new_column_name_lst)
            new_column_name_lst.append(new_name)

    df.columns = new_column_name_lst


def _convert_return_value_to_data_frame(obj):

    def _get_column_name_lst(column_count):
        if column_count > 1:
            column_name_lst = [f'{BASE_COLUMN_NAME_FOR_RETURNED_DATA_FRAME}_{i}' for i in range(column_count)]
        else:
            column_name_lst = [BASE_COLUMN_NAME_FOR_RETURNED_DATA_FRAME]
        return column_name_lst

    try:
        if isinstance(obj, dict):
            return pd.DataFrame(obj)
        elif isinstance(obj, np.ndarray):
            column_num = 1 if len(obj.shape) == 1 else obj.shape[1]
            column_names = _get_column_name_lst(column_num)
            return pd.DataFrame(obj, columns=column_names)
        elif isinstance(obj, (list, tuple)):
            return pd.DataFrame(obj, columns=[BASE_COLUMN_NAME_FOR_RETURNED_DATA_FRAME])
        elif isinstance(obj, pd.Series):
            return obj.to_frame(name=BASE_COLUMN_NAME_FOR_RETURNED_DATA_FRAME if obj.name is None else obj.name)
        else:
            return pd.DataFrame([obj], columns=[BASE_COLUMN_NAME_FOR_RETURNED_DATA_FRAME])
    except Exception as ex:
        raise TypeError(
            f'Unsupported return type. Failed to convert return value from type {type(obj)} to type pd.DataFrame.') \
            from ex


def _get_error_line_number(ex: BaseException, func_name: str) -> Union[int, None]:
    """Get line number in a specific function where error is raised. If not found, return None."""
    for tb, line_number in traceback.walk_tb(ex.__traceback__):
        if tb.f_code.co_name == func_name:
            return line_number
    return None
