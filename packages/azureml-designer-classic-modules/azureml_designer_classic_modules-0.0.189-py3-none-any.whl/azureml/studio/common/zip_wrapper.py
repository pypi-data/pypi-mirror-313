import os
import zipfile

from azureml.studio.common.error import InvalidZipFileError


class ZipFileWrapper:
    def __init__(self, file_path: str):
        """
        :param file_path: path of the zip file
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f'File: "{file_path}" does not exist.')

        self._file_path = file_path

    def extractall(self, target_dir: str):
        """
        extract zip file to target_dir
        :param target_dir: path of the target directory
        """
        if not os.path.isdir(target_dir):
            raise NotADirectoryError(f'Directory: "{target_dir}" does not exist.')

        try:
            with zipfile.ZipFile(self._file_path) as zf:
                zf.extractall(target_dir)
        except Exception as e:
            raise InvalidZipFileError() from e
