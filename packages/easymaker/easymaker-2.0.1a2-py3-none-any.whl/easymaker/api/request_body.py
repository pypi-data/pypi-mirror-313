import os
from typing import Any, List, Optional

from pydantic import Field

from easymaker.common.base_model.easymaker_base_model import EasyMakerBaseModel


class EasyMakerResourceCreateCommonBody(EasyMakerBaseModel):
    parent_pipeline_run_id: Optional[str] = Field(os.getenv("EM_PIPELINE_RUN_ID", None), repr=False)
    parent_pipeline_run_task_name: Optional[str] = Field(os.getenv("EM_KUBEFLOW_PIPELINE_RUN_TASK_NAME", None), repr=False)


class ExperimentCreateBody(EasyMakerResourceCreateCommonBody):
    experiment_name: Optional[str] = None


class ModelCreateBody(EasyMakerResourceCreateCommonBody):
    model_name: str
    training_id: Optional[str] = None
    hyperparameter_tuning_id: Optional[str] = None
    model_type_code: Optional[str] = None
    parameter_list: Optional[List[Any]] = None
    model_upload_uri: Optional[str] = None


class TrainingCommonBody(EasyMakerResourceCreateCommonBody):
    experiment_id: Optional[str] = None
    experiment_name: Optional[str] = None
    experiment_description: Optional[str] = None
    experiment_tag_list: Optional[List[Any]] = None
    image_id: str
    flavor_id: str
    instance_count: int = 1
    data_storage_size: Optional[int] = None
    algorithm_id: Optional[str] = None
    dataset_list: Optional[List[Any]] = []
    check_point_input_uri: Optional[str] = None
    check_point_upload_uri: Optional[str] = None
    source_dir_uri: Optional[str] = None
    entry_point: Optional[str] = None
    model_upload_uri: str
    timeout_minutes: int = 43200
    use_log: Optional[bool] = False
    nproc_per_node: Optional[int] = 1
    use_torchrun: Optional[bool] = False


class TrainingCreateBody(TrainingCommonBody):
    training_name: str
    hyperparameter_list: Optional[List[Any]] = None
    training_type_code: str


class HyperparameterTuningCreateBody(TrainingCommonBody):
    hyperparameter_tuning_name: str
    hyperparameter_spec_list: Optional[List[Any]] = None
    metric_list: Optional[List[Any]] = None
    metric_regex: Optional[str] = None
    objective_metric: Optional[dict] = None
    objective_type_code: Optional[str] = None
    objective_goal: Optional[float] = None
    max_failed_trial_count: Optional[int] = None
    max_trial_count: Optional[int] = None
    parallel_trial_count: Optional[int] = None
    tuning_strategy_name: Optional[str] = None
    tuning_strategy_random_state: Optional[int] = None
    early_stopping_algorithm: Optional[str] = None
    early_stopping_min_trial_count: Optional[int] = None
    early_stopping_start_step: Optional[int] = None


class EndpointCreateBody(EasyMakerResourceCreateCommonBody):
    endpoint_name: str
    flavor_id: str
    endpoint_model_resource_list: List[Any] = None
    node_count: int
    ca_enable: Optional[bool] = None
    ca_min_node_count: Optional[int] = None
    ca_max_node_count: Optional[int] = None
    ca_scale_down_enable: Optional[bool] = None
    ca_scale_down_util_thresh: Optional[int] = None
    ca_scale_down_unneeded_time: Optional[int] = None
    ca_scale_down_delay_after_add: Optional[int] = None
    use_log: Optional[bool] = None


class StageCreateBody(EasyMakerResourceCreateCommonBody):
    endpoint_id: str
    apigw_stage_name: str
    flavor_id: str
    endpoint_model_resource_list: List[Any] = None
    node_count: int
    ca_enable: Optional[bool] = None
    ca_min_node_count: Optional[int] = None
    ca_max_node_count: Optional[int] = None
    ca_scale_down_enable: Optional[bool] = None
    ca_scale_down_util_thresh: Optional[int] = None
    ca_scale_down_unneeded_time: Optional[int] = None
    ca_scale_down_delay_after_add: Optional[int] = None
    use_log: Optional[bool] = None


class BatchInferenceBody(EasyMakerResourceCreateCommonBody):
    batch_inference_name: str
    instance_count: int
    timeout_minutes: int
    flavor_id: str
    model_id: str
    image_id: Optional[str] = None
    pod_count: int
    max_batch_size: int
    inference_timeout_seconds: int
    input_data_uri: str
    input_data_type_code: str
    include_glob_pattern: Optional[str] = None
    exclude_glob_pattern: Optional[str] = None
    output_upload_uri: str
    data_storage_size: int
    use_log: Optional[bool] = None


class PipelineUploadBody(EasyMakerResourceCreateCommonBody):
    pipeline_name: Optional[str] = None
    base64_pipeline_spec_manifest: Optional[str] = None


class PipelineRunCreateBody(EasyMakerResourceCreateCommonBody):
    pipeline_run_or_recurring_run_name: Optional[str] = None
    pipeline_id: Optional[str] = None
    experiment_id: Optional[str] = None
    experiment_name: Optional[str] = None
    experiment_description: Optional[str] = None
    experiment_tag_list: Optional[List[Any]] = None
    parameter_list: Optional[List[Any]] = None
    flavor_id: Optional[str] = None
    instance_count: Optional[int] = None
    boot_storage_size: Optional[int] = None
    nas_list: Optional[List[Any]] = None


class PipelineRecurringRunCreateBody(PipelineRunCreateBody):
    schedule_periodic_minutes: Optional[int] = None
    schedule_cron_expression: Optional[str] = None
    max_concurrency_count: Optional[int] = None
    schedule_start_datetime: Optional[str] = None
    schedule_end_datetime: Optional[str] = None
    use_catchup: Optional[bool] = None
