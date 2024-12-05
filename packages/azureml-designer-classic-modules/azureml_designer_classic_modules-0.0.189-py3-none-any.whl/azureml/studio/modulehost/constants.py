import sys

# Many files in modulehost and modules import the following constants from here,
# the imports here is for backward compatibility to ensure those codes work well.
from azureml.studio.common.datatable.constants import ColumnTypeName, ElementTypeName  # noqa: F401

FLOAT_MIN_POSITIVE = sys.float_info.epsilon
FLOAT_MAX = sys.float_info.max
UINT32_MAX = 2 ** 32 - 1
