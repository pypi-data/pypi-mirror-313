class ScoreColumnConstants:
    # Label and Task Type Region
    BinaryClassScoredLabelType = "Binary Class Assigned Labels"
    MultiClassScoredLabelType = "Multi Class Assigned Labels"
    RegressionScoredLabelType = "Regression Assigned Labels"
    ClusterScoredLabelType = "Cluster Assigned Labels"
    AnomalyDetectionScoredLabelType = "Anomaly Detection Assigned Labels"
    ScoredLabelsColumnName = "Scored Labels"
    ClusterAssignmentsColumnName = "Assignments"
    QuantileScoredLabelsColumnName = "Scores for quantile :"
    # Probability Region
    CalibratedScoreType = "Calibrated Score"
    ScoredProbabilitiesColumnName = "Scored Probabilities"
    ScoredProbabilitiesMulticlassColumnNamePattern = "Scored Probabilities"
    # Distance Region
    ClusterDistanceMetricsColumnNamePattern = "DistancesToClusterCenter no."
    # Score Column Names Region
    # This region is for the contract that allows users to specify score columns according
    # column names. Each task corresponds unique score column names, so the evaluate model
    # module can deduce task type from score column names.
    BinaryClassScoredLabelColumnName = "Binary Class Scored Labels"
    BinaryClassScoredProbabilitiesColumnName = "Binary Class Scored Probabilities"
    MultiClassScoredLabelColumnName = "Multi Class Scored Labels"
    RegressionScoredLabelColumnName = "Regression Scored Labels"
    AnomalyDetectionScoredLabelColumnName = "Anomaly Detection Scored Labels"
    AnomalyDetectionProbabilitiesColumnName = "Anomaly Detection Scored Probabilities"


META_PROPERTY_LABEL_ENCODER_KEY = 'label_encoder'

# part for score column names for different task
BINARY_CLASS_SCORED_COLUMN_NAMES = [ScoreColumnConstants.BinaryClassScoredLabelColumnName,
                                    ScoreColumnConstants.BinaryClassScoredProbabilitiesColumnName]
MULTI_CLASS_SCORED_COLUMN_NAMES = [ScoreColumnConstants.MultiClassScoredLabelColumnName]
REGRESSION_SCORED_COLUMN_NAMES = [ScoreColumnConstants.RegressionScoredLabelColumnName]
CLUSTER_SCORED_COLUMN_NAMES = [ScoreColumnConstants.ClusterAssignmentsColumnName]
ANOMALY_DETECTION_COLUMN_NAMES = [ScoreColumnConstants.AnomalyDetectionScoredLabelColumnName,
                                  ScoreColumnConstants.AnomalyDetectionProbabilitiesColumnName]
