import os
import sys
import json
from abc import abstractmethod
from importlib import import_module
import argparse
import inspect
import glob
from pathlib import Path
from azureml.core import Environment
from pkgutil import iter_modules
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.error import AlghostRuntimeError
from azureml.studio.core.utils.fileutils import clear_folder
from azureml.studio.core.utils.strutils import join_stripped
from azureml.studio.core.utils.yamlutils import dump_to_yaml
from azureml.studio.modulehost.module_reflector import ModuleEntry, BaseModule, is_valid_module_entry
from azureml.studio.tool.module_spec import ModuleSpec
from azureml.studio.tool.checkers import assert_str_val_pass_rules


class SpecHandler:
    @abstractmethod
    def handle_specs(self, specs: list):
        pass


class UpdateEnvironmentHandler(SpecHandler):
    DEFAULT_ENV_FOLDER = Path(__file__).parent / 'output' / 'environments'
    DEFINITION_FILE_NAME = "azureml_environment.json"
    ENV_CONFIG_FILE = "env_config.json"

    def __init__(self, env_folder: Path = DEFAULT_ENV_FOLDER):
        self.env_folder = env_folder
        self.env_config = self.load_env_config()

    @staticmethod
    def get_readable_environment_name(module_name):
        if module_name in ('Execute R Script',):
            env_name = 'AzureML-Designer-R'
        else:
            env_name = 'AzureML-Designer'

        return env_name

    def load_env_config(self):
        config_path = self.env_folder / self.ENV_CONFIG_FILE
        try:
            with open(config_path, 'r') as f:
                env_config = json.load(f)
        except FileNotFoundError:
            env_config = {}
        return env_config

    def handle_specs(self, specs: list):
        loaded_env = {}

        for env_def_path in glob.glob(f"{self.DEFAULT_ENV_FOLDER}/**/{self.DEFINITION_FILE_NAME}"):
            env_def_folder = Path(env_def_path).parent
            env = Environment.load_from_directory(str(env_def_folder))
            loaded_env[env.name] = env

        # set env in module spec
        for s in specs:
            s.env = self.env_config[self.get_readable_environment_name(s.name)]


class PrintStatisticsHandler(SpecHandler):
    def handle_specs(self, specs: list):
        print("\n--------------------------------------------------------------")
        self._print_module_category_tree(specs)
        print("\n--------------------------------------------------------------\n")
        self._print_module_statistics(specs)
        print("\n--------------------------------------------------------------\n")

    @staticmethod
    def _print_module_category_tree(specs):
        last_category = None
        for index, module in enumerate(specs, start=1):
            category = module.category
            if category != last_category:
                print(f"\n  {category}")
                last_category = category

            name = module.name
            release_state = module.release_state
            released = release_state == ReleaseState.Release

            marker = '*' if released else '-'
            badge = f"[{release_state.name.upper()}]" if not released else None
            print(f"    {join_stripped(marker, badge, name)}")

    @staticmethod
    def _print_module_statistics(specs):
        def count_by_state(state):
            return sum(m.release_state == state for m in specs)

        count_by_states = {s.name: count_by_state(s) for s in ReleaseState}
        formatted_counts = [f"{count} {name}" for name, count in count_by_states.items() if count > 0]
        print(f"  Total {len(specs)} ({join_stripped(*formatted_counts, sep=', ')}) Modules.")


class SaveYamlSpecV2Handler(SpecHandler):
    def __init__(self, folder):
        os.makedirs(folder, exist_ok=True)
        self._folder = folder

    def handle_specs(self, specs: list):
        # Clear module path first, to detect module deletion
        clear_folder(self._folder)

        for s in specs:
            output_folder = os.path.join(self._folder, s.release_state.name.lower())
            os.makedirs(output_folder, exist_ok=True)
            self._save_yaml_spec_to_file(s, output_folder, lambda spec: spec.yaml_spec_dict_v2)

    @staticmethod
    def _save_yaml_spec_to_file(spec, folder, get_spec_func):
        module_name = _normalize_module_name(spec.name)
        file_name = f"{module_name}.yaml"
        with open(os.path.join(folder, file_name), 'w') as f:
            dump_to_yaml(get_spec_func(spec), f)


def _normalize_module_name(module_name):
    return module_name.replace(' ', '_').lower()


def _class_type_looks_like_a_module(cls):
    return issubclass(cls, BaseModule) and cls is not BaseModule


def _class_name_looks_like_a_module(cls):
    return cls.__name__.endswith('Module') and not cls.__name__ == 'BaseModule'


def _class_looks_like_a_module(cls):
    return _class_type_looks_like_a_module(cls) or _class_name_looks_like_a_module(cls)


def _validate_module_class(cls):
    if not _class_type_looks_like_a_module(cls):
        raise TypeError(f"{cls} must inherit from BaseModule.")

    if not _class_name_looks_like_a_module(cls):
        raise ValueError(f"{cls}: class name must end with 'Module'.")


