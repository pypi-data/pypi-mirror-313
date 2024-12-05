from enum import Enum
from pathlib import Path
from uuid import UUID

from azureml.studio.common.datatable.data_table import (DataTable, DataTableColumnSelection)
from azureml.studio.common.datatypes import DataTypes
from azureml.studio.common.error import (ErrorMapping, InvalidTransformationDirectoryError, InvalidZipFileError,
                                         InvalidDatasetError)
from azureml.studio.common.mixins import MetaExtractMixin
from azureml.studio.common.parameter_range import ParameterRangeSettings
from azureml.studio.common.types import AutoEnum, get_enum_values
from azureml.studio.common.zip_wrapper import ZipFileWrapper
from azureml.studio.core.utils.strutils import (generate_cls_str, quote, split_to_words)
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.internal.utils.dependencies import Dependencies
from azureml.studio.modules.datatransform.common.base_transform import BaseTransform
from azureml.studio.modules.package_info import PACKAGE_NAME, VERSION


DEFAULT_CPU_IMAGE = "mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:20240415.v1"
DEFAULT_GPU_IMAGE = "mcr.microsoft.com/azureml/openmpi4.1.0-cuda11.8-cudnn8-ubuntu20.04:20240415.v1"


class ItemInfo:
    __slots__ = ('_name', '_friendly_name', '_release_state')

    def __init__(self, name=None, friendly_name=None, release_state=ReleaseState.Release):
        self._name = name
        self._friendly_name = friendly_name
        self._release_state = release_state

    @property
    def name(self):
        return self._name

    @property
    def friendly_name(self):
        return self._friendly_name

    @property
    def release_state(self):
        return self._release_state

    @property
    def is_released(self):
        return self.release_state == ReleaseState.Release

    @classmethod
    def get_enum_value_by_name(cls, enum_type: type, value: str):
        for e in get_enum_values(enum_type):
            if value == cls.get_enum_name(e):
                return e
        if hasattr(enum_type, '__members__') and (value in enum_type.__members__):
            return enum_type[value]
        raise ValueError(f"Value '{value}' is not valid member of {enum_type}")

    @classmethod
    def get_enum_name(cls, enum_val: Enum) -> str:
        item_info = cls.get_item_info(enum_val)
        return item_info.name if item_info else enum_val.name

    @classmethod
    def get_enum_friendly_name(cls, enum_val: Enum):
        item_info = cls.get_item_info(enum_val)
        return item_info.friendly_name if item_info else enum_val.name

    @classmethod
    def get_enum_item_released_state(cls, enum_val: Enum) -> ReleaseState:
        item_info = cls.get_item_info(enum_val)
        return item_info.release_state if item_info else ReleaseState.Release

    @classmethod
    def get_item_info(cls, enum_val: Enum):
        enum_type = type(enum_val)
        if hasattr(enum_type, '__annotations__') and enum_val.name in enum_type.__annotations__:
            annotation = enum_type.__annotations__.get(enum_val.name)
            if isinstance(annotation, ItemInfo):
                return annotation
            else:
                # TODO: Exception type to be re-designed
                raise ValueError(f"Annotation for {enum_val} must be a ItemInfo type.")
        return None


class OutputPort(MetaExtractMixin):
    __slots__ = ('_return_type', '_name', '_friendly_name', '_description')

    def __init__(self, return_type, name=None, friendly_name=None, description=None):
        self._return_type = return_type
        self._name = name
        self._friendly_name = friendly_name or name
        self._description = description

    @property
    def return_type(self):
        return self._return_type

    @property
    def name(self):
        return self._name

    @property
    def friendly_name(self):
        return self._friendly_name

    @property
    def description(self):
        return self._description

    def to_dict(self):
        d = super().to_dict(exclude=('_return_type', ))
        d.update({
            'MarkupType': 'OutputPort',
            'Type': self._return_type.value.to_dict(),
        })
        return d

    def to_flat_dict(self):
        dct = {
            'name': self.name,
            'type': self.return_type.value.ws20_name,
        }
        if self.friendly_name != self.name:
            dct['label'] = self.friendly_name
        if self.description:
            dct['description'] = self.description
        return dct

    def __repr__(self):
        return generate_cls_str(self, quote(self.name))


