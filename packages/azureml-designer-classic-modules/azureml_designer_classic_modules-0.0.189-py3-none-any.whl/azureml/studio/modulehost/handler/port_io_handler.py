import os
from pathlib import Path

from azureml.studio.common.error import InvalidLearnerError, InvalidDatasetError
from azureml.studio.common.datatypes import DataTypes
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_table_directory import DataTableDirectory
from azureml.studio.core.logger import TimeProfile, common_logger
from azureml.studio.core.utils.strutils import remove_suffix
from azureml.studio.modulehost.handler.sidecar_files import SideCarFileBundle, FileDumper, AzureMLOutputDumper
from azureml.studio.modulehost.handler.sidecar_files import DataFrameSchemaDumper
from azureml.studio.core.utils.fileutils import get_file_name, make_file_name, iter_files
from azureml.studio.modulehost.handler.data_handler import DataTableDatasetHandler, DataTableCsvHandler, \
    ITransformHandler, ILearnerHandler, DataTableCsvNoHeaderHandler, DataTableTsvHandler, DataTableTsvNoHeaderHandler, \
    ZipHandler, IClusterHandler, IRecommenderHandler
from azureml.studio.common.io.directory_loader import load_from_directory
from azureml.studio.core.io.transformation_directory import save_pickle_transform_to_directory, TransformationDirectory
from azureml.studio.core.io.visualizer import ExistFileVisualizer
from azureml.studio.core.io.data_frame_directory import save_data_frame_to_directory, CSV_FORMAT, DataFrameDirectory
from azureml.studio.core.io.model_directory import save_model_to_directory, ModelDirectory, pickle_loader
from azureml.studio.common.io.data_table_io import get_meta_data_file_path, write_data_table
from azureml.studio.common.io.datatable.data_table_csv_io import DataTableCsvReader
from azureml.studio.common.datatable.data_table import set_empty_columns_to_str_type


_DATA_TYPE_HANDLERS = {
    DataTypes.DATASET: DataTableDatasetHandler,
    DataTypes.GENERIC_CSV: DataTableCsvHandler,
    DataTypes.GENERIC_CSV_NO_HEADER: DataTableCsvNoHeaderHandler,
    DataTypes.GENERIC_TSV: DataTableTsvHandler,
    DataTypes.GENERIC_TSV_NO_HEADER: DataTableTsvNoHeaderHandler,
    DataTypes.TRANSFORM: ITransformHandler,
    DataTypes.LEARNER: ILearnerHandler,
    DataTypes.CLUSTER: IClusterHandler,
    DataTypes.ZIP: ZipHandler,
    DataTypes.RECOMMENDER: IRecommenderHandler,
}

_DATA_TYPE_SAVERS = {
    DataTypes.DATASET: save_data_frame_to_directory,
    DataTypes.LEARNER: save_model_to_directory,
    DataTypes.CLUSTER: save_model_to_directory,
    DataTypes.RECOMMENDER: save_model_to_directory,
    DataTypes.TRANSFORM: save_pickle_transform_to_directory,
    DataTypes.GENERIC_CSV: save_data_frame_to_directory,
}


def build_model_dumper(data_type, file_name, data):
    """Return a dumper to dump LEARNER, CLUSTER, RECOMMENDER in ModelDirectory."""

    handler = _DATA_TYPE_HANDLERS.get(data_type)
    if not handler:
        raise NotImplementedError(f"DataType {data_type} does not support output for now")

    def model_dumper(save_to):
        # Use model handler to dump model into pickle file.
        full_path = os.path.join(save_to, file_name)
        with TimeProfile(f"Dump file {file_name}"):
            handler.handle_output(data, full_path)

        return {'model_type': data_type.value.name, 'file_name': file_name}
    return model_dumper


