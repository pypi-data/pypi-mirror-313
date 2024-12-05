import json
import math
import re
from enum import Enum
from json.decoder import JSONDecodeError
from typing import Union

import jsonschema

from azureml.studio.common.error import ErrorMapping, ParameterParsingError
from azureml.studio.core.logger import common_logger
from .types import get_enum_values

PARAMETER_TYPE_INTEGER = "Integer"
PARAMETER_TYPE_DOUBLE = "Double"


class ParameterRangeSettings:
    SCHEMA = {
        'description': 'An object that defines a range',
        'type': 'object',
        'properties': {
            'ParameterType': {'type': 'string'},
            'useRangeBuilder': {'type': 'boolean'},
            'literal': {'type': 'string'},
            'isLogarithmic': {'type': 'boolean'},
            'minValue': {'type': 'number'},
            'maxValue': {'type': 'number'},
            'count': {'type': 'number'}
        }
    }

    @staticmethod
    def from_json(s: str):
        try:
            obj_dict = json.loads(s)
            jsonschema.validate(obj_dict, ParameterRangeSettings.SCHEMA)

            prs = ParameterRangeSettings()

            if 'useRangeBuilder' in obj_dict and obj_dict['useRangeBuilder']:
                prs.is_literal = obj_dict.get('useRangeBuilder', False)
                prs.min = obj_dict.get('minValue', 0)
                prs.max = obj_dict.get('maxValue', 0)
                prs.count = obj_dict.get('count', 0)
                prs.is_log = obj_dict.get('isLogarithmic', False)
                prs.is_literal = True
            else:
                prs.parameter_type = obj_dict.get('ParameterType', None)
                prs.is_literal = False
                prs.literal_as_string = obj_dict.get('literal', None)
            prs.is_literal = not prs.is_literal
            return prs

        except (JSONDecodeError, jsonschema.ValidationError):
            common_logger.warning(f"Failed to parse '{s}' to ParameterRangeSettings as JSON.")
            return ParameterRangeSettings.from_literal(s)

    @staticmethod
    def from_value(val: Union[int, float]):
        is_int = isinstance(val, int)
        prs = ParameterRangeSettings(is_int=is_int)
        prs.list.append(val)
        prs.is_literal = True
        return prs

    @staticmethod
    def from_literal(literal: str):
        is_int = ("." not in literal)
        prs = ParameterRangeSettings(is_int=is_int)
        prs.is_literal = True
        prs.literal_as_string = literal.replace(';', ',')
        return prs

    def __init__(self, min_val=0, max_val=0, count=0, is_int=False, is_log=False):
        self._literal_string = None
        self.parameter_type = None
        self.list = []
        self.is_literal = False
        self.min = min_val
        self.max = max_val
        self.count = count
        self.parameter_type = PARAMETER_TYPE_INTEGER if is_int else PARAMETER_TYPE_DOUBLE
        self.is_log = is_log

    @property
    def literal_as_string(self):
        return self._literal_string

    @literal_as_string.setter
    def literal_as_string(self, value):
        self._literal_string = value
        self._parse_literal()

    def _parse_literal(self):
        if self.parameter_type == PARAMETER_TYPE_INTEGER:
            re_index = re.compile(r'^\s*(?P<item>-?\d+)\s*$')
        else:
            re_index = re.compile(r'^\s*(?P<item>(-?\d+\.?\d*([eE]-?\d+))|(-?\d*\.?\d+))\s*$')

        re_index_range = re.compile(r'^\s*(?P<start>-?\d+)\s*-\s*(?P<end>-?\d+)\s*$')

        self.list = []
        for item_string in self._literal_string.split(','):
            match = re_index.match(item_string)
            if match:
                self.list.append(float(match.group('item')))
            else:
                match = re_index_range.match(item_string)
                if match:
                    start_val = int(match.group('start'))
                    end_val = int(match.group('end'))
                    self.list += range(start_val, end_val + 1)

        self.count = len(self.list)

    def __str__(self):
        return json.dumps(self.__dict__)

    def verify(self, arg_name, min_limit, max_limit):
        if not self.list:
            # now the ParameterRangeSetting can not be initialized with RangeBuilder, so we simply add
            # self._literal_string to the error message
            ErrorMapping.throw(
                ParameterParsingError(arg_name_or_column=arg_name, arg_value=self._literal_string, from_type="str",
                                      to_type="ParameterRange"))

        for val in self.list:
            ErrorMapping.verify_value_in_range(val, min_limit, max_limit, arg_name=arg_name)


