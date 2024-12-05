import time
import pandas as pd
import numpy as np
from urllib.error import HTTPError, URLError

from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.modulehost.attributes import DataTableInputPort, ModuleMeta, DataTableOutputPort, \
    ColumnPickerParameter, SelectedColumnCategory, ModeParameter, IntParameter
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.input_parameter_checker import InputParameterChecker
from azureml.studio.common.error import ErrorMapping, NoColumnsSelectedError, InvalidTrainingDatasetError, \
    FailedToDownloadFilesError
from azureml.studio.common.types import AutoEnum
from azureml.studio.modulehost.attributes import ItemInfo
from collections import Counter
import itertools
from azureml.studio.core.logger import module_logger, TimeProfile, time_profile


class Word2VecStrategy(AutoEnum):
    """convert word to vector strategy choices, we support:
    :Spacy English pretrained model: en_core_web_sm
    :Gensim Word2Vec model
    :Gensim FastText"""
    GloVeModel: ItemInfo(name='GloVe pretrained English Model', friendly_name='GloVe pretrained English model') = ()
    GensimWord2Vec: ItemInfo(name='Gensim Word2Vec', friendly_name='Gensim Word2Vec model') = ()
    FastText: ItemInfo(name='Gensim FastText', friendly_name='Gensim FastText model') = ()


class TrainingAlgorithm(AutoEnum):
    """Training algorithm: Skip-Gram and CBOW."""
    SkipGram: ItemInfo(name='Skip_gram', friendly_name='Skip-Gram') = ()
    CBOW: ItemInfo(name='CBOW', friendly_name='CBOW') = ()


GLOVE_EMBEDDING_SIZE = 100
EMBEDDING_NAME_SUFFIX = "Embedding dim"
VOCAB_COL_NAME = 'Vocabulary'


