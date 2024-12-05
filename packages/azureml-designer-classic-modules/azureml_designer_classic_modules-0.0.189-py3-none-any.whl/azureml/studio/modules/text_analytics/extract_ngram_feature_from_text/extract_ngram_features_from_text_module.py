from collections import defaultdict
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from azureml.studio.modulehost.attributes import ModuleMeta, DataTableInputPort, DataTableOutputPort, \
    ColumnPickerParameter, ModeParameter, IntParameter, FloatParameter, BooleanParameter, SelectedColumnCategory
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import ErrorMapping, ColumnNotFoundError, NoColumnsSelectedError, \
    BadNumberOfSelectedColumnsError, FailedToCompleteOperationError, NullOrEmptyError
from azureml.studio.common.input_parameter_checker import InputParameterChecker
from azureml.studio.core.logger import module_logger, TimeProfile
from azureml.studio.modulehost.constants import ElementTypeName
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.text_analytics.extract_ngram_feature_from_text.ngram_extractors import \
    TfNGramFeatureExtractor, IdfNGramFeatureExtractor, PresenceNGramFeatureExtractor, TfIdfNGramFeatureExtractor, \
    FeatureExtractorParameters
from azureml.studio.modules.text_analytics.extract_ngram_feature_from_text.ngram_utils import ScoringMethod, \
    VocabularyMode, WeightingFunction, ReduceDimensionalityMode, NGramFeaturesConstants, \
    VocabDataSetColumnName, NGramInfo
from azureml.studio.core.utils.strutils import add_suffix_number_to_avoid_repetition_by_batch


