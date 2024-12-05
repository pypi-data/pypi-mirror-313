import os
import subprocess
import tempfile
from shutil import copyfile

from pandas.core.dtypes.common import is_categorical_dtype

from azureml.studio.core.data_frame_schema import DataFrameSchema
from azureml.studio.core.schema import ElementTypeName
from azureml.studio.core.utils.jsonutils import dump_to_json_file, load_json_file

from azureml.studio.common.datatable.data_type_conversion import convert_column_by_element_type
from azureml.studio.modulehost import validator
from azureml.studio.modulehost.attributes import ItemInfo, ModuleMeta, DataTableInputPort, ZipInputPort, \
    ScriptParameter, IntParameter, ModeParameter, DataTableOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import FailedToEvaluateScriptError, ErrorMapping
from azureml.studio.common.io.data_table_io import data_frame_to_parquet, data_frame_from_parquet
from azureml.studio.core.logger import TimeProfile, module_logger
from azureml.studio.common.types import AutoEnum
from azureml.studio.internal.utils.dependencies import Dependencies
from azureml.studio.core.utils.fileutils import ensure_folder
from azureml.studio.common.zip_wrapper import ZipFileWrapper
from azureml.studio.modulehost.custom_module_args import CustomModuleArguments
from azureml.studio.modulehost.custom_module_utils import CustomModuleUtils
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule


class ExecuteRScriptRVersion(AutoEnum):
    R310: ItemInfo(name="CRAN R 3.1.0", friendly_name="CRAN R 3.1.0") = ()
    R322: ItemInfo(name="Microsoft R Open 3.2.2", friendly_name="CRAN R 3.2.2") = ()
    R351: ItemInfo(name="Microsoft R Open 3.5.1", friendly_name="MRAN R 3.5.1") = ()

    def get_version(self):
        if self is self.R310:
            return "3.1.0"
        elif self is self.R322:
            return "3.2.2"
        elif self is self.R351:
            return "3.5.1"


R_SCRIPT_SAMPLE = """
# R version: 3.5.1
# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# Please note that functions dependant on X11 library
# such as "View" are not supported because X11 library
# is not pre-installed.

# The entry point function MUST have two input arguments.
# If the input port is not connected, the corresponding
# dataframe argument will be null.
#   Param<dataframe1>: a R DataFrame
#   Param<dataframe2>: a R DataFrame
azureml_main <- function(dataframe1, dataframe2){
  print("R script run.")

  # If a zip file is connected to the third input port, it is
  # unzipped under "./Script Bundle". This directory is added
  # to sys.path.

  # Return datasets as a Named List
  return(list(dataset1=dataframe1, dataset2=dataframe2))
}

"""
SCRIPT_FILE_PREFIX = "user_script"


class ExecuteRScriptModule(BaseModule):
    SCRIPT_LANGUAGE = "R"
    SCRIPT_ENTRY = "azureml_main"

    @staticmethod
    @module_entry(ModuleMeta(
        name="Execute R Script",
        description="Executes an R script from an Azure Machine Learning designer pipeline.",
        category="R Language",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="30806023-392B-42E0-94D6-6B775A6E0FD5",
        release_state=ReleaseState.Release,
        is_deterministic=True,
        conda_dependencies=Dependencies.update_from_default(
            channels=["conda-forge"],
            conda_packages=["pip=20.2",
                            "r=3.5.1",
                            "r-reticulate=1.12",
                            "r-randomforest=4.6",
                            "r-caret=6.0",
                            "r-e1071=1.7",
                            "r-nnet=7.3",
                            "r-glmnet=2.0",
                            "r-mgcv=1.8",
                            "r-cluster=2.1.0",
                            "r-nlme=3.1",
                            "r-tseries=0.10",
                            "r-dplyr=0.8.5",
                            "r-matrix=1.2",
                            "r-plyr=1.8.6",
                            "r-rpart=4.1",
                            "r-timedate=3043.102",
                            "r-forcats=0.5.0",
                            "r-stringr=1.4.0",
                            "r-catools=1.17.1",
                            "r-rocr=1.0",
                            "r-igraph=1.2.4",
                            "r-rodbc=1.3",
                            "r-forecast=8.12",
                            "r-mclust=5.4.6",
                            "r-tidyverse=1.2.1"],
            # Pin numpy version to avoid type error caused by unexpected latest version installation.
            pip_packages=["numpy==1.19.1"]
        )
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
                description="Set of R sources",
            ),
            r_stream_reader: ScriptParameter(
                name="R Script",
                friendly_name="R script",
                description="Specify a StreamReader pointing to the R script sources",
                script_name="script.R",
                default_value=R_SCRIPT_SAMPLE
            ),
            seed: IntParameter(
                name="Random Seed",
                friendly_name="Random seed",
                is_optional=True,
                description="Define a random seed value for use inside the R environment. Calls \"set.seed(value)\" ",
                min_value=0,
            ),
            r_lib_version: ModeParameter(
                ExecuteRScriptRVersion,
                name="R Version",
                friendly_name="R Version",
                description="Specify the version of R that the script will be run against.",
                default_value=ExecuteRScriptRVersion.R351,
                release_state=ReleaseState.Alpha
            )
    ) -> (
            DataTableOutputPort(
                name="Result Dataset",
                friendly_name="Result dataset",
                description="Output Dataset",
            ),
            DataTableOutputPort(
                name="R Device",
                friendly_name="Result dataset2",
                description="Output Dataset2",
            ),
    ):
        input_values = locals()
        validator.validate_parameters(ExecuteRScriptModule.run, input_values)
        return _run_impl(**input_values)


