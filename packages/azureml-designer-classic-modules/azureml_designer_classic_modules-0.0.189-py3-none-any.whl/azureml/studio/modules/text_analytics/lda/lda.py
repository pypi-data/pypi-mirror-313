from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.modulehost.attributes import DataTableInputPort, ModuleMeta, DataTableOutputPort, IntParameter, \
    BooleanParameter, ITransformOutputPort, ColumnPickerParameter, SelectedColumnCategory, ModeParameter, FloatParameter
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.input_parameter_checker import InputParameterChecker
from azureml.studio.modules.text_analytics.lda.lda_transform import LDATransform
from azureml.studio.core.logger import TimeProfile
from azureml.studio.modulehost.constants import FLOAT_MIN_POSITIVE
from azureml.studio.common.types import AutoEnum
from azureml.studio.modulehost.attributes import ItemInfo


class LDATrueFalseType(AutoEnum):
    TRUE: ItemInfo(name="True", friendly_name="True") = ()
    FALSE: ItemInfo(name="False", friendly_name="False") = ()


class LatentDirichletAllocationModule(BaseModule):
    @staticmethod
    @module_entry(ModuleMeta(
        name="Latent Dirichlet Allocation",
        description="Topic Modeling: Latent Dirichlet Allocation.",
        category="Text Analytics",
        version="1.0",
        owner="Microsoft Corporation",
        family_id="1aec5388-415d-4f7c-b33f-c9e9f4c0ce56",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            dataset: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Input dataset",
            ),
            target_column: ColumnPickerParameter(
                name="Target columns",
                friendly_name="Target column(s)",
                description="Target column name or index",
                column_picker_for="Dataset",
                single_column_selection=False,
                column_selection_categories=(SelectedColumnCategory.String,),
            ),
            topics: IntParameter(
                name="Number of topics to model",
                friendly_name="Number of topics to model",
                description="Model the document distribution against N topics",
                default_value=5,
                min_value=1,
                max_value=1000,
            ),
            ngrams: IntParameter(
                name="N-grams",
                friendly_name="N-grams",
                description="Order of N-grams generated during hashing",
                default_value=2,
                min_value=1,
                max_value=10,
            ),
            normalize: BooleanParameter(
                name="Normalize",
                friendly_name="Normalize",
                description="Normalize output to probabilities. The feature topic matrix will be P(word|topic).",
                default_value=True,
            ),
            show_all_options: ModeParameter(
                LDATrueFalseType,
                name="Show all options",
                friendly_name="Show all options",
                description="Presents additional parameters specific to Skleaarn online LDA",
                default_value=LDATrueFalseType.FALSE,
            ),
            rho: FloatParameter(
                name="Rho parameter",
                friendly_name="Rho parameter",
                is_optional=True,
                description="Rho parameter",
                default_value=0.01,
                parent_parameter="Show all options",
                parent_parameter_val=(LDATrueFalseType.TRUE, ),
                min_value=FLOAT_MIN_POSITIVE,
                max_value=1,
            ),
            alpha: FloatParameter(
                name="Alpha parameter",
                friendly_name="Alpha parameter",
                is_optional=True,
                description="Alpha parameter",
                default_value=0.01,
                parent_parameter="Show all options",
                parent_parameter_val=(LDATrueFalseType.TRUE, ),
                min_value=FLOAT_MIN_POSITIVE,
                max_value=1,
            ),
            lda_d: IntParameter(
                name="Estimated number of documents",
                friendly_name="Estimated number of documents",
                is_optional=True,
                description="Estimated number of documents",
                default_value=1000,
                parent_parameter="Show all options",
                parent_parameter_val=(LDATrueFalseType.TRUE, ),
                min_value=1,
                max_value=2147483647,
            ),
            minibatch: IntParameter(
                name="Size of the batch",
                friendly_name="Size of the batch",
                is_optional=True,
                description="Size of the batch",
                default_value=32,
                parent_parameter="Show all options",
                parent_parameter_val=(LDATrueFalseType.TRUE, ),
                min_value=1,
                max_value=1024,
            ),
            initial_t: IntParameter(
                name="Initial value of iteration count",
                friendly_name="Initial value of iteration used in learning rate update schedule",
                is_optional=True,
                description="Initial value of iteration count used in learning rate update schedule",
                default_value=10,
                parent_parameter="Show all options",
                parent_parameter_val=(LDATrueFalseType.TRUE, ),
                min_value=1,
                max_value=2147483647,
            ),
            power_t: FloatParameter(
                name="Power applied to the iteration during updates",
                friendly_name="Power applied to the iteration during updates",
                is_optional=True,
                description="Power applied to the iteration count during online updates",
                default_value=0.5,
                parent_parameter="Show all options",
                parent_parameter_val=(LDATrueFalseType.TRUE, ),
                min_value=0.5,
                max_value=1,
            ),
            passes: IntParameter(
                name="passes",
                friendly_name="Number of training iterations",
                is_optional=True,
                description="Number of training iterations",
                default_value=25,
                parent_parameter="Show all options",
                parent_parameter_val=(LDATrueFalseType.TRUE, ),
                min_value=1,
                max_value=1024,
            ),
            build_dictionary: ModeParameter(
                LDATrueFalseType,
                name="Build dictionary of ngrams",
                friendly_name="Build dictionary of ngrams",
                description="Builds a dictionary of ngrams prior to computing LDA. "
                            "Useful for model inspection and interpretation",
                default_value=LDATrueFalseType.TRUE,
                parent_parameter="Show all options",
                parent_parameter_val=(LDATrueFalseType.FALSE, ),
            ),
            dictionary_size: IntParameter(
                name="Maximum size of ngram dictionary",
                friendly_name="Maximum size of ngram dictionary",
                is_optional=True,
                description="Maximum size of the ngrams dictionary. "
                            "If number of tokens in the input exceed this size, collisions may occur",
                default_value=20000,
                parent_parameter="Build dictionary of ngrams",
                parent_parameter_val=(LDATrueFalseType.TRUE,),
                min_value=1,
                max_value=2147483647,
            ),
            hash_bits: IntParameter(
                name="Number of hash bits",
                friendly_name="Number of bits to use for feature hashing",
                is_optional=True,
                description="Number of bits to use during feature hashing",
                default_value=12,
                parent_parameter="Build dictionary of ngrams",
                parent_parameter_val=(LDATrueFalseType.FALSE,),
                min_value=1,
                max_value=31,
            ),
            build_dictionary_all_options: ModeParameter(
                LDATrueFalseType,
                name="Build dictionary of ngrams prior to LDA",
                friendly_name="Build dictionary of ngrams prior to LDA",
                description="Builds a dictionary of ngrams prior to LDA. "
                            "Useful for model inspection and interpretation",
                default_value=LDATrueFalseType.TRUE,
                parent_parameter="Show all options",
                parent_parameter_val=(LDATrueFalseType.TRUE,),
            ),
            dictionary_size_all_options: IntParameter(
                name="Maximum number of ngrams in dictionary",
                friendly_name="Maximum number of ngrams in dictionary",
                is_optional=True,
                description="Maximum size of the dictionary. If number of tokens in the input exceed this size, "
                            "collisions may occur",
                default_value=20000,
                parent_parameter="Build dictionary of ngrams prior to LDA",
                parent_parameter_val=(LDATrueFalseType.TRUE,),
                min_value=1,
                max_value=2147483647,
            ),
            hash_bits_all_options: IntParameter(
                name="Hash bits",
                friendly_name="Number of hash bits",
                is_optional=True,
                description="Number of bits to use for feature hashing",
                default_value=12,
                parent_parameter="Build dictionary of ngrams prior to LDA",
                parent_parameter_val=(LDATrueFalseType.FALSE,),
                min_value=1,
                max_value=31,
            ),
    ) -> (
            DataTableOutputPort(
                name="Transformed dataset",
                friendly_name="Transformed dataset",
                description="Output dataset",
            ),
            DataTableOutputPort(
                name="Feature topic matrix",
                friendly_name="Feature topic matrix",
                description="Feature topic matrix produced by LDA",
            ),
            ITransformOutputPort(
                name="LDA transformation",
                friendly_name="LDA transformation",
                description="Transformation that applies LDA to the dataset",
            ),
    ):
        input_values = locals()
        output_values = LatentDirichletAllocationModule.run_impl(**input_values)
        return output_values

    @classmethod
    def run_impl(
            cls,
            dataset: DataTable,
            target_column: DataTableColumnSelection,
            topics: int,
            ngrams: int,
            normalize: bool,
            show_all_options: LDATrueFalseType,
            rho: float,
            alpha: float,
            lda_d: int,
            minibatch: int,
            initial_t: int,
            power_t: float,
            passes: int,
            build_dictionary: LDATrueFalseType,
            dictionary_size: int,
            hash_bits: int,
            build_dictionary_all_options: LDATrueFalseType,
            dictionary_size_all_options: int,
            hash_bits_all_options: int,
            ):
        selected_data: DataTable = target_column.select(dataset)
        InputParameterChecker.verify_data_table(selected_data, dataset.name)
        InputParameterChecker.verify_all_columns_are_string_type(selected_data, dataset.name)

        show_all_options = cls.enum_to_bool(show_all_options)
        build_dictionary = cls.enum_to_bool(build_dictionary)
        build_dictionary_all_options = cls.enum_to_bool(build_dictionary_all_options)

        build_dictionary = build_dictionary_all_options if show_all_options else build_dictionary
        hash_bits = hash_bits_all_options if show_all_options else hash_bits
        dictionary_size = dictionary_size_all_options if show_all_options else dictionary_size

        max_feature = dictionary_size if build_dictionary else pow(2, hash_bits)

        transform = LDATransform(
            target_column_names=selected_data.column_names,
            topics_number=topics,
            ngrams=ngrams,
            normalize=normalize,
            show_all_options=show_all_options,
            rho=rho,
            alpha=alpha,
            lda_d=lda_d,
            minibatch=minibatch,
            initial_t=initial_t,
            power_t=power_t,
            passes=passes,
            build_dictionary=build_dictionary,
            max_feature=max_feature
        )
        with TimeProfile("Apply Latent Dirichlet allocation to target texts"):
            document_topic_result_dt = transform.train_lda_model(dataset)
            with TimeProfile("Get feature-topic matrix"):
                feature_topic_matrix_dt = DataTable(transform.get_feature_topic_matrix())

        return document_topic_result_dt, feature_topic_matrix_dt, transform

    @classmethod
    def enum_to_bool(cls, value: LDATrueFalseType):
        return value == LDATrueFalseType.TRUE
