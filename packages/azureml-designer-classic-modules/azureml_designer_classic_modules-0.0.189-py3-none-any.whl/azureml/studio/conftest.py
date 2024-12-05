from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.modulehost.constants import ElementTypeName
from azureml.studio.modulehost.module_host_executor import execute
from azureml.studio.core.conftest import get_extended_int_dtype_test_samples
from azureml.studio.core.conftest import column_selection_legacy_and_sdk_formats


assert_array_almost_equal = np.testing.assert_array_almost_equal
assert_array_equal = np.testing.assert_array_equal
get_extended_int_dtype_test_samples = get_extended_int_dtype_test_samples
column_selection_legacy_and_sdk_formats = column_selection_legacy_and_sdk_formats


@pytest.fixture
def conftest_data_path():
    return Path(__file__).parent / 'tests/conftest'


@pytest.fixture
def input_dt_german_credit_card_uci(conftest_data_path):
    df = pd.read_csv(conftest_data_path / 'german_credit_card_uci_data.csv')
    return DataTable(df)


@pytest.fixture
def input_dt_adult_census_income(conftest_data_path):
    df = pd.read_csv(conftest_data_path / 'adult_census_income_data.csv')
    return DataTable(df)


@pytest.fixture
def input_dt_book_reviews_from_amazon_small(conftest_data_path):
    df = pd.read_csv(conftest_data_path / 'book_reviews_from_amazon_small.csv')
    return DataTable(df)


@pytest.fixture
def input_train_test_df_check_col_type_compatible(conftest_data_path):
    input_path = conftest_data_path / 'check_col_type_compatible/'
    data_type = {'f0': np.int16, 'f1': np.float64, 'f2': str, 'label': np.int16}
    train_df = pd.read_csv(input_path / 'train.csv', dtype=data_type)
    test_df = pd.read_csv(input_path / 'test_negative.csv')
    return train_df, test_df


@pytest.fixture
def input_df_clientid_unique_values_dataset(conftest_data_path):
    return pd.read_csv(conftest_data_path / 'unique_values_dataset/clientid_data.tsv',
                       sep='\t')


@pytest.fixture
def input_df_text_unique_values_dataset(conftest_data_path):
    return pd.read_csv(conftest_data_path / 'unique_values_dataset/text_data.tsv', sep='\t')


@pytest.fixture
def input_dt_index_not_equal_to_row_index():
    df = pd.DataFrame({
        'label': [0]*21 + [1]*21 + [2]*22,
        'f0': [i for i in range(64)],
        'index': [i*2 for i in range(64)]
    })
    df.set_index('index')
    return DataTable(df=df)


@pytest.fixture
def input_multi_index_data_table():
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4], 'C': [5, 6]}, index=pd.MultiIndex.from_tuples([(0, 0), (1, 1)]))
    return DataTable(df)


@pytest.fixture
def run_train_cluster_model_e2e():
    def _run_train_cluster_model_e2e(untrained_model_dir, input_data_dir, trained_model_dir, output_data_dir):
        execute([
            '--module-name=azureml.studio.modules.ml.train.train_clustering_model.train_clustering_model',
            '--untrained-model', untrained_model_dir,
            '--dataset', input_data_dir,
            '--trained-model', trained_model_dir,
            '--results-dataset', output_data_dir,
            '--column-set={\"isFilter\":true,\"rules\":[{\"exclude\":false,\"ruleType\":\"AllColumns\"}]}',
            '--check-for-append-or-uncheck-for-result-only=True'
        ])

    return _run_train_cluster_model_e2e


@pytest.fixture
def run_train_generic_model_e2e():
    def _run_train_generic_model_e2e(untrained_model_dir, input_data_dir, trained_model_dir):
        execute([
            '--module-name=azureml.studio.modules.ml.train.train_generic_model.train_generic_model',
            '--untrained-model', untrained_model_dir,
            '--dataset', input_data_dir,
            '--trained-model', trained_model_dir,
            '--model-explanations=False',
            '--label-column={\"isFilter\":true,\"rules\":[{\"exclude\":false,\"ruleType\":\"ColumnNames\",\"columns\":'
            '[\"class\"]}]}'
        ])

    return _run_train_generic_model_e2e


@pytest.fixture
def run_train_anomaly_detection_model_e2e():
    def _run_train_anomaly_detection_model_e2e(untrained_model_dir, input_data_dir, trained_model_dir):
        execute([
            '--module-name=azureml.studio.modules.anomaly_detection.train_anomaly_detection.train_anomaly_detection',
            '--untrained-model', untrained_model_dir,
            '--dataset', input_data_dir,
            '--trained-model', trained_model_dir
        ])

    return _run_train_anomaly_detection_model_e2e


