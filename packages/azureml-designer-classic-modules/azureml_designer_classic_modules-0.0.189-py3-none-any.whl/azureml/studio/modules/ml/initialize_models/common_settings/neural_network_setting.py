import azureml.studio.core.utils.strutils as strutils
from azureml.studio.common.parameter_range import ParameterRangeSettings, Sweepable
from azureml.studio.common.types import AutoEnum
from azureml.studio.modulehost.attributes import ReleaseState, ItemInfo
from azureml.studio.modules.ml.common.base_learner import CreateLearnerMode
from azureml.studio.modules.ml.common.base_learner_setting import BaseLearnerSetting
from azureml.studio.common.error import ParameterParsingError, ErrorMapping, GreaterThanError


def _parse_int_list(arg_name, arg_val):
    int_list = strutils.int_str_to_int_list(arg_val)
    if int_list is None:
        ErrorMapping.throw(ParameterParsingError(arg_name_or_column=arg_name, to_type='integer list'))

    return int_list


class CreateNeuralNetworkModelTopology(AutoEnum):
    DefaultHiddenLayers: ItemInfo(name="Fully-connected case", friendly_name="Fully-connected case") = ()
    # TODO:
    CustomHiddenLayers: ItemInfo(name="Custom definition script", friendly_name="Custom definition script",
                                 release_state=ReleaseState.Alpha) = ()


class CreateNeuralNetworkModelNormalizationMethod(AutoEnum):
    Binning: ItemInfo(name="Binning normalizer", friendly_name="Binning normalizer",
                      release_state=ReleaseState.Alpha) = ()
    Gaussian: ItemInfo(name="Gaussian normalizer", friendly_name="Gaussian normalizer",
                       release_state=ReleaseState.Alpha) = ()
    MinMax: ItemInfo(name="Min-Max normalizer", friendly_name="Min-Max normalizer", ) = ()
    NONE: ItemInfo(name="Do not normalize", friendly_name="Do not normalize",
                   release_state=ReleaseState.Alpha) = ()


class NeuralNetworkDefaultParameters:
    Mode = CreateLearnerMode.SingleParameter
    NeuralNetworkTopology = CreateNeuralNetworkModelTopology.DefaultHiddenLayers
    NeuralNetworkTopologyForRange = CreateNeuralNetworkModelTopology.DefaultHiddenLayers
    InitialWeightsDiameter = 0.1
    LearningRate = 0.1
    PsLearningRate = "0.1; 0.2; 0.4"
    Momentum = 0
    NormalizerType = CreateNeuralNetworkModelNormalizationMethod.MinMax
    NumHiddenNodes = "100"
    NumHiddenNodesList = _parse_int_list("num_hidden_nodes", NumHiddenNodes)
    NumHiddenNodesForRange = "100"
    NumIterations = 100
    PsNumIterations = "20; 40; 80; 160"
    Shuffle = True
    RandomNumberSeed = None
    AllowUnknownLevels = True

    @classmethod
    def to_dict(cls):
        return {
            "mode": cls.Mode,
            "neural_network_topology": cls.NeuralNetworkTopology,
            "neural_network_topology_for_range": cls.NeuralNetworkTopologyForRange,
            "initial_weights_diameter": cls.InitialWeightsDiameter,
            "learning_rate": cls.LearningRate,
            "ps_learning_rate": cls.PsLearningRate,
            "momentum": cls.Momentum,
            "normalizer_type": cls.NormalizerType,
            "num_hidden_nodes": cls.NumHiddenNodes,
            "num_hidden_nodes_for_range": cls.NumHiddenNodesForRange,
            "num_iterations": cls.NumIterations,
            "ps_num_iterations": ParameterRangeSettings.from_literal(cls.PsNumIterations),
            "shuffle": cls.Shuffle,
            "random_number_seed": cls.RandomNumberSeed,
            "allow_unknown_levels": cls.AllowUnknownLevels,
        }