class OutputHandler:
    @staticmethod
    def handle_output_directory(data, file_path, file_name, data_type, saver):
        """Store the output data to directory with a save function.

        This method assume that the data in the directory has been stored in old logic.
        TODO: Store the data here and replace the old logic.
        """

        # Update visualization
        visualizers = []
        extension = '.' + data_type.value.file_extension
        # Using `strutils.remove_suffix` instead of built-in `os.path.splitext` here.
        # Because some data types have multi-level extensions such as '.nh.csv', '.dataset.parquet',
        # which the built-in method does not handle correctly.
        file_name_without_extension = remove_suffix(file_name, extension)
        bundle = OutputHandler._get_or_create_bundle(data)
        if bundle.visualizer:
            visualization_file = make_file_name(
                file_name_without_extension,
                bundle.visualizer.file_extension,
            )
            visualizers = [
                ExistFileVisualizer('Visualization', visualization_file),
            ]

        extensions = {}
        kwargs = {}
        if data_type in {DataTypes.DATASET, DataTypes.GENERIC_CSV}:
            if data_type == DataTypes.DATASET:
                # Add datatable meta to extension
                dt_meta_path = get_meta_data_file_path(file_name)
                if os.path.exists(os.path.join(file_path, dt_meta_path)):
                    extensions['DataTableMeta'] = dt_meta_path

            if data_type == DataTypes.GENERIC_CSV:
                kwargs['file_format'] = CSV_FORMAT

            # Add schema of datatable
            # Check the type to avoid bug when sidecarfiles bundle is passed in some hack case of extra_folder
            if isinstance(data, DataTable):
                kwargs['schema'] = DataFrameSchemaDumper(data).dump_to_dict()
                kwargs['data'] = data.data_frame
            elif isinstance(data, SideCarFileBundle) and isinstance(data.data, DataTable):
                kwargs['schema'] = DataFrameSchemaDumper(data.data).dump_to_dict()

            # Add other fields
            kwargs['file_path'] = file_name
            kwargs['overwrite_if_exist'] = False
            kwargs['validate_if_exist'] = False

        elif data_type in {DataTypes.CLUSTER, DataTypes.LEARNER, DataTypes.RECOMMENDER}:
            # Add model_dumper for CLUSTER and LEANER and RECOMMENDER
            kwargs['model_dumper'] = build_model_dumper(data_type, file_name, data)
            kwargs['model'] = data

        elif data_type == DataTypes.TRANSFORM:
            # Add file_path for TRANSFORM
            kwargs['file_path'] = file_name
            kwargs['transform'] = data

        saver(
            save_to=file_path,
            visualizers=visualizers,
            extensions=extensions,
            **kwargs,
        )
        common_logger.info(f"Writing meta successfully, datatype={data_type}")

    @staticmethod
    def handle_output(data, file_path, file_name, data_type, sidecar_files_only=False, azureml_output_folder=None):
        # Remove columns causing pyarrow bugs, such as '__index_level_0__'.
        if data_type == DataTypes.DATASET:
            OutputHandler._handle_dataset_output(data, file_path, file_name, sidecar_files_only)

        # `data` comes from module's return tuple,
        # may be an `OutputPortBundle` or "pure" object (such as `DataTable`, `BaseLearner`, etc.).
        #   1) When `data` is a "pure" object, generate a default `OutputPortBundle` here to perform the
        #      sidecar files handling.
        #   2) When `data` is an `OutputPortBundle` object already, use it directly.
        #      Modules can generate custom visualization methods using this mechanism.
        bundle = OutputHandler._get_or_create_bundle(data)

        # dump sidecar files
        extension = '.' + data_type.value.file_extension
        # Using `strutils.remove_suffix` instead of built-in `os.path.splitext` here.
        # Because some data types have multi-level extensions such as '.nh.csv', '.dataset.parquet',
        # which the built-in method does not handle correctly.
        file_name_without_extension = remove_suffix(file_name, suffix=extension)
        dumpers = [FileDumper(file_path, file_name_without_extension)]
        if azureml_output_folder:
            dumpers.append(AzureMLOutputDumper(azureml_output_folder, file_name_without_extension))
        bundle.dump_sidecar_files(dumpers, file_name_without_extension)

        saver = _DATA_TYPE_SAVERS.get(data_type)
        if saver:
            OutputHandler.handle_output_directory(data, file_path, file_name, data_type, saver)

    @staticmethod
    def _handle_dataset_output(data, file_path, file_name, sidecar_files_only):
        if isinstance(data, SideCarFileBundle):
            data = data.data

        df, meta_data = DataFrameDirectory.remove_arrow_bug_columns_from_data_frame_and_schema(
            data.data_frame, data.meta_data)
        data = DataTable(df, meta_data)

        # Dump datatableusing the legacy method write_data_table because:
        # 1) This method has some extra logic to avoid errros compared to data_frame_to_parquet.
        # 2) There is gap between meta_data serialization with pickle and json. The difference
        #    is field 'extended_properties', which currently is not json-serializable.
        # Todo: Remove "write_data_table_meta_data_to_pickle" in "write_data_table" after extended_properties
        # Todo: is serialized by json.
        if not sidecar_files_only:
            full_path = os.path.join(file_path, file_name)
            write_data_table(data, full_path)

    @staticmethod
    def _get_or_create_bundle(obj):
        if isinstance(obj, SideCarFileBundle):
            return obj
        else:
            return SideCarFileBundle.create(obj)


