from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.modulehost.attributes import Parameter, InputPort, DataTableInputPort


class ValidateError(Exception):
    pass


def validate_parameters(entrypoint, input_values: dict):
    parameterinfos = dict((key, value) for key, value in entrypoint.__annotations__.items()
                          if isinstance(value, (Parameter, InputPort)))
    id_by_name = dict((pi.name, name) for name, pi in parameterinfos.items())
    info_by_name = dict((pi.name, pi) for pi in parameterinfos.values())

    def is_selected_in_relevancy_tree(pi):
        parent_id = id_by_name[pi.parent_parameter]

        if parent_id not in input_values:
            return False

        if input_values[parent_id] not in pi.parent_parameter_val:
            return False
        else:
            parent_pi = info_by_name[pi.parent_parameter]
            if parent_pi.parent_parameter:
                return is_selected_in_relevancy_tree(parent_pi)
            else:
                return True

    def validate_param(value, pi):
        if value is None:
            # allow optional params/ports to be None
            if pi.is_optional:
                return

            # for parameters (but not input ports), do the following additional check
            if isinstance(pi, Parameter):
                # allow hidden params to be None
                # because these params are hidden to UX,
                # UX cannot set values for these params.
                if not pi.is_released:
                    return

                # for sub parameters, allow to be None if parent is not selected.
                if pi.parent_parameter:
                    if not is_selected_in_relevancy_tree(pi):
                        return

        pi.validate_or_throw(value)

    def validate_input_port(value, pi):
        pi.validate_or_throw(value)

    result = dict(input_values)

    for name, pi in parameterinfos.items():
        # Append default value 'None' if not exist in input_values
        # TODO: rethink: should return pi.default_value if not specified in input_values?
        # value = input_values.get(name, pi.default_value)
        value = input_values.get(name)
        result[name] = value

        if isinstance(pi, InputPort):
            validate_input_port(value, pi)
            # For DataTableInputPorts, set the port's friendly name as the underlying DataTable's name.
            # Note: Do NOT remove this logic since module will use the DataTable's name for log output,
            #       error message formatting, etc.
            if isinstance(pi, DataTableInputPort) and isinstance(value, DataTable):
                value.name = pi.friendly_name
        else:
            validate_param(value, pi)

    return result
