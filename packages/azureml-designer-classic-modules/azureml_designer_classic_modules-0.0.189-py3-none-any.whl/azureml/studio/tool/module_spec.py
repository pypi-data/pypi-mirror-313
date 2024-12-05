from collections import OrderedDict
from azureml.core import Environment
from azureml.studio.modules.package_info import VERSION
from azureml.studio.modulehost.attributes import ModeParameter, ItemInfo, OutputPort, InputPort, Parameter, \
    ModuleMeta, ColumnPickerParameter, DataTableInputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.core.logger import common_logger as log
from azureml.studio.common.types import get_enum_values, is_null_or_empty
from azureml.studio.core.utils.strutils import quote, to_cli_option_str
from azureml.studio.modulehost.module_reflector import MODULE_META_ATTR


class ParameterStore:
    def __init__(self, module_entry=None):
        self._dict = OrderedDict({})

        if module_entry:
            for a in module_entry.input_port_annotations.values():
                self.append(a)
            for a in module_entry.output_port_annotations:
                self.append(a)
            for a in module_entry.parameter_annotations.values():
                self.append(a)

    def append(self, parameter, name=None):
        if is_null_or_empty(parameter.name):
            raise ValueError(f"Annotation {name or ''} must contain `name`")
        key = parameter.name
        if key in self._dict:
            raise ValueError(f"Parameter '{key}' already exists. Duplicate in `name`?")
        self._dict[key] = parameter

    def _get_or_none(self, name):
        return self._dict.get(name)

    @property
    def parameters(self):
        return [p for p in self._dict.values() if isinstance(p, Parameter)]

    @property
    def root_parameters(self):
        return [p for p in self.parameters if is_null_or_empty(p.parent_parameter)]

    @staticmethod
    def _append_if_absent(lst, *to_be_added):
        for item in to_be_added:
            if item not in lst:
                lst.append(item)

    def _get_nested_visible_params(self, parameter):
        result = list()
        if not parameter.is_released:
            return result

        self._append_if_absent(result, parameter)

        if isinstance(parameter, ModeParameter):
            for e in get_enum_values(parameter.data_type):
                release_state = ItemInfo.get_enum_item_released_state(e)
                if release_state is ReleaseState.Beta:
                    raise ValueError(f"ItemInfo does not support to set release state to Beta. "
                                     f"To hide the item, please set to Alpha.")
                if release_state is ReleaseState.Release:
                    child_params = [p for p in self.parameters
                                    if p.parent_parameter == parameter.name and e in p.parent_parameter_val]
                    for child in child_params:
                        self._append_if_absent(result, *self._get_nested_visible_params(child))

        return result

    @property
    def visible_parameters(self):
        visible_list = list()
        for parameter in self.root_parameters:
            self._append_if_absent(visible_list, *self._get_nested_visible_params(parameter))

        return [p for p in self.parameters if p in visible_list]

    @property
    def input_ports(self):
        return [p for p in self._dict.values() if isinstance(p, InputPort)]

    @property
    def output_ports(self):
        return [p for p in self._dict.values() if isinstance(p, OutputPort)]

    def _path_to_root(self, p):
        """
        Given a parameter, find it's parent parameter recursively towards the root parameter.

        :param p: The given parameter.
        :return: A generator which generates parameters on the path to root.
        """
        current = p
        while current.parent_parameter:
            yield current
            current = self._get_or_none(current.parent_parameter)
        yield current

    def _path_to_root_detecting_loop(self, parameter):
        """
        Get the parameters on path to root, raising error when a loop in path detected.

        :param parameter: The parameter from where to start the path-detecting.
        :return: The parameters on the path.
        """
        path = list()
        for p in self._path_to_root(parameter):
            if p in path:
                raise ValueError(f"Loop reference detected in {[p.name for p in path]}")
            path.append(p)
        return path

    def _check_loop_reference_or_throw(self):
        """
        Check if the parameters have a loop reference. Will raise error when loop detected.
        """
        verified_parameters = set()

        for p in reversed(self.parameters):
            if p not in verified_parameters:
                verified_parameters.update(self._path_to_root_detecting_loop(p))

    def _check_column_picker_parameter_or_throw(self):
        """
        Check ColumnPickerParameter must have associated with a DataTableInputPort type.
        """
        for p in self.parameters:
            if isinstance(p, ColumnPickerParameter):
                parent_name = p.column_picker_for
                if is_null_or_empty(parent_name):
                    raise ValueError(f"ColumnPickerParameter must have 'column_picker_for' specified")
                parent = self._get_or_none(parent_name)
                if not isinstance(parent, DataTableInputPort):
                    raise ValueError(f"ColumnPickerParameter '{p.name}' associated '{parent_name}' "
                                     f"must be DataTableInputPort type")

    def _validate_or_throw(self):
        for p in self.parameters:
            if isinstance(p, Parameter) and p.parent_parameter:
                if p.parent_parameter not in self._dict:
                    raise ValueError(f"Parent parameter '{p.parent_parameter}' of '{p.name}' does not exist")

                parent = self._dict[p.parent_parameter]
                if not isinstance(parent, ModeParameter):
                    raise ValueError(f"Parent parameter '{p.parent_parameter}' must be EnumeratedParameter type")

                if not p.parent_parameter_val:
                    raise ValueError(f"param_parameter_val for '{p.name}' should not be empty")
                for val in p.parent_parameter_val:
                    if not isinstance(val, parent.data_type):
                        raise ValueError(f"parent_val '{val}' of '{p.name}' is not valid type")

        self._check_column_picker_parameter_or_throw()
        self._check_loop_reference_or_throw()

    def _get_spec(self, parameter):
        d = parameter.to_dict()
        if isinstance(parameter, ModeParameter):
            child_specs = {}
            for e in get_enum_values(parameter.data_type):
                child_params = [p for p in self.parameters
                                if p.parent_parameter == parameter.name and e in p.parent_parameter_val]

                key = ItemInfo.get_enum_name(e)
                value = {
                    'DisplayValue': ItemInfo.get_enum_friendly_name(e),
                    'Parameters': [self._get_spec(child) for child in child_params if child.is_released]
                }

                # We don't add the enum mode if it is not in released state.
                # We did not add this test on top of this `for` clause, because we want
                # the child parameters be processed normally to detect any potential problems.
                release_state = ItemInfo.get_enum_item_released_state(e)
                if release_state is ReleaseState.Release:
                    child_specs[key] = value
                else:
                    log.warning(f"{e} is not in release state, skipping")

            d.update({'ModeValuesInfo': child_specs})
        return d

    def get_nested_param_spec(self, parameter):
        d = parameter.to_flat_dict()
        if isinstance(parameter, ModeParameter):
            options = []
            for e in get_enum_values(parameter.data_type):
                child_params = [p for p in self.parameters
                                if p.parent_parameter == parameter.name and e in p.parent_parameter_val]

                # We don't add the enum mode if it is not in released state.
                # We did not add this test on top of this `for` clause, because we want
                # the child parameters be processed normally to detect any potential problems.
                release_state = ItemInfo.get_enum_item_released_state(e)
                if release_state is ReleaseState.Release:
                    # TODO: ItemInfo's friendly name is not dumped into yaml spec
                    #       due to there is no storage for this information in the AML service level.
                    #       This issue will be discussed in the future.
                    key = ItemInfo.get_enum_name(e)
                    value = [self.get_nested_param_spec(child) for child in child_params if child.is_released]
                    if value:
                        options.append({key: value})
                    else:
                        options.append(key)
                else:
                    log.warning(f"{e} is not in release state, skipping")

            d.update({'options': options})
        return d

    def get_spec_tree(self):
        self._validate_or_throw()

        return {
            'InputPorts': [self._get_spec(p) for p in self.input_ports],
            'OutputPorts': [self._get_spec(p) for p in self.output_ports],
            'Parameters': [self._get_spec(p) for p in self.root_parameters if p.is_released],
        }


