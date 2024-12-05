from azureml.studio.internal.attributes.release_state import ReleaseState

from azureml.studio.common.datatable.data_table import DataTable, DataTableColumnSelection
from azureml.studio.modulehost.attributes import ModuleMeta, DataTableInputPort, ModeParameter, \
    ColumnPickerParameter, SelectedColumnCategory, BooleanParameter, IntParameter, FloatParameter, StringParameter, \
    DataTableOutputPort, ITransformOutputPort
from azureml.studio.modulehost.module_reflector import BaseModule, module_entry
from azureml.studio.modules.datatransform.group_data_into_bins.group_data_into_bins_transform import QuantizationMode, \
    OutputMode, BinningNormalization, GroupDataIntoBinsTransform
from azureml.studio.core.logger import module_logger


class GroupDataIntoBinsModule(BaseModule):
    @staticmethod
    @module_entry(ModuleMeta(
        name='Group Data into Bins',
        description='Map input values to a smaller number of bins using a quantization function.',
        category='Data Transformation',
        version='0.1',
        owner='Microsoft Corporation',
        family_id='08550DD9-C5D3-4538-8188-96A9024ED92D',
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            data_table: DataTableInputPort(
                name='Dataset',
                friendly_name='Dataset',
                description='Dataset to be analyzed',
            ),
            binning_mode: ModeParameter(
                data_type=QuantizationMode,
                name='Binning mode',
                friendly_name='Binning mode',
                description='Choose a binning method',
                default_value=QuantizationMode.Quantiles,
            ),
            column_filter: ColumnPickerParameter(
                name='Columns to bin',
                friendly_name='Columns to bin',
                description='Choose columns for quantization',
                column_picker_for="Dataset",
                single_column_selection=False,
                column_selection_categories=(SelectedColumnCategory.Numeric, ),
            ),
            output_mode: ModeParameter(
                data_type=OutputMode,
                name='Output mode',
                friendly_name='Output mode',
                description='Indicate how quantized columns should be output',
                default_value=OutputMode.Append,
            ),
            categorical: BooleanParameter(
                name='Tag columns as categorical',
                friendly_name='Tag columns as categorical',
                description='Indicate whether output columns should be tagged as categorical',
                default_value=True,
            ),
            bin_count: IntParameter(
                name='Number of bins',
                friendly_name='Number of bins',
                description='Specify the desired number of bins',
                parent_parameter='Binning mode',
                parent_parameter_val=(
                        QuantizationMode.Quantiles, QuantizationMode.EqualWidth, QuantizationMode.EntropyMDL),
                min_value=1,
                default_value=10,
            ),
            normalization: ModeParameter(
                data_type=BinningNormalization,
                name='Quantile normalization',
                friendly_name='Quantile normalization',
                description='Choose the method for normalizing quantiles',
                parent_parameter='Binning mode',
                parent_parameter_val=(QuantizationMode.Quantiles, ),
                default_value=BinningNormalization.Percent,
            ),
            first_edge: FloatParameter(
                name='First edge position',
                friendly_name='First edge position',
                description='Specify the value for the first bin edge',
                parent_parameter='Binning mode',
                parent_parameter_val=(QuantizationMode.EqualWidthCustomStartAndStop, ),
                default_value=0.0
            ),
            bin_width: FloatParameter(
                name='Bin width',
                friendly_name='Bin width',
                description='Specify a custom bin width',
                parent_parameter='Binning mode',
                parent_parameter_val=(QuantizationMode.EqualWidthCustomStartAndStop, ),
                default_value=0.5
            ),
            last_edge: FloatParameter(
                name='Last edge position',
                friendly_name='Last edge position',
                description='Specify the value for the last bin edge',
                parent_parameter='Binning mode',
                parent_parameter_val=(QuantizationMode.EqualWidthCustomStartAndStop, ),
                default_value=1.0
            ),
            bin_edge_list: StringParameter(
                name='Comma-separated list of bin edges',
                friendly_name='Comma-separated list of bin edges',
                description='Type a comma-separated list of numbers to use as bin edges',
                parent_parameter='Binning mode',
                parent_parameter_val=(QuantizationMode.CustomEdges,),
            )
    ) -> (
        DataTableOutputPort(
            name='Quantized dataset',
            friendly_name='Quantized dataset',
            description='Dataset with quantized columns',
        ),
        ITransformOutputPort(
            name="Binning transformation",
            friendly_name="Binning transformation",
            description="Transformation that applies quantization to the dataset",
        )
    ):
        input_values = locals()
        return GroupDataIntoBinsModule._run_impl(**input_values)

    @classmethod
    def _run_impl(
            cls,
            data_table: DataTable,
            binning_mode: QuantizationMode,
            column_filter: DataTableColumnSelection,
            output_mode: OutputMode,
            categorical: bool,
            bin_count: int,
            normalization: BinningNormalization,
            first_edge: float,
            bin_width: float,
            last_edge: float,
            bin_edge_list: str
    ):
        module_logger.info(f'Initialize {GroupDataIntoBinsTransform.__name__} instance.')
        transform = GroupDataIntoBinsTransform(
            binning_mode,
            column_filter,
            output_mode,
            categorical,
            bin_count,
            normalization,
            first_edge,
            bin_width,
            last_edge,
            bin_edge_list
        )

        module_logger.info('Apply transform.')
        output_data_table = transform.apply(data_table)

        return output_data_table, transform
