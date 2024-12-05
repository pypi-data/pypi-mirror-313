import os

from azureml.studio.common.error import (ErrorMapping,
                                         FailedToEvaluateScriptError,
                                         InvalidTransformationDirectoryError)
from azureml.studio.common.io.datatable.data_table_csv_io import (
    DataTableCsvReader, DataTableCsvSep)
from azureml.studio.common.zip_wrapper import ZipFileWrapper
from azureml.studio.core.logger import module_host_logger
from azureml.studio.modulehost.io.reader import Reader
from azureml.studio.modulehost.io.writer import Writer


class DataTableCsvHandler:
    @staticmethod
    def handle_argument_string(file_name):
        module_host_logger.info('Read DataTable from CSV with header')
        return DataTableCsvReader.read(
            filepath_or_buffer=file_name,
            sep=DataTableCsvSep.CSV,
            has_header=True)


class DataTableCsvNoHeaderHandler:
    @staticmethod
    def handle_argument_string(file_name):
        module_host_logger.info('Read DataTable from CSV without header')
        return DataTableCsvReader.read(
            filepath_or_buffer=file_name,
            sep=DataTableCsvSep.CSV,
            has_header=False)


class DataTableTsvHandler:
    @staticmethod
    def handle_argument_string(file_name):
        module_host_logger.info('Read DataTable from TSV with header')
        return DataTableCsvReader.read(
            filepath_or_buffer=file_name,
            sep=DataTableCsvSep.TSV,
            has_header=True)


class DataTableTsvNoHeaderHandler:
    @staticmethod
    def handle_argument_string(file_name):
        module_host_logger.info('Read DataTable from TSV without header')
        return DataTableCsvReader.read(
            filepath_or_buffer=file_name,
            sep=DataTableCsvSep.TSV,
            has_header=False)


class DataTableDatasetHandler:

    @staticmethod
    def handle_argument_string(file_name):
        module_host_logger.info('Read DataTable from Dataset')
        return Reader.read_into_data_table(file_name)


class ITransformHandler:
    @staticmethod
    def handle_argument_string(file_name):
        if not os.path.isfile(file_name):
            _raise_input_asset_not_found_error(
                file_path=file_name,
                detail_message='Please check the train experiment which generates the Transform file '
                               'has been deleted or not. If deleted, please re-generate and save the Transform file.'
            )
        with open(file_name, 'rb') as f:
            try:
                transform = ITransformHandler.handle_stream_source(f)
            except AttributeError as e:
                ErrorMapping.rethrow(e, InvalidTransformationDirectoryError(
                    arg_name=file_name,
                    reason=ErrorMapping.get_exception_message(e),
                    troubleshoot_hint='Please rerun training experiment which generates the Transform file. '
                                      'If training experiment was deleted, please recreate and save the Transform file.'
                ))
        return transform

    @staticmethod
    def handle_stream_source(stream):
        module_host_logger.info('Read transform')
        return Reader.read_into_base_transform(stream)


class ILearnerHandler:
    @staticmethod
    def handle_argument_string(file_name):
        if not os.path.isfile(file_name):
            _raise_input_asset_not_found_error(
                file_path=file_name,
                detail_message='Please check the train experiment which generates the Learner file '
                               'has been deleted or not. If deleted, please re-generate and save the Learner file.'
            )
        with open(file_name, 'rb') as f:
            learner = ILearnerHandler.handle_stream_source(f)

        return learner

    @staticmethod
    def handle_stream_source(stream):
        module_host_logger.info('Read learner')
        return Reader.read_into_base_learner(stream)

    @staticmethod
    def handle_output(learner, file_name):
        module_host_logger.info('Write learner')
        try:
            Writer.write_into_base_learner(learner, file_name)
        except (TypeError, AttributeError, RuntimeError) as err:
            # If a TypeError or AttributeError is raised, it may be caused by a customized model
            # when calling pickle.dump
            import re
            from azureml.studio.modules.python_language_modules.create_python_model.create_python_model import \
                CustomModelProxy, SCRIPT_LANGUAGE
            if isinstance(learner, CustomModelProxy):
                if isinstance(err, RuntimeError):
                    if re.match('Pickling of ".*" instances is not enabled',
                                ErrorMapping.get_exception_message(err),
                                re.IGNORECASE) is None:
                        raise
                err_msg = ErrorMapping.get_exception_message(err)
                ErrorMapping.rethrow(err, FailedToEvaluateScriptError(
                    script_language=SCRIPT_LANGUAGE,
                    message=f"Got exception when dumping custom model with pickle: '{err_msg}'.",
                ))
            else:
                raise


class IRecommenderHandler:
    @staticmethod
    def handle_output(recommender, file_name):
        module_host_logger.info("Write recommender")
        Writer.write_into_base_recommender(recommender, file_name)


class IClusterHandler:
    @staticmethod
    def handle_argument_string(file_name):
        if not os.path.isfile(file_name):
            _raise_input_asset_not_found_error(
                file_path=file_name,
                detail_message='Please check the train experiment which generates the Cluster file '
                               'has been deleted or not. If deleted, please re-generate and save the Cluster file.'
            )
        with open(file_name, 'rb') as f:
            cluster = IClusterHandler.handle_stream_source(f)

        return cluster

    @staticmethod
    def handle_stream_source(stream):
        module_host_logger.info('Read cluster')
        return Reader.read_into_base_cluster(stream)

    @staticmethod
    def handle_output(cluster, file_name):
        module_host_logger.info('Write cluster')
        Writer.write_into_base_cluster(cluster, file_name)


class ZipHandler:
    @staticmethod
    def handle_argument_string(file_name):
        module_host_logger.info('Read zip file')
        return ZipFileWrapper(file_name)


def _raise_input_asset_not_found_error(file_path, detail_message):
    raise FileNotFoundError(f'File: "{file_path}" does not exist: {detail_message}')
