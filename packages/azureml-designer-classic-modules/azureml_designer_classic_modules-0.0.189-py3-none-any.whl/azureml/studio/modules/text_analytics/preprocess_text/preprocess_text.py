import re
import spacy
import pandas as pd
from spacy.lang.en.stop_words import STOP_WORDS as sp_stopwords
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.error import ErrorMapping, InvalidColumnTypeError, FailedToCompleteOperationError
from azureml.studio.modulehost.constants import ElementTypeName
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.core.logger import module_logger, TimeProfile
from azureml.studio.modulehost.attributes import DataTableInputPort, ColumnPickerParameter, ModeParameter, \
    SelectedColumnCategory, BooleanParameter, StringParameter, ModuleMeta, DataTableOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modules.text_analytics.preprocess_text.preprocess_text_utils import PreprocessTextTrueFalseType, \
    PreprocessTextLanguage, PreprocessTextConstant, POSTag, \
    PreprocessTextPattern
from functools import partial


class PreprocessTextModule(BaseModule):
    @staticmethod
    @module_entry(ModuleMeta(
        name="Preprocess Text",
        description="Performs cleaning operations on text.",
        category="Text Analytics",
        version="1.0",
        owner="Microsoft Corporation",
        family_id="{BF9E794A-9E2B-4662-902A-0E73B255C135}",
        release_state=ReleaseState.Release,
        is_deterministic=True
    ))
    def run(
            dataset: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Input data",
            ),
            stopwords: DataTableInputPort(
                name="Stop words",
                friendly_name="Stop words",
                is_optional=True,
                description="Optional custom list of stop words to remove",
            ),
            language: ModeParameter(
                PreprocessTextLanguage,
                name="Language",
                friendly_name="Language",
                description="Select the language to preprocess",
                default_value=PreprocessTextLanguage.English,
            ),
            # the actual parent parameter value is PreprocessTextLanguage.Column,
            # however, we do not support it now
            language_column: ColumnPickerParameter(
                name="Culture-language column",
                friendly_name="Culture-language column",
                description="Name or one-based index of the column containing the culture-language information",
                parent_parameter="Language",
                parent_parameter_val=(PreprocessTextLanguage.English,),
                column_picker_for="Dataset",
                single_column_selection=True,
                column_selection_categories=(SelectedColumnCategory.String,),
                release_state=ReleaseState.Alpha
            ),
            text_column: ColumnPickerParameter(
                name="Text column to clean",
                friendly_name="Text column to clean",
                description="Select the text column to clean",
                column_picker_for="Dataset",
                single_column_selection=True,
                column_selection_categories=(SelectedColumnCategory.String,),
            ),
            remove_stopwords: BooleanParameter(
                name="Remove stop words",
                friendly_name="Remove stop words",
                description="Remove stop words",
                default_value=True,
            ),
            use_lemmatization: BooleanParameter(
                name="Use lemmatization",
                friendly_name="Use lemmatization",
                description="Use lemmatization",
                default_value=True,
            ),
            # add more parent parameter value if we support more languages
            part_of_speech_filter: ModeParameter(
                PreprocessTextTrueFalseType,
                name="Remove by part-of-speech",
                friendly_name="Remove by part-of-speech",
                description="Indicate whether part-of-speech analysis should be used "
                            "to identify and remove certain word classes",
                default_value=PreprocessTextTrueFalseType.FALSE,
                parent_parameter="Language",
                parent_parameter_val=(PreprocessTextLanguage.English,),
                release_state=ReleaseState.Alpha
            ),
            filter_nouns: BooleanParameter(
                name="Remove nouns",
                friendly_name="Remove nouns",
                description="Remove nouns",
                default_value=True,
                parent_parameter="Remove by part-of-speech",
                parent_parameter_val=(PreprocessTextTrueFalseType.TRUE,),
            ),
            filter_adjectives: BooleanParameter(
                name="Remove adjectives",
                friendly_name="Remove adjectives",
                description="Remove adjectives",
                default_value=True,
                parent_parameter="Remove by part-of-speech",
                parent_parameter_val=(PreprocessTextTrueFalseType.TRUE,),
            ),
            filter_verbs: BooleanParameter(
                name="Remove verbs",
                friendly_name="Remove verbs",
                description="Remove verbs",
                default_value=True,
                parent_parameter="Remove by part-of-speech",
                parent_parameter_val=(PreprocessTextTrueFalseType.TRUE,),
            ),
            detect_sentences: BooleanParameter(
                name="Detect sentences",
                friendly_name="Detect sentences",
                description="Detect sentences by adding a sentence terminator \"|||\" that can be used by the "
                            "n-gram features extractor module",
                default_value=True,
            ),
            normalize_case: BooleanParameter(
                name="Normalize case to lowercase",
                friendly_name="Normalize case to lowercase",
                description="Normalize case to lowercase",
                default_value=True,
            ),
            remove_numbers: BooleanParameter(
                name="Remove numbers",
                friendly_name="Remove numbers",
                description="Remove numbers",
                default_value=True,
            ),
            remove_special_characters: BooleanParameter(
                name="Remove special characters",
                friendly_name="Remove special characters",
                description="Remove non-alphanumeric special characters and replace them with \"|\" character",
                default_value=True,
            ),
            remove_duplicate_characters: BooleanParameter(
                name="Remove duplicate characters",
                friendly_name="Remove duplicate characters",
                description="Remove duplicate characters",
                default_value=True,
            ),
            remove_emails: BooleanParameter(
                name="Remove email addresses",
                friendly_name="Remove email addresses",
                description="Remove email addresses",
                default_value=True,
            ),
            remove_urls: BooleanParameter(
                name="Remove URLs",
                friendly_name="Remove URLs",
                description="Remove URLs",
                default_value=True,
            ),
            expand_verb_contractions: BooleanParameter(
                name="Expand verb contractions",
                friendly_name="Expand verb contractions",
                description="Expand verb contractions (English only)",
                default_value=True,
                parent_parameter="Language",
                parent_parameter_val=(PreprocessTextLanguage.English,),
            ),
            normalize_slashes: BooleanParameter(
                name="Normalize backslashes to slashes",
                friendly_name="Normalize backslashes to slashes",
                description="Normalize backslashes to slashes",
                default_value=True,
            ),
            split_tokens_by_chars: BooleanParameter(
                name="Split tokens on special characters",
                friendly_name="Split tokens on special characters",
                description="Split tokens on special characters",
                default_value=True,
            ),
            custom_expression: StringParameter(
                name="Custom regular expression",
                friendly_name="Custom regular expression",
                is_optional=True,
                description="Specify the custom regular expression",
            ),
            custom_replacement: StringParameter(
                name="Custom replacement string",
                friendly_name="Custom replacement string",
                is_optional=True,
                description="Specify the custom replacement string for the custom regular expression",
            )
    ) -> (
            DataTableOutputPort(
                name="Results dataset",
                friendly_name="Results dataset",
                description="Results dataset",
            ),
    ):
        input_values = locals()
        output_values = PreprocessTextModule.preprocess(**input_values)
        return output_values

    @classmethod
    def _validate_arguments(cls, dataset: DataTable, stopwords: DataTable, text_column):
        # verify dataset
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(curr_column_count=dataset.number_of_columns,
                                                                       required_column_count=1,
                                                                       arg_name=cls._args.dataset.friendly_name)
        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=dataset.number_of_rows,
                                                                    required_row_count=1,
                                                                    arg_name=cls._args.dataset.friendly_name)

        # verify text columns
        ErrorMapping.verify_not_null_or_empty(text_column, cls._args.text_column.friendly_name)
        column_index = text_column.select_column_indexes(dataset)
        ErrorMapping.verify_if_all_columns_selected(
            act_col_count=len(column_index), exp_col_count=1,
            selection_pattern_friendly_name=cls._args.text_column.friendly_name,
            long_description=True)
        PreprocessTextModule._verify_string_column_type(dataset, dataset.get_column_name(column_index[0]),
                                                        cls._args.text_column.friendly_name)

        # verify that stopwords dataset contains only 1 column
        if stopwords:
            stopwords_column_count = stopwords.number_of_columns
            ErrorMapping.verify_number_of_columns_equal_to(curr_column_count=stopwords_column_count,
                                                           required_column_count=1,
                                                           arg_name=cls._args.stopwords.friendly_name)

            # verify that stopwords is of type string
            PreprocessTextModule._verify_string_column_type(stopwords, stopwords.get_column_name(0),
                                                            cls._args.stopwords.friendly_name)
        return

    @staticmethod
    def _verify_string_column_type(datatable: DataTable, column_name, arg_name=None):
        if datatable.get_element_type(column_name) != ElementTypeName.STRING:
            ErrorMapping.throw(
                InvalidColumnTypeError(col_name=column_name, col_type=datatable.get_column_type(column_name),
                                       arg_name=arg_name))

    @staticmethod
    def tokenize(document, sp_language_model):
        tokenized_document = []
        if len(document) > sp_language_model.max_length:
            ErrorMapping.throw(FailedToCompleteOperationError(failed_operation="parser",
                                                              reason=f"Text length {len(document)} exceeds maximum "
                                                              f"requirement of {sp_language_model.max_length}"))
        for sentence in sp_language_model(document).sents:
            tokenized_sentence = []
            for token in sentence:
                if not token.is_space:
                    tokenized_sentence.append(token)
            tokenized_document.append(tokenized_sentence)
        return tokenized_document

    @staticmethod
    def remove_numbers_and_characters(document, removed_tag_set):
        preprocessed_document = []
        for sentence in document:
            preprocessed_sentence = []
            for token in sentence:
                if token.pos_ not in removed_tag_set:
                    preprocessed_sentence.append(token)
            preprocessed_document.append(preprocessed_sentence)
        return preprocessed_document

    @staticmethod
    def remove_stopwords(document, stopwords):
        preprocessed_document = []
        for sentence in document:
            preprocessed_sentence = []
            for token in sentence:
                if (token.pos_ != POSTag.Pron and token.lemma_ not in stopwords) \
                        or (token.pos_ == POSTag.Pron and token.text not in stopwords):
                    preprocessed_sentence.append(token)
            preprocessed_document.append(preprocessed_sentence)
        return preprocessed_document

    @staticmethod
    def normalize_document(document, use_lemmatization, normalize_case):
        preprocessed_document = []
        for sentence in document:
            preprocessed_sentence = []
            for token in sentence:
                if use_lemmatization and token.pos_ != POSTag.Pron:
                    token = token.lemma_
                if normalize_case:
                    token = str(token).lower()
                preprocessed_sentence.append(token)
            preprocessed_document.append(preprocessed_sentence)
        return preprocessed_document

    @staticmethod
    def apply_custom_expression(document, custom_expression, custom_replacement):
        try:
            if custom_replacement:
                document = re.sub(custom_expression, custom_replacement, document)
            else:
                document = re.sub(custom_expression, "", document)
        except re.error:
            ErrorMapping.throw(
                FailedToCompleteOperationError(f"apply custom regular expression"))
        return document

    @staticmethod
    def expand_verb_contractions(document):
        for pattern, replacement in PreprocessTextPattern.VerbContractionDict.items():
            document = re.sub(pattern, replacement, document)

        return document

    @staticmethod
    def normalize_slashes(document):
        document = document.replace('\\', '/')
        return document

    @staticmethod
    def detect_document_sentences(document):
        preprocessed_document = []
        for sentence in document:
            if not sentence:
                continue
            if preprocessed_document:
                sentence = [PreprocessTextConstant.SentenceSeparator] + sentence
            preprocessed_document.append(sentence)

        return preprocessed_document

    @staticmethod
    def document_to_string(document):
        preprocessed_token = []
        for sentence in document:
            for token in sentence:
                preprocessed_token.append(str(token))
        return PreprocessTextConstant.TokenSeparator.join(preprocessed_token)

    # some arguments are not used, but we keep them for being consistent with v1
    @staticmethod
    def preprocess(dataset: DataTable,
                   stopwords: DataTable,
                   language: PreprocessTextLanguage,
                   language_column: DataTableColumnSelection,
                   text_column: DataTableColumnSelection,
                   remove_stopwords: bool,
                   use_lemmatization: bool,
                   part_of_speech_filter: PreprocessTextTrueFalseType,
                   filter_nouns: bool,
                   filter_adjectives: bool,
                   filter_verbs: bool,
                   detect_sentences: bool,
                   normalize_case: bool,
                   remove_numbers: bool,
                   remove_special_characters: bool,
                   remove_duplicate_characters: bool,
                   remove_emails: bool,
                   remove_urls: bool,
                   expand_verb_contractions: bool,
                   normalize_slashes: bool,
                   split_tokens_by_chars: bool,
                   custom_expression: str,
                   custom_replacement: str):
        # validate arguments
        PreprocessTextModule._validate_arguments(dataset, stopwords, text_column)
        # get text column
        text_column_index = text_column.select_column_indexes(dataset)[0]
        text_column_name = dataset.get_column_name(text_column_index)
        documents = dataset.get_column(text_column_name)
        # get language corresponding model
        module_logger.info("Loading corresponding language model.")
        sp_language_model = spacy.load(PreprocessTextConstant.LanguageModelDict[language], disable=["ner"])
        # load stopwords
        if stopwords:
            stopwords = set(stopwords.get_column(0).values)
        else:
            stopwords = sp_stopwords
        # generate removed tag set with remove_numbers and remove_special_characters params
        removed_tag_set = {POSTag.Num} if remove_numbers else set()
        removed_tag_set = removed_tag_set.union({POSTag.Sym,
                                                 POSTag.Punct}) \
            if remove_special_characters else removed_tag_set

        # define all preprocessors
        custom_expression_preprocessor = partial(PreprocessTextModule.apply_custom_expression,
                                                 custom_expression=custom_expression,
                                                 custom_replacement=custom_replacement)
        remove_urls_preprocessor = partial(re.sub, PreprocessTextPattern.URLPattern, "")
        expand_verb_contractions_preprocessor = PreprocessTextModule.expand_verb_contractions
        remove_emails_preprocessor = partial(re.sub, PreprocessTextPattern.EmailPattern, "")
        normalize_slashes_preprocessor = PreprocessTextModule.normalize_slashes
        split_tokens_by_chars_preprocessor = partial(re.sub, PreprocessTextPattern.SpecialCharsPattern, r" \1 ")
        remove_duplicate_characters_preprocessor = partial(re.sub, PreprocessTextPattern.DuplicateCharsPattern, r"\1\1")
        tokenize_preprocessor = partial(PreprocessTextModule.tokenize, sp_language_model=sp_language_model)
        remove_numbers_and_characters_preprocessor = partial(PreprocessTextModule.remove_numbers_and_characters,
                                                             removed_tag_set=removed_tag_set)
        remove_stopwords_preprocessor = partial(PreprocessTextModule.remove_stopwords, stopwords=stopwords)
        normalize_document_preprocessor = partial(PreprocessTextModule.normalize_document,
                                                  use_lemmatization=use_lemmatization, normalize_case=normalize_case)
        detect_sentences_preprocessor = PreprocessTextModule.detect_document_sentences
        to_string_preprocessor = PreprocessTextModule.document_to_string
        # include necessary preprocessors
        param_preprocessor = [(custom_expression, custom_expression_preprocessor),
                              (remove_urls, remove_urls_preprocessor),
                              (expand_verb_contractions, expand_verb_contractions_preprocessor),
                              (remove_emails, remove_emails_preprocessor),
                              (normalize_slashes, normalize_slashes_preprocessor),
                              (split_tokens_by_chars, split_tokens_by_chars_preprocessor),
                              (remove_duplicate_characters, remove_duplicate_characters_preprocessor),
                              (True, tokenize_preprocessor),
                              (remove_numbers or remove_special_characters, remove_numbers_and_characters_preprocessor),
                              (remove_stopwords, remove_stopwords_preprocessor),
                              (normalize_case or use_lemmatization, normalize_document_preprocessor),
                              (detect_sentences, detect_sentences_preprocessor),
                              (True, to_string_preprocessor)]
        preprocessors = [preprocessor for param, preprocessor in param_preprocessor if param]

        # preprocess documents
        preprocessed_documents = []
        with TimeProfile("Apply preprocess function to target texts"):
            for document in documents:
                if isinstance(document, str):
                    for preprocessor in preprocessors:
                        document = preprocessor(document)
                preprocessed_documents.append(document)
        # get a column name for preprocessed text
        candidate_preprocessed_text_column_name = f"{PreprocessTextConstant.PreprocessedColumnPrefix}" \
            f" {text_column_name}"
        preprocessed_text_column_name = candidate_preprocessed_text_column_name
        preprocessed_id = 0
        while preprocessed_text_column_name in dataset.column_names:
            preprocessed_id += 1
            preprocessed_text_column_name = f"{candidate_preprocessed_text_column_name}" \
                f" {str(preprocessed_id)}"
        preprocessed_documents = pd.Series(preprocessed_documents, name=preprocessed_text_column_name)
        # get result data table
        dataset_df = dataset.data_frame.reset_index(drop=True)
        result_dt = DataTable(pd.concat([dataset_df, preprocessed_documents], axis=1))

        return result_dt,
