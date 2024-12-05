import copy
import pyarrow.parquet as pq

from azureml.studio.core.io.data_frame_directory import DataFrameDirectory
from azureml.studio.core.utils.strutils import to_variable_name
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.modulehost.attributes import InputPort
from azureml.studio.modules.package_info import VERSION as ALGHOST_VERSION
from azureml.studio.core.logger import module_logger as log
from azureml.studio.modulehost.handler.parameter_handler import ParameterHandler
from azureml.studio.modulehost.handler.sidecar_files import SideCarFileBundle

RETURN_KEY = "return"


class DeploymentServiceModuleHost:
    def __init__(self, module_entry):
        log.info(f"ALGHOST {ALGHOST_VERSION}")

        # PyArrow depends on new libstdc++ API, so we need to load it as early as possible
        # Because some other library might depend on the classic libstdc++ API, if these libraries are loaded first,
        # PyArrow will fail on writing parquet.
        # If all packages are installed by conda or pip in one time, this issue would be avoided since conda or pip
        # will resolve the dependencies automatically.
        # If user install some packages separately, this issue would happen.
        # For more details, please see: https://jira.apache.org/jira/browse/ARROW-3346
        log.info(f"Load pyarrow.parquet explicitly: {pq}")

        self._method = module_entry.func

        self._parameters_dict = dict()
        self._resources_dict = dict()
        self._input_ports = dict()
        self._global_parameters_dict = dict()

    @property
    def parameters_dict(self):
        return self._parameters_dict

    @parameters_dict.setter
    def parameters_dict(self, param_dict):
        self._parameters_dict = param_dict

    @property
    def resources_dict(self):
        return self._resources_dict

    @resources_dict.setter
    def resources_dict(self, dictionary):
        # Deep copy resources to avoid mutating resources by other modules
        # This is only necessary for deployment service, where modules are executed
        # in the same process
        for resource_name, resource in dictionary.items():
            self._resources_dict.update({
               resource_name: copy.deepcopy(resource)
            })

    def execute(self, input_ports=None, global_parameters_dict=None):
        if input_ports:
            # Deep copy input_ports to avoid mutating input ports by other modules
            # This is only necessary for deployment service, where modules are executed
            # in the same process
            for port_name, port in input_ports.items():
                if isinstance(port, DataFrameDirectory):
                    port = DataTable.from_dfd(port)
                # We assume that DS only provides DataFrameDirectory/DataTable as input_ports,
                # so the port instance cannot be any other types.
                if not isinstance(port, DataTable):
                    raise TypeError(f'Unexpected port type: {port.__class__.__name__}')
                self._input_ports.update({
                    port_name: copy.deepcopy(port)
                })

        if global_parameters_dict:
            self._global_parameters_dict = global_parameters_dict

        parameter_values = self._initialize_parameters()

        output = self._method(**parameter_values)

        # `output` may be an tuple of `OutputPortBundle` or "pure" object (such as `DataTable`, `BaseLearner`, etc.).
        # When `data` is an `OutputPortBundle` object here, get the "pure" object out from it as a result to return.
        output_data_tables = tuple(o.data if isinstance(o, SideCarFileBundle) else o for o in output)
        # Output the data as DFD instead of DataTable
        output_data_frame_directories = tuple(
            DataFrameDirectory.create(
                data=table.data_frame,
                schema=table.meta_data.to_dict(),
                compute_visualization=False,
            ) if isinstance(table, DataTable) else table for table in output_data_tables
        )
        return output_data_frame_directories

    @staticmethod
    def normalize_port_name(name):
        """Normalize port names to AzureML Service compatible format.

        In AzureML Service, port names are not allowed to contain whitespaces.
        Use this method to replace all the whitespaces with underscores.

        NOTE: Do NOT edit the implementation of this method.

              This implementation must keep the same with the module register logic,
              which is currently located in the following property:
              azureml.studio.tools.module_spec._BaseParam.data_reference_name
        """
        return to_variable_name(name, separator='_')

    def _initialize_parameters(self):
        parameter_values = dict()
        argument_dict = self._group_arguments()

        parameter_annotations = self._method.__annotations__
        for parameter_name, annotation in parameter_annotations.items():
            name = annotation.name if hasattr(annotation, "name") else None
            if name:
                # When registering modules, we replaced the spaces in port names with underscores,
                # due to a limitation of AzureML Service that does not allow whitespaces in port names.
                # Thus, when invoking modules in deployment mode, the port names passed to module host
                # will not match with the original names. So we added this two lines here as a workaround.
                if isinstance(annotation, InputPort) and name not in argument_dict:
                    name = self.normalize_port_name(name)

                if name in argument_dict:
                    input_value = argument_dict[name]
                    value = ParameterHandler().handle_argument_string(input_value, annotation)
                    parameter_values.update({parameter_name: value})

        return parameter_values

    def _group_arguments(self):
        return {**self._parameters_dict, **self._resources_dict,
                **self._input_ports, **self._global_parameters_dict}
