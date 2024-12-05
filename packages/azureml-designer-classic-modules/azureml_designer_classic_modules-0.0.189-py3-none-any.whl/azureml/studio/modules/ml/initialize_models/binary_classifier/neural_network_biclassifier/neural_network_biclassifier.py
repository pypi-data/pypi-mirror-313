from sklearn.neural_network import MLPClassifier

from azureml.studio.common.parameter_range import ParameterRangeSettings
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.attributes import ModeParameter, BooleanParameter, FloatParameter, IntParameter, \
    ParameterRangeParameter, StringParameter, ModuleMeta, UntrainedLearnerOutputPort
from azureml.studio.modulehost.constants import FLOAT_MIN_POSITIVE, UINT32_MAX
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.ml.common.base_learner import TaskType, CreateLearnerMode, RestoreInfo
from azureml.studio.modules.ml.common.supervised_learners import BinaryClassificationLearner
from azureml.studio.modules.ml.initialize_models.common_settings.neural_network_setting import \
    NeuralNetworkDefaultParameters, CreateNeuralNetworkModelTopology, CreateNeuralNetworkModelNormalizationMethod, \
    NeuralNetworkSetting


class TwoClassNeuralNetworkModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Two-Class Neural Network",
        description="Creates a binary classifier using a neural network algorithm.",
        category="Machine Learning Algorithms/Classification",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="EBC29F52-719D-4D0F-B66A-2CE85F527C7D",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            mode: ModeParameter(
                CreateLearnerMode,
                name="Create trainer mode",
                friendly_name="Create trainer mode",
                description="Create advanced learner options",
                default_value=NeuralNetworkDefaultParameters.Mode,
            ),
            neural_network_topology: ModeParameter(
                CreateNeuralNetworkModelTopology,
                name="Hidden layer specification",
                friendly_name="Hidden layer specification",
                description="Specify the architecture of the hidden layer or layers",
                default_value=NeuralNetworkDefaultParameters.NeuralNetworkTopology,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
            ),
            neural_network_topology_for_range: ModeParameter(
                CreateNeuralNetworkModelTopology,
                name="Hidden layer specification1",
                friendly_name="Hidden layer specification",
                description="Specify the architecture of the hidden layer or layers for range",
                default_value=NeuralNetworkDefaultParameters.NeuralNetworkTopologyForRange,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
            ),
            initial_weights_diameter: FloatParameter(
                name="The initial learning weights diameter",
                friendly_name="The initial learning weights diameter",
                description="Specify the node weights at the start of the learning process",
                default_value=NeuralNetworkDefaultParameters.InitialWeightsDiameter,
                min_value=FLOAT_MIN_POSITIVE,
                release_state=ReleaseState.Alpha
            ),
            learning_rate: FloatParameter(
                name="The learning rate",
                friendly_name="Learning rate",
                description="Specify the size of each step in the learning process",
                default_value=NeuralNetworkDefaultParameters.LearningRate,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=FLOAT_MIN_POSITIVE,
                max_value=2.0,
            ),
            ps_learning_rate: ParameterRangeParameter(
                name="Range for learning rate",
                friendly_name="Learning rate",
                description="Specify the range for the size of each step in the learning process",
                default_value=NeuralNetworkDefaultParameters.PsLearningRate,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=FLOAT_MIN_POSITIVE,
                max_limit=2,
                is_int=False,
                is_log=True,
                slider_min=0.0001,
                slider_max=2,
            ),
            momentum: FloatParameter(
                name="The momentum",
                friendly_name="The momentum",
                description="Specify a weight to apply during learning to nodes from previous iterations",
                default_value=NeuralNetworkDefaultParameters.Momentum,
                min_value=0,
                max_value=1,
            ),
            # TODO: ADD NormalizationMethod After Normalize Data Done
            normalizer_type: ModeParameter(
                CreateNeuralNetworkModelNormalizationMethod,
                name="The type of normalizer",
                friendly_name="The type of normalizer",
                description="elect the type of normalization to apply to learning examples",
                default_value=NeuralNetworkDefaultParameters.NormalizerType,
                release_state=ReleaseState.Alpha
            ),
            num_hidden_nodes: StringParameter(
                name="Number of hidden nodes",
                friendly_name="Number of hidden nodes",
                description="Type the number of nodes in the hidden layer. For multiple hidden layers, "
                            "type a comma-separated list.",
                default_value=NeuralNetworkDefaultParameters.NumHiddenNodes,
                parent_parameter="Hidden layer specification",
                parent_parameter_val=(CreateNeuralNetworkModelTopology.DefaultHiddenLayers,),
            ),
            num_hidden_nodes_for_range: StringParameter(
                name="Number of hidden nodes1",
                friendly_name="Number of hidden nodes",
                description="Type the number of nodes in the hidden layer, or for multiple hidden layers, "
                            "type a comma-separated list.",
                default_value=NeuralNetworkDefaultParameters.NumHiddenNodesForRange,
                parent_parameter="Hidden layer specification1",
                parent_parameter_val=(CreateNeuralNetworkModelTopology.DefaultHiddenLayers,),
            ),
            num_iterations: IntParameter(
                name="Number of learning iterations",
                friendly_name="Number of learning iterations",
                description="Specify the number of iterations while learning",
                default_value=NeuralNetworkDefaultParameters.NumIterations,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.SingleParameter,),
                min_value=1,
            ),
            ps_num_iterations: ParameterRangeParameter(
                name="Range for number of learning iterations",
                friendly_name="Number of learning iterations",
                description="Specify the range for the number of iterations while learning",
                default_value=NeuralNetworkDefaultParameters.PsNumIterations,
                parent_parameter="Create trainer mode",
                parent_parameter_val=(CreateLearnerMode.ParameterRange,),
                min_limit=1,
                max_limit=2147483647,
                is_int=True,
                is_log=False,
                slider_min=1,
                slider_max=500,
            ),
            shuffle: BooleanParameter(
                name="Shuffle examples",
                friendly_name="Shuffle examples",
                description="Select this option to change the order of instances between learning iterations",
                default_value=NeuralNetworkDefaultParameters.Shuffle,
            ),
            random_number_seed: IntParameter(
                name="Random number seed",
                friendly_name="Random number seed",
                min_value=0,
                max_value=UINT32_MAX,
                is_optional=True,
                description="Specify a numeric seed to use for random number generation. "
                            "Leave blank to use the default seed.",
            ),
            allow_unknown_levels: BooleanParameter(
                name="Allow unknown levels in categorical features",
                friendly_name="Allow unknown categorical levels",
                description="Indicate whether an additional level should be created for unknown categories. "
                            "If the test dataset contains categories not present in the training dataset "
                            "they are mapped to this unknown level.",
                default_value=NeuralNetworkDefaultParameters.AllowUnknownLevels,
                release_state=ReleaseState.Alpha
            )
    ) -> (
            UntrainedLearnerOutputPort(
                name="Untrained model",
                friendly_name="Untrained model",
                description="An untrained binary classification model",
            ),
    ):
        """Module Entry of the Neural Network Module

        SingleParameter -> neural_network_topology, num_hidden_nodes
        ParameterRange  -> neural_network_topology_for_range, num_hidden_nodes_for_range
        :return: UntrainedLearner
        """
        input_values = locals()

        output_values = TwoClassNeuralNetworkModule.create_neural_network_biclassifier(**input_values)
        return output_values

    @staticmethod
    def create_neural_network_biclassifier(
            mode: CreateLearnerMode = NeuralNetworkDefaultParameters.Mode,
            neural_network_topology: CreateNeuralNetworkModelTopology =
            NeuralNetworkDefaultParameters.NeuralNetworkTopology,
            neural_network_topology_for_range: CreateNeuralNetworkModelTopology =
            NeuralNetworkDefaultParameters.NeuralNetworkTopologyForRange,
            initial_weights_diameter: float = NeuralNetworkDefaultParameters.InitialWeightsDiameter,
            momentum: float = NeuralNetworkDefaultParameters.Momentum,
            num_hidden_nodes: str = NeuralNetworkDefaultParameters.NumHiddenNodes,
            num_hidden_nodes_for_range: str = NeuralNetworkDefaultParameters.NumHiddenNodesForRange,
            learning_rate: float = NeuralNetworkDefaultParameters.LearningRate,
            ps_learning_rate: ParameterRangeSettings = NeuralNetworkDefaultParameters.PsLearningRate,
            num_iterations: int = NeuralNetworkDefaultParameters.NumIterations,
            ps_num_iterations: ParameterRangeSettings = NeuralNetworkDefaultParameters.PsNumIterations,
            shuffle: bool = NeuralNetworkDefaultParameters.Shuffle,
            random_number_seed: int = NeuralNetworkDefaultParameters.RandomNumberSeed,
            normalizer_type: CreateNeuralNetworkModelNormalizationMethod =
            NeuralNetworkDefaultParameters.NormalizerType,
            allow_unknown_levels: bool = NeuralNetworkDefaultParameters.AllowUnknownLevels,
    ):  # todo replace type by attribute
        setting = NeuralNetworkSetting.init(**locals())
        return tuple([NeuralNetworkBiClassifier(setting)])


class NeuralNetworkBiClassifierSetting(NeuralNetworkSetting):
    # Compatible with old models
    pass


class NeuralNetworkBiClassifier(BinaryClassificationLearner):
    def __init__(self, setting: NeuralNetworkSetting):
        super().__init__(setting, task_type=TaskType.BinaryClassification)

    @property
    def parameter_mapping(self):
        return {
            'learning_rate_init': RestoreInfo(TwoClassNeuralNetworkModule._args.learning_rate.friendly_name),
            'max_iter': RestoreInfo(TwoClassNeuralNetworkModule._args.num_iterations.friendly_name)
        }

    def init_model(self):
        self.model = MLPClassifier(
            hidden_layer_sizes=self.setting.num_hidden_nodes,
            solver='sgd',
            learning_rate='adaptive',
            learning_rate_init=self.setting.learning_rate,
            max_iter=self.setting.num_iterations,
            shuffle=self.setting.shuffle,
            random_state=self.setting.random_number_seed,
            momentum=self.setting.momentum,
            # TODO, other parameter in tlc
        )
