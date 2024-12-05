from enum import Enum
from urllib.parse import unquote

from azureml.studio.core.utils.strutils import decode_script_string
from azureml.studio.modulehost.attributes import ItemInfo, ScriptParameter
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.error import ParameterParsingError
from azureml.studio.core.logger import module_host_logger
from azureml.studio.common.parameter_range import ParameterRangeSettings


class ParameterHandler:
    def handle_argument_string(self, value_string, parameter_annotation):
        if not value_string:
            return None

        try:
            if issubclass(parameter_annotation.data_type, Enum):
                module_host_logger.info('Parse enum parameter')
                return self.parse_enum(value_string, parameter_annotation)
            elif parameter_annotation.data_type is bool:
                module_host_logger.info('Parse bool parameter')
                return self.parse_bool(value_string, parameter_annotation)
            elif parameter_annotation.data_type is int:
                module_host_logger.info('Parse int parameter')
                return self.parse_int(value_string, parameter_annotation)
            elif parameter_annotation.data_type is float:
                module_host_logger.info('Parse float parameter')
                return self.parse_float(value_string, parameter_annotation)
            elif parameter_annotation.data_type is str:
                module_host_logger.info('Parse str parameter')
                return self.parse_str(value_string, parameter_annotation)
            elif parameter_annotation.data_type is DataTableColumnSelection:
                module_host_logger.info('Parse ColumnSelection parameter')
                return self.parse_column_selection(value_string, parameter_annotation)
            elif parameter_annotation.data_type is ParameterRangeSettings:
                module_host_logger.info('Parse ParameterRangeSettings parameter')
                return self.parse_parameter_range_settings(value_string, parameter_annotation)
            elif parameter_annotation.data_type is ScriptParameter:
                return self.parse_script_parameter(value_string)
            else:
                module_host_logger.info('Return without parsing')
                return value_string
        except Exception:
            raise ParameterParsingError(
                arg_name_or_column=parameter_annotation.name,
                to_type=parameter_annotation.data_type.__name__,
                from_type='str',
                arg_value=value_string)

    @staticmethod
    def parse_enum(value_string, parameter_annotation):
        enum_type = parameter_annotation.data_type
        enum_value = ItemInfo.get_enum_value_by_name(enum_type, value_string)
        return enum_value

    @staticmethod
    def parse_bool(value_string, parameter_annotation):
        if value_string.casefold() == "True".casefold():
            return True
        elif value_string.casefold() == "False".casefold():
            return False
        else:
            raise Exception('Parse error.')

    @staticmethod
    def parse_int(value_string, parameter_annotation):
        return int(value_string)

    @staticmethod
    def parse_float(value_string, parameter_annotation):
        return float(value_string)

    @staticmethod
    def parse_str(value_string, parameter_annotation):
        return value_string

    @staticmethod
    def parse_column_selection(value_string, parameter_annotation=None):
        json_string = unquote(value_string)
        return DataTableColumnSelection(json_string)

    @staticmethod
    def parse_parameter_range_settings(value_string, parameter_annotation):
        try:
            value = float(value_string)
            if parameter_annotation.is_int:
                value = int(value)
            return ParameterRangeSettings.from_value(value)

        except ValueError:
            module_host_logger.warning(f"Failed to parse ParameterRangeSettings from value. Try parse from JSON.")
            return ParameterRangeSettings.from_json(value_string)

    @staticmethod
    def parse_script_parameter(value_string):
        # Script parameter can be zipped and base64-encoded before passing.
        # So decode and decompress the input string here. If any error occurs, pass the input string directly.
        return decode_script_string(value_string)