class Word2VecModule(BaseModule):
    @staticmethod
    @module_entry(ModuleMeta(
        name="Convert Word to Vector",
        description="Convert word to vector.",
        category="Text Analytics",
        version="1.0",
        owner="Microsoft Corporation",
        family_id="0d1e165e-3cf7-4d76-909b-9f9193951aaf",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            dataset: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Input data",
            ),
            target_column: ColumnPickerParameter(
                name="Target column",
                friendly_name="Target column",
                description="Select one target column whose vocabulary embeddings will be generated",
                column_picker_for="Dataset",
                single_column_selection=True,
                column_selection_categories=(SelectedColumnCategory.String,),
            ),
            word2vec_strategy: ModeParameter(
                Word2VecStrategy,
                name="Word2Vec strategy",
                friendly_name="Word2Vec strategy",
                description="Select the strategy for computing word embedding",
                default_value=Word2VecStrategy.GensimWord2Vec,
            ),
            training_mode: ModeParameter(
                TrainingAlgorithm,
                name="Word2Vec Training Algorithm",
                friendly_name="Word2Vec Training Algorithm",
                description="Select the training algorithm for training Word2Vec model",
                default_value=TrainingAlgorithm.SkipGram,
                parent_parameter="Word2Vec strategy",
                parent_parameter_val=(Word2VecStrategy.GensimWord2Vec, Word2VecStrategy.FastText),
            ),
            max_vocabulary_size: IntParameter(
                name="Maximum vocabulary size",
                friendly_name="Maximum number of words in vocabulary",
                description="Specify the maximum number of the words in vocabulary",
                default_value=10000,
                min_value=10,
                max_value=2147483647,
            ),
            min_count: IntParameter(
                name="Minimum word count",
                friendly_name="Minimum count of one word",
                description="Ignores all words that have a frequency lower than this value",
                default_value=5,
                min_value=1,
                max_value=100,
            ),
            embedding_size: IntParameter(
                name="Length of word embedding",
                friendly_name="Length of word embedding",
                description="Specify the length of the word embedding/vector",
                default_value=100,
                min_value=10,
                max_value=2000,
                parent_parameter="Word2Vec strategy",
                parent_parameter_val=(Word2VecStrategy.GensimWord2Vec, Word2VecStrategy.FastText),
            ),
            window_size: IntParameter(
                name="Context window size",
                friendly_name="Context window size",
                description="Specify the maximum distance between the word being predicted and the current word",
                default_value=5,
                min_value=1,
                max_value=100,
                parent_parameter="Word2Vec strategy",
                parent_parameter_val=(Word2VecStrategy.GensimWord2Vec, Word2VecStrategy.FastText),
            ),
            train_epochs: IntParameter(
                name="Number of epochs",
                friendly_name="Number of epochs",
                description="Specify the number of epochs (iterations) over the corpus",
                default_value=5,
                min_value=1,
                max_value=1024,
                parent_parameter="Word2Vec strategy",
                parent_parameter_val=(Word2VecStrategy.GensimWord2Vec, Word2VecStrategy.FastText),
            ),
    ) -> (
            DataTableOutputPort(
                name="Vocabulary with embeddings",
                friendly_name="Vocabulary with embeddings",
                description="Vocabulary with embeddings",
            ),
    ):
        input_values = locals()
        output_values = Word2VecModule.word2vec(**input_values)
        return output_values

    @classmethod
    def word2vec(cls,
                 dataset: DataTable,
                 target_column: DataTableColumnSelection,
                 word2vec_strategy: Word2VecStrategy,
                 max_vocabulary_size,
                 embedding_size,
                 window_size,
                 min_count,
                 training_mode,
                 train_epochs
                 ):
        selected_data: DataTable = target_column.select(dataset)
        df = cls.validate_input_args(dataset=dataset, selected_data=selected_data, target_column=target_column)
        selected_df = df.loc[:, selected_data.column_names]
        # simple preprocess text data: remove punctuation，lower-case characters
        from gensim.parsing.preprocessing import strip_punctuation, preprocess_string
        filters = [lambda x: x.lower(), strip_punctuation]
        preprocessed_selected_data = selected_df.applymap(lambda x: preprocess_string(x, filters))

        if word2vec_strategy == Word2VecStrategy.GloVeModel:
            vocab_embedding_df = cls.glove_english_model(dataset=preprocessed_selected_data, min_count=min_count,
                                                         max_vocabulary_size=max_vocabulary_size)
        elif word2vec_strategy in (Word2VecStrategy.GensimWord2Vec, Word2VecStrategy.FastText):
            vocab_embedding_df = cls.gensim_models(
                word2vec_strategy=word2vec_strategy, dataset=preprocessed_selected_data,
                max_vocabulary_size=max_vocabulary_size, embedding_size=embedding_size, window_size=window_size,
                min_count=min_count, training_mode=training_mode, train_epochs=train_epochs)
        else:
            raise ValueError(f'Unsupported strategy {word2vec_strategy}')

        return DataTable(vocab_embedding_df),

    @classmethod
    def glove_english_model(cls, dataset, min_count, max_vocabulary_size):
        # get vocabulary
        vocab = cls._generate_vocabulary_from_corpus(dataset=dataset, min_count=min_count,
                                                     max_vocabulary_size=max_vocabulary_size)
        vocab_df = pd.DataFrame({VOCAB_COL_NAME: vocab})
        # 'glove-wiki-gigaword-100' is a pretrained language model, trained using wikipedia corpus by GloVe model
        import gensim.downloader as api
        module_logger.info("Loading Glove pretrained language model: glove-wiki-gigaword-100.")
        try:
            glove_model_wiki = retry(
                func=lambda: api.load("glove-wiki-gigaword-100"),
                logging_message="Failed to download glove-wiki-gigaword-100.",
                exception_to_check=HTTPError)
        except URLError as ex:
            raise FailedToDownloadFilesError(file_names="glove-wiki-gigaword-100") from ex

        with TimeProfile("Obtain word embeddings from Glove pretrained model"):
            embeddings = []
            for word in vocab:
                if word in glove_model_wiki.wv:
                    embeddings.append(glove_model_wiki[word])
                else:
                    embeddings.append(np.zeros(GLOVE_EMBEDDING_SIZE))
        embeddings_df = pd.DataFrame(embeddings)
        # add column names
        # fix length mismatch error by using embeddings_df column length as max value in generating column names.
        # cannot use 'GLOVE_EMBEDDING_SIZE' as max value because embeddings_df may be empty.
        embeddings_col_names = [f'{EMBEDDING_NAME_SUFFIX} {i}' for i in range(embeddings_df.shape[1])]
        embeddings_df.columns = embeddings_col_names
        vocab_embedding_df = pd.concat([vocab_df, embeddings_df], axis=1)

        return vocab_embedding_df

    @classmethod
    @time_profile
    def _generate_vocabulary_from_corpus(cls, dataset, min_count, max_vocabulary_size):
        sentences_list = dataset.iloc[:, 0]
        words_list = list(itertools.chain.from_iterable(sentences_list))
        vocab = Counter(words_list)
        # remove words with occurrence lower than min_count, vocab is sorted by words occurrence
        vocab = itertools.takewhile(lambda x: x[1] >= min_count, vocab.most_common())
        vocab = list(dict(vocab).keys())
        if len(vocab) > max_vocabulary_size:
            vocab = vocab[0:max_vocabulary_size]
        return vocab

    @classmethod
    def gensim_models(cls, word2vec_strategy, dataset, max_vocabulary_size, embedding_size, window_size, min_count,
                      training_mode, train_epochs):
        """used for gensim Word2Vec model and FastText model
        FastText is an unsupervised algorithm created by Facebook Research for efficiently learning word embeddings,
        which performs better than word2vec and Glove on smaller datasets.
        Word2Vec and FastText models have many different parameters
        ref https://radimrehurek.com/gensim/models/word2vec.html#gensim.models.word2vec.Word2Vec and
        https://radimrehurek.com/gensim/models/fasttext.html#gensim.models.fasttext.FastText
        for more info
        but the ones that are useful to know about are:
        - size: length of the word embedding/vector (defaults to 100)
        - window: maximum distance between the word being predicted and the current word (defaults to 5)
        - min_count: ignores all words that have a frequency lower than this value (defaults to 5)
        - sg: training algorithm; 1 for skip-gram and 0 for CBOW (defaults to 0)
        - iter: number of epochs (defaults to 5)
        """
        dataset_sentences = dataset.values.flatten()

        sg = 1 if training_mode == TrainingAlgorithm.SkipGram else 0
        if word2vec_strategy == Word2VecStrategy.GensimWord2Vec:
            from gensim.models import Word2Vec
            with TimeProfile("Train Word2Vec model"):
                try:
                    model = Word2Vec(sentences=dataset_sentences, size=embedding_size, window=window_size,
                                     min_count=min_count, sg=sg, iter=train_epochs)
                except RuntimeError as e:
                    if "you must first build vocabulary before training the model" in str(e.args):
                        ErrorMapping.throw(InvalidTrainingDatasetError(
                            action_name='Train Word2Vec model',
                            data_name=cls._args.dataset.friendly_name,
                            reason=f"no word in vocab with frequency greater than {min_count}",
                            troubleshoot_hint='Please check target text column or decrease parameter '
                                              '"Minimum word count" value to avoid empty vocab.'))
                    else:
                        raise e

        elif word2vec_strategy == Word2VecStrategy.FastText:
            from gensim.models.fasttext import FastText
            with TimeProfile("Train FastText model"):
                model = FastText(sentences=dataset_sentences, size=embedding_size, window=window_size,
                                 min_count=min_count, sg=sg, iter=train_epochs)
        else:
            raise ValueError(f'Unsupported strategy {word2vec_strategy}')

        vocab = list(model.wv.vocab)
        vocab_df = pd.DataFrame({VOCAB_COL_NAME: vocab})
        if len(vocab) > max_vocabulary_size:
            vocab = vocab[0:max_vocabulary_size]
        embeddings = []
        for word in vocab:
            embeddings.append(model.wv[word])
        embeddings_df = pd.DataFrame(embeddings)
        # add column names
        embeddings_col_names = [f'{EMBEDDING_NAME_SUFFIX} {i}' for i in range(embedding_size)]
        embeddings_df.columns = embeddings_col_names
        vocab_embedding_df = pd.concat([vocab_df, embeddings_df], axis=1)

        return vocab_embedding_df

    @classmethod
    def validate_input_args(cls, dataset: DataTable, selected_data: DataTable, target_column: DataTableColumnSelection):
        # Verify dataset is not empty
        InputParameterChecker.verify_data_table(data_table=dataset, friendly_name=dataset.name)

        # verify select onr and only one column as target column
        target_column_index = target_column.select_column_indexes(dataset)
        if not target_column_index:
            ErrorMapping.throw(NoColumnsSelectedError(column_set=cls._args.target_column_index.friendly_name))
        ErrorMapping.verify_if_all_columns_selected(
            act_col_count=len(target_column_index), exp_col_count=1,
            selection_pattern_friendly_name=cls._args.target_column.friendly_name,
            long_description=True)

        # Verify selected text column is a string column.
        InputParameterChecker.verify_all_columns_are_string_type(selected_data, cls._args.target_column.friendly_name)
        # Verify dataframe dropped null value by target columns
        return InputParameterChecker.drop_null_value_by_target_columns(dataset, selected_data.column_names)


def retry(func, retry_times=3, sleep_time=3, logging_message=None, exception_to_check=BaseException):
    """ Retry invoking function input func.

    :param func: a no-argument function.
    :param retry_times: int, the number of times to try to invoke func.
    :param sleep_time: int, seconds between each invoking.
    :param logging_message: str, message to log.
    :param exception_to_check: BaseException, exceptions to catch if execution fails.
    :return: the return value of func.
    """
    for i in range(retry_times):
        try:
            return func()
        except exception_to_check as ex:
            module_logger.warning(f'{ex}')
            if logging_message:
                module_logger.info(f"{logging_message} Retry in {sleep_time} seconds...")
            else:
                module_logger.info(f"Retry in {sleep_time} seconds...")
            time.sleep(sleep_time)
    return func()
