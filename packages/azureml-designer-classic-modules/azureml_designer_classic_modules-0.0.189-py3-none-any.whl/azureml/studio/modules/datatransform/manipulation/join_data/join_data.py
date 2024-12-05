import uuid
import pandas as pd

from azureml.studio.modulehost.attributes import ModuleMeta, ItemInfo, DataTableInputPort, \
    ModeParameter, ColumnPickerParameter, SelectedColumnCategory, BooleanParameter, DataTableOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.types import AutoEnum, get_enum_values
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.common.error import ErrorMapping, DuplicatedColumnNameError, InconsistentSizeError, \
    ParameterParsingError, JoinOnIncompatibleColumnTypesError, FailedJoinOperationError
from azureml.studio.modulehost.constants import ElementTypeName
from azureml.studio.core.logger import module_logger as logger, TimeProfile
from azureml.studio.core.utils.missing_value_utils import df_isnull


class JoinType(AutoEnum):
    Inner: ItemInfo(name="Inner Join", friendly_name="Inner Join") = ()
    LeftOuter: ItemInfo(name="Left Outer Join", friendly_name="Left Outer Join") = ()
    FullOuter: ItemInfo(name="Full Outer Join", friendly_name="Full Outer Join") = ()
    LeftSemi: ItemInfo(name="Left Semi-Join", friendly_name="Left Semi-Join") = ()


class JoinDataModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Join Data",
        description="Joins two datasets on selected key columns.",
        category="Data Transformation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="124865f7-e901-4656-adac-f4cb08248099",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            table1: DataTableInputPort(
                name="Dataset1",
                friendly_name="Left dataset",
                description="First dataset to join",
            ),
            table2: DataTableInputPort(
                name="Dataset2",
                friendly_name="Right dataset",
                description="Second dataset to join",
            ),
            keys1: ColumnPickerParameter(
                name="Comma-separated case-sensitive names of join key columns for L",
                friendly_name="Join key columns for left dataset",
                description="Select the join key columns for the first dataset",
                column_picker_for="Dataset1",
                single_column_selection=False,
                column_selection_categories=(SelectedColumnCategory.All,),
            ),
            keys2: ColumnPickerParameter(
                name="Comma-separated case-sensitive names of join key columns for R",
                friendly_name="Join key columns for right dataset",
                description="Select the join key columns for the second dataset",
                column_picker_for="Dataset2",
                single_column_selection=False,
                column_selection_categories=(SelectedColumnCategory.All,),
            ),
            case_sensitive: BooleanParameter(
                name="Match case",
                friendly_name="Match case",
                description="Indicate whether a case-sensitive comparison is allowed on key columns",
                default_value=True,
            ),
            join_type: ModeParameter(
                JoinType,
                name="Join type",
                friendly_name="Join type",
                description="Choose a join type",
                default_value=JoinType.Inner,
            ),
            keep2: BooleanParameter(
                name="Keep right key columns in joined table",
                friendly_name="Keep right key columns in joined table",
                description="Indicate whether to keep key columns from the second dataset in the joined dataset",
                default_value=True,
                parent_parameter="Join type",
                parent_parameter_val=(JoinType.Inner, JoinType.LeftOuter, JoinType.FullOuter),
            )
    ) -> (
            DataTableOutputPort(
                name="Results dataset",
                friendly_name="Results dataset",
                description="Result of join operation",
            ),
    ):
        input_values = locals()
        output_values = JoinDataModule.run_impl(**input_values)
        return output_values

    @classmethod
    def run_impl(
            cls,
            table1: DataTable,
            table2: DataTable,
            keys1: DataTableColumnSelection,
            keys2: DataTableColumnSelection,
            case_sensitive: bool,
            join_type: JoinType,
            keep2: bool
    ):
        cls._validate_args(table1, table2, keys1, keys2, join_type)

        key1_names = [table1.get_column_name(i) for i in keys1.select_column_indexes(table1)]
        key2_names = [table2.get_column_name(i) for i in keys2.select_column_indexes(table2)]

        df_out = cls._pandas_join_data(table1, table2, key1_names, key2_names, case_sensitive, join_type, keep2)
        # df_out = cls._manual_join_data(table1, table2, key1_names, key2_names, case_sensitive, join_type, keep2)
        return DataTable(df_out),

    @classmethod
    def _pandas_join_data(
            cls,
            table1: DataTable,
            table2: DataTable,
            key1_names: list,
            key2_names: list,
            case_sensitive: bool,
            join_type: JoinType,
            keep2: bool
    ):
        df1: pd.DataFrame = table1.data_frame
        df2: pd.DataFrame = table2.data_frame
        df1_columns_clone = list(df1.columns)
        key1_names_clone = list(key1_names)
        key2_names_clone = list(key2_names)
        key1_is_str = [table1.get_element_type(n) in (ElementTypeName.STRING, ElementTypeName.CATEGORY)
                       for n in key1_names]
        key2_is_str = [table2.get_element_type(n) in (ElementTypeName.STRING, ElementTypeName.CATEGORY)
                       for n in key2_names]

        if join_type == JoinType.Inner or join_type == JoinType.LeftSemi:
            merge_type = 'inner'
        elif join_type == JoinType.LeftOuter:
            merge_type = 'left'
        elif join_type == JoinType.FullOuter:
            merge_type = 'outer'
        else:
            raise ValueError(f"Unexpected join type '{JoinType}'")

        # find a appropriate suffix on right table
        logger.debug("Get column name suffix for merged table")
        suffix = cls._get_suffix_on_right_table(table1, table2)

        # rename key columns of tableR for keeping them in merging
        logger.debug("Rename tableR key columns if need")
        # df.merge will combine key columns if key names are equivalent.
        # eg:
        #  tableL   tableR                          output           expect
        #    A B      A B    -outer merge on ->   A B_x B_y      A_x B_x A_y B_y
        #    1 1      2 2      left:['A']         1  1  nan       1   1  nan nan
        #                      right:['A']        2 nan  2       nan nan  2   2
        # So we should manually rename them before merging.
        key2_names, df2_col_rename_mapper = cls._check_key_name_collision(key1_names, key2_names, suffix)

        if any(df2_col_rename_mapper):
            df2.rename(df2_col_rename_mapper, axis=1, inplace=True)

        columns_to_be_dropped = []

        # for semi join, we use left table rowID only.
        logger.debug("Duplicate index on tableL if need")
        left_index_col_name = str(uuid.uuid4())
        if join_type == JoinType.LeftSemi:
            df1[left_index_col_name] = range(df1.shape[0])

        # create extra column if case insensitive
        logger.debug("Prepare case insensitive keys if need")
        if not case_sensitive:
            pairs = [
                (df1, key1_names, key1_is_str),
                (df2, key2_names, key2_is_str)
            ]

            def to_upper(val):
                if isinstance(val, str):
                    return val.upper()
                return val

            for df, key_names, key_is_str in pairs:
                for i, col_name in enumerate(key_names):
                    if key_is_str[i]:
                        # For case insensitive join on string and category columns,
                        # We will create a new column with all str-like values to Upper case,
                        # and use the new column to join.
                        new_col_name = str(uuid.uuid4())
                        df[new_col_name] = df[col_name].apply(to_upper, convert_dtype=False)
                        key_names[i] = new_col_name
                        # It will be dropped after merging.
                        columns_to_be_dropped.append(new_col_name)

        # Unlike sql join or join data from studio v1, df.merge will join null with null.
        # See https://github.com/pandas-dev/pandas/issues/7473
        #
        # So, we should drop null rows from tableR first.
        logger.debug("Clear null rows in tableR")
        df2_isnull_flags = df_isnull(df2, key2_names)
        df2_null_rows = None
        if df2_isnull_flags.any():
            df2_null_rows = df2[df2_isnull_flags]
            df2 = df2[~df2_isnull_flags]

        with TimeProfile("Execute merging"):
            try:
                # TODO: We already know that bool/datetime with missing values will make an 'object' dtype series.
                #   But we have cleared all rows with missing values from tableR.
                #   If user attempts to join on bool/datetime with missing value on tableL, it will raise an error that
                #   the user is not expected. (try to merge 'object' on 'bool/datetime')
                #   There're several solutions to fix it:
                #   1> Convert left keys to 'category' dtype, because 'category' can join anything.
                #   2> Convert right keys to 'object' dtype. But we have to detect dtype compatibility before merging.
                #   3> Remove rows with missing values on tableL before merging, then append to the result after merging
                #      if join type is outer join. But it will slow down semi-join performance.
                #   This is an edge case so we are not planning to fix it in short time. Workaround for this case is to
                #   add clean missing data module on bool/datetime columns before join data.
                df_out = df1.merge(df2, how=merge_type, left_on=key1_names, right_on=key2_names, suffixes=('', suffix))
            except ValueError as err:
                keys_left_expr = str.join(", ", ["{0}:{1}".format(n, df1.dtypes[n].name)
                                                 for n in key1_names_clone])
                key2_with_fmt = ["{0}:{1}".format(n, df2.dtypes[df2_col_rename_mapper.get(n, n)].name)
                                 for n in key2_names_clone]
                keys_right_expr = str.join(", ", key2_with_fmt)

                if "You are trying to merge on" in err.args[0]:
                    # Original error message is like:
                    #   You are trying to merge on float64 and object columns.
                    #   If you wish to proceed you should use pd.concat
                    # Rethrow as an user error.
                    #   Key column element types are not compatible:
                    #     left: key1:int64, key2:object ...
                    #     right: key1:int64, key2:float64 ...
                    # For string/category column, we show dtype of original column instead of case converted column
                    # in error messages.
                    ErrorMapping.rethrow(err, JoinOnIncompatibleColumnTypesError(keys_left_expr, keys_right_expr))
                elif "both an index level and a column label" in str(err.args):
                    trouble_shoot_hint = "Please rename column or index level name."
                    ErrorMapping.rethrow(err, FailedJoinOperationError(str(err), trouble_shoot_hint))
                elif "invalid literal for" in str(err.args):
                    trouble_shoot_hint = "Please check if column type matches."
                    ErrorMapping.rethrow(err, FailedJoinOperationError(str(err), trouble_shoot_hint))
                else:
                    # unknown ValueError, log diagnostics information and throw exception as-is
                    logger.error(f"Error on merging dataframes. (Left: {keys_left_expr}, Right: {keys_right_expr})")
                    raise

        all_column_names = list(df_out.columns)

        def find_df2_column_name_after_merge(old_col_name):
            col_renamed = df2_col_rename_mapper.get(old_col_name, None)
            if col_renamed:  # manually rename
                return col_renamed
            if old_col_name + suffix in all_column_names:  # auto rename by df.merge
                return old_col_name + suffix
            if old_col_name in all_column_names:  # use original name
                return old_col_name
            return None

        logger.debug("Post process")
        if join_type == JoinType.LeftSemi:
            # take the original df1 row indices from inner join result, sort and remove duplicate
            df1_select_row_indices = sorted(set(df_out[left_index_col_name]))
            # Select rows from df1
            #
            # We have append additional columns on df1 before merging,
            # So simply take left n columns here. (n=original df1 columns count))
            df_out = df1.iloc[df1_select_row_indices, 0:len(df1_columns_clone)]
            df_out.reset_index(drop=True, inplace=True)
            return df_out
        elif join_type == JoinType.FullOuter:
            # append non-joined rows to result from tableR.
            if df2_null_rows is not None:
                rename_dict = {}
                for col_name in df2_null_rows.columns:
                    new_col_name = find_df2_column_name_after_merge(col_name)
                    if new_col_name and col_name != new_col_name:
                        rename_dict[col_name] = new_col_name
                if any(rename_dict):
                    df2_null_rows = df2_null_rows.rename(rename_dict, axis=1)
                df_out = df_out.append(df2_null_rows, ignore_index=True, sort=False)

        logger.debug("Clear auxiliary columns")
        if not keep2:
            # drop right keys.
            for col_name in key2_names_clone:
                new_col_name = find_df2_column_name_after_merge(col_name)
                if new_col_name:
                    columns_to_be_dropped.append(new_col_name)

        if any(columns_to_be_dropped):
            # Drop columns also sucks in outer join.
            # For better performance suggestion in DS mode:
            #   - Avoid key column name conflicts and keep right keys
            #   - Avoid case insensitive join
            df_out.drop(columns_to_be_dropped, axis=1, inplace=True)

        df_out.reset_index(drop=True, inplace=True)

        logger.debug("Merge complete")
        return df_out

    @classmethod
    def _manual_join_data(
            cls,
            table1: DataTable,
            table2: DataTable,
            key1_names: list,
            key2_names: list,
            case_sensitive: bool,
            join_type: JoinType,
            keep2: bool
    ):
        """
        This function is for correctness test only.
        Do not use it on production environment for its bad performance.
        """
        df1: pd.DataFrame = table1.data_frame
        df2: pd.DataFrame = table2.data_frame

        with TimeProfile("matching rows"):
            df_matching_rows = \
                cls._find_matching_rows(table1, table2, key1_names, key2_names, case_sensitive, join_type)

        if join_type == JoinType.LeftSemi:
            df_out = table1.data_frame.iloc[df_matching_rows["table1"]]
            return df_out

        left_has_null = (df_matching_rows['table1'] == -1).any()
        right_has_null = (df_matching_rows['table2'] == -1).any()

        if left_has_null:
            df1 = df1.append(pd.Series(), ignore_index=True)

        if right_has_null:
            df2 = df2.append(pd.Series(), ignore_index=True)

        suffix = cls._get_suffix_on_right_table(table1, table2)
        df_out_data = {}

        with TimeProfile("constructing result dataframe"):
            df1_row_indices = df_matching_rows['table1'].values
            for i, col_name in enumerate(df1.columns):
                df_out_data[col_name] = df1.iloc[df1_row_indices, i].values

            df2_row_indices = df_matching_rows['table2'].values
            for i, col_name in enumerate(df2.columns):
                if keep2 or col_name not in key2_names:
                    # rename columns in right table to avoid duplicates
                    col_name_new = col_name + suffix if col_name in df1.columns else col_name
                    df_out_data[col_name_new] = df2.iloc[df2_row_indices, i].values

        df_out = pd.DataFrame(df_out_data)
        return df_out

    @classmethod
    def _find_matching_rows(
            cls,
            table1: DataTable,
            table2: DataTable,
            key1_names: list,
            key2_names: list,
            case_sensitive: bool,
            join_type: JoinType,
    ):
        """
        This function is for correctness test only.
        Do not use it on production environment for its bad performance.
        """
        df1: pd.DataFrame = table1.data_frame
        df2: pd.DataFrame = table2.data_frame

        # generate multiple columns index on tableR, and check each row in tableL.
        if not case_sensitive:
            key2_data = {}
            for col_name in key2_names:
                if table2.get_element_type(col_name) == ElementTypeName.STRING:
                    key2_data[col_name] = df2[col_name].str.upper()
                else:
                    key2_data[col_name] = df2[col_name]
            key2_df = pd.DataFrame(key2_data)
            df2_key_grp = key2_df.groupby(key2_names)

            dt1_key_is_string = dict([(col_name, table1.get_element_type(col_name) == ElementTypeName.STRING)
                                      for col_name in key1_names])

            def get_key_elem(row, col):
                val = row[col]
                if val is not None and dt1_key_is_string[col]:
                    val = val.upper()
                return val

            if len(key1_names) == 1:
                key_name = key1_names[0]

                def filter_func(row):
                    left_key = get_key_elem(row, key_name)
                    return df2_key_grp.indices.get(left_key)
            else:
                def filter_func(row):
                    left_key = tuple([get_key_elem(row, col_name1) for col_name1 in key1_names])
                    return df2_key_grp.indices.get(left_key)
        else:
            df2_key_grp = df2.groupby(key2_names)

            if len(key1_names) == 1:
                key_name = key1_names[0]

                def filter_func(row):
                    left_key = row[key_name]
                    return df2_key_grp.indices.get(left_key)
            else:
                def filter_func(row):
                    left_key = tuple([row[col_name1] for col_name1 in key1_names])
                    return df2_key_grp.indices.get(left_key)

        # create a mapping of join result.
        # [                    [
        #   (0, [0]),            (0, 0),
        #   (1, [1, 2]),   ->    (1, 1),
        #   (2, None),           (1, 2),
        #   ....                 (2, None),
        # ]                      ...
        #                      ]
        mapping_result = []
        for i, df_row in zip(range(df1.shape[0]), df1.iterrows()):
            left_id = i
            right_id = filter_func(df_row[1])

            if join_type == JoinType.LeftSemi:
                if right_id is not None:
                    mapping_result.append((left_id, 0))
            else:
                if right_id is not None:
                    for j in right_id:
                        mapping_result.append((left_id, j))
                elif join_type != JoinType.Inner:
                    mapping_result.append((left_id, -1))

        # post process for full outer join
        if join_type == JoinType.FullOuter:
            right_indices = set(range(df2.shape[0])).difference(map(lambda x: x[1], mapping_result))
            mapping_result.extend(map(lambda right_id2: (-1, right_id2), right_indices))

        return pd.DataFrame(
            data=mapping_result,
            columns=['table1', 'table2']
        )

    @classmethod
    def _get_suffix_on_right_table(cls, table1: DataTable, table2: DataTable):
        # To ensure that each column name is unique after merging, here we try to find a suffix for right-hand table.
        # Suffix format is like "_R{index}". eg. '_R', '_R1', '_R2'...
        suffix = '_R'
        suffix_index = 1
        all_column_names = set(table1.column_names + table2.column_names)
        while any(map(lambda col_name: col_name + suffix in all_column_names, table2.column_names)):
            suffix = '_R' + str(suffix_index)
            suffix_index += 1
        return suffix

    @classmethod
    def _check_key_name_collision(cls, key1_names: list, key2_names: list, suffix: str):
        # Check if column names are equal on the same position.
        # Return the checked key names and mapper dict for later use.
        key2_names_checked = []
        key2_rename_mapper = {}
        for key1, key2 in zip(key1_names, key2_names):
            if key1 == key2:
                key2_with_suffix = key2 + suffix
                key2_rename_mapper[key2] = key2_with_suffix
                key2_names_checked.append(key2_with_suffix)
            else:
                key2_names_checked.append(key2)

        return key2_names_checked, key2_rename_mapper

    @classmethod
    def _validate_args(
            cls,
            table1: DataTable,
            table2: DataTable,
            keys1: DataTableColumnSelection,
            keys2: DataTableColumnSelection,
            join_type: JoinType
    ):
        if table1.number_of_columns == 0:
            ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(curr_column_count=table1.number_of_columns,
                                                                           required_column_count=1,
                                                                           arg_name=cls._args.table1.name)
        if table2.number_of_columns == 0:
            ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(curr_column_count=table2.number_of_columns,
                                                                           required_column_count=1,
                                                                           arg_name=cls._args.table2.name)

        ErrorMapping.verify_not_null_or_empty(keys1, cls._args.keys1.name)
        ErrorMapping.verify_not_null_or_empty(keys2, cls._args.keys2.name)
        keys1_indices = keys1.select_column_indexes(table1)
        keys2_indices = keys2.select_column_indexes(table2)
        ErrorMapping.verify_are_columns_selected(len(keys1_indices), 1, cls._args.keys1.name)
        ErrorMapping.verify_are_columns_selected(len(keys2_indices), 1, cls._args.keys2.name)
        cls._throw_if_not_all_columns_unique(keys1_indices, table1)
        cls._throw_if_not_all_columns_unique(keys2_indices, table2)
        if len(keys1_indices) != len(keys2_indices):
            ErrorMapping.throw(InconsistentSizeError(cls._args.keys1.name, cls._args.keys2.name))
        if join_type not in get_enum_values(JoinType):
            ErrorMapping.throw(ParameterParsingError(cls._args.join_type.name))

    @classmethod
    def _throw_if_not_all_columns_unique(cls, col_indices, dt: DataTable):
        s = set()
        for idx in col_indices:
            if idx in s:
                ErrorMapping.throw(DuplicatedColumnNameError(dt.get_column_name(idx)))
            s.add(idx)
