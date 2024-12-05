import re

from functools import partial


class Pattern:
    EXTRA_SPACES = re.compile(r'\s\s+')
    END_WITH_SPACE = re.compile(r'\s$')
    START_WITH_SPACE = re.compile(r'^\s')


def has_pattern(val, pattern):
    return pattern.search(val) is not None


def has_both_tab_and_space(val):
    return ' ' in val and '\t' in val


rule2checker = {
    "Extra spaces/tabs are not allowed": partial(has_pattern, pattern=Pattern.EXTRA_SPACES),
    "Starting with space/tab is not allowed": partial(has_pattern, pattern=Pattern.START_WITH_SPACE),
    "Ending with space/tab is not allowed": partial(has_pattern, pattern=Pattern.END_WITH_SPACE),
    "Mixing space and tab is not allowed": has_both_tab_and_space,
}


def assert_str_val_pass_rules(val):
    for rule, checker in rule2checker.items():
        if checker(val):
            raise ValueError(f"{rule}, val={val}")


def is_conda_dependencies_same(conda_dict_left: dict, conda_dict_right: dict):
    def _check_section(section_name: str):
        return conda_dict_left.get(section_name) == conda_dict_right.get(section_name)

    return _check_section("name") and _check_section("channels") and _check_section("dependencies")