class DataTableOutputPort(OutputPort):
    def __init__(self, data_type=DataTypes.DATASET, name=None, friendly_name=None, description=None):
        super().__init__(data_type, name, friendly_name, description=description)


class ILearnerOutputPort(OutputPort):
    def __init__(self, name=None, friendly_name=None, description=None):
        super().__init__(DataTypes.LEARNER, name, friendly_name, description=description)


class UntrainedLearnerOutputPort(ILearnerOutputPort):
    def __init__(self, name=None, friendly_name=None, description=None):
        super().__init__(name, friendly_name, description=description)

    def to_flat_dict(self):
        dct = super().to_flat_dict()
        dct['type'] = 'UntrainedModelDirectory'
        return dct


class IFilterOutputPort(OutputPort):
    def __init__(self, name=None, friendly_name=None, description=None):
        super().__init__(DataTypes.FILTER, name, friendly_name, description=description)


class ITransformOutputPort(OutputPort):
    def __init__(self, name=None, friendly_name=None, description=None):
        super().__init__(DataTypes.TRANSFORM, name, friendly_name, description=description)


class IClusterOutputPort(OutputPort):
    def __init__(self, name=None, friendly_name=None, description=None):
        super().__init__(DataTypes.CLUSTER, name, friendly_name, description=description)


class UntrainedClusterOutputPort(IClusterOutputPort):
    def __init__(self, name=None, friendly_name=None, description=None):
        super().__init__(name, friendly_name, description=description)

    def to_flat_dict(self):
        dct = super().to_flat_dict()
        dct['type'] = 'UntrainedModelDirectory'
        return dct


class IRecommenderOutputPort(OutputPort):
    def __init__(self, name=None, friendly_name=None, description=None):
        super().__init__(DataTypes.RECOMMENDER, name, friendly_name, description=description)


class InputPort(MetaExtractMixin):
    __slots__ = ('_data_type', '_allowed_data_types', '_name', '_friendly_name', '_is_optional', '_description')

    def __init__(self,
                 data_type,
                 allowed_data_types=None,
                 name=None,
                 friendly_name=None,
                 is_optional=False,
                 description=None):
        self._data_type = data_type
        self._allowed_data_types = allowed_data_types
        self._name = name
        self._friendly_name = friendly_name or name
        self._is_optional = is_optional
        self._description = description

    @property
    def data_type(self):
        return self._data_type

    @property
    def allowed_data_types(self):
        return self._allowed_data_types

    @property
    def name(self):
        return self._name

    @property
    def friendly_name(self):
        return self._friendly_name

    @property
    def is_optional(self):
        return self._is_optional

    @property
    def description(self):
        return self._description

    @property
    def is_model_directory_port(self):
        _MODEL_DIRECTORY_NAME = "ModelDirectory"
        return any(x.value.ws20_name == _MODEL_DIRECTORY_NAME for x in self.allowed_data_types)

    def validate_or_throw(self, value):
        """
        Validate input value, throw exception if not as required.

        :param value: Input value.
        :return: will throw exception if validate failed, otherwise do nothing.
        """
        if self.data_type is not None and value is not None:
            if self.is_model_directory_port:
                ErrorMapping.verify_model_type(value, self.data_type, arg_name=self.name)
            if not isinstance(value, self.data_type):
                reason = f"Expected {self.data_type} but got {type(value)}"
                if self.data_type == BaseTransform:
                    ErrorMapping.throw(
                        InvalidTransformationDirectoryError(
                            arg_name=self.name,
                            reason=reason,
                            troubleshoot_hint='Please rerun training experiment which generates the Transform file. '
                                              'If training experiment was deleted, please recreate '
                                              'and save the Transform file.'))
                elif self.data_type == DataTable:
                    ErrorMapping.throw(InvalidDatasetError(dataset1=self.name, reason=reason))
                elif self.data_type == ZipFileWrapper:
                    ErrorMapping.throw(InvalidZipFileError())

        if not self.is_optional:
            ErrorMapping.verify_not_null_or_empty(value, self.name)

    def validate_indicated_type_or_throw(self, data_type: DataTypes):
        """
        Validate data type of input without loading data, throw exception if not as required.

        :param data_type: Indicated data type of actual input
        :return: will throw exception if validate failed, otherwise do nothing.
        """
        if data_type is not None and self.allowed_data_types:
            if self.is_model_directory_port:
                ErrorMapping.verify_model_indicated_type(data_type=data_type,
                                                         allowed_data_types=self.allowed_data_types,
                                                         arg_name=self.friendly_name)

    def to_dict(self):
        d = super().to_dict(exclude=('_data_type', '_allowed_data_types'))
        d.update({
            'MarkupType': 'InputPort',
            'Types': [t.value.to_dict() for t in self.allowed_data_types],
        })
        return d

    def to_flat_dict(self):
        # TODO: This is a hack to get only the first item of allowed_data_types.
        #       in V2, an InputPort represents a dataset can support multiple types like
        #       Dataset|GenericCSV|GenericCSVNoHeader|GenericTSV|GenericTSVNoHeader,
        #       but in Workspace 2.0, we only support DataFrameDirectory for now,
        #       so get the first item from list works well currently.
        #       Other types of InputPorts like ModuleDirectory only support one type of input,
        #       so getting the first item will not cause any problem either.
        port_type = self.allowed_data_types[0].value.ws20_name

        dct = {
            'name': self.name,
            'type': port_type,
        }
        if self.friendly_name != self.name:
            dct['label'] = self.friendly_name
        if self.is_optional:
            dct['optional'] = self.is_optional
        if self.description:
            dct['description'] = self.description
        return dct

    def __repr__(self):
        return generate_cls_str(self, quote(self.name))


