from .abstract_ngrams_feature_extractor import AbstractNGramsFeatureExtractor


class IdfNGramFeatureExtractor(AbstractNGramsFeatureExtractor):
    def __init__(self, input_params):
        super().__init__(input_params)
        self.multiply_by_idf = True
        self.record_term_freq = False  # count one n-gram one time. (binary indicate whether it appeared)
