import math
from collections import defaultdict

from azureml.studio.modulehost.attributes import AutoEnum, ItemInfo
from azureml.studio.internal.attributes.release_state import ReleaseState


class NGramFeaturesConstants:
    NumberOfDocuments = "total.num.docs"
    InvalidVocabularyErrMsg = "Total number of documents at end of vocabulary not found.  Input vocabulary"


class SeparatorConstants:
    SentenceSeparator = "|||"
    TokenSeparator = " "
    GramSeparator = "_"


class VocabDataSetColumnName:
    NGramID = 'Id'
    NGramString = 'NGram'
    DocumentFrequency = 'DF'
    InverseDocumentFrequency = 'IDF'


class NGramInfo:
    def __init__(self, doc_freq: int, inv_doc_freq: int = 0, gram_id: int = -1):
        self._gram_id = gram_id
        self._doc_freq = doc_freq
        self._inv_doc_freq = inv_doc_freq

    @property
    def gram_id(self):
        return self._gram_id

    @gram_id.setter
    def gram_id(self, value):
        self._gram_id = value

    @property
    def doc_freq(self):
        return self._doc_freq

    @property
    def inv_doc_freq(self):
        return self._inv_doc_freq

    def update_inv_doc_freq(self, n_docs):
        # todo: check safe divide
        self._inv_doc_freq = math.log10(n_docs / self.doc_freq)

    def inc_doc_freq(self, delta):
        """Add inc_df and inc_idf to df and idf"""
        self._doc_freq += delta

    def to_dict(self, ngram):
        return {
            VocabDataSetColumnName.NGramID: self.gram_id,
            VocabDataSetColumnName.NGramString: ngram,
            VocabDataSetColumnName.DocumentFrequency: self.doc_freq,
            VocabDataSetColumnName.InverseDocumentFrequency: self.inv_doc_freq
        }


class InstanceFeature:
    """ Record features of a data instance"""

    def __init__(self, label=None, record_term_freq=False):
        """

        :param label:
        :param record_term_freq: if True, record how many times this gram appear in the doc. [TF, TFIDF]
                                 if False, record appear or not. [BIN, IDF]
        """
        self.label = label
        self.features = defaultdict(float)  # map n-gram to float, default dict will initialize the value to zero
        self.record_term_freq = record_term_freq

    def update_ngram(self, ngram):
        if self.record_term_freq:
            # update frequency
            self.features[ngram] += 1
        elif ngram not in self.features:
            # update in or not flag
            self.features[ngram] = 1

    def items(self):
        # This attribute makes this object could be use by six(package).
        # And six will be used to create sparse feature matrices.
        return self.features.items()


class VocabularyMode(AutoEnum):
    Create: ItemInfo(name="Create", friendly_name="Create") = ()
    ReadOnly: ItemInfo(name="ReadOnly", friendly_name="ReadOnly") = ()
    Update: ItemInfo(name="Update", friendly_name="Update", release_state=ReleaseState.Alpha) = ()
    Merge: ItemInfo(name="Merge", friendly_name="Merge", release_state=ReleaseState.Alpha) = ()


class WeightingFunction(AutoEnum):
    WeightBin: ItemInfo(name="Binary Weight", friendly_name="Binary Weight") = ()
    WeightTf: ItemInfo(name="TF Weight", friendly_name="TF Weight") = ()
    WeightIdf: ItemInfo(name="IDF Weight", friendly_name="IDF Weight") = ()
    WeightTFIDF: ItemInfo(name="TF-IDF Weight", friendly_name="TF-IDF Weight") = ()
    WeightGraph: ItemInfo(name="Graph Weight", friendly_name="Graph Weight", release_state=ReleaseState.Alpha) = ()


class ReduceDimensionalityMode(AutoEnum):
    TRUE: ItemInfo(name="True", friendly_name="True", release_state=ReleaseState.Alpha) = ()
    FALSE: ItemInfo(name="False", friendly_name="False") = ()


class ScoringMethod(AutoEnum):
    PearsonCorrelation: ItemInfo(name="Pearson Correlation", friendly_name="Pearson Correlation",
                                 release_state=ReleaseState.Alpha) = ()
    MutualInformation: ItemInfo(name="Mutual Information", friendly_name="Mutual Information",
                                release_state=ReleaseState.Alpha) = ()
    KendallCorrelation: ItemInfo(name="Kendall Correlation", friendly_name="Kendall Correlation",
                                 release_state=ReleaseState.Alpha) = ()
    SpearmanCorrelation: ItemInfo(name="Spearman Correlation", friendly_name="Spearman Correlation",
                                  release_state=ReleaseState.Alpha) = ()
    ChiSquared: ItemInfo(name="Chi Squared", friendly_name="Chi Squared", release_state=ReleaseState.Alpha) = ()
    FisherScore: ItemInfo(name="Fisher Score", friendly_name="Fisher Score", release_state=ReleaseState.Alpha) = ()
    CountBased: ItemInfo(name="Count Based", friendly_name="Count Based", release_state=ReleaseState.Alpha) = ()