class DataTableInputPort(InputPort):
    _default_data_types = [
        DataTypes.DATASET,
        DataTypes.GENERIC_CSV,
        DataTypes.GENERIC_CSV_NO_HEADER,
        DataTypes.ARFF,
        DataTypes.GENERIC_TSV,
        DataTypes.GENERIC_TSV_NO_HEADER,
    ]

    def __init__(self, name=None, friendly_name=None, is_optional=False, description=None):
        super().__init__(DataTable, self._default_data_types, name, friendly_name, is_optional, description)


class ZipInputPort(InputPort):
    _default_data_types = [
        DataTypes.ZIP,
    ]

    def __init__(self, name=None, friendly_name=None, is_optional=False, description=None):
        super().__init__(ZipFileWrapper, self._default_data_types, name, friendly_name, is_optional, description)


class ILearnerInputPort(InputPort):
    _default_data_types = [
        DataTypes.LEARNER,
    ]

    def __init__(self, name=None, friendly_name=None, is_optional=False, description=None):
        from azureml.studio.modules.ml.common.base_learner import BaseLearner
        super().__init__(BaseLearner, self._default_data_types, name, friendly_name, is_optional, description)


class UntrainedLearnerInputPort(ILearnerInputPort):
    def __init__(self, name=None, friendly_name=None, is_optional=False, description=None):
        super().__init__(name, friendly_name, is_optional, description)

    def to_flat_dict(self):
        dct = super().to_flat_dict()
        dct['type'] = 'UntrainedModelDirectory'
        return dct


class IFilterInputPort(InputPort):
    _default_data_types = [
        DataTypes.FILTER,
    ]

    def __init__(self, name=None, friendly_name=None, is_optional=False, description=None):
        # TODO: change first parameter to IFilter class
        super().__init__(DataTable, self._default_data_types, name, friendly_name, is_optional, description)


class ITransformInputPort(InputPort):
    _default_data_types = [
        DataTypes.TRANSFORM,
    ]

    def __init__(self, name=None, friendly_name=None, is_optional=False, description=None):
        from azureml.studio.modules.datatransform.common.base_transform import BaseTransform
        super().__init__(BaseTransform, self._default_data_types, name, friendly_name, is_optional, description)


class IClusterInputPort(InputPort):
    _default_data_types = [
        DataTypes.CLUSTER,
    ]

    def __init__(self, name=None, friendly_name=None, is_optional=False, description=None):
        from azureml.studio.modules.ml.common.base_clustser import BaseCluster
        super().__init__(BaseCluster, self._default_data_types, name, friendly_name, is_optional, description)


