import os

from azureml.studio.core.logger import common_logger
from azureml.studio.core.io.data_frame_directory import DataFrameDirectory
from azureml.studio.core.utils.fileutils import ensure_folder

from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.io.pickle_utils import read_with_pickle_from_file, write_with_pickle


class DataTableDirectory(DataFrameDirectory):
    """This class is used for handling the DataTableMeta file dumped by DataTable class."""
    DATA_TABLE_META_FILE_KEY = 'DataTableMeta'
    DATA_TABLE_META_DEFAULT_FILE = 'data.dataset'

    def __init__(self, data=None, schema=None, meta=None):
        super().__init__(data, schema, meta)
        self._data_table = None

    @property
    def data_table(self):
        return self._data_table

    @data_table.setter
    def data_table(self, value):
        self._data_table = value

    @classmethod
    def load(cls, load_from_dir, meta_file_path=None, load_data=True):
        dfd = super().load(load_from_dir, meta_file_path, load_data)
        data_table_meta = None
        dt_meta_path = dfd.get_extension(cls.DATA_TABLE_META_FILE_KEY)
        if dt_meta_path:
            # Assume the path is valid
            data_table_meta = read_with_pickle_from_file(os.path.join(load_from_dir, dt_meta_path))
            cls.update_schema_according_to_data(dfd.data, data_table_meta)
            common_logger.info(f"Load DataTableMeta successfully, path={dt_meta_path}")
        dfd.data_table = DataTable.from_dfd(dfd, data_table_meta=data_table_meta)
        return dfd

    def dump(self, save_to, meta_file_path=None, overwrite_if_exist=True, validate_if_exist=False):
        if self.data_table is not None:
            self.update_extension(self.DATA_TABLE_META_FILE_KEY, self.DATA_TABLE_META_DEFAULT_FILE, override=True)
            ensure_folder(save_to)
            write_with_pickle(self.data_table.meta_data, os.path.join(save_to, self.DATA_TABLE_META_DEFAULT_FILE))
        super().dump(save_to, meta_file_path, overwrite_if_exist, validate_if_exist)