class InputHandler:
    @staticmethod
    def handle_input_directory(file_path, input_port=None):
        with TimeProfile(f"Try to read from {file_path} via meta"):

            def model_loader_with_validation(load_from_dir, model_spec):
                if not ModelDirectory.is_legacy_pickle_model(load_from_dir):
                    raise InvalidLearnerError(
                        exception_message='The input model is not a valid ILearner. '
                                          'Please ensure this module is compatible with the upstream module.')

                if input_port:
                    InputHandler.validate_model_spec(model_spec, input_port)
                return pickle_loader(load_from_dir, model_spec)

            directory = load_from_directory(file_path, model_loader=model_loader_with_validation)
            common_logger.info(f"Load meta data from directory successfully, data={directory}, type={type(directory)}")

            # If the directory is DataFrame, convert it to DataTable
            if isinstance(directory, DataTableDirectory):
                dt = directory.data_table
                if is_tabular_dataset_to_dfd_input_pattern(file_path):
                    common_logger.info("Converting empty columns to string types when reading tabular dataset.")
                    set_empty_columns_to_str_type(dt)
                return dt

            # If the directory is Model, return model if model data is loaded
            elif isinstance(directory, ModelDirectory) and directory.data is not None:
                common_logger.info(f"Load {directory.TYPE_NAME} successfully, data={directory.data}")
                return directory.data

            elif isinstance(directory, TransformationDirectory) and directory.transform is not None:
                common_logger.info(f"Load {directory.TYPE_NAME} successfully, transform={directory.transform}")
                return directory.transform

            raise Exception(f"Unsupported directory type: {directory.dir_type}")

    @staticmethod
    def handle_tabular_dataset_input(file_path):
        """
        Reading raw parquet/csv files dumped by Dataset.Tabular dataset, no meta data.

        :param file_path: Directory path containing one/more parquet/csv files
        :return: DataTable instance
        """

        if not os.listdir(file_path):
            raise IOError(f'Input directory {file_path} is empty.')

        readers = [DataTable.from_raw_parquet, DataTableCsvReader.read_csv_files]
        for reader in readers:
            try:
                return reader(file_path)
            except BaseException as e:
                common_logger.warning(f'Failed to load data with {reader.__name__}. {e}')

        ex_message = f"Error reading tabular dataset from {file_path}. " \
            f"{file_path} must only contain parquet or csv file(s)."
        raise IOError(ex_message)

    @staticmethod
    def handle_input(file_path, file_name, data_type=None):
        full_path = os.path.join(file_path, file_name)
        handler = _DATA_TYPE_HANDLERS.get(data_type)
        if not handler:
            raise InvalidDatasetError(reason=f"Input data type {data_type.name} is unrecognized.")

        with TimeProfile(f"Read from '{get_file_name(full_path)}' via {handler.__name__}"):
            return handler.handle_argument_string(full_path)

    @staticmethod
    def handle_input_from_file_name(full_file_path, data_type=None):
        """De-serialization iLearner and iTransform into a python object
        Currently to support Deployment Service for reading resources

        :param full_file_path: full file path, including file name and file extension.
        :param data_type: specify data type explicitly, if not specified, refer from the file extension.
        :return: BaseLearner or BaseTransform
        """
        file_path = os.path.dirname(full_file_path)
        file_name = os.path.basename(full_file_path)

        if not data_type:
            data_type = DataTypes.from_file_name(file_name)

        return InputHandler.handle_input(file_path, file_name, data_type)

    @staticmethod
    def handle_input_one_file(file_path):
        if not os.path.exists(file_path):
            raise InvalidDatasetError(reason=f"Invalid file_path '{file_path}'")

        if os.path.isfile(file_path):
            common_logger.info(f"A regular file '{file_path}' is provided, try loading the file directly.")
            return InputHandler.handle_input_from_file_name(file_path)
        common_logger.info(f"A folder '{file_path}' is provided, try loading a valid file in the folder.")
        for f in iter_files(file_path):
            try:
                common_logger.info(f"Try loading regular file '{f}'.")
                return InputHandler.handle_input_from_file_name(f)
            except BaseException as e:
                common_logger.warning(f"Try parsing file '{f}' failed, exception={e}")
        raise InvalidDatasetError(
                reason=f"No valid input file in path '{file_path}'. Only parquet or csv file is accepted.")

    @staticmethod
    def validate_model_spec(model_spec, input_port):
        try:
            if model_spec:
                model_type = model_spec.get('model_type')
                data_type = DataTypes.from_name(model_type) if model_type else None
                input_port.validate_indicated_type_or_throw(data_type=data_type)
        except InvalidLearnerError:
            raise
        except Exception as e:
            common_logger.warning(f"Failed to validate model spec. Exception: {e}")


def is_tabular_dataset_input_pattern_without_meta(file_path: str) -> bool:
    return all(f.startswith('part-') for f in os.listdir(file_path)) or\
        all(f.endswith('.csv') for f in os.listdir(file_path)) or\
        all(f.endswith('.parquet') for f in os.listdir(file_path))


def is_tabular_dataset_to_dfd_input_pattern(file_path: str) -> bool:
    """Return whether the file_path is a input directory of dataframe directory converted from tabular dataset.

    The file structure under file_path of dataframe directory converted from tabular dataset is
    ./data/data.parquet
    ./_meta.yaml
    """
    expected_content = {Path("data"), Path("data/data.parquet"), Path("_meta.yaml")}
    content = set(i.relative_to(file_path) for i in Path(file_path).glob("**/*"))
    return expected_content == content