def _run_impl(
        dataset1: DataTable,
        dataset2: DataTable,
        bundle_file: ZipFileWrapper,
        r_stream_reader: str,
        seed: int,
        r_lib_version: ExecuteRScriptRVersion):
    if not r_lib_version:
        r_lib_version = ExecuteRScriptRVersion.R351
    CustomModuleUtils.check_r_package_installed(r_lib_version.get_version())

    with tempfile.TemporaryDirectory() as temp_dir_name:
        from azureml.studio.core.utils.strutils import generate_random_string
        # Prepare r script
        module_logger.info('Prepare r script')
        custom_script_file = f"{generate_random_string()}.R"
        with open(os.path.join(temp_dir_name, custom_script_file), "w") as text_file:
            text_file.write(r_stream_reader)

        # Check and extract bundle zip file
        module_logger.info('Check and extract bundle zip file')
        extract_to_path = os.path.join(temp_dir_name, 'Script Bundle')
        ensure_folder(extract_to_path)

        if bundle_file:
            bundle_file.extractall(extract_to_path)

        # Add current temporary directory into sys.path
        module_logger.info('Add current temporary directory into sys.path')
        CustomModuleUtils.add_directory_to_sys_path(temp_dir_name)
        CustomModuleUtils.add_directory_to_sys_path(extract_to_path)

        # Prepare input and output parquet paths
        module_logger.info('Prepare input and output parquet paths')
        r_input_parquet_path_1 = f"{generate_random_string()}.parquet"
        r_input_parquet_path_2 = f"{generate_random_string()}.parquet"
        r_input_schema_path_1 = f"{generate_random_string()}.json"
        r_input_schema_path_2 = f"{generate_random_string()}.json"
        r_output_parquet_path_1 = f"{generate_random_string()}.parquet"
        r_output_parquet_path_2 = f"{generate_random_string()}.parquet"
        r_output_schema_path_1 = f"{generate_random_string()}.json"
        r_output_schema_path_2 = f"{generate_random_string()}.json"

        # This is a temporary solution to dump the schema.json file manually with dump_to_json_file.
        # In the future, we would rewrite the Execute R Script with the Custom Module pattern,
        # and R script would handle the DataFrameDirectory directly.
        if dataset1 is not None:
            # Uncategorize categorical column in input dataset.
            # Otherwise pd$read_parquet in R script will raise error due to pandas is upgraded to 1.0.4.
            _uncategorize_categorical_column(dataset1)
            data_frame_to_parquet(dataset1.data_frame, os.path.join(temp_dir_name, r_input_parquet_path_1))
            dump_to_json_file(dataset1.meta_data.to_dict(), os.path.join(temp_dir_name, r_input_schema_path_1))
        if dataset2 is not None:
            _uncategorize_categorical_column(dataset2)
            data_frame_to_parquet(dataset2.data_frame, os.path.join(temp_dir_name, r_input_parquet_path_2))
            dump_to_json_file(dataset2.meta_data.to_dict(), os.path.join(temp_dir_name, r_input_schema_path_2))

        # Prepare arguments for R script
        module_logger.info('Prepare arguments for R script')
        arguments = CustomModuleArguments(
            input_paths=[r_input_parquet_path_1, r_input_parquet_path_2],
            input_schema_paths=[r_input_schema_path_1, r_input_schema_path_2],
            output_paths=[r_output_parquet_path_1, r_output_parquet_path_2],
            output_schema_paths=[r_output_schema_path_1, r_output_schema_path_2],
            custom_script=custom_script_file
        )

        # TODO: test this solution in AML Service with Pip package
        # TODO: refine this solution
        script_dir = os.path.dirname(os.path.realpath(__file__))
        entry_script_file = f"{SCRIPT_FILE_PREFIX}_{generate_random_string()}.R"
        copyfile(os.path.join(script_dir, "r_module_entry.R"),
                 os.path.join(temp_dir_name, entry_script_file))

        try:
            # Invoke script function
            exec_status_file = os.path.join(temp_dir_name, f"{generate_random_string()}.status")
            with TimeProfile('Execute R script'):
                subprocess.run(
                    f"Rscript {entry_script_file} {arguments.encoded_in_json()} {exec_status_file}",
                    cwd=temp_dir_name, shell=True)

            _validate_exec_status(exec_status_file)

            # Fix bug: 458229
            # The indexes of R data.frame are in str type, which is incompatible with the default behavior
            # of Python dataframe. So, it's required to reset_index here to convert the indexes to int type.
            with TimeProfile('Read output Parquet files to DataFrame'):
                result1 = data_frame_from_parquet(
                    os.path.join(temp_dir_name, r_output_parquet_path_1)).reset_index(drop=True)
                result_data_table_1 = _recover_schema(result1, os.path.join(temp_dir_name, r_output_schema_path_1))
                result2 = data_frame_from_parquet(
                    os.path.join(temp_dir_name, r_output_parquet_path_2)).reset_index(drop=True)
                result_data_table_2 = _recover_schema(result2, os.path.join(temp_dir_name, r_output_schema_path_2))

            # Verify if all column names are string
            ErrorMapping.verify_column_names_are_string(result1.columns)
            ErrorMapping.verify_column_names_are_string(result2.columns)

            return result_data_table_1, result_data_table_2
        except Exception as ex:
            ErrorMapping.throw(FailedToEvaluateScriptError(
                ExecuteRScriptModule.SCRIPT_LANGUAGE,
                f"Got exception when invoking script: '{ErrorMapping.get_exception_message(ex)}'."
            ))