def _enumerate_simple_modules(module_name, exclude=()):
    module = import_module(module_name)

    # Use __path__ attr to determine whether a module is a 'simple module' or a 'package module'.
    # A 'simple module' refers to a python file, and a 'package module' refers to a folder.
    # Detailed documentation: https://docs.python.org/3/reference/import.html#module-path
    path = getattr(module, '__path__', None)
    is_simple_module = path is None

    for module_name_suffix in exclude:
        if module.__name__.endswith(module_name_suffix):
            return

    if is_simple_module:
        # For 'simple module's, simply yield.
        yield module
    else:
        # For 'package module's, find simple modules recursively to yield.
        for module_spec in iter_modules(path=path, prefix=f"{module_name}."):
            sub_module_name = module_spec.name
            yield from _enumerate_simple_modules(sub_module_name, exclude=exclude)


def _enumerate_classes_in_module(module):
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            # Filter the classes roughly, and then check strictly.
            # The purpose for taking this strategy is that we want to detect human mistakes
            # (say, forgot to inherit from BaseModule) as much as we can.
            if _class_looks_like_a_module(obj):
                _validate_module_class(obj)
                yield obj


def _enumerate_functions_in_class(cls):
    for name, obj in inspect.getmembers(cls):
        if inspect.isfunction(obj):
            yield obj


def _enumerate_module_entry_in_class(cls):
    for f in _enumerate_functions_in_class(cls):
        try:
            if is_valid_module_entry(f):
                entry = ModuleEntry.from_func(f)
                yield entry
        except (ValueError, TypeError) as e:
            raise AlghostRuntimeError(f"Failed to create spec for {cls}") from e


def enumerate_module_entry(base_module_name, exclude=()):
    for module in _enumerate_simple_modules(base_module_name, exclude=exclude):
        for cls in _enumerate_classes_in_module(module):
            entries_detected = 0
            for entry in _enumerate_module_entry_in_class(cls):
                try:
                    entries_detected += 1
                    yield entry
                except GeneratorExit:
                    return
                except BaseException as e:
                    raise AlghostRuntimeError("Failed to generate module entry") from e
            if entries_detected <= 0:
                raise AlghostRuntimeError(f"{cls}: No module entry detected.")
            elif entries_detected > 1:
                raise AlghostRuntimeError(f"{cls}: Detected {entries_detected} module entries."
                                          f" Supposed to be only one.")


def _enumerate_module_specs(base_module_name, exclude=()):
    for entry in enumerate_module_entry(base_module_name, exclude):
        yield ModuleSpec(entry)


def get_module_spec_list(base_module_name, exclude=(), release_state_filter=None):
    result = []
    seen = {}

    for spec in _enumerate_module_specs(base_module_name, exclude=exclude):
        family_id = spec.family_id
        if family_id in seen:
            if seen[family_id] == spec:
                # Say, `EnterData.run` method is defined in modules.dataio.enter_data.enter_data,
                # and imported in the test source in modules.dataio.enter_data.tests.test_enter_data,
                # the method will be detected in both modules, with the same python object id.
                # We just simply skip the duplicate case here since it is not a family-id-duplicate error.
                print(f"    already seen, skip")
                continue

            raise ValueError(f"'{spec.name}': Duplicate family id with '{seen[family_id].name}'")

        seen.update({family_id: spec})
        if release_state_filter is None or spec.release_state in release_state_filter:
            result.append(spec)

    return result


def _output_path(*name):
    script_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_path, 'output', *name)


def _assert_module_meta_is_valid(spec):
    str_attrs = ['name', 'description']
    for attr in str_attrs:
        assert_str_val_pass_rules(getattr(spec.meta, attr))


def main(args):
    parser = argparse.ArgumentParser(
        "Module Collector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""A CLI tool to collect modules and generate spec files.

Example Usage:

python module_collector.py --base-module=azureml.studio.modules.dataio.enter_data'
    Generates JSON spec file for modules under 'azureml.studio.modules.dataio.enter_data'.

python module_collector.py
    Generates JSON spec file for modules under 'azureml.studio.modules',
    which is the default base module start point if not specified.
"""
    )

    parser.add_argument(
        '--base-module', type=str, default='azureml.studio.modules',
        help="Base module (along with all child modules) to be extracted."
    )
    parser.add_argument(
        '--exclude', action='append', default=['.simple', '.tests', '.test'],
        help="Package ends with these patterns will be excluded."
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help="Will do nothing if specified."
    )

    args = parser.parse_args(args)
    base_module_name = args.base_module
    exclude = args.exclude

    handlers = [
        PrintStatisticsHandler(),
        UpdateEnvironmentHandler(),
        SaveYamlSpecV2Handler(_output_path('yaml_spec_v2')),
    ]

    module_specs = get_module_spec_list(
        base_module_name=base_module_name,
        exclude=exclude,
        release_state_filter=(ReleaseState.Beta, ReleaseState.Release),
    )

    for spec in module_specs:
        _assert_module_meta_is_valid(spec)

    if not args.dry_run:
        for handler in handlers:
            handler.handle_specs(module_specs)


if __name__ == '__main__':
    main(sys.argv[1:])
