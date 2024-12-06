import time
from datetime import timedelta
from typing import Any, List, Optional

import easymaker
from easymaker.api.request_body import BatchInferenceBody
from easymaker.common import constants, exceptions, utils
from easymaker.common.base_model.easymaker_base_model import EasyMakerBaseModel


class BatchInference(EasyMakerBaseModel):
    batch_inference_id: Optional[str] = None
    batch_inference_name: Optional[str] = None
    batch_inference_status_code: Optional[str] = None
    instance_count: Optional[int] = None
    timeout_minutes: Optional[int] = None
    image: Optional[Any] = None
    model: Optional[Any] = None
    pod_count: Optional[int] = None
    max_batch_size: Optional[int] = None
    inference_timeout_seconds: Optional[int] = None
    input_data_uri: Optional[str] = None
    input_data_type_code: Optional[str] = None
    include_glob_pattern: Optional[str] = None
    exclude_glob_pattern: Optional[str] = None
    output_upload_uri: Optional[str] = None
    log_and_crash_app_key: Optional[str] = None
    input_file_count: Optional[int] = None
    input_data_count: Optional[int] = None
    process_count: Optional[int] = None
    success2xx_count: Optional[int] = None
    fail4xx_count: Optional[int] = None
    fail5xx_count: Optional[int] = None
    elapsed_time_seconds: Optional[int] = None
    flavor: Optional[Any] = None
    boot_storage: Optional[Any] = None
    data_storage_list: Optional[List[Any]] = None

    def __init__(self, batch_inference_id: str = None):
        if batch_inference_id:
            response = easymaker.easymaker_config.api_sender.get_batch_inference_by_id(batch_inference_id)
            super().__init__(**response)

    def run(
        self,
        batch_inference_name: str,
        instance_count: int = 1,
        timeout_hours: int = 720,
        instance_name: str = None,
        model_name: str = None,
        #
        pod_count: int = 1,
        batch_size: int = 32,
        inference_timeout_seconds: int = 120,
        #
        input_data_uri: str = None,
        input_data_type: str = None,
        include_glob_pattern: Optional[str] = None,
        exclude_glob_pattern: Optional[str] = None,
        output_upload_uri: str = None,
        #
        data_storage_size: int = None,
        #
        description: Optional[str] = None,
        tag_list: Optional[List[Any]] = None,
        use_log: Optional[bool] = False,
        wait: Optional[bool] = True,
    ):
        """
        Returns:
            batch_inference_id
        """
        instance_list = easymaker.easymaker_config.api_sender.get_instance_list()
        model_list = easymaker.easymaker_config.api_sender.get_model_list()
        response = easymaker.easymaker_config.api_sender.run_batch_inference(
            BatchInferenceBody(
                batch_inference_name=batch_inference_name,
                instance_count=instance_count,
                timeout_minutes=timeout_hours * 60,
                flavor_id=utils.from_name_to_id(instance_list, instance_name, "instance"),
                model_id=utils.from_name_to_id(model_list, model_name, "model"),
                #
                pod_count=pod_count,
                max_batch_size=batch_size,
                inference_timeout_seconds=inference_timeout_seconds,
                #
                input_data_uri=input_data_uri,
                input_data_type_code=input_data_type,
                include_glob_pattern=include_glob_pattern,
                exclude_glob_pattern=exclude_glob_pattern,
                output_upload_uri=output_upload_uri,
                #
                data_storage_size=data_storage_size,
                #
                description=description,
                tag_list=tag_list,
                use_log=use_log,
            )
        )
        super().__init__(**response)
        if wait:
            waiting_time_seconds = 0
            while self.batch_inference_status_code != "COMPLETE":
                print(f"[AI EasyMaker] Batch Inference create status: {self.batch_inference_status_code} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                response = easymaker.easymaker_config.api_sender.get_batch_inference_by_id(self.batch_inference_id)
                super().__init__(**response)
                if "FAIL" in self.batch_inference_status_code or "STOPPED" in self.batch_inference_status_code:
                    raise exceptions.EasyMakerError("Batch Inference create failed.")
            print(f"[AI EasyMaker] Batch Inference create complete. batch_inference_id: {self.batch_inference_id}")
        else:
            print(f"[AI EasyMaker] Batch Inference create request complete. batch_inference_id: {self.batch_inference_id}")

        return self

    def delete(self):
        if self.batch_inference_id:
            easymaker.easymaker_config.api_sender.delete_batch_inference_by_id(self.batch_inference_id)
            super().__init__()
            print(f"[AI EasyMaker] Batch inference delete request complete. Batch inference ID : {self.batch_inference_id}")
        else:
            print("[AI EasyMaker] Failed to delete batch inference. The batch_inference_id is empty.")


def delete(batch_inference_id: str):
    if batch_inference_id:
        easymaker.easymaker_config.api_sender.delete_batch_inference_by_id(batch_inference_id)
        print(f"[AI EasyMaker] Batch inference delete request complete. Batch inference ID : {batch_inference_id}")
    else:
        print("[AI EasyMaker] Failed to delete batch inference. The batch_inference_id is empty.")