class UntrainedClusterInputPort(IClusterInputPort):
    def __init__(self, name=None, friendly_name=None, is_optional=False, description=None):
        super().__init__(name, friendly_name, is_optional, description)

    def to_flat_dict(self):
        dct = super().to_flat_dict()
        dct['type'] = 'UntrainedModelDirectory'
        return dct


class IRecommenderInputPort(InputPort):
    _default_data_types = [
        DataTypes.RECOMMENDER,
    ]

    def __init__(self, name=None, friendly_name=None, is_optional=False, description=None):
        from azureml.studio.modules.recommendation.common.base_recommender import BaseRecommender
        super().__init__(BaseRecommender, self._default_data_types, name, friendly_name, is_optional, description)


class SelectedColumnCategory(AutoEnum):
    Numeric = ()
    Boolean = ()
    Categorical = ()
    String = ()
    Label = ()
    Feature = ()
    Score = ()
    ObjectTime = ()
    AllWithNoObjects = ()
    All = ()


class Parameter(MetaExtractMixin):
    __slots__ = ('_data_type', '_name', '_friendly_name', '_is_optional', '_description', '_default_value',
                 '_parent_parameter', '_parent_parameter_val', '_release_state')

    def __init__(self,
                 data_type,
                 name=None,
                 friendly_name=None,
                 is_optional=False,
                 description=None,
                 default_value=None,
                 parent_parameter=None,
                 parent_parameter_val=None,
                 release_state=ReleaseState.Release):
        self._data_type = data_type
        # name: the name operated by program, not changeable when created. will not be seen by end user.
        # friendly_name: the name displayed to end user, should be the same with `name` when not specified.
        self._name = name
        self._friendly_name = friendly_name or name
        self._is_optional = is_optional
        self._description = description
        self._default_value = default_value
        self._parent_parameter = parent_parameter
        self._parent_parameter_val = parent_parameter_val
        self._release_state = release_state

    @property
    def data_type(self):
        return self._data_type

    @property
    def name(self):
        return self._name

    @property
    def friendly_name(self):
        return self._friendly_name

    @property
    def is_optional(self):
        return self._is_optional

    @property
    def description(self):
        return self._description

    @property
    def default_value(self):
        return self._default_value

    @property
    def stringified_default_value(self):
        if self.default_value is None:
            return None

        return str(self.default_value)

    @property
    def parent_parameter(self):
        return self._parent_parameter

    @property
    def parent_parameter_val(self):
        return self._parent_parameter_val

    @property
    def release_state(self):
        return self._release_state

    @property
    def is_released(self):
        return self._release_state is ReleaseState.Release

    def _parameter_type_name(self):
        """
        Parameter type name should be the class name removed the tailing 'Parameter',

        Examples:
          IntParameter -> Int
          ColumnPickerParameter -> ColumnPicker
          ParameterRangeParameter -> ParameterRange
        """
        return self.__class__.__name__[:-len('Parameter')]

    def to_dict(self):
        d = super().to_dict(exclude=('_data_type', '_parent_parameter', '_parent_parameter_val', '_release_state'))
        d.update({
            'ParameterType': self._parameter_type_name(),
            'HasDefaultValue': self.default_value is not None,
            'DefaultValue': self.stringified_default_value,
            'MarkupType': 'Parameter',
        })
        return d

    def to_flat_dict(self):
        dct = {
            'name': self.name,
            'type': self._parameter_type_name(),
        }
        if self.friendly_name != self.name:
            dct['label'] = self.friendly_name
        if self.default_value is not None:
            dct['default'] = self.default_value
        if self.is_optional:
            dct['optional'] = self.is_optional
        if self.description:
            dct['description'] = self.description
        return dct

    def validate_or_throw(self, value):
        """
        Validate input parameter value, throw exception if not as required.

        :param value: Input value.
        :return: will throw exception if validate failed, otherwise do nothing.
        """
        if self.data_type is not None and value is not None and not isinstance(value, self.data_type):
            raise TypeError(f"Unexpected data type for parameter '{self.name}'."
                            f" Expected {self.data_type} but got {type(value)}.")

        if not self.is_optional:
            ErrorMapping.verify_not_null_or_empty(value, self.name)

    def __repr__(self):
        return generate_cls_str(self, quote(self.name))


