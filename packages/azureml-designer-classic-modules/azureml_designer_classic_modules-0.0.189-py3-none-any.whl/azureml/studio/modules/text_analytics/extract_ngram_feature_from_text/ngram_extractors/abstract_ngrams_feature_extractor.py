import functools
import math
from collections import defaultdict

from azureml.studio.common.error import ErrorMapping, InvalidDatasetError
from azureml.studio.core.logger import module_logger
from azureml.studio.modules.text_analytics.extract_ngram_feature_from_text.ngram_utils import NGramInfo, \
    VocabularyMode, NGramFeaturesConstants, SeparatorConstants, InstanceFeature


class FeatureExtractorParameters:
    def __init__(self,
                 vocabulary_mode: VocabularyMode,
                 ngram_size: int,
                 k_skip_size: int,
                 min_word_length: int,
                 max_word_length: int,
                 min_doc_freq: float,
                 max_doc_freq: float,
                 detect_oov: bool,
                 normalize_feature_vector: bool,
                 include_sentence_prefix: bool
                 ):
        self.vocabulary_mode = vocabulary_mode
        self.ngram_size = ngram_size
        self.k_skip_size = k_skip_size
        self.min_word_length = min_word_length
        self.max_word_length = max_word_length
        self.min_doc_freq = min_doc_freq
        self.max_doc_freq = max_doc_freq
        self.detect_oov = detect_oov
        self.normalize_vector = normalize_feature_vector
        self.include_sentence_prefix = include_sentence_prefix