def is_numeric_type(t: type):
    return t in [int, float]


class Sweepable:
    @staticmethod
    def from_prs(name, prs: ParameterRangeSettings):
        if prs.parameter_type == PARAMETER_TYPE_INTEGER:
            attr_type = int
            if prs.is_literal:
                return Sweepable(name, attr_type, False, values=[int(v) for v in prs.list])
        else:
            attr_type = float
            if prs.is_literal:
                return Sweepable(name, attr_type, False, values=[float(v) for v in prs.list])

        return Sweepable(name, attr_type, prs.is_log, min_val=prs.min, max_val=prs.max, num_grids=prs.count)

    def __init__(self, name, attr_type: type, log_scale: bool = False, values: list = None,
                 min_val=None, max_val=None, num_grids: int = 0):
        self._name = name
        self._attribute_type = attr_type

        if issubclass(attr_type, Enum):
            self._log_scale = False
            self._attribute_value = get_enum_values(attr_type)
        elif values:
            self._log_scale = False
            self._attribute_value = values
            if is_numeric_type(attr_type):
                self._regenerate_min_max()
        else:
            self._log_scale = log_scale
            self._min_val = min_val
            self._max_val = max_val
            self._num_grids = num_grids
            self._regenerate_values()

    @property
    def name(self):
        return self._name

    @property
    def attribute_type(self):
        return self._attribute_type

    @property
    def log_scale(self):
        return self._log_scale

    @log_scale.setter
    def log_scale(self, value):
        self._log_scale = value
        self._regenerate_values()

    @property
    def attribute_value(self):
        return self._attribute_value

    @attribute_value.setter
    def attribute_value(self, value):
        self._attribute_value = value

    @property
    def max_value(self):
        return self._max_val

    @max_value.setter
    def max_value(self, value):
        self._max_val = value
        self._regenerate_values()

    @property
    def min_value(self):
        return self._min_val

    @min_value.setter
    def min_value(self, value):
        self._min_val = value
        self._regenerate_values()

    @property
    def num_grids(self):
        return self._num_grids

    @num_grids.setter
    def num_grids(self, value):
        self._num_grids = value
        self._regenerate_values()

    def _regenerate_values(self):
        if is_numeric_type(self.attribute_type):
            temp_list = []
            interval = 0
            if self._num_grids > 0:
                if self.log_scale:
                    interval = (math.log(self.max_value) - math.log(self.min_value)) / self.num_grids
                    interval = math.exp(interval)
                else:
                    interval = (self.max_value - self.min_value) / self.num_grids

            p = self.min_value
            temp_list.append(p)
            for i in range(1, self.num_grids):
                if self.log_scale:
                    p *= interval
                else:
                    p += interval
                temp_list.append(p)
            temp_list.append(self.max_value)

            if self.attribute_type == float:
                self._attribute_value = temp_list
            elif self.attribute_type == int:
                self._attribute_value = [int(v) for v in temp_list]
        else:
            raise Exception("Cannot sweep over learner of type: {0}".format(self.name))

    def _regenerate_min_max(self):
        if is_numeric_type(self.attribute_type):
            self._num_grids = len(self._attribute_value)
            self._max_val = max(self._attribute_value)
            self._min_val = min(self._attribute_value)
        else:
            raise Exception("Cannot sweep over learner of type: {0}".format(self.name))

    def __str__(self):
        buf = []
        buf.extend(["[", str(self.attribute_type), "]"])
        if is_numeric_type(self.attribute_type):
            if self._log_scale:
                buf.append("(logScale) ")
            buf.extend(["Min=", str(self.min_value), " "])
            buf.extend(["Max=", str(self.max_value), " "])
            buf.extend(["NumGrid=", str(self.num_grids), " "])
        elif issubclass(self.attribute_type, Enum):
            buf.append(",".join([e.name for e in get_enum_values(self.attribute_type)]))
        return ''.join(buf)
