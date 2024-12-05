from argparse import Namespace
from functools import wraps
from importlib import import_module
import os
from inspect import isfunction

from more_itertools import first

from azureml.studio.modules.package_info import PACKAGE_NAME, VERSION
from azureml.studio.modulehost import validator
from azureml.studio.common.error import ErrorMapping, ModuleError, LibraryExceptionError, InvalidDatasetError, \
    ModuleErrorInfo, LibraryErrorInfo, CUSTOMER_SUPPORT_GUIDANCE, ModuleOutOfMemoryError, UserErrorInfo
from azureml.studio.core.logger import module_host_logger as log, log_dict_values, TimeProfile, log_list_values, \
    time_profile, module_host_logger
from azureml.studio.core.error import UserError
from azureml.studio.modulehost.env import JesRuntimeEnv
from azureml.studio.modulehost.handler.parameter_handler import ParameterHandler
from azureml.studio.modulehost.attributes import InputPort, Parameter, OutputPort, ModuleMeta
from azureml.studio.core.utils.jsonutils import dump_to_json
from azureml.studio.internal.io.rwbuffer_manager import AzureMLOutput
from azureml.studio.internal.module_telemetry import ModuleTelemetryHandler


RETURN_KEY = "return"
MODULE_META_ATTR = '_module_meta'
MODULES_HAVE_CUSTOMIZED_OUTPUT = {'Execute Python Script'}


class ArgHolder(Namespace):
    _cache = dict()

    def __init__(self, func):
        super().__init__()
        for name, annotation in func.__annotations__.items():
            if isinstance(annotation, (Parameter, InputPort)):
                setattr(self, name, annotation)

    @classmethod
    def from_func(cls, func):
        if func not in cls._cache:
            cls._cache[func] = ArgHolder(func)
        return cls._cache.get(func)


def module_entry(meta: ModuleMeta = None):

    # @module_entry is supposed to be applied with a param,
    # if no params provided, input value type would be a <function> type.
    #
    # Add a check here to avoid these misuse.
    #
    # Do:
    # ```
    #   @module_entry(ModuleMeta(...))
    #   def func()
    # ```
    #
    # Don't:
    # ```
    #   @module_entry
    #   def func()
    # ```
    if isfunction(meta):
        raise ValueError(f"{meta}: @module_entry decorator must contain a ModuleMeta parameter")

    def _module_entry_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if args:
                raise ValueError(f"Module entry must be called as kwargs style.")

            with TimeProfile(func.__qualname__):
                log_dict_values("kwargs", kwargs, truncate_long_item_text=True)
                validated_args = validator.validate_parameters(func, kwargs)
                log_dict_values("validated_args", validated_args, truncate_long_item_text=True)
                ret = func(*args, **validated_args)
                log_list_values("return", ret)
                return ret

        # Set module meta as an attribute to the wrapper.
        # This value will be checked in `validate_decorator_as_a_module_entry`.
        setattr(wrapper, MODULE_META_ATTR, meta)
        return wrapper

    return _module_entry_decorator


def is_valid_module_entry(func):
    """
    Given a callable `func`, check the decorators for the func
    to judge if this func is a valid module entry.

    Will raise error if any misuse in decorators was detected.

    :param func: func to be checked.
    :return: True if is a module entry, else False.
    """
    # If user annotated with a decorator, `func` will have a `__wrapped__` attribute.
    # This is the by Python's design. (Magic lays inside `@wraps`.)
    if hasattr(func, '__wrapped__'):
        # In normal cases, our '@module_entry' decorator will automatically generate a
        # `MODULE_META_ATTR attribute to the wrapper itself.
        # If no such attribute exists, the decorate must not be '@module_entry'.
        # So raise error here.
        if not hasattr(func, MODULE_META_ATTR):
            raise ValueError(f"{func}: must have a @module_entry decorator")

        # Assert that `MODULE_META_ATTR` attribute value must be a ModuleMeta type.
        # Raise error if not as expected.
        meta = getattr(func, MODULE_META_ATTR)
        if meta is None:
            raise ValueError(f"{func}: @module_entry must have a ModuleMeta parameter")
        if not isinstance(meta, ModuleMeta):
            raise TypeError(f"{func}: @module_entry's parameter is expected to be a ModuleMeta type"
                            f" but got {type(meta)}")
        else:
            # `func` will be a valid module entry if code goes here, so return True.
            return True

    # Function with no decorators will fall down to here,
    # This is a normal function, not a module entry.
    # Simply return False in this case.
    return False


