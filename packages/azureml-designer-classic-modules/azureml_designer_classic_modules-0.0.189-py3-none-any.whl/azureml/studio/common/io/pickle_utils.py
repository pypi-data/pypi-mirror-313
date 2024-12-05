import errno
import os
import pickle

from azureml.studio.modules.package_info import VERSION as ALGHOST_VERSION
from azureml.studio.modules.package_info import PACKAGE_NAME as ALGHOST_PACKAGE_NAME
from azureml.studio.core.logger import common_logger


_ALGHOST_VERSION_ATTR = '__alghost_version__'


def read_with_pickle_from_stream(stream, check_version=True):
    obj = pickle.load(stream)
    if check_version:
        version_in_pickle_file = getattr(obj, _ALGHOST_VERSION_ATTR, None)
        if version_in_pickle_file != ALGHOST_VERSION:
            common_logger.warning(f"Version mismatch. "
                                  f"Pickle file was dumped by {ALGHOST_PACKAGE_NAME} {version_in_pickle_file} "
                                  f"but currently is {ALGHOST_VERSION}.")
    return obj


def read_with_pickle_from_file(file_name, check_version=True):
    if not os.path.isfile(file_name):
        raise FileNotFoundError(
            errno.ENOENT,
            os.strerror(errno.ENOENT),
            file_name)

    with open(file_name, 'rb') as f:
        return read_with_pickle_from_stream(f, check_version)


def write_with_pickle(obj, file_name):
    with open(file_name, 'wb') as f:
        setattr(obj, _ALGHOST_VERSION_ATTR, ALGHOST_VERSION)
        pickle.dump(obj, f, protocol=4)
