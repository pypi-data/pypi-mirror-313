from azureml.studio.modulehost.attributes import ItemInfo, ModeParameter, ScriptParameter, \
    BooleanParameter, DataTableOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.attributes import ModuleMeta
from azureml.studio.common.types import AutoEnum
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.common.io.datatable.data_table_arff_reader import DataTableArffReader
from azureml.studio.common.io.datatable.data_table_csv_io import DataTableCsvReader, DataTableCsvSep
from azureml.studio.common.io.datatable.data_table_svmlight_reader import DataTableSvmLightReader


class EnterDataDataFormat(AutoEnum):
    ARFF: ItemInfo(name="ARFF", friendly_name="ARFF") = ()
    CSV: ItemInfo(name="CSV", friendly_name="CSV") = ()
    SvmLight: ItemInfo(name="SvmLight", friendly_name="SvmLight") = ()
    TSV: ItemInfo(name="TSV", friendly_name="TSV") = ()


class EnterDataModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Enter Data Manually",
        description="Enables entering and editing small datasets by typing values.",
        category="Data Input and Output",
        version="0.1",
        owner="Microsoft Corporation",
        family_id="4fbef0ab-2c8e-4a25-b5c4-7be76eac33d6",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            data_format: ModeParameter(
                EnterDataDataFormat,
                name="DataFormat",
                friendly_name="Data format",
                is_optional=False,
                default_value=EnterDataDataFormat.CSV,
                description="Select which format data will be entered",
            ),
            data: ScriptParameter(
                name="Data",
                is_optional=False,
                script_name="empty",
                description="Text to output as DataTable",
            ),
            has_header: BooleanParameter(
                name="HasHeader",
                friendly_name="Has header",
                is_optional=False,
                parent_parameter="DataFormat",
                parent_parameter_val=[EnterDataDataFormat.TSV, EnterDataDataFormat.CSV],
                default_value=True,
                description="CSV or TSV file has a header",
            )
    ) -> (
            DataTableOutputPort(
                name="dataset",
                friendly_name="Dataset",
                description="Entered data",
            ),
    ):
        """
        Enables entering and editing small datasets by typing values
        :param data_format: Select which format data will be entered
        :param data: Text to output as DataTable
        :param has_header: CSV or TSV file has a header
        :return: Entered data
        """
        return EnterDataModule._run_impl(data_format, data, has_header),

    @classmethod
    def _run_impl(cls, data_format: EnterDataDataFormat, data, has_header):
        """
        Read input into a DataTable
        :param data_format: The format of the input data which can be ARFF, CSV, SvmLight, TSV
        :param data: Input data from stream
        :param has_header: Indicates whether CSV or TSV data has a header row
        :return: Data Table
        """

        if data_format is EnterDataDataFormat.CSV or data_format is EnterDataDataFormat.TSV:
            # Remove zero-width space character in input text
            data = data.replace("\u200b", "")

            from io import StringIO
            f = StringIO(data)
            sep = DataTableCsvSep.CSV if data_format is EnterDataDataFormat.CSV else DataTableCsvSep.TSV
            return DataTableCsvReader.read(filepath_or_buffer=f,
                                           sep=sep,
                                           has_header=has_header)
        elif data_format is EnterDataDataFormat.ARFF:
            from io import StringIO
            f = StringIO(data)
            dt = DataTableArffReader.read(filepath_or_buffer=f)
            return dt
        elif data_format is EnterDataDataFormat.SvmLight:
            from io import BytesIO
            f = BytesIO(data.encode())
            dt = DataTableSvmLightReader.read(filepath_or_buffer=f)
            return dt
        else:
            raise NotImplementedError(
                f"Unsupported input '{data_format}' for parameter '{cls._args.data_format.name}'")
