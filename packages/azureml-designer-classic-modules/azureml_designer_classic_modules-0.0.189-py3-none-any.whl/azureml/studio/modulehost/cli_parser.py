import argparse
import os
from more_itertools import first

from azureml.studio.core.logger import module_host_logger as log
from azureml.studio.core.utils.strutils import to_cli_option_str
from azureml.studio.tool.module_collector import enumerate_module_entry
from azureml.studio.common.datatypes import DataTypes


INPUT_PORT = 'InputPortsInternal'
OUTPUT_PORT = 'OutputPortsInternal'
PARAMS = 'ModuleParameters'
GROUPS = [INPUT_PORT, OUTPUT_PORT, PARAMS]


def _make_action(name):
    """To define custom action of parsing arguments

    >>> parser = argparse.ArgumentParser()
    >>> _ = parser.add_argument(
    ...        '--untrained-model',
    ...        type=str,
    ...        dest='InputPortsInternal',
    ...        action=_make_action('Untrained model')
    ... )
    >>> vars(parser.parse_args(['--untrained-model=model_folder']))
    {'InputPortsInternal': {'Untrained model': 'model_folder'}}

    :param name: str, the name of input ports, parameters or output ports
    :return: CustomAction class
    """
    class CustomAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            group_dict = vars(namespace).get(self.dest, None)
            if group_dict:
                group_dict.update({
                    name: values
                })
            else:
                group_dict = {name: values}

            setattr(namespace, self.dest, group_dict)
    return CustomAction


class CliInputValue:
    """To store the input port info, such as name, folder."""
    def __init__(self, value):
        if os.path.isfile(value):
            self.folder = os.path.dirname(value)
            self.file_name = os.path.basename(value)
            self.data_type = DataTypes.from_file_name(self.file_name)
        else:
            self.folder = value
            self.file_name = None
            self.data_type = None
        self.extra_folder = None


class CliArgumentParser:
    """Extract information from command line arguments for ModuleHost usage."""
    def __init__(self, arguments):
        """
        :param arguments: list, command line arguments, for example:
        [
            '-m',
            'azureml.studio.modules.ml.train.train_generic_model.train_generic_model',
            '--untrained-model=untrained_model_folder',
            '--dataset=dataset_folder',
            '--label-column=label_column_string'
            '--trained-model=trained_model_string'
        ]

        """
        self._arguments = arguments
        self._parser = argparse.ArgumentParser(
            "Command Line Entry",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="A CLI to run modules."
        )
        self._module_entry = self._parse_module_entry()
        self._args_dict = self._parse_arguments()
        log.info(f"CLI arguments parsed: {self._args_dict}")

    def _parse_module_entry(self):
        """
        :return: ModuleEntry instance
        """
        self._parser.add_argument(
            '--module-name',
            type=str,
            help="The module to be run",
            required=True,
        )
        module_entry_args, _ = self._parser.parse_known_args(self._arguments)
        return first(enumerate_module_entry(module_entry_args.module_name))

    def _parse_arguments(self):
        """
        :return: dict, for example:
        {
            'InputPortsInternal': {
                'Untrained model': 'untrained_model_folder',
                'Dataset': 'dataset_folder'
            }
            'ModuleParameters': {
                'Label column': 'label_column_string'
            }
            'OutputPortsInternal': {
                'Trained model': 'trained_model_string'
            }
        }
        """
        for group in [OUTPUT_PORT, INPUT_PORT, PARAMS]:
            self._add_parser(group)
        args, _ = self._parser.parse_known_args(self._arguments)
        return vars(args)

    def _add_parser(self, group):
        parser_group = self._parser.add_argument_group(group)
        for annotation in self._get_annotations_by_group(group):
            required = getattr(annotation, 'is_optional', False) is False and \
                       getattr(annotation, 'default_value', None) is None
            kargs = {}
            if required:
                # For compatibility, currently many parameters are optional but is_optional != True
                # kargs['required'] = True
                pass
            cli_str = to_cli_option_str(annotation.name)
            parser_group.add_argument(
                cli_str,
                type=str,
                help=annotation.description,
                dest=group,
                action=_make_action(annotation.name),
                **kargs,
            )

    def _get_annotations_by_group(self, group):
        if group == INPUT_PORT:
            return self._module_entry.input_port_annotations.values()
        elif group == OUTPUT_PORT:
            return self._module_entry.output_port_annotations
        elif group == PARAMS:
            return self._module_entry.parameter_annotations.values()
        else:
            raise TypeError(f'group must be one of {GROUPS}')

    @property
    def module_entry(self):
        """
        :return: A ModuleEntry instance.
        """
        return self._module_entry

    @property
    def input_port_dict(self):
        """
        :return: a dict of input ports' name and folder path, eg:
        {
            'Untrained model': 'untrained_model_folder',
            'Dataset': 'dataset_folder'
        }
        """
        original = self._args_dict.get(INPUT_PORT) or dict()
        return {k: CliInputValue(v) for k, v in original.items() if v is not None}

    @property
    def output_port_dict(self):
        """
        :return:  a dict of output ports' name and folder path, eg:
        {'Trained model': 'trained_model_string'}
        """
        return self._args_dict.get(OUTPUT_PORT) or dict()

    @property
    def param_dict(self):
        """
        :return: a dict of parameters' name and value, eg:
        {'Label column': 'label_column_string'}
        """
        return self._args_dict.get(PARAMS) or dict()

    @property
    def credential_param_dict(self):
        # TODO: add the logic of handling credential parameters here
        return dict()

    @property
    def module_statistics_folder(self):
        return None
