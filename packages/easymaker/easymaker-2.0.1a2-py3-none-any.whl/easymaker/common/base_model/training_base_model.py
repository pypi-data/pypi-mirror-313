from typing import Any, List, Optional

from easymaker.common.base_model.easymaker_base_model import EasyMakerBaseModel


class TrainingCommonBaseModel(EasyMakerBaseModel):
    experiment: Optional[Any] = None
    instance_count: Optional[int] = None
    nproc_per_node: Optional[int] = None
    algorithm: Optional[Any] = None
    source_dir_uri: Optional[str] = None
    entry_point: Optional[str] = None
    model_upload_uri: Optional[str] = None
    check_point_input_uri: Optional[str] = None
    check_point_upload_uri: Optional[str] = None
    log_and_crash_app_key: Optional[str] = None
    timeout_minutes: Optional[int] = None
    elapsed_time_seconds: Optional[int] = None
    tensorboard_access_uri: Optional[str] = None
    tensorboard_access_path: Optional[str] = None
    dataset_list: Optional[List[Any]] = None
    flavor: Optional[Any] = None
    image: Optional[Any] = None
    boot_storage: Optional[Any] = None
    data_storage_list: Optional[List[Any]] = None
    model_list: Optional[List[Any]] = None


class TrainingBaseModel(TrainingCommonBaseModel):
    training_id: Optional[str] = None
    training_name: Optional[str] = None
    training_status_code: Optional[str] = None
    hyperparameter_list: Optional[List[Any]] = None
