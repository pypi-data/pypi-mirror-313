from .abstract_ngrams_feature_extractor import AbstractNGramsFeatureExtractor


class PresenceNGramFeatureExtractor(AbstractNGramsFeatureExtractor):
    def __init__(self, input_params):
        super().__init__(input_params)
        self.multiply_by_idf = False
        self.record_term_freq = False  # count one n-gram one time. (binary indicate whether it appeared)
