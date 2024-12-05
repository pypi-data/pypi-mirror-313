from azureml.studio.modulehost.attributes import ModuleMeta, ITransformInputPort, DataTableInputPort, \
    DataTableOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.error import ErrorMapping
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule


class ApplyTransformationModule(BaseModule):
    _param_keys = {
        "transform": "Transformation",
        "data": "Dataset",
    }

    @staticmethod
    @module_entry(ModuleMeta(
        name="Apply Transformation",
        description="Applies a well-specified data transformation to a dataset.",
        category="Model Scoring & Evaluation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="805e592d-0f1f-48eb-97c9-688ed0c1dc70",
        release_state=ReleaseState.Release,
        is_deterministic=True
    ))
    def run(
            transform: ITransformInputPort(
                name="Transformation",
                friendly_name="Transformation",
                description="A unary data transformation",
            ),
            data: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Dataset to be transformed",
            )
    ) -> (
            DataTableOutputPort(
                name="Transformed dataset",
                friendly_name="Transformed dataset",
                description="Transformed dataset",
            ),
    ):
        input_values = locals()

        ErrorMapping.verify_not_null_or_empty(
            transform, ApplyTransformationModule._param_keys.get('transform'))

        ErrorMapping.verify_not_null_or_empty(
            data, ApplyTransformationModule._param_keys.get('data'))

        return transform.apply(data),
