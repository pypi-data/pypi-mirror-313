from typing import Any, List, Optional

from easymaker.common.base_model.training_base_model import TrainingCommonBaseModel


class HyperparameterTuningBaseModel(TrainingCommonBaseModel):
    hyperparameter_tuning_id: Optional[str] = None
    hyperparameter_tuning_name: Optional[str] = None
    hyperparameter_tuning_status_code: Optional[str] = None
    hyperparameter_tuning_status_reason: Optional[str] = None
    hyperparameter_spec_list: Optional[List[Any]] = None
    metricList: Optional[List[Any]] = None
    metricRegex: Optional[str] = None
    objectiveMetricName: Optional[str] = None
    objectiveTypeCode: Optional[str] = None
    objectiveGoal: Optional[float] = None
    maxFailedTrialCount: Optional[int] = None
    maxTrialCount: Optional[int] = None
    parallelTrialCount: Optional[int] = None
    tuningStrategyName: Optional[str] = None
    tuningStrategyRandomState: Optional[int] = None
    earlyStoppingAlgorithm: Optional[str] = None
    earlyStoppingMinTrialCount: Optional[int] = None
    earlyStoppingStartStep: Optional[int] = None
    successfulTrialCount: Optional[int] = None
    runningTrialCount: Optional[int] = None
    failedTrialCount: Optional[int] = None
    optimalTrialId: Optional[str] = None
    optimalTrial: Optional[Any] = None
