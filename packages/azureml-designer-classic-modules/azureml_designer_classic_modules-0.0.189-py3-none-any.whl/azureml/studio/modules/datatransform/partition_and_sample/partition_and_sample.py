import itertools
import numpy as np

from azureml.studio.modulehost.constants import UINT32_MAX
from azureml.studio.modulehost.attributes import StringParameter, ItemInfo, ModeParameter, FloatParameter,\
    IntParameter, BooleanParameter, DataTableInputPort, ColumnPickerParameter, SelectedColumnCategory, \
    DataTableOutputPort, ModuleMeta
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import NaNError, NotInRangeValueError, ColumnNotFoundError, InvalidDatasetError, \
    ParameterParsingError, ErrorMapping
from azureml.studio.core.logger import module_logger as logger, log_list_values
from azureml.studio.common.types import AutoEnum
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
import azureml.studio.modules.datatransform.common.splitter as splitter

_META_PROPERTY_KEY = 'logical_split'


class SampleMethods(AutoEnum):
    NFoldSplit: ItemInfo(name="Assign to Folds", friendly_name="Assign to Folds") = ()
    FoldPicker: ItemInfo(name="Pick Fold", friendly_name="Pick Fold") = ()
    Sampling: ItemInfo(name="Sampling", friendly_name="Sampling") = ()
    Head: ItemInfo(name="Head", friendly_name="Head") = ()


class PartitionMethods(AutoEnum):
    EvenSizePartitioner: ItemInfo(name="Partition evenly", friendly_name="Partition evenly") = ()
    CustomizedPartitioner: ItemInfo(
        name="Partition with customized proportions",
        friendly_name="Partition with customized proportions") = ()


class TrueFalseType(AutoEnum):
    TRUE: ItemInfo(name="True", friendly_name="True") = ()
    FALSE: ItemInfo(name="False", friendly_name="False") = ()


