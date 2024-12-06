import importlib_metadata

from easymaker import initializer
from easymaker.batch_inference import batch_inference
from easymaker.common import constants
from easymaker.endpoint import endpoint
from easymaker.experiment import experiment
from easymaker.log import logger
from easymaker.model import model
from easymaker.pipeline import pipeline, pipeline_recurring_run, pipeline_run
from easymaker.storage import objectstorage
from easymaker.training import hyperparameter_tuning, training

try:
    __version__ = importlib_metadata.version("easymaker")
except importlib_metadata.PackageNotFoundError:
    __version__ = "unknown"

easymaker_config = initializer.global_config

init = easymaker_config.init

logger = logger.Logger

Experiment = experiment.Experiment

Training = training.Training

HyperparameterTuning = hyperparameter_tuning.HyperparameterTuning

Model = model.Model

Endpoint = endpoint.Endpoint
EndpointStage = endpoint.EndpointStage
EndpointModel = endpoint.EndpointModel

BatchInference = batch_inference.BatchInference

Pipeline = pipeline.Pipeline

PipelineRun = pipeline_run.PipelineRun

PipelineRecurringRun = pipeline_recurring_run.PipelineRecurringRun

download = objectstorage.download

upload = objectstorage.upload

ObjectStorage = objectstorage.ObjectStorage

TENSORFLOW = "TENSORFLOW"
PYTORCH = "PYTORCH"
SCIKIT_LEARN = "SCIKIT_LEARN"
HUGGING_FACE = "HUGGING_FACE"

HYPERPARAMETER_TYPE_CODE = constants.HYPERPARAMETER_TYPE_CODE
OBJECTIVE_TYPE_CODE = constants.OBJECTIVE_TYPE_CODE
TUNING_STRATEGY = constants.TUNING_STRATEGY
EARLY_STOPPING_ALGORITHM = constants.EARLY_STOPPING_ALGORITHM
INPUT_DATA_TYPE_CODE = constants.INPUT_DATA_TYPE_CODE

__all__ = (
    "init",
    "Training",
)