@pytest.fixture
def run_tune_hyper_e2e():
    def _run_tune_hyper_e2e(untrained_model_dir, input_data_dir, trained_model_dir, tune_result_dir):
        execute([
            '--module-name=azureml.studio.modules.ml.train.tune_model_hyperparameters.tune_model_hyperparameters',
            '--untrained-model', untrained_model_dir,
            '--training-dataset', input_data_dir,
            '--sweep-results', tune_result_dir,
            '--trained-best-model', trained_model_dir,
            '--specify-parameter-sweeping-mode', "Random sweep",
            '--maximum-number-of-runs-on-random-sweep=5',
            '--random-seed=0',
            '--name-or-numerical-index-of-the-label-column='
            '{\"isFilter\":true,\"rules\":[{\"exclude\":false,\"ruleType\":'
            '\"ColumnNames\",\"columns\":[\"class\"]}]}',
            '--metric-for-measuring-performance-for-classification=Accuracy',
            '--metric-for-measuring-performance-for-regression', "Mean absolute error"
        ])

    return _run_tune_hyper_e2e


@pytest.fixture
def run_score_generic_e2e():
    def _run_score_generic_e2e(trained_model_dir, input_data_dir, scored_data_dir):
        execute([
            '--module-name=azureml.studio.modules.ml.score.score_generic_module.score_generic_module',
            '--trained-model', trained_model_dir,
            '--dataset', input_data_dir,
            '--scored-dataset', scored_data_dir,
            '--append-score-columns-to-output=True'
        ])

    return _run_score_generic_e2e


@pytest.fixture(params=['True', 'False'])
def run_lda_e2e(request):
    def _run_lda_e2e(input_data_dir, output_data_dir1, output_data_dir2, output_data_dir3, target_column):
        execute([
            '--module-name=azureml.studio.modules.text_analytics.lda.lda',
            '--dataset', input_data_dir,
            '--target-columns', target_column,
            '--number-of-topics-to-model=5',
            '--n-grams=2',
            '--normalize=True',
            '--show-all-options', request.param,
            # show_all_option is False paras
            '--build-dictionary-of-ngrams', 'True',
            '--maximum-size-of-ngram-dictionary=20000',
            # show_all_option is True paras
            '--rho-parameter=0.01',
            '--alpha-parameter=0.01',
            '--estimated-number-of-documents=1000',
            '--size-of-the-batch=32',
            '--initial-value-of-iteration-count=10',
            '--power-applied-to-the-iteration-during-updates=0.7',
            '--passes=5',
            '--build-dictionary-of-ngrams-prior-to-lda', 'True',
            '--maximum-number-of-ngrams-in-dictionary=20000',
            '--transformed-dataset', output_data_dir1,
            '--feature-topic-matrix', output_data_dir2,
            '--lda-transformation', output_data_dir3,
        ])
    return _run_lda_e2e


@pytest.fixture
def run_word2vec_e2e():
    def _run_word2vec_e2e(input_data_dir, target_column, output_data_dir):
        execute([
            '--module-name=azureml.studio.modules.text_analytics.word2vec.word2vec',
            '--dataset', input_data_dir,
            '--target-column', target_column,
            '--maximum-vocabulary-size=10000',
            '--length-of-word-embedding=10',
            '--context-window-size=5',
            '--minimum-word-count=3',
            '--number-of-epochs=2',
            '--vocabulary-with-embeddings', output_data_dir,
            '--word2-vec-strategy', 'Gensim Word2Vec',
            '--word2-vec-training-algorithm', "Skip_gram"
        ])

    return _run_word2vec_e2e


@pytest.fixture
def assert_data_table_equals():
    def _assert_data_table_equals(data_table_ref, data_table_now):
        """
        check two data table is equals.
        1. their column names
        2. not float column: strict equals
        3. float column: almost equals up to desired precision.
        :param data_table_ref: reference data table
        :param data_table_now: new output data table
        :return: None
        """
        assert set(data_table_now.column_names) == set(data_table_ref.column_names)
        for column_name in data_table_ref.column_names:
            s1 = data_table_now.get_column(column_name)
            s2 = data_table_ref.get_column(column_name)
            if data_table_now.get_element_type(column_name) == ElementTypeName.FLOAT:
                assert_array_almost_equal(s1, s2)
            else:
                assert_array_equal(s1, s2)

    return _assert_data_table_equals