class ExtractNGramFeaturesFromTextModule(BaseModule):
    @staticmethod
    @module_entry(
        ModuleMeta(
            name="Extract N-Gram Features from Text",
            description="Creates N-Gram dictionary features and does feature selection on them.",
            category="Text Analytics",
            version="1.0",
            owner="Microsoft Corporation",
            family_id="a8a662d0-89bb-48c9-8562-9b9589124c4a",
            release_state=ReleaseState.Release,
            is_deterministic=True,
        ))
    def run(
            input_dataset: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Input data",
            ),
            vocab_dataset: DataTableInputPort(
                name="Input vocabulary",
                friendly_name="Input vocabulary",
                is_optional=True,
                description="Input vocabulary",
            ),
            text_column_index_or_name: ColumnPickerParameter(
                name="Text column",
                friendly_name="Text column",
                description="Name or index (one-based) of text column",
                column_picker_for="Dataset",
                single_column_selection=True,
                column_selection_categories=(SelectedColumnCategory.String,),
            ),
            vocabulary_mode: ModeParameter(
                VocabularyMode,
                name="Vocabulary mode",
                friendly_name="Vocabulary mode",
                description="Specify how the n-gram vocabulary should be created from the corpus",
                default_value=VocabularyMode.Create,
            ),
            ngrams_size: IntParameter(
                name="N-Grams size",
                friendly_name="N-grams size",
                description="Indicate the maximum size of n-grams to create",
                default_value=1,
                min_value=1,
            ),
            k_skip_size: IntParameter(
                name="K-Skip size",
                friendly_name="K-Skip size",
                description="Indicate the k-skip size",
                default_value=0,
                min_value=0,
                release_state=ReleaseState.Alpha
            ),
            weighting_func: ModeParameter(
                WeightingFunction,
                name="Weighting function",
                friendly_name="Weighting function",
                description="Choose the weighting function to apply to each n-gram value",
                default_value=WeightingFunction.WeightBin,
            ),
            min_word_length: IntParameter(
                name="Minimum word length",
                friendly_name="Minimum word length",
                description="Specify the minimum length of words to include in n-grams",
                default_value=3,
                min_value=1,
            ),
            max_word_length: IntParameter(
                name="Maximum word length",
                friendly_name="Maximum word length",
                description="Specify the maximum length of words to include in n-grams",
                default_value=25,
                min_value=2,
            ),
            min_doc_freq: FloatParameter(
                name="Minimum n-gram document absolute frequency",
                friendly_name="Minimum n-gram document absolute frequency",
                description="Minimum n-gram document absolute frequency",
                default_value=5,
                min_value=1,
            ),
            max_doc_freq: FloatParameter(
                name="Maximum n-gram document ratio",
                friendly_name="Maximum n-gram document ratio",
                description="Maximum n-gram document ratio",
                default_value=1,
                min_value=0.0001,
            ),
            detect_oov: BooleanParameter(
                name="Detect out-of-vocabulary rows",
                friendly_name="Detect out-of-vocabulary rows",
                description="Detect rows that have words not in the n-gram vocabulary (OOV)",
                default_value=True,
                release_state=ReleaseState.Alpha
            ),
            include_sentence_prefix: BooleanParameter(
                name="Mark begin-of-sentence",
                friendly_name="Mark begin-of-sentence",
                description="Indicate whether a begin-sentence mark should be added to n-grams",
                default_value=False,
                release_state=ReleaseState.Alpha
            ),
            normalize_feature_vector: BooleanParameter(
                name="Normalize n-gram feature vectors",
                friendly_name="Normalize n-gram feature vectors",
                default_value=False,
                description="Normalize n-gram feature vectors.  "
                            "If true, then the n-gram feature vector is divided by its L2 norm.",
            ),
            reduce_dimensionality: ModeParameter(
                ReduceDimensionalityMode,
                name="Use filter-based feature selection",
                friendly_name="Use filter-based feature selection",
                description="Use filter-based feature selection to reduce dimensionality",
                default_value=ReduceDimensionalityMode.TRUE,
                release_state=ReleaseState.Alpha
            ),
            method: ModeParameter(
                ScoringMethod,
                name="Feature scoring method",
                friendly_name="Feature scoring method",
                description="Choose the method to use for scoring",
                default_value=ScoringMethod.FisherScore,
                parent_parameter="Use filter-based feature selection",
                parent_parameter_val=(ReduceDimensionalityMode.TRUE,),
                release_state=ReleaseState.Alpha
            ),
            target_column_index_or_name: ColumnPickerParameter(
                name="Target column",
                friendly_name="Target column",
                description="Specify the target column",
                parent_parameter="Feature scoring method",
                parent_parameter_val=(ScoringMethod.PearsonCorrelation,
                                      ScoringMethod.MutualInformation,
                                      ScoringMethod.KendallCorrelation,
                                      ScoringMethod.SpearmanCorrelation,
                                      ScoringMethod.ChiSquared,
                                      ScoringMethod.FisherScore),
                column_picker_for="Dataset",
                single_column_selection=True,
                column_selection_categories=(SelectedColumnCategory.All,),
                release_state=ReleaseState.Alpha
            ),
            feature_count: IntParameter(
                name="Number of desired features",
                friendly_name="Number of desired features",
                description="Specify the number of features to output in results",
                default_value=1,
                parent_parameter="Feature scoring method",
                parent_parameter_val=(ScoringMethod.PearsonCorrelation,
                                      ScoringMethod.MutualInformation,
                                      ScoringMethod.KendallCorrelation,
                                      ScoringMethod.SpearmanCorrelation,
                                      ScoringMethod.ChiSquared,
                                      ScoringMethod.FisherScore),
                min_value=1,
                release_state=ReleaseState.Alpha
            ),
            threshold: IntParameter(
                name="Minimum number of non-zero elements",
                friendly_name="Minimum number of non-zero elements",
                description="Specify the number of features to output (for CountBased method)",
                default_value=1,
                parent_parameter="Feature scoring method",
                parent_parameter_val=(ScoringMethod.CountBased,),
                min_value=1,
                release_state=ReleaseState.Alpha
            )
    ) -> (
            DataTableOutputPort(
                name="Results dataset",
                friendly_name="Results dataset",
                description="Extracted features",
            ),
            DataTableOutputPort(
                name="Result vocabulary",
                friendly_name="Result vocabulary",
                description="Result vocabulary",
            )):
        input_values = locals()
        output_values = ExtractNGramFeaturesFromTextModule.extract_ngram_features_from_text_module(**input_values)
        return output_values

    @classmethod
    def extract_ngram_features_from_text_module(
            cls,
            input_dataset: DataTable,
            vocab_dataset: DataTable,
            text_column_index_or_name: DataTableColumnSelection,
            vocabulary_mode: VocabularyMode,
            ngrams_size: int,
            k_skip_size: int,
            weighting_func: WeightingFunction,
            min_word_length: int,
            max_word_length: int,
            min_doc_freq: float,
            max_doc_freq: float,
            detect_oov: bool,
            include_sentence_prefix: bool,
            normalize_feature_vector: bool,
            reduce_dimensionality: bool,
            method: ScoringMethod,
            target_column_index_or_name: DataTableColumnSelection,
            feature_count: int,
            threshold: int,
    ):
        input_param = FeatureExtractorParameters(
            vocabulary_mode=vocabulary_mode,
            ngram_size=ngrams_size,
            k_skip_size=k_skip_size,
            min_word_length=min_word_length, max_word_length=max_word_length,
            min_doc_freq=min_doc_freq, max_doc_freq=max_doc_freq,
            detect_oov=detect_oov,
            normalize_feature_vector=normalize_feature_vector,
            include_sentence_prefix=include_sentence_prefix)
        cls.validate_input_args(
            input_dataset=input_dataset,
            vocab_dataset=vocab_dataset,
            text_column_index_or_name=text_column_index_or_name,
            input_params=input_param,
            target_column_index_or_name=target_column_index_or_name)

        text_column_index = text_column_index_or_name.select_column_indexes(input_dataset)
        text_column_name = input_dataset.column_names[text_column_index[0]]
        input_vocabulary = None
        if vocabulary_mode != VocabularyMode.Create:
            input_vocabulary = cls.read_vocabulary_table(vocab_dataset=vocab_dataset)

        feature_dt, output_vocab = cls.extract_features(
            weighting_func=weighting_func,
            input_data=input_dataset,
            input_params=input_param,
            text_column_name=text_column_name, target_column_name=None,
            input_vocabulary=input_vocabulary)
        return feature_dt, output_vocab

    @classmethod
    def _get_extractor_by_weighting_func(
            cls,
            weighting_func: WeightingFunction,
            input_params: FeatureExtractorParameters):
        if weighting_func == WeightingFunction.WeightTf:
            return TfNGramFeatureExtractor(input_params=input_params)
        if weighting_func == WeightingFunction.WeightIdf:
            return IdfNGramFeatureExtractor(input_params=input_params)
        if weighting_func == WeightingFunction.WeightTFIDF:
            return TfIdfNGramFeatureExtractor(input_params=input_params)
        if weighting_func == WeightingFunction.WeightBin:
            return PresenceNGramFeatureExtractor(input_params=input_params)
        else:
            raise NotImplementedError("Not Implemented Weighting Function!")

    @classmethod
    def extract_features(
            cls,
            weighting_func,
            input_params,
            input_data: DataTable,
            text_column_name,
            target_column_name,
            input_vocabulary):
        ErrorMapping.verify_greater_than_or_equal_to(value=input_params.ngram_size, b=1,
                                                     arg_name=cls._args.ngrams_size.friendly_name)
        ngrams_extractor = cls._get_extractor_by_weighting_func(weighting_func=weighting_func,
                                                                input_params=input_params)
        # get text column (and label) column
        text_data = input_data.data_frame[[text_column_name]].copy()
        text_data.columns = ['text']
        if target_column_name is not None:
            text_data['label'] = input_data.get_column(target_column_name)
        else:
            text_data['label'] = None
        ngrams_extractor.extract(text_data, input_vocabulary=input_vocabulary)

        # Build Output Vocabulary
        vocab_df = cls._build_vocabulary_dataframe(vocabulary_dict=ngrams_extractor.output_vocabulary,
                                                   reset_id=(input_params.vocabulary_mode != VocabularyMode.ReadOnly))
        # Build Output N-Gram Feature
        vectorizer = cls._create_vecotrizer_by_vocab(vocab_df)
        # convert features to sparse matrix. instance i -> row i, and ngram j -> column j.
        feature_matrix = vectorizer.transform(ngrams_extractor.feature_vectors)

        # TODO: Add sparse data structure support.
        # Try to convert sparse matrix to dense pandas dataframe
        # Todo: add a try catch here to throw ModuleOutOfMemoryError with details?
        feature_df_column_names = [f"{text_column_name}.[{feature_name}]" for feature_name in vectorizer.feature_names_]
        feature_df = pd.DataFrame(feature_matrix.todense(), columns=feature_df_column_names)
        out_df = cls._build_output_df(input_df=input_data.data_frame, feature_df=feature_df)
        return DataTable(out_df), DataTable(vocab_df)

    @classmethod
    def _build_output_df(cls, input_df, feature_df):
        feature_columns = add_suffix_number_to_avoid_repetition_by_batch(input_strs=feature_df.columns,
                                                                         existed_strs=input_df.columns,
                                                                         starting_suffix_number=1)
        feature_df = feature_df.rename(columns=dict(zip(feature_df.columns, feature_columns)))
        # Fix bug 1523346: need to reset index of input df in case it has duplicated indices.
        # Or concat will meet shape mismatch error.
        input_df.reset_index(drop=True, inplace=True)
        res_df = pd.concat([input_df, feature_df], axis=1)
        return res_df

    @classmethod
    def _create_vecotrizer_by_vocab(cls, vocab_df):
        # todo: encapsulate the DictVectorizer?
        vectorizer = DictVectorizer()
        # use existing ids
        vectorizer.feature_names_ = \
            vocab_df.loc[vocab_df[VocabDataSetColumnName.NGramString] != NGramFeaturesConstants.NumberOfDocuments,
                         VocabDataSetColumnName.NGramString].tolist()
        vectorizer.vocabulary_ = dict(zip(vocab_df[VocabDataSetColumnName.NGramString],
                                          vocab_df[VocabDataSetColumnName.NGramID]))
        # delete NGramFeaturesConstants.NumberOfDocuments from vocabulary
        vectorizer.vocabulary_.pop(NGramFeaturesConstants.NumberOfDocuments, None)
        return vectorizer

    @classmethod
    def _build_vocabulary_dataframe(cls, vocabulary_dict, reset_id):
        if len(vocabulary_dict) == 1:
            # Improper document frequency thresholds may lead to the result that
            # only "number of documents" in the output vocabulary.
            ErrorMapping.throw(FailedToCompleteOperationError(
                failed_operation="Extract n-grams vocabulary from text features. The vocabulary is empty. "
                                 "Please check the minimum n-gram document frequency"))
        vocab_df = pd.DataFrame.from_records(v.to_dict(x) for x, v in vocabulary_dict.items())
        if reset_id:
            # If vocabulary is new created, give a unique id to every n-gram by the idf
            vocab_df = vocab_df.sort_values(
                by=[VocabDataSetColumnName.InverseDocumentFrequency, VocabDataSetColumnName.NGramString],
                ascending=[False, True])
            vocab_df.reset_index(drop=True, inplace=True)
            # reset the id
            vocab_df[VocabDataSetColumnName.NGramID] = vocab_df.index.tolist()
            # Set the total number of documents' id to -1
            vocab_df.loc[vocab_df[VocabDataSetColumnName.NGramString] == NGramFeaturesConstants.NumberOfDocuments,
                         VocabDataSetColumnName.NGramID] = -1
        return vocab_df

    @classmethod
    def read_vocabulary_table(cls, vocab_dataset: DataTable):
        """ Verify input vocabulary dataset is valid, and generate vocabulary dict from it.

        :param vocab_dataset: The column names in VocabDatasetColumnName should be in vocab_dataset as well.
        :return: vocabulary dict, map n-gram string to NGramInfo
        """
        input_vocabulary = defaultdict(NGramInfo)

        module_logger.info("Verify the columns number of vocabulary dataset success.")
        # Verify the Vocabulary has at least one row.
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(vocab_dataset.number_of_rows, 1,
                                                                       cls._args.vocab_dataset.friendly_name)
        module_logger.info("Verify the rows number of vocabulary dataset success.")
        # Verify the Vocabulary has required columns
        required_columns = {VocabDataSetColumnName.NGramID, VocabDataSetColumnName.NGramString,
                            VocabDataSetColumnName.DocumentFrequency, VocabDataSetColumnName.InverseDocumentFrequency}
        vocab_dataset_columns = set(vocab_dataset.column_names)
        missing_column = required_columns - vocab_dataset_columns
        if missing_column:
            ErrorMapping.throw(ColumnNotFoundError(column_id=','.join(missing_column),
                                                   arg_name_missing_column=cls._args.vocab_dataset.friendly_name))

        module_logger.info("Verify the column names of vocabulary dataset success.")
        # Verify the column types of vocabulary
        ErrorMapping.verify_element_type(vocab_dataset.get_element_type(VocabDataSetColumnName.NGramID),
                                         ElementTypeName.INT)
        ErrorMapping.verify_element_type(vocab_dataset.get_element_type(VocabDataSetColumnName.NGramString),
                                         ElementTypeName.STRING)
        ErrorMapping.verify_element_type(vocab_dataset.get_element_type(VocabDataSetColumnName.DocumentFrequency),
                                         ElementTypeName.INT)
        ErrorMapping.verify_element_type(
            vocab_dataset.get_element_type(VocabDataSetColumnName.InverseDocumentFrequency), ElementTypeName.FLOAT)
        module_logger.info("Verify the column types of vocabulary dataset success.")

        # read vocabulary
        with TimeProfile("Reading Vocabulary"):
            for _, row in vocab_dataset.data_frame.iterrows():
                input_vocabulary[row[VocabDataSetColumnName.NGramString]] = NGramInfo(
                    gram_id=row[VocabDataSetColumnName.NGramID],
                    doc_freq=row[VocabDataSetColumnName.DocumentFrequency],
                    inv_doc_freq=row[VocabDataSetColumnName.InverseDocumentFrequency])
        return input_vocabulary

    @classmethod
    def validate_input_args(cls, input_dataset: DataTable, text_column_index_or_name: DataTableColumnSelection,
                            vocab_dataset: DataTable, input_params: FeatureExtractorParameters,
                            target_column_index_or_name: DataTableColumnSelection):
        # Verify input data is not empty.
        InputParameterChecker.verify_data_table(data_table=input_dataset,
                                                friendly_name=cls._args.input_dataset.friendly_name)
        # Verify vocab data is valid.
        if input_params.vocabulary_mode != VocabularyMode.Create:
            if vocab_dataset is None:
                ErrorMapping.throw(
                    NullOrEmptyError(name=cls._args.vocab_dataset.friendly_name,
                                     troubleshoot_hint=f'"{cls._args.vocab_dataset.friendly_name}" can be null only '
                                     f'when "{cls._args.vocabulary_mode.friendly_name}" is "Create".'))

            InputParameterChecker.verify_data_table(data_table=vocab_dataset,
                                                    friendly_name=cls._args.vocab_dataset.friendly_name)
        # Verify select one and only one column as text column.
        ErrorMapping.verify_not_null_or_empty(x=text_column_index_or_name,
                                              name=cls._args.text_column_index_or_name.friendly_name)
        text_column_index = text_column_index_or_name.select_column_indexes(input_dataset)
        if not text_column_index:
            ErrorMapping.throw(NoColumnsSelectedError(column_set=cls._args.text_column_index_or_name.friendly_name))
        if len(text_column_index) > 1:
            ErrorMapping.throw(BadNumberOfSelectedColumnsError(
                selection_pattern_friendly_name=cls._args.text_column_index_or_name.friendly_name,
                expected_col_count=1,
                selected_col_count=len(text_column_index)))
        text_column_name = input_dataset.get_column_name(text_column_index[0])

        # Verify selected text column is a string column.
        ErrorMapping.verify_element_type(type_=input_dataset.get_element_type(text_column_name),
                                         expected_type=ElementTypeName.STRING, column_name=text_column_name,
                                         arg_name=cls._args.input_dataset.friendly_name)
