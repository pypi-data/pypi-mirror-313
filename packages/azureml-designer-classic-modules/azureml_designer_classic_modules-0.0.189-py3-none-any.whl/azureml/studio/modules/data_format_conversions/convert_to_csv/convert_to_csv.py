from azureml.studio.modulehost.attributes import ModuleMeta, DataTableInputPort, DataTableOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.datatypes import DataTypes
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule


class ConvertToCSVModule(BaseModule):
    _param_keys = {
        "dt": "Dataset",
    }

    @staticmethod
    @module_entry(ModuleMeta(
        name="Convert to CSV",
        description="Converts data input to a comma-separated values format.",
        category="Data Transformation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="FAA6BA63-383C-4086-BA58-7ABF26B85814",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            dt: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Input dataset",
            )
    ) -> (
            DataTableOutputPort(
                data_type=DataTypes.GENERIC_CSV,
                name="Results dataset",
                friendly_name="Results dataset",
                description="Output dataset",
            ),
    ):
        input_values = locals()

        return dt.clone(),