class NeuralNetworkSetting(BaseLearnerSetting):
    """ Neural Network

        there remains some problem:
        1. initial_weights_diameter was not supported by sklearn
        2. momentum only used when optimizer = 'sgd', so which optimizer is used by tlc?
        3. learning rate can be {'constant', 'invscaling','adaptive'} in sklearn
        4. did not support parameter range
        5. did not support custom define script [ imp by StreamReader nnScript in v1]
    """

    def __init__(self, mode: NeuralNetworkDefaultParameters.Mode,
                 initial_weights_diameter: float = NeuralNetworkDefaultParameters.InitialWeightsDiameter,
                 learning_rate: float = NeuralNetworkDefaultParameters.LearningRate,
                 momentum: float = NeuralNetworkDefaultParameters.Momentum,
                 num_hidden_nodes: list = NeuralNetworkDefaultParameters.NumHiddenNodesList,
                 num_iterations: int = NeuralNetworkDefaultParameters.NumIterations,
                 shuffle: bool = NeuralNetworkDefaultParameters.Shuffle,
                 random_number_seed: int = NeuralNetworkDefaultParameters.RandomNumberSeed,
                 ps_learning_rate=ParameterRangeSettings.from_literal(NeuralNetworkDefaultParameters.PsLearningRate),
                 ps_num_iterations=ParameterRangeSettings.from_literal(NeuralNetworkDefaultParameters.PsNumIterations)
                 ):
        """ Initialize a neural network model

        :param initial_weights_diameter: float, the initial learning weights diameter, None
        :param learning_rate: float, the learning rate, learning_rate_init
        :param momentum: float, the momentum, momentum
        :param num_hidden_nodes: list(int), number of hidden nodes, hidden_layer_sizes
        :param num_iterations: int, number of learning iterations, max_iter
        :param shuffle: bool, Shuffle examples, shuffle
        :param random_number_seed: int, Random number seed, random_state
        :param ps_learning_rate: ParameterRange, range of the learning rate, learning_rate_init
        :param ps_num_iterations, ParameterRange, range of number of learning iterations, max_iter
        :return: None
        """
        super().__init__()

        self.create_learner_mode = mode
        self.initial_weights_diameter = initial_weights_diameter  # TODO : Sklearn had not supported it yet
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.num_hidden_nodes = num_hidden_nodes
        self.num_iterations = num_iterations
        self.shuffle = shuffle
        self.random_number_seed = random_number_seed
        self.parameter_range = {
            'learning_rate_init': Sweepable.from_prs("learning_rate_init", ps_learning_rate).attribute_value,
            'max_iter': Sweepable.from_prs("max_iter", ps_num_iterations).attribute_value,
        }

    @staticmethod
    def init(mode, neural_network_topology, neural_network_topology_for_range, initial_weights_diameter, momentum,
             num_hidden_nodes, num_hidden_nodes_for_range, learning_rate, ps_learning_rate, num_iterations,
             ps_num_iterations, shuffle, random_number_seed, normalizer_type, allow_unknown_levels,
             ):
        if mode == CreateLearnerMode.SingleParameter:
            num_hidden_nodes = _parse_int_list("num_hidden_nodes", num_hidden_nodes)
            NeuralNetworkSetting._verify_num_hidden_nodes(num_hidden_nodes)
            setting = NeuralNetworkSetting.init_single(
                initial_weights_diameter=initial_weights_diameter,
                learning_rate=learning_rate,
                momentum=momentum,
                num_hidden_nodes=num_hidden_nodes,
                num_iterations=num_iterations,
                shuffle=shuffle,
                random_number_seed=random_number_seed
            )
        else:
            num_hidden_nodes_for_range = _parse_int_list(
                "num_hidden_nodes_for_range", num_hidden_nodes_for_range)
            NeuralNetworkSetting._verify_num_hidden_nodes(num_hidden_nodes_for_range)
            setting = NeuralNetworkSetting.init_range(
                initial_weights_diameter=initial_weights_diameter, ps_learning_rate=ps_learning_rate,
                momentum=momentum, num_hidden_nodes=num_hidden_nodes_for_range,
                ps_num_iterations=ps_num_iterations, shuffle=shuffle,
                random_number_seed=random_number_seed)

        return setting

    @staticmethod
    def init_single(
            initial_weights_diameter: float = NeuralNetworkDefaultParameters.InitialWeightsDiameter,
            learning_rate: float = NeuralNetworkDefaultParameters.LearningRate,
            momentum: float = NeuralNetworkDefaultParameters.Momentum,
            num_hidden_nodes: list = NeuralNetworkDefaultParameters.NumHiddenNodesList,
            num_iterations: int = NeuralNetworkDefaultParameters.NumIterations,
            shuffle: bool = NeuralNetworkDefaultParameters.Shuffle,
            random_number_seed: int = NeuralNetworkDefaultParameters.RandomNumberSeed
    ):
        setting = NeuralNetworkSetting(mode=CreateLearnerMode.SingleParameter, **locals())
        return setting

    @staticmethod
    def init_range(initial_weights_diameter: float = 0.1, ps_learning_rate: ParameterRangeSettings = None,
                   momentum: float = 1, num_hidden_nodes: list = None, ps_num_iterations: ParameterRangeSettings = None,
                   shuffle: bool = True, random_number_seed: int = None):
        setting = NeuralNetworkSetting(mode=CreateLearnerMode.ParameterRange, **locals())
        return setting

    @staticmethod
    def _verify_num_hidden_nodes(num_hidden_nodes, arg_name='Number of hidden nodes'):
        if any(num <= 0 for num in num_hidden_nodes):
            ErrorMapping.throw(GreaterThanError(arg_name=arg_name,
                                                lower_boundary=0,
                                                actual_value=num_hidden_nodes))
