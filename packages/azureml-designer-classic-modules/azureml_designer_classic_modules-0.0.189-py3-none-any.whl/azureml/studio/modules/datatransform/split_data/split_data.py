import itertools
import numpy as np
import pandas as pd
import re
from typing import Callable

from azureml.studio.modulehost.attributes import ItemInfo, DataTableInputPort, ModeParameter, FloatParameter, \
    BooleanParameter, ColumnPickerParameter, SelectedColumnCategory, IntParameter, StringParameter, ModuleMeta, \
    DataTableOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import ErrorMapping, ModuleError, ColumnNotFoundError, ParameterParsingError, \
    InvalidColumnTypeError
from azureml.studio.common.input_parameter_checker import InputParameterChecker
from azureml.studio.core.logger import module_logger as logger, log_list_values
from azureml.studio.common.types import AutoEnum, parse_datetime, parse_timedelta
from azureml.studio.modulehost.constants import ElementTypeName, UINT32_MAX
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
import azureml.studio.modules.datatransform.common.splitter as splitter


class SplitterSplitMode(AutoEnum):
    GenericSplit: ItemInfo(name="Split Rows", friendly_name="Split Rows") = ()
    RecommenderSplit: ItemInfo(
        name="Recommender Split",
        friendly_name="Recommender Split",
        release_state=ReleaseState.Alpha) = ()
    RegEx: ItemInfo(name="Regular Expression", friendly_name="Regular Expression") = ()
    RelEx: ItemInfo(name="Relative Expression", friendly_name="Relative Expression") = ()


class SplitterTrueFalseType(AutoEnum):
    TRUE: ItemInfo(name="True", friendly_name="True") = ()
    FALSE: ItemInfo(name="False", friendly_name="False") = ()


