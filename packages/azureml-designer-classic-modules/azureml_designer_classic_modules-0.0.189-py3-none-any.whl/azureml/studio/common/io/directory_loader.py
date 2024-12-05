from azureml.studio.core.io.any_directory import AnyDirectory
from azureml.studio.common.datatable.data_table_directory import DataTableDirectory
from azureml.studio.core.io.model_directory import ModelDirectory
from azureml.studio.core.io.transformation_directory import PickleTransformationDirectory


DirectoryTypes = [
    # We use DataTableDirectory/PickleTransformationDirectory instead of DataFrameDirectory/TransformationDirectory,
    # since official modules only uses these subclasses.
    AnyDirectory, DataTableDirectory, ModelDirectory, PickleTransformationDirectory
]


def load_from_directory(load_from, meta_file_path=None, model_loader=None):
    directory = AnyDirectory.load(load_from)
    for cls in DirectoryTypes:
        if cls.TYPE_NAME == directory.type:
            if cls == ModelDirectory:
                return cls.load(load_from, meta_file_path=meta_file_path, model_loader=model_loader)
            return cls.load(load_from, meta_file_path=meta_file_path)
    raise NotImplementedError(f"Not a supported directory type: {directory.meta['type']}.")