def is_module_entry(func):
    """
    Same as `is_valid_module_entry`, but do not raise Exceptions.

    :param func: func to be checked.
    :return: True if is a module entry, else False.
    """
    try:
        return is_valid_module_entry(func)
    except (TypeError, ValueError):
        return False


class ModuleEntry:
    def __init__(self, module_name, class_name, method_name=None):
        self._module_name = module_name
        self._class_name = class_name
        self._method_name = method_name

    @classmethod
    def from_dict(cls, d):
        return ModuleEntry(d['ModuleName'], d['ClassName'], d['MethodName'])

    @classmethod
    def from_func(cls, func):
        module_name = func.__module__
        method_name = func.__name__
        class_name = func.__qualname__[:-len(method_name)-1]
        return ModuleEntry(module_name, class_name, method_name)

    @property
    def module_name(self):
        return self._module_name

    @property
    def class_name(self):
        return self._class_name

    @property
    def func_name(self):
        return self._method_name

    @property
    def cls(self):
        module = import_module(self._module_name)
        return getattr(module, self._class_name)

    @property
    def func(self):
        """
        A callable python function
        """
        return getattr(self.cls, self._method_name)

    @property
    def input_port_annotations(self):
        return {k: v for k, v in self.func.__annotations__.items() if isinstance(v, InputPort)}

    @property
    def output_port_annotations(self):
        return [a for a in self.func.__annotations__[RETURN_KEY] if isinstance(a, OutputPort)]

    @property
    def parameter_annotations(self):
        return {k: v for k, v in self.func.__annotations__.items() if isinstance(v, Parameter)}

    def to_dict(self):
        return {
            'ModuleEntry': {
                'ModuleName': self._module_name,
                'ClassName': self._class_name,
                'MethodName': self._method_name,
                'PipRequirement': f"{PACKAGE_NAME}=={VERSION}",
            }
        }

    def __str__(self):
        return f"ModuleEntry({self._module_name}; {self._class_name}; {self._method_name})"


class ModuleMetaClass(type):
    """
    This metaclass is designed to inject an `_args` object into module class.

    `_args` is an `ArgHolder` object, which acts like a key-value reference,
    easy to get annotations for each parameter in module entry.

    For example, there is a `data_format` parameter in EnterDataModule class,
    source code snippet listed as below:

    ```python
    def run(
            data_format: ModeParameter(
                EnterDataDataFormat,
                name="DataFormat",
                friendly_name="DataFormat",
                is_optional=False,
                default_value=EnterDataDataFormat.CSV,
                description="Select which format data will be entered",
            ),
            ...
            )
    ```

    We can retrieve annotation object for `data_format` by:

    ```python
    cls._args.data_format
    ```

    e.g. If we want to get `friendly_name` for `data_format`, just use:

    ```python
    cls._args.data_format.friendly_name
    ```
    """
    def __new__(mcs, name, bases, namespace, **kargs):
        # Only check subclasses, do not check for base class.
        if name != 'BaseModule':
            entry_func = mcs._get_module_entry(namespace)
            if entry_func is None:
                raise ValueError(f"No module entry found in {name}.")

            # Append `_args` object into module class
            args = ArgHolder.from_func(entry_func)
            cls = super().__new__(mcs, name, bases, namespace)
            setattr(cls, '_args', args)

            return cls

        return super().__new__(mcs, name, bases, namespace)

    @classmethod
    def _iter_all_functions(mcs, namespace):
        """
        Iterate all callable items in given `namespace`.
        Where `namespace` is the parameter passed to metaclass's `__new__` method,
        which contains all methods of the about-to-create class object.

        :param namespace: the `namespace` parameter passed to `__new__` method.
        :return: the callable functions.
        """
        for item in namespace.values():
            if isinstance(item, (staticmethod, classmethod)):
                # If item is a staticmethod or classmethod,
                # we must get the wrapped real callable function using __get__ method.
                yield item.__get__(object)
            elif callable(item):
                yield item

    @classmethod
    def _get_module_entry(mcs, namespace):
        """
        Get module entry function from given namespace.
        Where `namespace` is the parameter passed to metaclass's `__new__` method,
        which contains all methods of the about-to-create class object.

        :param namespace: the `namespace` parameter passed to `__new__` method.
        :return: the first callable function which is a module entry.
                 return `None` if no module entry found.
        """
        return first(mcs._iter_all_functions(namespace), default=None)


