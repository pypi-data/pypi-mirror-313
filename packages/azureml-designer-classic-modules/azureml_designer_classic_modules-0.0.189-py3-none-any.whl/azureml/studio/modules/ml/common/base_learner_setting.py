from abc import abstractmethod

from azureml.studio.common.parameter_range import Sweepable


class BaseLearnerSetting:
    @abstractmethod
    def __init__(self):
        self.parameter_range = dict()
        self._random_number_seed = 42
        # enable_log = True, will set verbose = 1 if verbose can be an integer, else set verbose = False
        # enable_log = False, will not print anything during training sklearn model.
        self.enable_log = True

    @property
    def random_number_seed(self):
        if self._random_number_seed is not None:
            return self._random_number_seed
        return 42

    @random_number_seed.setter
    def random_number_seed(self, value):
        if value is not None:
            self._random_number_seed = value

    @abstractmethod
    def init_single(self):
        pass

    @abstractmethod
    def init_range(self):
        pass

    def add_sweepable(self, sweep: Sweepable):
        self.parameter_range[sweep.name] = sweep.attribute_value

    def add_list(self, name, para_list):
        self.parameter_range[name] = para_list

    def get_sweepable(self, name, literal_value):
        return Sweepable.from_prs(name, literal_value).attribute_value
