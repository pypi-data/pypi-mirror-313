import numpy as np
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction import stop_words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize

from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import (ColumnNotFoundError, ErrorMapping, InvalidDatasetError)
from azureml.studio.common.input_parameter_checker import InputParameterChecker
from azureml.studio.core.logger import TimeProfile, module_logger
from azureml.studio.modules.datatransform.common.base_transform import BaseTransform

LEARNING_METHOD = 'online'
STOP_WORDS = 'english'
MIN_N_GRAMS = 1
# TOKEN_PATTERN: '[a-zA-Z]{2,}' regular express, which means Vectorizer only accepts terms including alphabet,
# with length longer than 2
TOKEN_PATTERN = '[a-zA-Z]{2,}'
FEATURE_NAME = 'Feature'


class LDATransform(BaseTransform):
    def __init__(self, target_column_names: list, topics_number: int, ngrams: int, normalize: bool,
                 show_all_options: bool, rho: float, alpha: float, lda_d: int, minibatch: int, initial_t: int,
                 power_t: float, passes: int, build_dictionary: bool, max_feature: int):
        """
        :param topics_number: Number of topics.
        :param ngrams: order of n-grams feature to be extracted.
        :param normalize: Normalize output score values to probabilities.
        :param show_all_options: Presents additional parameters of LDA
        :param transform_build_dictionary: Builds a dictionary of ngrams prior to computing LDA.
        :param rho: Prior of topic word distribution beta.
        :param alpha: Prior of document topic distribution theta.
        :param lda_d: Estimated number of documents
        :param minibatch: Number of documents to use in each iteration.
        :param initial_t: A (positive) parameter that downweights early iterations in online learning.
        :param power_t: Learning rate in the online learning method.
        :param passes: Number of training iterations.
        :param max_feature: Maximum number of features for ngram dictionary
        """
        self._target_column_names = target_column_names
        self._topics_number = topics_number
        self._ngrams = ngrams
        self._normalize = normalize
        self._show_all_options = show_all_options
        self._topic_word_prior = rho
        self._doc_topic_prior = alpha
        self._total_samples = lda_d
        self._batch_size = minibatch
        self._learning_offset = initial_t
        self._learning_decay = power_t
        self._max_iteration = passes
        self._build_dictionary = build_dictionary
        self._max_feature = max_feature
        self._vectorizer = None
        self._lda_model = None

    @property
    def vectorizer(self):
        if self._vectorizer is None:
            self._vectorizer = CountVectorizer(stop_words=STOP_WORDS,
                                               ngram_range=(MIN_N_GRAMS, self._ngrams),
                                               token_pattern=TOKEN_PATTERN,
                                               max_features=self._max_feature)
        return self._vectorizer

    @property
    def lda_model(self):
        if self._lda_model is None:
            module_logger.info("Create Latent Dirichlet Allocation model")
            if self._show_all_options:
                self._lda_model = LatentDirichletAllocation(n_components=self._topics_number,
                                                            max_iter=self._max_iteration,
                                                            learning_method=LEARNING_METHOD,
                                                            doc_topic_prior=self._doc_topic_prior,
                                                            topic_word_prior=self._topic_word_prior,
                                                            total_samples=self._total_samples,
                                                            learning_decay=self._learning_decay,
                                                            learning_offset=float(self._learning_offset),
                                                            batch_size=self._batch_size,
                                                            random_state=0)
            else:
                self._lda_model = LatentDirichletAllocation(n_components=self._topics_number,
                                                            learning_method=LEARNING_METHOD,
                                                            random_state=0)
        return self._lda_model

    def validate_and_clean_dataset(self, dataset: DataTable):
        # Check if dataset is valid
        InputParameterChecker.verify_data_table(dataset, dataset.name)
        # Check if self._target_column_names are included in dataset's column name list
        excluded_column_names = set(self._target_column_names) - set(dataset.column_names)
        if excluded_column_names:
            raise ColumnNotFoundError(column_names=list(excluded_column_names),
                                      arg_name_has_column='Transformation',
                                      arg_name_missing_column='Dataset')

        df = InputParameterChecker.drop_null_value_by_target_columns(dataset, self._target_column_names)
        # Check target_column datatype is string
        selected_data_df = df.loc[:, self._target_column_names]
        InputParameterChecker.verify_all_columns_are_string_type(DataTable(selected_data_df), dataset.name)
        # Get document column, combine if multiple document cols.
        document_col = selected_data_df[self._target_column_names[0]]
        if len(self._target_column_names) > 1:
            # combine target columns into one column
            combined_target_columns = pd.DataFrame()
            combined_target_columns['all_text'] = selected_data_df[self._target_column_names[0]].str.cat(
                selected_data_df[self._target_column_names[1:]], sep=' ')
            document_col = combined_target_columns['all_text']

        return df, document_col, dataset.name

    def train_lda_model(self, dataset: DataTable):
        df, document_col, dataset_name = self.validate_and_clean_dataset(dataset)
        try:
            vectorized_sentences = self.vectorizer.fit_transform(document_col)
        except ValueError as e:
            if 'empty vocabulary; perhaps the documents only contain stop words' in e.args[0]:
                ErrorMapping.rethrow(
                    e,
                    InvalidDatasetError(dataset1=dataset_name,
                                        reason=ErrorMapping.get_exception_message(e),
                                        troubleshoot_hint="Please make sure input documents contain words more than "
                                                          f"sklearn stop words: {list(stop_words.ENGLISH_STOP_WORDS)}"))
            raise e
        with TimeProfile("Fit Latent Dirichlet allocation model"):
            self.lda_model.fit(vectorized_sentences)
        with TimeProfile("Get document-topic distribution"):
            document_topic = self.get_document_topic_distribution(vectorized_sentences)
        # get result datatable
        transformed_dataset = pd.concat([df, document_topic], axis=1)
        return DataTable(transformed_dataset)

    def apply(self, dataset: DataTable):
        df, document_col, dataset_name = self.validate_and_clean_dataset(dataset)
        try:
            vectorized_sentences = self.vectorizer.transform(document_col)
        except ValueError as e:
            if 'empty vocabulary; perhaps the documents only contain stop words' in e.args[0]:
                ErrorMapping.rethrow(
                    e,
                    InvalidDatasetError(dataset1=dataset_name,
                                        reason=ErrorMapping.get_exception_message(e),
                                        troubleshoot_hint="Please make sure input documents contain words more than "
                                                          f"sklearn stop words: {list(stop_words.ENGLISH_STOP_WORDS)}"))
            raise e

        with TimeProfile("Transform based on trained Latent Dirichlet allocation model"):
            self.lda_model.transform(vectorized_sentences)

        with TimeProfile("Get document-topic distribution"):
            document_topic = self.get_document_topic_distribution(vectorized_sentences)
        # get result datatable
        transformed_dataset = pd.concat([df, document_topic], axis=1)

        return DataTable(transformed_dataset)

    def get_document_topic_distribution(self, vectorized_sentences):
        """Generate the Document-Topic probability distribution
        :param topic_names: [Topic 1, Topic 2, Topic 3, Topic 4, Topic 5]
        Output example: document-topic normalized
                Topic 1   Topic 2   Topic 3   Topic 4   Topic 5
        Doc0    0.000286  0.998858  0.000285  0.000287  0.000284
        Doc1    0.001737  0.001753  0.993032  0.001746  0.001731
        Doc2    0.990195  0.002451  0.002454  0.002452  0.002448
        Doc3    0.005183  0.005207  0.979275  0.005167  0.005167
        """
        topic_names = [f'Topic {i+1}' for i in range(self._topics_number)]
        document_topic_prob_matrix = self.lda_model.transform(vectorized_sentences)
        document_topic_df = pd.DataFrame(np.round(document_topic_prob_matrix, 6), columns=topic_names)

        return document_topic_df

    def get_feature_topic_matrix(self):
        """Generate the feature-topic matrix
        Output example 1: feature-topic matrix non-normalized, build_dictionary = True
        Feature   Topic 1	    Topic 2	        Topic 3	       Topic 4         Topic 5
        wonders	  68.254152	    50.060690	    685.320487	   1004.683473	   471.012446
        word	  2.006199	    2170.872490	    1060.562261	   1297.363465	   957.106688
        words	  0.941689	    411.578107	    1.126587	   944.239073	   47.731937
        wordy	  297.463170    14190.487656    5054.782010    19892.078162    4110.913594
         ...
        Output example 2: feature-topic matrix normalized, build_dictionary = True
        Feature   Topic 1	Topic 2	    Topic 3	    Topic 4     Topic 5
        wonders	  0.006945	0.452661	0.001167	0.538274	0.000953
        word	  0.025600	0.098316	0.202452	0.498039	0.175592
        words	  0.086277	0.174954	0.000323	0.537901	0.200545
        wordy	  0.236823	0.525313	0.001173	0.235252	0.001439
         ...
        Output example 3: feature-topic matrix non-normalized, build_dictionary = False
        Feature Topic 1	        Topic 2	        Topic 3	       Topic 4         Topic 5
        0	    68.254152	    50.060690	    685.320487	   1004.683473	   471.012446
        1	    2.006199	    2170.872490	    1060.562261	   1297.363465	   957.106688
        2	    0.941689	    411.578107	    1.126587	   944.239073	   47.731937
        3	    297.463170      14190.487656    5054.782010    19892.078162    4110.913594
        ...
        Output example 4: feature-topic matrix normalized, build_dictionary = False
        Feature Topic 1	    Topic 2	    Topic 3	    Topic 4     Topic 5
        0	    0.006945	0.452661	0.001167	0.538274	0.000953
        1	    0.025600	0.098316	0.202452	0.498039	0.175592
        2	    0.086277	0.174954	0.000323	0.537901	0.200545
        3	    0.236823	0.525313	0.001173	0.235252	0.00143
        """
        feature_topic_values = np.array(self.lda_model.components_).T
        feature_topic_df = pd.DataFrame(normalize(feature_topic_values, axis=0, norm='l1')) if self._normalize \
            else pd.DataFrame(feature_topic_values)
        topic_names = [f'Topic {i + 1}' for i in range(self._topics_number)]
        feature_topic_df.columns = topic_names
        features_df = pd.DataFrame({FEATURE_NAME: self.vectorizer.get_feature_names()}) if self._build_dictionary \
            else pd.DataFrame({FEATURE_NAME: [i for i in range(self._max_feature)]})
        feature_topic_matrix = pd.concat([features_df, feature_topic_df], axis=1)

        return feature_topic_matrix