class PartitionAndSampleModule(BaseModule):
    _param_keys = {
        "table": "Dataset",
        "method": "Partition or sample mode",
        "with_replacement": "Use replacement in the partitioning",
        "random_flag": "Randomized Split",
        "seed": "Random seed",
        "partition_method": "Specify the partitioner method",
        "num_partitions": "Specify how many folds do you want to split evenly into",
        "stratify_flag1": "Stratified split",
        "strats_column1": "Stratification key column",
        "folds_prop_list": "Proportion list of customized folds separated by comma",
        "stratify_flag2": "Stratified split for customized fold assignment",
        "strats_column2": "Stratification key column for customized fold assignment",
        "fold_index": "Specify which fold to be sampled from",
        "pick_complement": "Pick complement of the selected fold",
        "rate": "Rate of sampling",
        "seed_sampling": "Random seed for sampling",
        "stratify_flag3": "Stratified split for sampling",
        "strats_column3": "Stratification key column for sampling",
        "head_num_rows": "Number of rows to select",
    }

    @staticmethod
    @module_entry(ModuleMeta(
        name="Partition and Sample",
        description="Creates multiple partitions of a dataset based on sampling.",
        category="Data Transformation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="A8726E34-1B3E-4515-B59A-3E4A475654B8",
        release_state=ReleaseState.Release,
        is_deterministic=True,
        pass_through_in_real_time_inference=True,
    ))
    def run(
            table: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Dataset to be split",
            ),
            method: ModeParameter(
                SampleMethods,
                name="Partition or sample mode",
                friendly_name="Partition or sample mode",
                description="Select the partition or sampling mode",
                default_value=SampleMethods.Sampling,
            ),
            with_replacement: BooleanParameter(
                name="Use replacement in the partitioning",
                friendly_name="Use replacement in the partitioning",
                description="Indicate whether the dataset should be replaced when split, or split without replacement",
                default_value=False,
                parent_parameter="Partition or sample mode",
                parent_parameter_val=(SampleMethods.NFoldSplit,),
            ),
            random_flag: BooleanParameter(
                name="Randomized Split",
                friendly_name="Randomized split",
                description="Indicates whether split is random or not",
                default_value=True,
                parent_parameter="Partition or sample mode",
                parent_parameter_val=(SampleMethods.NFoldSplit,),
            ),
            seed: IntParameter(
                name="Random seed",
                friendly_name="Random seed",
                min_value=0,
                max_value=UINT32_MAX,
                description="Specify a seed for the random number generator",
                default_value=0,
                parent_parameter="Partition or sample mode",
                parent_parameter_val=(SampleMethods.NFoldSplit,),
            ),
            partition_method: ModeParameter(
                PartitionMethods,
                name="Specify the partitioner method",
                friendly_name="Specify the partitioner method",
                description="EvenSize where you specify number of folds, "
                            "or ShapeInPct where you specify a list of percentage numbers",
                default_value=PartitionMethods.EvenSizePartitioner,
                parent_parameter="Partition or sample mode",
                parent_parameter_val=(SampleMethods.NFoldSplit,),
            ),
            num_partitions: IntParameter(
                name="Specify how many folds do you want to split evenly into",
                friendly_name="Specify number of folds to split evenly into",
                description="Number of even partitions to be evenly split into",
                default_value=5,
                parent_parameter="Specify the partitioner method",
                parent_parameter_val=(PartitionMethods.EvenSizePartitioner,),
                min_value=1,
            ),
            stratify_flag1: ModeParameter(
                TrueFalseType,
                name="Stratified split",
                friendly_name="Stratified split",
                description="Indicates whether the split is stratified or not",
                default_value=TrueFalseType.FALSE,
                parent_parameter="Specify the partitioner method",
                parent_parameter_val=(PartitionMethods.EvenSizePartitioner,),
            ),
            strats_column1: ColumnPickerParameter(
                name="Stratification key column",
                friendly_name="Stratification key column",
                description="Column containing stratification key",
                parent_parameter="Stratified split",
                parent_parameter_val=(TrueFalseType.TRUE,),
                column_picker_for="Dataset",
                single_column_selection=True,
                column_selection_categories=(SelectedColumnCategory.All,),
            ),
            folds_prop_list: StringParameter(
                name="Proportion list of customized folds separated by comma",
                friendly_name="List of proportions separated by comma",
                description="List of proportions separated by comma",
                parent_parameter="Specify the partitioner method",
                parent_parameter_val=(PartitionMethods.CustomizedPartitioner,),
            ),
            stratify_flag2: ModeParameter(
                TrueFalseType,
                name="Stratified split for customized fold assignment",
                friendly_name="Stratified split for customized fold assignment",
                description="Indicates whether the split is stratified or not for customized fold assignments",
                default_value=TrueFalseType.FALSE,
                parent_parameter="Specify the partitioner method",
                parent_parameter_val=(PartitionMethods.CustomizedPartitioner,),
            ),
            strats_column2: ColumnPickerParameter(
                name="Stratification key column for customized fold assignment",
                friendly_name="Stratification key column for customized fold assignment",
                description="Column containing stratification key for customized fold assignments",
                parent_parameter="Stratified split for customized fold assignment",
                parent_parameter_val=(TrueFalseType.TRUE,),
                column_picker_for="Dataset",
                single_column_selection=True,
                column_selection_categories=(SelectedColumnCategory.All,),
            ),
            fold_index: IntParameter(
                name="Specify which fold to be sampled from",
                friendly_name="Specify which fold to be sampled from",
                description="Index of the partitioned fold to be sampled from",
                default_value=1,
                parent_parameter="Partition or sample mode",
                parent_parameter_val=(SampleMethods.FoldPicker,),
                min_value=1,
            ),
            pick_complement: BooleanParameter(
                name="Pick complement of the selected fold",
                friendly_name="Pick complement of the selected fold",
                description="Complement of the logic fold",
                default_value=False,
                parent_parameter="Partition or sample mode",
                parent_parameter_val=(SampleMethods.FoldPicker,),
            ),
            rate: FloatParameter(
                name="Rate of sampling",
                friendly_name="Rate of sampling",
                description="Sampling rate",
                default_value=0.01,
                parent_parameter="Partition or sample mode",
                parent_parameter_val=(SampleMethods.Sampling,),
            ),
            seed_sampling: IntParameter(
                name="Random seed for sampling",
                friendly_name="Random seed for sampling",
                min_value=0,
                max_value=UINT32_MAX,
                description="Random number generator seed for sampling",
                default_value=0,
                parent_parameter="Partition or sample mode",
                parent_parameter_val=(SampleMethods.Sampling,),
            ),
            stratify_flag3: ModeParameter(
                TrueFalseType,
                name="Stratified split for sampling",
                friendly_name="Stratified split for sampling",
                description="Indicates whether the split is stratified or not for sampling",
                default_value=TrueFalseType.FALSE,
                parent_parameter="Partition or sample mode",
                parent_parameter_val=(SampleMethods.Sampling,),
            ),
            strats_column3: ColumnPickerParameter(
                name="Stratification key column for sampling",
                friendly_name="Stratification key column for sampling",
                description="Column containing stratification key for sampling",
                parent_parameter="Stratified split for sampling",
                parent_parameter_val=(TrueFalseType.TRUE,),
                column_picker_for="Dataset",
                single_column_selection=True,
                column_selection_categories=(SelectedColumnCategory.All,),
            ),
            head_num_rows: IntParameter(
                name="Number of rows to select",
                friendly_name="Number of rows to select",
                description="Maximum number of records that will be allowed to pass through to the next module",
                default_value=10,
                parent_parameter="Partition or sample mode",
                parent_parameter_val=(SampleMethods.Head,),
                min_value=0,
            )
    ) -> (
            DataTableOutputPort(
                name="oDataset",
                friendly_name="Results dataset",
                description="Dataset resulting from the split",
            ),
    ):
        input_values = locals()
        return PartitionAndSampleModule._run_impl(**input_values)

    @classmethod
    def _run_impl(cls,
                  table: DataTable,
                  method: SampleMethods,
                  with_replacement: bool,
                  random_flag: bool,
                  seed: int,
                  partition_method: PartitionMethods,
                  num_partitions: int,
                  stratify_flag1: TrueFalseType,
                  strats_column1: DataTableColumnSelection,
                  folds_prop_list: str,
                  stratify_flag2: TrueFalseType,
                  strats_column2: DataTableColumnSelection,
                  fold_index: int,
                  pick_complement: bool,
                  rate: float,
                  seed_sampling: int,
                  stratify_flag3: TrueFalseType,
                  strats_column3: DataTableColumnSelection,
                  head_num_rows: int
                  ):
        if method == SampleMethods.NFoldSplit:
            logger.info('method is SampleMethods.NFoldSplit')
            if partition_method == PartitionMethods.EvenSizePartitioner:
                logger.info('partition_method is PartitionMethods.EvenSizePartitioner')
                stratify_flag = (stratify_flag1 == TrueFalseType.TRUE)
                strats_column = strats_column1
            else:
                logger.info('partition_method is PartitionMethods.CustomizedPartitioner')
                stratify_flag = (stratify_flag2 == TrueFalseType.TRUE)
                strats_column = strats_column2

            return cls._n_fold_partition(table=table,
                                         with_replacement=with_replacement,
                                         random_flag=random_flag,
                                         seed=seed,
                                         partition_method=partition_method,
                                         num_partitions=num_partitions,
                                         folds_prop_list=folds_prop_list,
                                         stratify_flag=stratify_flag,
                                         strats_column=strats_column)

        elif method == SampleMethods.FoldPicker:
            logger.info('method is SampleMethods.FoldPicker')
            return cls._fold_picker(table=table,
                                    fold_index=fold_index,
                                    pick_complement=pick_complement)

        elif method == SampleMethods.Sampling:
            logger.info('method is SampleMethods.Sampling')
            return cls._sampling(table=table,
                                 rate=rate,
                                 seed_sampling=seed_sampling,
                                 stratify_flag=(stratify_flag3 == TrueFalseType.TRUE),
                                 strats_column=strats_column3)

        elif method == SampleMethods.Head:
            logger.info('method is SampleMethods.Head')
            return cls._select_head_rows(table=table,
                                         head_num_rows=head_num_rows)

    @classmethod
    def _n_fold_partition(cls,
                          table: DataTable,
                          with_replacement: bool,
                          random_flag: bool,
                          seed: int,
                          partition_method: PartitionMethods,
                          num_partitions: int,
                          folds_prop_list: str,
                          stratify_flag: bool,
                          strats_column: DataTableColumnSelection):
        cls._verify_num_partitions(table, num_partitions)
        if partition_method == PartitionMethods.EvenSizePartitioner:
            cls._verify_table_parameters_strata(table, stratify_flag, strats_column, 'strats_column1')
        else:
            cls._verify_table_parameters_strata(table, stratify_flag, strats_column, 'strats_column2')

        is_even = partition_method == PartitionMethods.EvenSizePartitioner

        # stratify datatable
        if stratify_flag:
            data_groups = splitter.stratify_split_to_indices_groups(table, strats_column)
        else:
            # use df.index instead of row-index to align the result of stratify split.
            data_groups = [table.data_frame.index]

        # calc percentage
        if is_even:
            logger.info(f"create fold percentage: partition={num_partitions}")
            pct_values = cls._create_percentage(partition_num=num_partitions)
        else:
            logger.info(f"create fold percentage: fold_list={folds_prop_list}")
            try:
                pct_values = cls._create_percentage(fold_list=folds_prop_list)
            except ValueError:
                raise ParameterParsingError(cls._param_keys['folds_prop_list'])

            if not all([0 <= pct <= 1 for pct in pct_values]):
                raise NotInRangeValueError(
                    arg_name=cls._param_keys['folds_prop_list'], lower_boundary=0.0, upper_boundary=1.0)

        num_folds = len(pct_values)
        rand = np.random.RandomState(seed) if random_flag else None
        log_list_values("folds", pct_values)

        # split function
        def create_shape(total_rows):
            if is_even:
                per_fold_cnt, left_over = divmod(total_rows, num_folds)
                index_shuffled = list(range(0, num_folds))
                if rand:
                    rand.shuffle(index_shuffled)

                shape = [per_fold_cnt for _ in range(0, num_folds)]
                for i in range(0, left_over):
                    shape[index_shuffled[i]] += 1
                return shape
            else:
                sum_cnt = 0
                shape = [0] * num_folds
                for i in range(0, num_folds - 1):
                    shape[i] = round(total_rows * pct_values[i])
                    if sum_cnt + shape[i] > total_rows:
                        shape[i] = total_rows - sum_cnt
                    sum_cnt += shape[i]
                shape[num_folds - 1] = total_rows - sum_cnt
                return shape

        def execute_split(index_array):
            shape = create_shape(len(index_array))
            log_list_values("shape", shape)
            return splitter.split(index_array, shape, rand, with_replacement)

        logger.info(f"execute split, {len(data_groups)} groups")
        splitted_groups = [execute_split(x) for x in data_groups]
        fold_indices = [list(itertools.chain.from_iterable(g[fold] for g in splitted_groups))
                        for fold in range(0, num_folds)]

        if rand:
            logger.info(f"randomize folds.")
            for ary in fold_indices:
                rand.shuffle(ary)

        logger.info(f"generate {len(fold_indices)} fold indices data")
        log_list_values("fold sizes", [len(indices) for indices in fold_indices])

        cls._remove_partition_data(table)
        cls._save_partition_info(table, fold_indices)
        return table,

    @classmethod
    def _fold_picker(cls,
                     table: DataTable,
                     fold_index: int,
                     pick_complement: bool):
        # 1-based to 0-based index
        fold_index -= 1
        ErrorMapping.verify_not_null_or_empty(table, cls._param_keys['table'])

        fold_indices = cls._get_partition_info(table)
        logger.info(f"get partition info: {len(fold_indices) if fold_indices is not None else 'None'} folds")
        if not (fold_indices and 0 <= fold_index < len(fold_indices)):
            raise InvalidDatasetError(cls._param_keys['table'])

        df = table.data_frame
        df_indices = fold_indices[fold_index]
        if pick_complement:
            df_indices = df.index.difference(df_indices)

        logger.info(f"picking fold[{fold_index}] {'complement' if pick_complement else ''}, {len(df_indices)} rows")
        table_selected = df.loc[df_indices]
        table_selected.reset_index(drop=True, inplace=True)

        # Bug 476541:
        #   pandas.read_csv does not ensure that all rows in one column have the same data type. A column could consist
        #   of int/nan/str values, and shown as dtype.object. Sampling a subset may pick all rows with the same type
        #   (eg: take 1 row), and raise errors when checking data type. So we won't pass the original metadata any more.
        # TODO: complement column kinds, categorical, extended properties to the result datatable in future.
        #
        # dt = DataTable(table_selected, table.get_meta_data(if_clone=True))
        dt = DataTable(table_selected)
        cls._remove_partition_data(dt)
        return dt,

    @classmethod
    def _sampling(cls,
                  table: DataTable,
                  rate: float,
                  seed_sampling: int,
                  stratify_flag: bool,
                  strats_column: DataTableColumnSelection):
        # verify parameters
        ErrorMapping.verify_not_null_or_empty(table, cls._param_keys['table'])

        if table.number_of_columns:
            ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(curr_column_count=table.number_of_columns,
                                                                           required_column_count=1,
                                                                           arg_name=cls._param_keys['table'])

        if np.isnan(rate):
            raise NaNError(cls._param_keys['rate'])

        if rate < 0 or rate > 1:
            raise NotInRangeValueError(arg_name=cls._param_keys['rate'], lower_boundary=0, upper_boundary=1)

        cls._verify_table_parameters_strata(table, stratify_flag, strats_column, 'strats_column3')

        if table.number_of_rows == 0:
            return table.clone(),

        df = table.data_frame
        rand = np.random.RandomState(seed=seed_sampling)

        if stratify_flag:
            df_indices = splitter.stratify_split_to_indices_groups(table, strats_column)

        else:
            # use df.index instead of row-index to align the result of stratify split.
            df_indices = [table.data_frame.index]

        def sampling_index(df_index):
            df_index = splitter.sample_index(df_index, frac=1, random_state=rand)
            select_row_count = int(round(len(df_index) * rate))
            logger.info(f"sample row count: {select_row_count}")
            return df_index[0:select_row_count]

        sampling_result = list(itertools.chain.from_iterable([sampling_index(df_index) for df_index in df_indices]))
        table_selected = df.loc[sampling_result]
        table_selected.reset_index(drop=True, inplace=True)

        # Bug 476541:
        # dt = DataTable(table_selected, table.get_meta_data(if_clone=True))
        dt = DataTable(table_selected)

        return dt,

    @classmethod
    def _select_head_rows(cls,
                          table: DataTable,
                          head_num_rows: int):
        # verify table
        ErrorMapping.verify_not_null_or_empty(table, cls._param_keys['table'])

        if table.number_of_columns:
            ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(curr_column_count=table.number_of_columns,
                                                                           required_column_count=1,
                                                                           arg_name=cls._param_keys['table'])

        # verify num
        ErrorMapping.verify_greater_than_or_equal_to(head_num_rows, 0, cls._param_keys['head_num_rows'])
        if head_num_rows > table.number_of_rows:
            head_num_rows = table.number_of_rows

        logger.info(f"get head row count: {head_num_rows}")
        table_selected = table.data_frame.head(head_num_rows)

        # Bug 476541:
        # dt = DataTable(table_selected, table.get_meta_data(if_clone=True))
        dt = DataTable(table_selected)

        return dt,

    @classmethod
    def _verify_num_partitions(cls,
                               table: DataTable,
                               num_partitions: int):
        # Throw TooFewRowsInDatasetError when num_samples less than num_partitions
        # in table like what sklearn check_cv does.
        if num_partitions is not None and table is not None:
            num_samples = table.data_frame.shape[0]
            ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(
                curr_row_count=num_samples, required_row_count=num_partitions, arg_name='num_samples')

    @classmethod
    def _verify_table_parameters_strata(cls,
                                        table: DataTable,
                                        stratify_flag: bool,
                                        strats_column: DataTableColumnSelection,
                                        strata_name):
        if stratify_flag:
            ErrorMapping.verify_not_null_or_empty(strats_column, cls._param_keys[strata_name])
            column_indices = strats_column.select_column_indexes(table)
            if len(column_indices) == 0:
                raise ColumnNotFoundError()

    @classmethod
    def _create_percentage(cls, partition_num: int = None, fold_list: str = None):
        if partition_num is not None:
            ErrorMapping.verify_greater_than(partition_num, 0, "partition_num")
            return [1.0 / partition_num for _ in range(0, partition_num)]

        elif fold_list is not None:
            pct_values = [float(s) for s in fold_list.split(',')]
            total = sum(pct_values)
            if total > 1:
                raise ValueError('Percentage sum > 1.')
            elif total < 1:
                pct_values.append(1 - total)
            return pct_values

    @classmethod
    def _remove_partition_data(cls, table: DataTable):
        table.meta_data.extended_properties.pop(_META_PROPERTY_KEY, None)

    @classmethod
    def _save_partition_info(cls, table: DataTable, fold_indices):
        table.meta_data.extended_properties[_META_PROPERTY_KEY] = fold_indices

    @classmethod
    def _get_partition_info(cls, table: DataTable):
        return table.meta_data.extended_properties.get(_META_PROPERTY_KEY, None)


# The class containing a module_entry decorator can not be imported directly due to a limit of module_collector,
# (A 'Duplicate family id' error will occur.)
# Add this top level function as a workaround as this class is imported in other module class.
def n_fold_partition(table, with_replacement, random_flag, seed, partition_method,
                     num_partitions, folds_prop_list, stratify_flag, strats_column):
    return PartitionAndSampleModule._n_fold_partition(
        table, with_replacement, random_flag, seed, partition_method,
        num_partitions, folds_prop_list, stratify_flag, strats_column)
