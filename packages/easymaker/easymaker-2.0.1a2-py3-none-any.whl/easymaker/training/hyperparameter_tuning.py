import os
import time
from datetime import timedelta
from typing import Any, List, Optional

import easymaker
from easymaker.api.request_body import HyperparameterTuningCreateBody
from easymaker.common import constants, exceptions, utils
from easymaker.common.base_model.hyperparameter_tuning_base_model import (
    HyperparameterTuningBaseModel,
)


class HyperparameterTuning(HyperparameterTuningBaseModel):
    def __init__(self, hyperparameter_tuning_id: str = None):
        if hyperparameter_tuning_id:
            response = easymaker.easymaker_config.api_sender.get_hyperparameter_tuning_by_id(hyperparameter_tuning_id)
            super().__init__(**response)

    def run(
        self,
        hyperparameter_tuning_name: str,
        experiment_id: Optional[str] = None,
        description: Optional[str] = None,
        algorithm_name: Optional[str] = None,
        image_name: Optional[str] = None,
        instance_name: Optional[str] = None,
        distributed_node_count: Optional[int] = 1,
        parallel_trial_count: Optional[int] = 1,
        data_storage_size: Optional[int] = None,
        source_dir_uri: Optional[str] = None,
        entry_point: Optional[str] = None,
        hyperparameter_spec_list: Optional[List[Any]] = None,  # [{"name": "","type": easymaker.HYPERPARAMETER_TYPE_CODE,"feasibleSpace": {"min": "","max": "","list": "","step": "",}}, ]
        dataset_list: Optional[List[Any]] = None,
        check_point_input_uri: Optional[str] = None,
        check_point_upload_uri: Optional[str] = None,
        model_upload_uri: Optional[str] = None,
        timeout_hours: Optional[int] = 720,
        tag_list: Optional[List[Any]] = None,
        use_log: Optional[bool] = False,
        wait: Optional[bool] = True,
        metric_list: Optional[List[Any]] = None,  # name 리스트만 입력받아  [{"name": ""}, {"name": ""}] 형태로 변경
        metric_regex: Optional[str] = None,
        objective_metric_name: Optional[str] = None,  # name 값만 입력받아 {"name": ""} 형태로 변경
        objective_type_code: Optional[str] = None,  # easymaker.OBJECTIVE_TYPE_CODE.MINIMIZE, MAXIMIZE
        objective_goal: Optional[float] = None,
        max_failed_trial_count: Optional[int] = None,
        max_trial_count: Optional[int] = None,
        tuning_strategy_name: Optional[str] = None,  # easymaker.TUNING_STRATEGY.BAYESIAN_OPTIMIZATION, RANDOM, GRID
        tuning_strategy_random_state: Optional[int] = None,
        early_stopping_algorithm: Optional[str] = None,  # easymaker.EARLY_STOPPING_ALGORITHM.MEDIAN
        early_stopping_min_trial_count: Optional[int] = 3,
        early_stopping_start_step: Optional[int] = 4,
        use_torchrun: Optional[bool] = False,
        nproc_per_node: Optional[int] = 0,
    ):
        """
        Returns:
            hyperparameter_tuning_id
        """

        def convertMetricFormat(name):
            return {"name": name}

        # run hyperparameter tuning
        instance_list = easymaker.easymaker_config.api_sender.get_instance_list()
        image_list = easymaker.easymaker_config.api_sender.get_image_list()
        algorithm_list = easymaker.easymaker_config.api_sender.get_algorithm_list()
        if not experiment_id:
            experiment_id = os.environ.get("EM_EXPERIMENT_ID")
        response = easymaker.easymaker_config.api_sender.run_hyperparameter_tuning(
            HyperparameterTuningCreateBody(
                hyperparameter_tuning_name=hyperparameter_tuning_name,
                description=description,
                experiment_id=experiment_id,
                algorithm_id=utils.from_name_to_id(algorithm_list, algorithm_name, "algorithm") if algorithm_name else None,
                image_id=utils.from_name_to_id(image_list, image_name, "image"),
                flavor_id=utils.from_name_to_id(instance_list, instance_name, "instance"),
                instance_count=distributed_node_count * parallel_trial_count,
                parallel_trial_count=parallel_trial_count,
                data_storage_size=data_storage_size,
                source_dir_uri=source_dir_uri,
                entry_point=entry_point,
                hyperparameter_spec_list=hyperparameter_spec_list,
                dataset_list=dataset_list,
                check_point_input_uri=check_point_input_uri,
                check_point_upload_uri=check_point_upload_uri,
                model_upload_uri=model_upload_uri,
                timeout_minutes=timeout_hours * 60,
                tag_list=tag_list,
                use_log=use_log,
                metric_list=list(map(convertMetricFormat, metric_list)) if metric_list else None,
                metric_regex=metric_regex,
                objective_metric=convertMetricFormat(objective_metric_name) if objective_metric_name else None,
                objective_type_code=objective_type_code,
                objective_goal=objective_goal,
                max_failed_trial_count=max_failed_trial_count,
                max_trial_count=max_trial_count,
                tuning_strategy_name=tuning_strategy_name,
                tuning_strategy_random_state=tuning_strategy_random_state,
                early_stopping_algorithm=early_stopping_algorithm,
                early_stopping_min_trial_count=early_stopping_min_trial_count,
                early_stopping_start_step=early_stopping_start_step,
                use_torchrun=use_torchrun,
                nproc_per_node=nproc_per_node,
            )
        )
        super().__init__(**response)
        if wait:
            waiting_time_seconds = 0
            while self.hyperparameter_tuning_status_code != "COMPLETE":
                print(f"[AI EasyMaker] Hyperparameter Tuning create status: {self.hyperparameter_tuning_status_code} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                response = easymaker.easymaker_config.api_sender.get_hyperparameter_tuning_by_id(self.hyperparameter_tuning_id)
                super().__init__(**response)
                if "FAIL" in self.hyperparameter_tuning_status_code or "STOPPED" in self.hyperparameter_tuning_status_code:
                    raise exceptions.EasyMakerError("Hyperparameter Tuning create failed.")
            print(f"[AI EasyMaker] Hyperparameter Tuning create complete. hyperparameter_tuning_id: {self.hyperparameter_tuning_id}")
        else:
            print(f"[AI EasyMaker] Hyperparameter Tuning create request complete. hyperparameter_tuning_id: {self.hyperparameter_tuning_id}")

        return self

    def delete(self):
        if self.hyperparameter_tuning_id:
            easymaker.easymaker_config.api_sender.delete_hyperparameter_tuning_by_id(self.hyperparameter_tuning_id)
            super().__init__()


def delete(hyperparameter_tuning_id: str):
    if hyperparameter_tuning_id:
        easymaker.easymaker_config.api_sender.delete_hyperparameter_tuning_by_id(hyperparameter_tuning_id)