def _validate_exec_status(exec_status_file):
    if os.path.exists(exec_status_file):
        with open(exec_status_file, 'r') as text_file:
            exec_status = text_file.read()
            if exec_status.strip():
                raise RuntimeError(f"Script failed with error message:\n{exec_status}")
    else:
        raise RuntimeError(f"Failed to find execution status file {exec_status_file}. "
                           "Please check driver log for detailed error info. "
                           "A possible cause is the compute target does not have enough memory. "
                           "In such case, please use a compute target with more memory.")


def _recover_schema(df, output_schema_file):
    """
    This is a temporary solution to solve the schema consistence for now.
    For long term, the execute r script would be rewrite as a custom module with R framework directly.
    :param output_schema_file:
    :param dataframe:
    :return:
    """
    if os.path.exists(output_schema_file):
        schema = DataFrameSchema.from_dict(load_json_file(output_schema_file))
        for column_attribute in schema.column_attributes:
            column = df[column_attribute.name]
            if column_attribute.element_type == ElementTypeName.CATEGORY and not is_categorical_dtype(column):
                df[column_attribute.name] = column.astype('category')
    else:
        schema = None

    return DataTable(df, meta_data=schema)


def _uncategorize_categorical_column(dt: DataTable):
    for col_name in dt.column_names:
        if dt.get_element_type(col_name) == ElementTypeName.CATEGORY:
            dt.data_frame[col_name] = \
                convert_column_by_element_type(dt.data_frame[col_name], ElementTypeName.UNCATEGORY)