class _NumericParameter(Parameter):
    __slots__ = ('_min_value', '_max_value')

    def __init__(self,
                 data_type,
                 name=None,
                 friendly_name=None,
                 is_optional=False,
                 description=None,
                 default_value=None,
                 parent_parameter=None,
                 parent_parameter_val=None,
                 release_state=ReleaseState.Release,
                 min_value=None,
                 max_value=None):
        super().__init__(data_type, name, friendly_name, is_optional, description, default_value, parent_parameter,
                         parent_parameter_val, release_state)
        self._min_value = min_value
        self._max_value = max_value

    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value

    def validate_or_throw(self, value):
        super().validate_or_throw(value)

        if self._min_value is not None:
            if self._max_value is not None:
                ErrorMapping.verify_value_in_range(value, self._min_value, self._max_value, self.friendly_name)
            else:
                ErrorMapping.verify_greater_than_or_equal_to(value, self._min_value, self.friendly_name)

        if self._max_value is not None:
            ErrorMapping.verify_less_than_or_equal_to(value, self._max_value, self.friendly_name)

    def to_flat_dict(self):
        dct = super().to_flat_dict()
        if self.default_value is not None:
            dct['default'] = self.default_value
        if self.min_value is not None:
            dct['min'] = self.min_value
        if self.max_value is not None:
            dct['max'] = self.max_value
        return dct


class IntParameter(_NumericParameter):
    def __init__(self,
                 name=None,
                 friendly_name=None,
                 is_optional=False,
                 description=None,
                 default_value=None,
                 parent_parameter=None,
                 parent_parameter_val=None,
                 release_state=ReleaseState.Release,
                 min_value=None,
                 max_value=None):
        super().__init__(int, name, friendly_name, is_optional, description, default_value, parent_parameter,
                         parent_parameter_val, release_state, min_value, max_value)


class FloatParameter(_NumericParameter):
    def __init__(self,
                 name=None,
                 friendly_name=None,
                 is_optional=False,
                 description=None,
                 default_value=None,
                 parent_parameter=None,
                 parent_parameter_val=None,
                 release_state=ReleaseState.Release,
                 min_value=None,
                 max_value=None):
        super().__init__(float, name, friendly_name, is_optional, description, default_value, parent_parameter,
                         parent_parameter_val, release_state, min_value, max_value)


class StringParameter(Parameter):
    def __init__(self,
                 name=None,
                 friendly_name=None,
                 is_optional=False,
                 description=None,
                 default_value=None,
                 parent_parameter=None,
                 parent_parameter_val=None,
                 release_state=ReleaseState.Release):
        super().__init__(str, name, friendly_name, is_optional, description, default_value, parent_parameter,
                         parent_parameter_val, release_state)


class BooleanParameter(Parameter):
    def __init__(self,
                 name=None,
                 friendly_name=None,
                 is_optional=False,
                 description=None,
                 default_value=None,
                 parent_parameter=None,
                 parent_parameter_val=None,
                 release_state=ReleaseState.Release):
        super().__init__(bool, name, friendly_name, is_optional, description, default_value, parent_parameter,
                         parent_parameter_val, release_state)


class ModeParameter(Parameter):
    def __init__(self,
                 data_type,
                 name=None,
                 friendly_name=None,
                 is_optional=False,
                 description=None,
                 default_value=None,
                 parent_parameter=None,
                 parent_parameter_val=None,
                 release_state=ReleaseState.Release):
        super().__init__(data_type, name, friendly_name, is_optional, description, default_value, parent_parameter,
                         parent_parameter_val, release_state)

    @property
    def stringified_default_value(self):
        if self.default_value is None:
            return None

        if isinstance(self.default_value, AutoEnum):
            return ItemInfo.get_enum_name(self.default_value)

        raise ValueError(f"ModeParameter default value must be of type AutoEnum")

    def to_flat_dict(self):
        dct = super().to_flat_dict()
        dct['default'] = self.stringified_default_value
        return dct