class BaseModule(metaclass=ModuleMetaClass):
    """
    Base class for all modules.
    """

    # @module_entry decorator will create a `_args` attr for each module at runtime.
    # We add this field in base class to avoid pylint 'no-member' error.
    _args = None


class ModuleStatistics:
    ERROR_INFO_FILE = 'error_info.json'
    _AZUREML_STATISTICS_FOLDER = 'module_statistics'

    def __init__(self):
        self._error_info = None
        try:
            self._telemetry_handler = ModuleTelemetryHandler()
        except Exception as ex:
            module_host_logger.error(f"Failed to initialize ModuleTelemetryHandler instance due to {ex}")
            self._telemetry_handler = None

    @property
    def error_info(self):
        return {'Exception': self._error_info.to_dict() if self._error_info else None}

    @error_info.setter
    def error_info(self, error: BaseException):

        if not isinstance(error, BaseException):
            raise TypeError('Input error must be BaseException Type')

        if isinstance(error, ModuleError):
            self._error_info = ModuleErrorInfo(error)

        elif isinstance(error, UserError):
            self._error_info = UserErrorInfo(error)

        else:
            self._error_info = LibraryErrorInfo(error)

    def save_to_file(self, env, folder):
        env.save_module_statistics_to_file(self.error_info, folder, self.ERROR_INFO_FILE)

    @time_profile
    def save_to_azureml(self):
        azureml_file_path = os.path.join(self._AZUREML_STATISTICS_FOLDER, self.ERROR_INFO_FILE)
        with AzureMLOutput.open(azureml_file_path, 'w') as f:
            dump_to_json(self.error_info, f)

    @time_profile
    def log_stack_trace_telemetry(self, session_id: str = None):
        if self._telemetry_handler:
            self._telemetry_handler.log_telemetry(
                designer_event_name="Traceback",
                traceback=self._error_info.traceback,
                session_id=session_id,
                error_message=self._error_info.message,
            )
        else:
            module_host_logger.error(
                "Failed to log stack trace due to failing to initialize ModuleTelemetryHandler instance.")