class ModuleSpec:
    def __init__(self, module_entry):
        self._module_entry = module_entry
        self._interface = ParameterStore(module_entry)
        self._env = None

        class_name = module_entry.class_name
        if not class_name.endswith('Module'):
            raise ValueError(f'Bad class name {quote(class_name)}: Should end with "Module".')

    @property
    def module_entry(self):
        return self._module_entry

    @property
    def meta(self):
        func = self.module_entry.func

        if not hasattr(func, '__wrapped__'):
            raise ValueError(f"no decorator for {self.module_entry}?")

        meta = getattr(func, MODULE_META_ATTR)
        if not meta:
            raise ValueError(f"no @module_entry decorator for {self.module_entry}?")
        if not isinstance(meta, ModuleMeta):
            raise TypeError(f"@module_entry expected a ModuleMeta parameter but got a {type(meta)}")
        if not hasattr(meta, 'is_deterministic'):
            raise ValueError(f"_is_deterministic must be specified for ModuleMeta in '{meta.name}'")

        return meta

    @property
    def visible_parameters(self):
        return self._interface.visible_parameters

    @property
    def input_ports(self):
        return self._interface.input_ports

    @property
    def top_level_parameters(self):
        return [p for p in self._interface.root_parameters if p.is_released]

    @property
    def output_ports(self):
        return self._interface.output_ports

    def get_command(self, spec_version=2):
        cmd = ['python', '-m', 'azureml.studio.modulehost.module_invoker',
               f'--module-name={self.module_entry.module_name}']
        if spec_version == 2:
            cmd = ['python', 'invoker.py'] + cmd
        return cmd

    _OUTPUT_FORMAT_KUBEFLOW = 'kubeflow'
    _OUTPUT_FORMAT_CSHARP_STRING_TEMPLATE = 'csharp_string_template'
    _OUTPUT_FORMAT_CLI_OPTION_MAP = 'cli_option_map'

    def _iter_args(self, output_format, spec_version=2):
        def generate_one_arg(param_type, param):
            if output_format == self._OUTPUT_FORMAT_KUBEFLOW:
                yield to_cli_option_str(param.name)
                yield {param_type: param.name}
            elif output_format == self._OUTPUT_FORMAT_CSHARP_STRING_TEMPLATE:
                yield f'{to_cli_option_str(param.name)}={{{param.friendly_name}}}'
            elif output_format == self._OUTPUT_FORMAT_CLI_OPTION_MAP:
                yield (param.friendly_name, to_cli_option_str(param.name))
            else:
                raise ValueError(f"Unknown output format {quote(output_format)}")

        for param in self.input_ports:
            if param.is_optional and spec_version == 2:
                yield list(generate_one_arg('inputPath', param))
            else:
                yield from generate_one_arg('inputPath', param)

        for param in self.visible_parameters:
            if (param.is_optional or param.parent_parameter_val) and spec_version == 2:
                yield list(generate_one_arg('inputValue', param))
            else:
                yield from generate_one_arg('inputValue', param)

        for param in self.output_ports:
            yield from generate_one_arg('outputPath', param)

    @property
    def args(self):
        return list(self._iter_args(output_format=self._OUTPUT_FORMAT_KUBEFLOW))

    def get_args(self, spec_version=2):
        return list(self._iter_args(output_format=self._OUTPUT_FORMAT_KUBEFLOW, spec_version=spec_version))

    @property
    def name(self):
        return self.meta.name

    @property
    def category(self):
        return self.meta.category

    @property
    def family_id(self):
        return self.meta.family_id

    @property
    def release_state(self):
        return self.meta.release_state

    @property
    def pass_through_in_real_time_inference(self):
        return self.meta.pass_through_in_real_time_inference

    @property
    def conda_dependencies(self):
        return self.meta.conda_dependencies

    @property
    def has_serving_entry(self):
        return self.meta.has_serving_entry

    @property
    def serving_entry(self):
        return {
            'module': self.module_entry.module_name,
            'class': self.module_entry.class_name,
            'func': self.module_entry.func_name,
        }

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, value: Environment):
        self._env = value

    @property
    def yaml_spec_dict_v2(self):
        """The dict compatible with YAML custom module spec"""
        input_port_specs = [p.to_flat_dict() for p in self.input_ports]
        parameter_specs = [self._interface.get_nested_param_spec(p) for p in self.top_level_parameters]
        output_port_specs = [p.to_flat_dict() for p in self.output_ports]

        if self.env is None:
            aml_env = {
                'amlEnvironment': {
                    'python': {
                        'condaDependencies': self.meta.conda_dependencies.conda_dependency_dict,
                    },
                    'docker': {
                        'baseImage': self.meta.module_meta_parameters.base_docker_image,
                    }
                }}
        else:
            aml_env = self.env

        container = {
            **aml_env,
            'command': self.get_command(spec_version=2),
            'args': self.get_args(spec_version=2),
        }

        dct = {
            'amlModuleIdentifier': {
                'namespace': 'azureml',
                'moduleName': self.name,
                'moduleVersion': VERSION,
            },
            'meta': {
                'collectLogs': True
            },
            'metadata': {
                'annotations': {
                    'tags': [],
                    'familyId': str(self.family_id),
                    'contact': self.meta.owner,
                    'helpDocument': self.meta.help_document,
                }
            },
            'category': self.category,
            'description': self.meta.description,
            'isDeterministic': self.meta.is_deterministic,
            'inputs': input_port_specs + parameter_specs,
            'outputs': output_port_specs,
            'implementation': {
                'container': container
            }
        }

        if self.has_serving_entry:
            dct['implementation']['servingEntry'] = self.serving_entry

        if self.pass_through_in_real_time_inference:
            if dct.get('meta'):
                dct['meta']['passThroughInRealTimeInference'] = self.pass_through_in_real_time_inference
            else:
                dct.update({
                    'meta': {
                        'passThroughInRealTimeInference': self.pass_through_in_real_time_inference,
                    }
                })

        return dct
