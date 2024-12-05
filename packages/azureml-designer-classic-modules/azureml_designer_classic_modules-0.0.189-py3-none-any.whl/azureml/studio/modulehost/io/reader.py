import os

import pandas as pd

from azureml.studio.common.io.pickle_utils import read_with_pickle_from_stream
from azureml.studio.common.io.data_table_io import read_data_table


class Reader:

    @classmethod
    def read_into_data_table(cls, file_name):
        return read_data_table(file_name)

    @classmethod
    def read_into_data_frame_from_csv(cls, file_name):
        if not os.path.isfile(file_name):
            raise FileNotFoundError
        return pd.read_csv(file_name)

    @classmethod
    def read_into_base_learner(cls, stream):
        return read_with_pickle_from_stream(stream)

    @classmethod
    def read_into_base_cluster(cls, stream):
        return read_with_pickle_from_stream(stream)

    @classmethod
    def read_into_base_transform(cls, stream):
        return read_with_pickle_from_stream(stream)
