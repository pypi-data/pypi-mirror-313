from .abstract_ngrams_feature_extractor import AbstractNGramsFeatureExtractor


class TfIdfNGramFeatureExtractor(AbstractNGramsFeatureExtractor):
    def __init__(self, input_params):
        super().__init__(input_params)
        self.multiply_by_idf = True
        # count tf, so count n-gram count in features dict every time it appears to count its number
        self.record_term_freq = True
