from abc import ABC

from azureml.studio.common.datatable.data_table import DataTable


class BaseTransform(ABC):

    def apply(self, dt: DataTable):
        pass