class ModuleReflector:

    def __init__(self, entry, env=JesRuntimeEnv()):
        self._entry = entry
        self._env = env
        self._module_statistics = ModuleStatistics()

    def exec(self, input_ports, output_ports, parameters, credential_parameters=None, module_statistics_folder=None):
        try:
            log.info(f"Invoking {self._entry}")
            log_dict_values('Input Ports', input_ports)
            log_dict_values('Output Ports', output_ports)
            log_dict_values('Parameters', parameters, truncate_long_item_text=True)
            log_dict_values('Environment Variables', os.environ, key_filter=JesRuntimeEnv.is_valid_env_name)

            try:
                with TimeProfile('Reflect input ports and parameters'):
                    reflected_input_ports = self._reflect_input_ports(input_ports)
                    reflected_parameters = self._reflect_parameters(parameters)

                if credential_parameters:
                    reflected_credential_parameters = self._reflect_parameters(credential_parameters)
                    reflected_parameters.update(reflected_credential_parameters)

                # Execute the method
                output_tuple = self._entry.func(**reflected_input_ports, **reflected_parameters)
                # Handle outputs
                self._handle_output_ports(output_tuple, output_ports)
            except KeyError as key_error:
                # Bug ID: 480862
                # When using pandas.dataframe,
                # pandas.core.indexing._LocIndexer._getbool_axis will catch the exception and convert it to KeyError.
                # In this case, when MemoryError occurs, we can only catch a KeyError,
                # so we catch the KeyError and check whether it is caused by a MemoryError,
                # if it is caused by a MemoryError, we rethrow it as ModuleOutOfMemoryError
                if len(key_error.args) > 0 and isinstance(key_error.args[0], MemoryError):
                    ErrorMapping.rethrow(e=key_error, err=ModuleOutOfMemoryError())
                else:
                    raise key_error
            except MemoryError as mem_error:
                ErrorMapping.rethrow(e=mem_error,
                                     err=ModuleOutOfMemoryError())
        except BaseException as bex:
            self._handle_exception(bex)
        finally:
            self._save_statistics(module_statistics_folder)

    def _save_statistics(self, module_statistics_folder):
        try:
            # Output module statistics
            if module_statistics_folder:
                module_host_logger.info(f"Save module statistics to json")
                self._module_statistics.save_to_file(self._env, module_statistics_folder)

            self._module_statistics.save_to_azureml()
        except BaseException as bex:
            log.error(f"Exception occurs when saving module statistics: {bex}")

    def _reflect_input_ports(self, input_values):
        result = dict()
        for var_name, annotation in self._entry.input_port_annotations.items():
            # extra_output is a environment variable, which points to the path to dump
            # sidecar files of input data
            input_value = input_values.get(annotation.name, None)
            value = self._env.handle_input_port(annotation, input_value)
            result.update({var_name: value})
        return result

    def _reflect_parameters(self, input_values):
        result = dict()
        for var_name, annotation in self._entry.parameter_annotations.items():
            if annotation.name in input_values:
                input_value = input_values.get(annotation.name, None)
                value = ParameterHandler().handle_argument_string(input_value, annotation)
                result.update({var_name: value})
        return result

    @time_profile
    def _handle_output_ports(self, module_return, output_ports):
        try:
            for index, annotation in enumerate(self._entry.output_port_annotations):
                # return data (a tuple) is in the same order as annotations
                data = module_return[index]
                output_value = output_ports.get(annotation.name, None)
                self._env.handle_output_port(data, annotation, output_value)
        except UserError:
            raise  # If a UserError is raised, directly raises it.
        except ModuleError:
            raise  # If a ModuleError is raised, directly raises it.
        except MemoryError:
            raise  # If a MemoryError is raised, directly raises it.
        except BaseException as bex:
            if self._entry.func._module_meta.name in MODULES_HAVE_CUSTOMIZED_OUTPUT:
                raise InvalidDatasetError(dataset1=annotation.friendly_name, reason=str(bex)) from bex
            raise RuntimeError(f"Get exception when generating outputs.") from bex

    def _handle_exception(self, exception):

        module_host_logger.info(f"Set error info in module statistics")
        self._module_statistics.error_info = exception
        with TimeProfile("Logging exception information of module execution"):
            # Try to print the session id for better debugging Dataset issues.
            session_id = None
            try:
                from azureml._base_sdk_common import _ClientSessionId
                session_id = _ClientSessionId
            except Exception:
                module_host_logger.info('Session_id cannot be imported.')

            try:
                self._module_statistics.log_stack_trace_telemetry(session_id)
            except Exception as e:
                module_host_logger.exception(f'Failed to log error traceback due to {e}')

            if isinstance(exception, ModuleError):
                module_host_logger.exception(f"Get ModuleError when invoking {self._entry}")
                raise exception
            elif isinstance(exception, UserError):
                module_host_logger.exception(f"Get UserError when invoking {self._entry}")
                raise exception
            else:
                module_host_logger.exception(f"Get library exception when invoking {self._entry}")
                ErrorMapping.rethrow(
                    e=exception,
                    err=LibraryExceptionError(exception, CUSTOMER_SUPPORT_GUIDANCE)
                )
