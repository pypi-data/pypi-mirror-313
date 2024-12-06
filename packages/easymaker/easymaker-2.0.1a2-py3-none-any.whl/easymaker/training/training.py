import os
import time
from datetime import timedelta
from typing import Any, List, Optional

import easymaker
from easymaker.api.request_body import TrainingCreateBody
from easymaker.common import constants, exceptions, utils
from easymaker.common.base_model.training_base_model import TrainingBaseModel


class Training(TrainingBaseModel):
    def __init__(self, training_id: str = None):
        if training_id:
            response = easymaker.easymaker_config.api_sender.get_training_by_id(training_id)
            super().__init__(**response)

    def run(
        self,
        training_name: str,
        experiment_id: Optional[str] = None,
        description: Optional[str] = None,
        image_name: Optional[str] = None,
        instance_name: Optional[str] = None,
        distributed_node_count: Optional[int] = 1,
        data_storage_size: Optional[int] = None,
        source_dir_uri: Optional[str] = None,
        entry_point: Optional[str] = None,
        algorithm_name: Optional[str] = None,
        hyperparameter_list: Optional[List[Any]] = None,  # [{"name": "","type": easymaker.HYPERPARAMETER_TYPE_CODE,"feasibleSpace": {"min": "","max": "","list": "","step": "",}}, ]
        dataset_list: Optional[List[Any]] = None,
        check_point_input_uri: Optional[str] = None,
        check_point_upload_uri: Optional[str] = None,
        model_upload_uri: Optional[str] = None,
        timeout_hours: Optional[int] = 720,
        tag_list: Optional[List[Any]] = None,
        use_log: Optional[bool] = False,
        wait: Optional[bool] = True,
        use_torchrun: Optional[bool] = False,
        nproc_per_node: Optional[int] = 0,
    ):
        """
        Returns:
            training_id
        """
        # run training
        instance_list = easymaker.easymaker_config.api_sender.get_instance_list()
        image_list = easymaker.easymaker_config.api_sender.get_image_list()
        algorithm_list = easymaker.easymaker_config.api_sender.get_algorithm_list()
        if not experiment_id:
            experiment_id = os.environ.get("EM_EXPERIMENT_ID")
        response = easymaker.easymaker_config.api_sender.run_training(
            TrainingCreateBody(
                training_name=training_name,
                description=description,
                experiment_id=experiment_id,
                image_id=utils.from_name_to_id(image_list, image_name, "image"),
                flavor_id=utils.from_name_to_id(instance_list, instance_name, "instance"),
                instance_count=distributed_node_count,
                data_storage_size=data_storage_size,
                source_dir_uri=source_dir_uri,
                entry_point=entry_point,
                algorithm_id=utils.from_name_to_id(algorithm_list, algorithm_name, "algorithm") if algorithm_name else None,
                hyperparameter_list=hyperparameter_list,
                dataset_list=dataset_list,
                check_point_input_uri=check_point_input_uri,
                check_point_upload_uri=check_point_upload_uri,
                model_upload_uri=model_upload_uri,
                training_type_code="NORMAL",
                timeout_minutes=timeout_hours * 60,
                tag_list=tag_list,
                use_log=use_log,
                use_torchrun=use_torchrun,
                nproc_per_node=nproc_per_node,
            )
        )
        super().__init__(**response)
        if wait:
            waiting_time_seconds = 0
            while self.training_status_code != "COMPLETE":
                print(f"[AI EasyMaker] Training create status: {self.training_status_code} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                response = easymaker.easymaker_config.api_sender.get_training_by_id(self.training_id)
                super().__init__(**response)
                if "FAIL" in self.training_status_code or "STOPPED" in self.training_status_code:
                    raise exceptions.EasyMakerError("Training create failed.")
            print(f"[AI EasyMaker] Training create complete. training_id: {self.training_id}")
        else:
            print(f"[AI EasyMaker] Training create request complete. training_id: {self.training_id}")

        return self

    def delete(self):
        if self.training_id:
            easymaker.easymaker_config.api_sender.delete_training_by_id(self.training_id)
            super().__init__()
            print(f"[AI EasyMaker] Training delete request complete. Training ID : {self.training_id}")
        else:
            print("[AI EasyMaker] Failed to delete training. The training_id is empty.")


def delete(training_id: str):
    if training_id:
        easymaker.easymaker_config.api_sender.delete_training_by_id(training_id)
        print(f"[AI EasyMaker] Training delete request complete. Training ID : {training_id}")
    else:
        print("[AI EasyMaker] Failed to delete training. The training_id is empty.")