class AbstractNGramsFeatureExtractor:
    def __init__(self, input_params):
        """Initializes a new instance of the AbstractNGramsFeatureExtractor class

        Feature Extractor Parameters includes:
        - ngrams_size: int, Number of NGrams to be extracted
        - min_word_length: int, Minimum length of word to be included
        - max_word_length: int, Maximum length of word to be included
        - min_doc_freq: float, Minimum document frequency of an Ngram to be included
        - max_doc_freq: float, Maximum document frequency of an Ngram to be included
        - vocabulary_mode: Vocabulary Mode.
        - normalize_vector: bool, normalize the vector or not.
        - k_skip_size: int, not implemented now, set as the default value 0.
        - include_sentence_prefix: bool, not implemented now, set as the default value False.
        - detect_oov: bool, not implemented now, set as the default value False.
        - feature_vectors: list of dict, which maps string to float
        - output_vocabulary: map ngram string to NGramInfo
        """
        self.num_sample = 0
        self.min_doc_freq = input_params.min_doc_freq
        self.max_doc_freq = input_params.max_doc_freq
        self.min_word_length = input_params.min_word_length
        self.max_word_length = input_params.max_word_length
        self.ngram_size = input_params.ngram_size
        self.vocabulary_mode = input_params.vocabulary_mode
        self.normalize_vector = input_params.normalize_vector
        self.k_skip_size = 0
        self.include_sentence_prefix = False
        self.detect_oov = False
        self.feature_vectors = []
        self.output_vocabulary = defaultdict(NGramInfo)
        self.multiply_by_idf = False  # will be reassign in subclass
        self.record_term_freq = False  # will be reassign in subclass

    def extract_and_create_vocabulary(self, data_instance):
        """Extract NGram tokens from input DataInstance.

        :param data_instance: single data instance
        :return: instance feature containing n-gram tokens
        """

        instance_feature = InstanceFeature(data_instance.label, self.record_term_freq)
        if not isinstance(data_instance.text, str):
            return instance_feature

        for ngram in self._ngrams_generator(data_instance.text):
            if ngram not in instance_feature.features:
                # if the n-gram appeared in this data instance for the first time,
                # add one to doc_freq
                if ngram not in self.output_vocabulary:
                    self.output_vocabulary[ngram] = NGramInfo(doc_freq=1)
                else:
                    self.output_vocabulary[ngram].inc_doc_freq(1)
            instance_feature.update_ngram(ngram)
        return instance_feature

    def extract_with_read_only_vocabulary(self, data_instance, input_vocabulary):
        instance_feature = InstanceFeature(data_instance.label, self.record_term_freq)
        if not isinstance(data_instance.text, str):
            return instance_feature
        for ngram in self._ngrams_generator(data_instance.text):
            if ngram in input_vocabulary:
                instance_feature.update_ngram(ngram)
        return instance_feature

    def _ngrams_generator(self, sentences):
        sentences = sentences.split(SeparatorConstants.SentenceSeparator)
        for sentence in sentences:
            tokens = sentence.split(SeparatorConstants.TokenSeparator)
            # filter tokens with invalid word length
            tokens = self.filter_tokens_by_word_length(tokens=tokens)
            for n in range(1, self.ngram_size + 1):
                for ngram in self.get_ngrams(tokens=tokens, ngram_size=n):
                    yield ngram

    def _calculate_word_freq_threshold(self, num_samples):
        """Calculate minimum and maximum occurrences threshold according to num_samples, min_doc_freq and max_doc_freq.

        doc_freq supports both percentage and times.
        If num_samples * min_doc_freq is less than 1, it would be set to 1.
        Maximum threshold will set to num_samples if max_doc_freq is an improper value.
        i.e. max_doc_freq * min_doc_freq is less than 1.
        """
        if 1 <= self.min_doc_freq:
            # If this value represents the times.
            min_threshold = self.min_doc_freq
        elif self.min_doc_freq * num_samples < 1:
            # If this value represents the percentage but too small to get a legal threshold.
            module_logger.warning('Invalid Minimum n-gram document frequency, '
                                  'minimum threshold will be set to 1.')
            min_threshold = 1
        else:
            # If this value represents the percentage and is in the proper range
            min_threshold = int(self.min_doc_freq * num_samples)
        module_logger.info(f"Minimum n-gram document frequency be set to {min_threshold}")
        if self.max_doc_freq > 1:
            # If this value represents the times
            max_threshold = int(self.max_doc_freq)
        elif self.max_doc_freq * num_samples < 1:
            # If this value represents the percentage but is illegal.
            module_logger.warning(f'Invalid Maximum n-gram document frequency, '
                                  'maximum threshold will be set to {num_samples}')
            max_threshold = num_samples
        else:
            # If this value represents the percentage and is legal.
            max_threshold = int(self.max_doc_freq * num_samples)
        module_logger.info(f"Maximum n-gram document frequency be set to {max_threshold}")
        return min_threshold, max_threshold

    def filter_vocabulary_by_doc_freq(self, num_samples: int):
        """Filter the created vocabulary based on min_doc_freq and max_doc_freq."""
        min_threshold, max_threshold = self._calculate_word_freq_threshold(num_samples=num_samples)

        def _filter_by_threshold(x):
            return min_threshold <= x <= max_threshold

        self.output_vocabulary = {
            k: v for k, v in self.output_vocabulary.items() if _filter_by_threshold(v.doc_freq)
        }

    def filter_tokens_by_word_length(self, tokens: list) -> list:
        return [x for x in tokens if self.min_word_length <= len(x) <= self.max_word_length]

    def update_vocabulary(self, input_vocabulary):
        """Update the created vocabulary

        Left Outer join the new data vocabulary and the input vocabulary.
        """
        for ngram in self.output_vocabulary:
            if ngram in input_vocabulary:
                self.output_vocabulary[ngram].inc_doc_freq(delta=input_vocabulary[ngram].doc_freq)

    def get_ngrams(self, tokens, ngram_size, skip_size=0):
        """Constructs NGrams of specific size

        :param tokens: A list of tokens
        :param ngram_size: Input n-gram size
        :param skip_size: int, Input k-skip size
        :return: A list of all possible n-grams of this size.
        """
        # generate ngrams starting from 0, 1, ..., len(tokens) - ngram_size
        # and link tokens in the same gram with '_'.
        ngrams = [SeparatorConstants.GramSeparator.join(tokens[i:i + ngram_size]) for i in
                  range(0, len(tokens) - ngram_size + 1)]
        return ngrams
        # todo: skip word
        # todo: include sentence prefix

    def extract(self, text_data, input_vocabulary):
        self._extract_internal(text_data=text_data, input_vocabulary=input_vocabulary)
        # calculate the doc idf
        if self.vocabulary_mode != VocabularyMode.ReadOnly:
            n_docs = self.output_vocabulary[NGramFeaturesConstants.NumberOfDocuments].doc_freq
            for ngram in self.output_vocabulary:
                self.output_vocabulary[ngram].update_inv_doc_freq(n_docs)

        self.update_feature_vector()

    def update_feature_vector(self):
        """Remove the out of vocabulary features and normalize feature vector

        Removes out of vocabulary words from the feature vector.
        Detects whether the feature vector is totally empty.
        Normalizes the feature vector.

        return None
        """

        for vec_id, feature_vector in enumerate(self.feature_vectors):
            # select the ngrams in the vocabulary.
            reduced_features = {x: v for x, v in feature_vector.features.items() if x in self.output_vocabulary}
            if self.multiply_by_idf:
                reduced_features = {k: v * self.output_vocabulary[k].inv_doc_freq for k, v in reduced_features.items()}
            if self.normalize_vector:
                # normalize by sqrt(\sum(feature))
                norm = self._calculate_norm(reduced_features)
                # The 0.0 norm feature will be skipped, because they can not be normalized.
                # And this kind of cases can be caused by inv_doc_freq value of all ngram features being zero.
                if norm != 0.0:
                    reduced_features = {k: v / norm for k, v in reduced_features.items()}
            self.feature_vectors[vec_id].features = reduced_features

    def _calculate_norm(self, feature_vector):
        """Calculate the norm of the input feature vector

        :param feature_vector: dict, map string to float
        :return:float, The norm of the input feature vector.
        """
        num = 0.0
        if feature_vector:
            squares = map(lambda x: x ** 2, feature_vector.values())
            square_sum = functools.reduce(lambda x, y: x + y, squares)
            num = math.sqrt(square_sum)
        return num

    def _extract_internal(self, text_data, input_vocabulary):
        """Generate vocabulary from data instances"""
        self.feature_vectors = []
        num_old_docs = 0
        num_sample = text_data.shape[0]
        if self.vocabulary_mode == VocabularyMode.Create:
            self.feature_vectors = [self.extract_and_create_vocabulary(x) for _, x in text_data.iterrows()]
            self.filter_vocabulary_by_doc_freq(num_sample)
            self.output_vocabulary[NGramFeaturesConstants.NumberOfDocuments] = NGramInfo(doc_freq=num_sample)

        elif self.vocabulary_mode == VocabularyMode.ReadOnly:
            self.feature_vectors = [self.extract_with_read_only_vocabulary(x, input_vocabulary) for _, x in
                                    text_data.iterrows()]
            self.output_vocabulary = input_vocabulary

        elif self.vocabulary_mode == VocabularyMode.Update:
            if input_vocabulary is not None:
                if NGramFeaturesConstants.NumberOfDocuments not in input_vocabulary:
                    ErrorMapping.throw(InvalidDatasetError())  # TODO: MESSAGE PARAM
                num_old_docs = input_vocabulary[NGramFeaturesConstants.NumberOfDocuments].doc_freq
                self.feature_vectors = [self.extract_and_create_vocabulary(x) for _, x in text_data.iterrows()]
                self.filter_vocabulary_by_doc_freq(num_sample)
                self.update_vocabulary(input_vocabulary)
            self.output_vocabulary[NGramFeaturesConstants.NumberOfDocuments] = NGramInfo(
                doc_freq=num_old_docs + num_sample)

        elif self.vocabulary_mode == VocabularyMode.Merge:
            if input_vocabulary is not None:
                if NGramFeaturesConstants.NumberOfDocuments not in input_vocabulary:
                    ErrorMapping.throw(InvalidDatasetError())  # TODO: MESSAGE PARAM
                num_old_docs = input_vocabulary[NGramFeaturesConstants.NumberOfDocuments].doc_freq
                self.output_vocabulary = input_vocabulary
                self.feature_vectors = [self.extract_and_create_vocabulary(x) for _, x in text_data.iterrows()]
                self.filter_vocabulary_by_doc_freq(num_old_docs + num_sample)
            self.output_vocabulary[NGramFeaturesConstants.NumberOfDocuments] = NGramInfo(
                gram_id=self.output_vocabulary[NGramFeaturesConstants.NumberOfDocuments].gram_id,
                doc_freq=num_old_docs + num_sample,
                inv_doc_freq=self.output_vocabulary[NGramFeaturesConstants.NumberOfDocuments].inv_doc_freq)