class SplitDataModule(BaseModule):
    _param_keys = {
        "table": "Dataset",
        "mode": "Splitting mode",
        "ratio": "Fraction of rows in the first output dataset",
        "random_flag": "Randomized split",
        "seed": "Random seed",
        "stratify_flag": "Stratified split",
        "strats_column": "Stratification key column",
        "training_only_user_fraction": "Fraction of training-only users",
        "test_user_rating_training_fraction": "Fraction of test user ratings for training",
        "cold_user_fraction": "Fraction of cold users",
        "cold_item_fraction": "Fraction of cold items",
        "ignored_user_fraction": "Fraction of ignored users",
        "ignored_item_fraction": "Fraction of ignored items",
        "remove_occasional_cold_items": "Remove occasionally produced cold items",
        "seed_recommender": "Random seed for Recommender",
        "reg_ex": "Regular expression",
        "rel_ex": "Relational expression",
    }

    @staticmethod
    @module_entry(ModuleMeta(
        name="Split Data",
        description="Partitions the rows of a dataset into two distinct sets.",
        category="Data Transformation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="{70530644-C97A-4AB6-85F7-88BF30A8BE5F}",
        release_state=ReleaseState.Release,
        is_deterministic=True,
        pass_through_in_real_time_inference=True,
    ))
    def run(
            table: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Dataset to split",
            ),
            mode: ModeParameter(
                SplitterSplitMode,
                name="Splitting mode",
                friendly_name="Splitting mode",
                description="Choose the method for splitting the dataset",
                default_value=SplitterSplitMode.GenericSplit,
            ),
            ratio: FloatParameter(
                name="Fraction of rows in the first output dataset",
                friendly_name="Fraction of rows in the first output dataset",
                description="Specify a ratio representing the number of rows in the first output dataset over "
                            "the number of rows in the input dataset",
                default_value=0.5,
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.GenericSplit, ),
                min_value=0,
                max_value=1,
            ),
            random_flag: BooleanParameter(
                name="Randomized split",
                friendly_name="Randomized split",
                description="Indicate whether rows should be randomly selected",
                default_value=True,
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.GenericSplit, ),
            ),
            seed: IntParameter(
                name="Random seed",
                friendly_name="Random seed",
                description="Provide a value to see the random number generator seed",
                default_value=0,
                min_value=0,
                max_value=UINT32_MAX,
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.GenericSplit, ),
            ),
            stratify_flag: ModeParameter(
                SplitterTrueFalseType,
                name="Stratified split",
                friendly_name="Stratified split",
                description="Indicate whether the rows in each split should be grouped using a strata column",
                default_value=SplitterTrueFalseType.FALSE,
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.GenericSplit, ),
            ),
            strats_column: ColumnPickerParameter(
                name="Stratification key column",
                friendly_name="Stratification key column",
                description="Select the column containing the stratification key",
                parent_parameter="Stratified split",
                parent_parameter_val=(SplitterTrueFalseType.TRUE, ),
                column_picker_for="Dataset",
                single_column_selection=True,
                column_selection_categories=(SelectedColumnCategory.All, ),
            ),
            training_only_user_fraction: FloatParameter(
                name="Fraction of training-only users",
                friendly_name="Fraction of training-only users",
                description="Specify the fraction of users to allocate to the training-only set",
                default_value=0.5,
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.RecommenderSplit, ),
                min_value=0,
                max_value=1,
            ),
            test_user_rating_training_fraction: FloatParameter(
                name="Fraction of test user ratings for training",
                friendly_name="Fraction of test user ratings for training",
                description="Specify the fraction of user ratings that can be moved "
                              "from the test set to the training set",
                default_value=0.25,
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.RecommenderSplit, ),
                min_value=0,
                max_value=1,
            ),
            cold_user_fraction: FloatParameter(
                name="Fraction of cold users",
                friendly_name="Fraction of cold users",
                description="Specify the fraction of users to allocate to the test-only set",
                default_value=0,
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.RecommenderSplit, ),
                min_value=0,
                max_value=1,
            ),
            cold_item_fraction: FloatParameter(
                name="Fraction of cold items",
                friendly_name="Fraction of cold items",
                description="Specify the fraction of items to allocate to the test-only set",
                default_value=0,
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.RecommenderSplit, ),
                min_value=0,
                max_value=1,
            ),
            ignored_user_fraction: FloatParameter(
                name="Fraction of ignored users",
                friendly_name="Fraction of ignored users",
                description="Specify the fraction of users that should be excluded from both sets",
                default_value=0,
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.RecommenderSplit, ),
                min_value=0,
                max_value=1,
            ),
            ignored_item_fraction: FloatParameter(
                name="Fraction of ignored items",
                friendly_name="Fraction of ignored items",
                description="Specify the fraction of items that should be excluded from both sets",
                default_value=0,
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.RecommenderSplit, ),
                min_value=0,
                max_value=1,
            ),
            remove_occasional_cold_items: BooleanParameter(
                name="Remove occasionally produced cold items",
                friendly_name="Remove occasionally produced cold items",
                description="Indicate whether items that were put in the test set as a result of other exclusions"
                            " should remain in the test set or be removed",
                default_value=False,
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.RecommenderSplit, ),
            ),
            seed_recommender: IntParameter(
                name="Random seed for Recommender",
                friendly_name="Random seed for Recommender",
                min_value=0,
                max_value=UINT32_MAX,
                description="Specify a value to seed the random number generator",
                default_value=0,
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.RecommenderSplit, ),
            ),
            reg_ex: StringParameter(
                name="Regular expression",
                friendly_name="Regular expression",
                description="Type a regular expression to use as criteria "
                            "when splitting the dataset on a string column",
                default_value="\\\"column name\" ^start",
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.RegEx, ),
            ),
            rel_ex: StringParameter(
                name="Relational expression",
                friendly_name="Relational expression",
                description="Type a relational expression to use in splitting the dataset on a numeric column",
                default_value="\\\"column name\" > 3",
                parent_parameter="Splitting mode",
                parent_parameter_val=(SplitterSplitMode.RelEx, ),
            )
    ) -> (
            DataTableOutputPort(
                name="Results dataset1",
                friendly_name="Results dataset1",
                description="Dataset containing selected rows",
            ),
            DataTableOutputPort(
                name="Results dataset2",
                friendly_name="Results dataset2",
                description="Dataset containing all other rows",
            ),
    ):
        input_values = locals()
        return SplitDataModule._run_impl(**input_values)

    @classmethod
    def _run_impl(
            cls,
            table: DataTable,
            mode: SplitterSplitMode,
            ratio: float,
            random_flag: bool,
            seed: int,
            stratify_flag: SplitterTrueFalseType,
            strats_column: DataTableColumnSelection,
            training_only_user_fraction: float,
            test_user_rating_training_fraction: float,
            cold_user_fraction: float,
            cold_item_fraction: float,
            ignored_user_fraction: float,
            ignored_item_fraction: float,
            remove_occasional_cold_items: bool,
            seed_recommender: int,
            reg_ex: str,
            rel_ex: str):
        if mode is SplitterSplitMode.GenericSplit:
            logger.info('SplitterSplitMode.GenericSplit mode')
            return cls._general_split(
                table,
                ratio,
                random_flag,
                seed,
                stratify_flag == SplitterTrueFalseType.TRUE,
                strats_column
            )

        elif mode is SplitterSplitMode.RecommenderSplit:
            logger.info('SplitterSplitMode.RecommenderSplit mode')
            return cls._recommender_split(
                table,
                training_only_user_fraction,
                test_user_rating_training_fraction,
                cold_user_fraction,
                cold_item_fraction,
                ignored_user_fraction,
                ignored_item_fraction,
                remove_occasional_cold_items,
                seed_recommender
            )

        else:
            if mode is SplitterSplitMode.RegEx:
                logger.info('SplitterSplitMode.RegEx mode')
                return cls._reg_ex_split(table, reg_ex)

            elif mode is SplitterSplitMode.RelEx:
                logger.info('SplitterSplitMode.RelEx mode')
                return cls._rel_ex_split(table, rel_ex)

    @classmethod
    def _general_split(
            cls,
            table: DataTable,
            ratio: float,
            random_flag: bool,
            seed: int,
            stratify_flag: bool,
            strats_column: DataTableColumnSelection):

        # stratify datatable
        if stratify_flag:
            data_groups = splitter.stratify_split_to_indices_groups(table, strats_column)
        else:
            # use df.index instead of row-index to align the result of stratify split.
            data_groups = [table.data_frame.index]

        rand = np.random.RandomState(seed) if random_flag else None

        logger.info("begin split.")

        def execute_split(index_array):
            row_count = len(index_array)
            df1_count = int(round(row_count * ratio))
            shape = [df1_count, row_count - df1_count]
            log_list_values("shape", shape)
            return splitter.split(index_array, shape, rand, False)

        splitted_groups = [execute_split(x) for x in data_groups]
        fold_indices = [list(itertools.chain.from_iterable(g[fold] for g in splitted_groups))
                        for fold in range(0, 2)]

        if rand:
            logger.info(f"randomize folds.")
            for ary in fold_indices:
                rand.shuffle(ary)

        df = table.data_frame
        first_part = df.loc[fold_indices[0]]
        second_part = df.loc[fold_indices[1]]
        first_part.reset_index(drop=True, inplace=True)
        second_part.reset_index(drop=True, inplace=True)
        dt1 = DataTable(first_part, table.meta_data.copy(True))
        dt2 = DataTable(second_part, table.meta_data.copy(True))
        return dt1, dt2

    @classmethod
    def _recommender_split(
            cls,
            table: DataTable,
            training_only_user_fraction: float,
            test_user_rating_training_fraction: float,
            cold_user_fraction: float,
            cold_item_fraction: float,
            ignored_user_fraction: float,
            ignored_item_fraction: float,
            remove_occasional_cold_items: bool,
            seed_recommender: int):
        raise NotImplementedError()

    @classmethod
    def _reg_ex_split(cls, table: DataTable, reg_ex: str):
        # https://docs.microsoft.com/en-us/azure/machine-learning/studio-module-reference/split-data-using-regular-expression
        cls._validate_arguments_reg_ex(table, reg_ex)
        reg_ex = reg_ex.strip()

        if reg_ex[0] == '\\':
            col_name_end_index = reg_ex.index('"', 2)
            col_name = reg_ex[2:col_name_end_index].strip()
        else:
            col_name_end_index = reg_ex.index(')', 0)
            col_index = reg_ex[2:col_name_end_index]
            col_name = table.get_column_name(int(col_index)-1)  # 1-based in v2

        reg_ex_rest = reg_ex[col_name_end_index+1:].strip()
        try:
            re_pat = re.compile(reg_ex_rest)
        except BaseException as e:
            raise ParameterParsingError(arg_name_or_column=cls._param_keys['reg_ex'], arg_value=reg_ex) from e

        logger.info(f"regex filter: column: {col_name}, pattern: {reg_ex_rest}")

        def filter_func(item):
            item_str = '' if pd.isnull(item) else str(item)
            return re_pat.search(item_str) is not None

        # 416207: apply function on category column will result a object series, force convert to bool.
        selected_rows = table.data_frame[col_name].apply(filter_func).astype(bool)
        table_selected = table.data_frame[selected_rows]
        table_selected.reset_index(drop=True, inplace=True)
        table_remaining = table.data_frame[~selected_rows]
        table_remaining.reset_index(drop=True, inplace=True)

        dt1 = DataTable(table_selected, table.get_meta_data(True))
        dt2 = DataTable(table_remaining, table.get_meta_data(True))
        return dt1, dt2

    @classmethod
    def _rel_ex_split(cls, table: DataTable, rel_ex: str):
        # https://docs.microsoft.com/en-us/azure/machine-learning/studio-module-reference/split-data-using-relative-expression
        cls._validate_arguments_rel_ex(table, rel_ex)

        rel_ex = rel_ex.strip()

        if rel_ex[0] == '\\':
            col_name_end_index = rel_ex.index('"', 2)
            col_name = rel_ex[2:col_name_end_index].strip()
        else:
            col_name_end_index = rel_ex.index(')', 0)
            col_index = rel_ex[2:col_name_end_index]
            col_name = table.get_column_name(int(col_index)-1)  # 1-based in v2

        rel_ex_rest = rel_ex[col_name_end_index + 1:].strip()
        filter_func = cls._parse_relative_fold_func(table, col_name, rel_ex_rest)

        logger.info(f"relex filter: column: {col_name}, pattern: {rel_ex_rest}")

        selected_rows = table.data_frame[col_name].apply(filter_func).astype(bool)
        table_selected = table.data_frame[selected_rows]
        table_selected.reset_index(drop=True, inplace=True)
        table_remaining = table.data_frame[~selected_rows]
        table_remaining.reset_index(drop=True, inplace=True)

        dt1 = DataTable(table_selected, table.get_meta_data(True))
        dt2 = DataTable(table_remaining, table.get_meta_data(True))
        return dt1, dt2

    @classmethod
    def _validate_arguments_reg_ex(cls, table: DataTable, reg_ex: str):
        InputParameterChecker.verify_data_table(table, cls._param_keys['table'])
        ErrorMapping.verify_not_null_or_empty(reg_ex, cls._param_keys['reg_ex'])
        verify_str = reg_ex.strip()

        if verify_str[0] == '\\' and verify_str.count('"') == 2 and verify_str[1] == '"':
            # match \"{colName}" pattern
            next_occur = verify_str.index('"', 2)
            col_name = verify_str[2:next_occur].strip()
            if not table.contains_column(col_name):
                raise ColumnNotFoundError(col_name)

        elif verify_str[0] == '(' and verify_str[1] == '\\' and verify_str.count('(') == verify_str.count(')'):
            # match (\{colIndex}) pattern
            next_occur = verify_str.index(')', 2)
            try:
                col_index = int(verify_str[2:next_occur])
            except ValueError as e:
                raise ColumnNotFoundError(verify_str[2:next_occur]) from e

            if 1 <= col_index <= table.number_of_columns:
                col_name = table.get_column_name(col_index-1)
            else:
                raise ColumnNotFoundError(str(col_index))

        else:
            raise ParameterParsingError(arg_name_or_column=cls._param_keys['reg_ex'], arg_value=reg_ex)

    @classmethod
    def _validate_arguments_rel_ex(cls, table: DataTable, rel_ex: str):
        InputParameterChecker.verify_data_table(table, cls._param_keys['table'])
        ErrorMapping.verify_not_null_or_empty(rel_ex, cls._param_keys['rel_ex'])
        verify_str = rel_ex.strip()

        if verify_str[0] == '\\' and verify_str.count('"') == 2 and verify_str[1] == '"':
            # match \"{colName}" pattern
            next_occur = verify_str.index('"', 2)
            col_name = verify_str[2:next_occur].strip()
            if table.contains_column(col_name):
                col_elem_type = table.get_element_type(col_name)
                if not cls._is_rel_supported_type(col_elem_type):
                    ErrorMapping.throw_invalid_column_type(col_elem_type, col_name, cls._param_keys['rel_ex'])
            else:
                raise ColumnNotFoundError(col_name)

        elif verify_str[0] == '(' and verify_str[1] == '\\' and verify_str.count('(') == verify_str.count(')'):
            # match (\{colIndex}) pattern
            next_occur = verify_str.index(')', 2)

            try:
                col_index = int(verify_str[2:next_occur])
            except ValueError as e:
                raise ColumnNotFoundError(verify_str[2:next_occur]) from e

            if 1 <= col_index <= table.number_of_columns:
                col_name = table.get_column_name(col_index-1)
                col_elem_type = table.get_element_type(col_name)
                if not cls._is_rel_supported_type(col_elem_type):
                    ErrorMapping.throw_invalid_column_type(col_elem_type, col_name, cls._param_keys['rel_ex'])
            else:
                raise ColumnNotFoundError(str(col_index))

        else:
            raise ParameterParsingError(arg_name_or_column=cls._param_keys['reg_ex'], arg_value=rel_ex)

    @classmethod
    def _is_rel_supported_type(cls, elem_type: str):
        supported_types = (
            ElementTypeName.STRING,
            ElementTypeName.BOOL,
            ElementTypeName.FLOAT,
            ElementTypeName.INT,
            ElementTypeName.DATETIME,
            ElementTypeName.TIMESPAN
        )
        return elem_type in supported_types

    @classmethod
    def _parse_relative_fold_func(cls, table: DataTable, col_name: str, expr: str) -> Callable:
        """
        Split relative expression to terms and convert to a compare function.
        Support and(&) and or(|) operation.
        Group operations with '(' and ')' are not supported.

        Example expression:
            >=0 & <= 10 | ==20
            <00:01:00 & >00:00:30
        """
        regex = re.compile("[&|]")
        terms = [s.strip() for s in regex.split(expr)]
        delims = list()
        funcs = list()

        cur_pos = 0
        for term in terms:
            try:
                funcs.append(cls._parse_term_func(table, col_name, term))
            except ModuleError:
                raise
            except BaseException as e:
                if isinstance(e, ValueError):
                    logger.error(f"Parse term '{term}' failed, invalid format.")
                else:
                    logger.error(f"Parse term '{term}' failed, unexpected error.")
                raise ParameterParsingError(term) from e

            m = regex.search(expr, cur_pos)
            if m is not None:
                cur_pos = m.start()
                delims.append(expr[cur_pos])
                cur_pos += 1

        def filter_func(item):
            result = funcs[0](item)
            for i in range(1, len(funcs)):
                if delims[i-1] == '&':
                    result = result and funcs[i](item)
                else:
                    result = result or funcs[i](item)
            return result

        return filter_func

    @classmethod
    def _parse_term_func(cls, table: DataTable, col_name: str, term: str) -> Callable:
        """
        Parse Relative Expression to a compare function.

        Valid term format:
            {op}{right_value}

        Support operators:
            ==, !=, <, <=, >, >=

        Support column element types:
            int, float, string(only != and ==), datetime, timedelta

        Example terms:
            ==0
            !=3.14
            !=hello, world.
            >2019-01-01
            <5.02:13:14

        Return:
            func(any) -> bool
        """
        col_elem_type = table.get_element_type(col_name)
        term = term.strip()
        logger.debug(f"parse term {term} for column {col_name}({col_elem_type})")

        default_key = ''
        op_table = {
            '=': {
                '=': '==',
            },
            '!': {
                '=': '!=',
            },
            '<': {
                '=': '<=',
                default_key: '<',
            },
            '>': {
                '=': '>=',
                default_key: '>',
            },
        }

        try:
            op = op_table.get(term[0], None)
            if isinstance(op, dict):
                op = op.get(term[1], op.get(default_key, None))

        except Exception as e:
            raise ParameterParsingError(term) from e

        if not op:
            raise ParameterParsingError(term)

        expr = term[len(op):]

        if col_elem_type == ElementTypeName.STRING:
            str_val = expr
            if op == '==':
                return lambda x: x == str_val
            elif op == '!=':
                return lambda x: x != str_val
            elif op in ('>', '>=', '<', '<='):
                raise InvalidColumnTypeError(col_elem_type, col_name, op)
            else:
                raise ParameterParsingError(arg_name_or_column=op, to_type='Operator')

        elif col_elem_type == ElementTypeName.INT:
            int_val = int(expr)
            if op == '==':
                return lambda x: not pd.isnull(x) and x == int_val
            elif op == '!=':
                return lambda x: not pd.isnull(x) and x != int_val
            elif op == '>':
                return lambda x: not pd.isnull(x) and x > int_val
            elif op == '>=':
                return lambda x: not pd.isnull(x) and x >= int_val
            elif op == '<':
                return lambda x: not pd.isnull(x) and x < int_val
            elif op == '<=':
                return lambda x: not pd.isnull(x) and x <= int_val
            else:
                raise ParameterParsingError(arg_name_or_column=op, to_type='Operator')

        elif col_elem_type == ElementTypeName.FLOAT:
            float_val = float(expr)
            if op == '==':
                return lambda x: not pd.isnull(x) and x == float_val
            elif op == '!=':
                return lambda x: not pd.isnull(x) and x != float_val
            elif op == '>':
                return lambda x: not pd.isnull(x) and x > float_val
            elif op == '>=':
                return lambda x: not pd.isnull(x) and x >= float_val
            elif op == '<':
                return lambda x: not pd.isnull(x) and x < float_val
            elif op == '<=':
                return lambda x: not pd.isnull(x) and x <= float_val
            else:
                raise ParameterParsingError(arg_name_or_column=op, to_type='Operator')

        elif col_elem_type == ElementTypeName.DATETIME:
            datetime_val = parse_datetime(expr)

            # bug 551263: if the datetime series have timezone, convert the right value to Timestamp for comparing.
            col_dtype = table.data_frame.dtypes[col_name]
            if isinstance(col_dtype, pd.DatetimeTZDtype):
                datetime_val = pd.Timestamp(datetime_val, tz=col_dtype.tz)
            else:
                # bug 754894: if datetime series does not have timezone, remove tz from right value.
                datetime_val = pd.Timestamp(datetime_val).tz_localize(None)

            if op == '==':
                return lambda x: not pd.isnull(x) and x == datetime_val
            elif op == '!=':
                return lambda x: not pd.isnull(x) and x != datetime_val
            elif op == '>':
                return lambda x: not pd.isnull(x) and x > datetime_val
            elif op == '>=':
                return lambda x: not pd.isnull(x) and x >= datetime_val
            elif op == '<':
                return lambda x: not pd.isnull(x) and x < datetime_val
            elif op == '<=':
                return lambda x: not pd.isnull(x) and x <= datetime_val
            else:
                raise ParameterParsingError(arg_name_or_column=op, to_type='Operator')

        elif col_elem_type == ElementTypeName.TIMESPAN:
            timedelta_val = parse_timedelta(expr)
            if op == '==':
                return lambda x: not pd.isnull(x) and x == timedelta_val
            elif op == '!=':
                return lambda x: not pd.isnull(x) and x != timedelta_val
            elif op == '>':
                return lambda x: not pd.isnull(x) and x > timedelta_val
            elif op == '>=':
                return lambda x: not pd.isnull(x) and x >= timedelta_val
            elif op == '<':
                return lambda x: not pd.isnull(x) and x < timedelta_val
            elif op == '<=':
                return lambda x: not pd.isnull(x) and x <= timedelta_val
            else:
                raise ParameterParsingError(arg_name_or_column=op, to_type='Operator')

        else:
            ErrorMapping.throw_invalid_column_type(col_elem_type)