class ColumnPickerParameter(Parameter):
    __slots__ = ('_column_picker_for', '_single_column_selection', '_column_selection_categories')

    def __init__(
            self,
            name=None,
            friendly_name=None,
            is_optional=False,
            description=None,
            default_value=None,
            parent_parameter=None,
            parent_parameter_val=None,
            release_state=ReleaseState.Release,
            column_picker_for=None,
            single_column_selection=None,
            column_selection_categories=None,
    ):
        super().__init__(DataTableColumnSelection, name, friendly_name, is_optional, description, default_value,
                         parent_parameter, parent_parameter_val, release_state)

        if default_value is not None:
            raise ValueError(f"Default not supported for ColumnPickerParameter.")

        self._column_picker_for = column_picker_for
        self._single_column_selection = single_column_selection
        self._column_selection_categories = column_selection_categories

    @property
    def column_picker_for(self):
        return self._column_picker_for

    @property
    def single_column_selection(self):
        return self._single_column_selection

    @property
    def column_selection_categories(self):
        return self._column_selection_categories

    @property
    def stringified_default_value(self):
        if self.default_value is None:
            return None

        return super().stringified_default_value

    def to_flat_dict(self):
        dct = super().to_flat_dict()
        dct['columnPickerFor'] = self.column_picker_for
        if self.column_selection_categories != (SelectedColumnCategory.All, ):
            dct['columnSelectionCategories'] = self.column_selection_categories
        if self.single_column_selection:
            dct['singleColumnSelection'] = True
        return dct


class ScriptParameter(Parameter):
    __slots__ = ('_script_name', )

    FILE_TYPE_NAME = {
        '.py': 'Python',
        '.r': 'R',
        '.sql': 'Sql',
        '.json': 'Json',
    }

    def __init__(
            self,
            name=None,
            friendly_name=None,
            is_optional=False,
            description=None,
            default_value=None,
            parent_parameter=None,
            parent_parameter_val=None,
            release_state=ReleaseState.Release,
            script_name=None,
    ):
        super().__init__(str, name, friendly_name, is_optional, description, default_value, parent_parameter,
                         parent_parameter_val, release_state)
        self._script_name = script_name

    @property
    def script_name(self):
        return self._script_name

    @property
    def script_file_type(self):
        if not self.script_name:
            return None

        file_extension = Path(self.script_name).suffix
        if not file_extension:
            return None

        return self.FILE_TYPE_NAME.get(file_extension.lower())

    def to_flat_dict(self):
        dct = super().to_flat_dict()
        if self.script_file_type:
            dct['language'] = self.script_file_type
        return dct


class ParameterRangeParameter(Parameter):
    __slots__ = ('_min_limit', '_max_limit', '_is_int', '_is_log', '_slider_min', '_slider_max')

    def __init__(
            self,
            name=None,
            friendly_name=None,
            is_optional=False,
            description=None,
            default_value=None,
            parent_parameter=None,
            parent_parameter_val=None,
            release_state=ReleaseState.Release,
            min_limit=None,
            max_limit=None,
            is_int=False,
            is_log=False,
            slider_min=None,
            slider_max=None,
    ):
        super().__init__(ParameterRangeSettings, name, friendly_name, is_optional, description, default_value,
                         parent_parameter, parent_parameter_val, release_state)
        if min_limit is None or max_limit is None:
            raise ValueError("Min/Max limit can not be None for ParameterRange parameter.")

        self._min_limit = min_limit
        self._max_limit = max_limit
        self._is_int = is_int
        self._is_log = is_log
        self._slider_min = slider_min
        self._slider_max = slider_max

    @property
    def min_limit(self):
        return self._min_limit

    @property
    def max_limit(self):
        return self._max_limit

    @property
    def is_int(self):
        return self._is_int

    @property
    def is_log(self):
        return self._is_log

    @property
    def slider_min(self):
        return self._slider_min

    @property
    def slider_max(self):
        return self._slider_max

    def validate_or_throw(self, value):
        super().validate_or_throw(value)
        # Check whether the ParameterRangeSetting contains valid values
        if value is not None:
            value.verify(self.friendly_name, self.min_limit, self.max_limit)


