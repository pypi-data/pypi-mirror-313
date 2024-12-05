import argparse
import faulthandler
import json
import pyarrow.parquet as pq

from azureml.studio.modules.package_info import VERSION as ALGHOST_VERSION
from azureml.studio.core.logger import module_host_logger as log, time_profile, set_root_logger_level
from azureml.studio.modulehost.env import JesRuntimeEnv, FolderRuntimeEnv
from azureml.studio.modulehost.input_command_parser import InputCommandParser
from azureml.studio.modulehost.cli_parser import CliArgumentParser
from azureml.studio.modulehost.module_reflector import ModuleReflector


def execute(args):
    original_args = args
    # Add this line to enable native-level stack traces.
    # https://docs.python.org/3/library/faulthandler.html
    faulthandler.enable()

    parser = argparse.ArgumentParser("module executor")
    parser.add_argument('--command-file', type=str, help="Command file to be parsed")
    parser.add_argument('--log-level', choices=['debug', 'info', 'warning', 'error', 'fatal'], default='debug')
    parser.add_argument('--module-name', type=str, help="The module to be run")

    args, _ = parser.parse_known_args(args)
    command_file = args.command_file
    log_level = args.log_level.upper()
    set_root_logger_level(log_level)
    log.info(f"Reset logging level to {log_level}")

    # PyArrow depends on new libstdc++ API, so we need to load it as early as possible
    # Because some other library might depend on the classic libstdc++ API, if these libraries are loaded first,
    # PyArrow will fail on writing parquet.
    # If all packages are installed by conda or pip in one time, this issue would be avoided since conda or pip
    # will resolve the dependencies automatically.
    # If user install some packages separately, this issue would happen.
    # For more details, please see: https://jira.apache.org/jira/browse/ARROW-3346
    log.info(f"Load pyarrow.parquet explicitly: {pq}")

    if args.module_name is not None:
        return execute_with_cli(original_args)

    with open(command_file, "r") as f:
        command_dict = json.load(f)
        execute_with_env(command_dict, JesRuntimeEnv())


@time_profile
def execute_with_cli(args):
    log.info(f"ALGHOST {ALGHOST_VERSION}")
    parser = CliArgumentParser(args)
    do_execute_with_env(parser, FolderRuntimeEnv())


@time_profile
def execute_with_env(command_dict, env):
    log.info(f"ALGHOST {ALGHOST_VERSION}")
    parser = InputCommandParser(command_dict)
    do_execute_with_env(parser, env)


def do_execute_with_env(parser, env):
    ModuleReflector(parser.module_entry, env).exec(
        input_ports=parser.input_port_dict,
        output_ports=parser.output_port_dict,
        parameters=parser.param_dict,
        credential_parameters=parser.credential_param_dict,
        module_statistics_folder=parser.module_statistics_folder
    )