class ModuleMetaParameters(MetaExtractMixin):
    __slots__ = ('_base_docker_image', '_gpu_support')

    def __init__(self,
                 base_docker_image=DEFAULT_CPU_IMAGE,
                 gpu_support=False):
        self._base_docker_image = base_docker_image
        self._gpu_support = gpu_support

    @property
    def base_docker_image(self):
        return self._base_docker_image

    @property
    def gpu_support(self):
        return self._gpu_support


DEFAULT_CONDA_DEPENDENCIES = Dependencies.update_from_default(
    channels=["conda-forge"],
    conda_packages=["pip=20.2", "scikit-surprise=1.1.0"],
    pip_packages=[
        "spacy==2.1.7",
        "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz#egg=en_core_web_sm",  # noqa: do not wrap long urls
        # Need to pin numpy version to avoid unexpected latest version installation due to numpy
        # required-by package installation. Version 1.21.6 makes current unit tests meet error
        # "Cannot interpret '<attribute 'dtype' of 'numpy.generic' objects>' as a data type".
        "numpy==1.19.1"
    ])


class ModuleMeta(MetaExtractMixin):
    __slots__ = ('_name', '_friendly_name', '_description', '_category', '_version', '_owner', '_family_id',
                 '_release_state', '_is_deterministic', '_conda_dependencies', '_module_meta_parameters',
                 '_pass_through_in_real_time_inference', '_has_serving_entry', '_help_document')

    def __init__(self,
                 name=None,
                 description=None,
                 category=None,
                 version=None,
                 owner=None,
                 family_id=None,
                 release_state=ReleaseState.NONE,
                 is_deterministic=None,
                 conda_dependencies=None,
                 pass_through_in_real_time_inference=False,
                 has_serving_entry=True,
                 help_document=None):
        self._name = name
        self._friendly_name = name  # add 'FriendlyName' for old version compatibility
        self._description = description
        self._category = category
        self._version = version
        self._owner = owner
        self._family_id = UUID(family_id)
        self._release_state = release_state
        self._is_deterministic = is_deterministic
        d = conda_dependencies if conda_dependencies else DEFAULT_CONDA_DEPENDENCIES
        d.add_pip_packages(f'{PACKAGE_NAME}=={VERSION}')
        self._conda_dependencies = d
        self._module_meta_parameters = ModuleMetaParameters()
        self._pass_through_in_real_time_inference = pass_through_in_real_time_inference
        self._has_serving_entry = has_serving_entry

        if help_document is None and name is not None:
            # generate help document url by default.
            self._help_document = "https://aka.ms/aml/{0}".format("-".join(split_to_words(name)).lower())
        else:
            self._help_document = help_document

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def category(self):
        return self._category

    @property
    def version(self):
        return self._version

    @property
    def owner(self):
        return self._owner

    @property
    def family_id(self):
        return self._family_id

    @property
    def release_state(self):
        return self._release_state

    @property
    def conda_dependencies(self):
        return self._conda_dependencies

    @property
    def is_deterministic(self):
        """
        Run result would be reused if is_deterministic is True.

        Examples:
          1) For 'Enter Data Manually' module, is_deterministic is True
             because the output value will not change unless input value for parameter changes.
          2) For 'Import Data' module, is_deterministic is False
             because even input value (input_url itself) does not change,
             the output value COULD change when the data under input_url location has changed.
        """
        return self._is_deterministic

    @property
    def module_meta_parameters(self):
        """Extra parameters for AzureML Service's ModuleMetaParameter (BaseDockerImage, GpuSupport, etc.)"""
        return self._module_meta_parameters

    @property
    def pass_through_in_real_time_inference(self):
        """Some modules, such as "Split Data Module", is meaningless in a real-time inference pipeline.

        These modules should be "passed through" in the inference pipeline.

        By specifying `pass_through_in_real_time_inference == True` flag to a module,
        the module will be removed when creating the real-time inference pipeline,
        and the data connected to the module's input port will be redirected to its succeeding module.
        """
        return self._pass_through_in_real_time_inference

    @property
    def has_serving_entry(self):
        """If false, a module, such as train model or tune hyperparamters, will not have a entry function in real-time
        inference pipeline and therefore should be banned.
        """
        return self._has_serving_entry

    @property
    def help_document(self):
        return self._help_document
