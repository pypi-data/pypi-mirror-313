from typing import Any, List, Optional
import json
import time
from datetime import timedelta
import os

import easymaker
from easymaker.api.request_body import PipelineRunCreateBody
from easymaker.common.base_model.easymaker_base_model import EasyMakerBaseModel
from easymaker.common import constants, exceptions, utils


class PipelineRun(EasyMakerBaseModel):
    pipeline_run_id: Optional[str] = None
    pipeline_run_name: Optional[str] = None
    pipeline_run_status_code: Optional[str] = None
    pipeline: Optional[Any] = None
    experiment: Optional[Any] = None
    pipeline_recurring_run: Optional[Any] = None
    flavor: Optional[Any] = None
    instance_count: Optional[Any] = None
    boot_storage: Optional[Any] = None
    nas_list: Optional[List[Any]] = None
    elapsed_time_seconds: Optional[Any] = None
    started_datetime: Optional[Any] = None
    finished_datetime: Optional[Any] = None
    parameter_list: Optional[List[Any]] = None

    def __init__(self, pipeline_run_id: str = None):
        if pipeline_run_id:
            pipeline_run_response = easymaker.easymaker_config.api_sender.get_pipeline_run_by_id(pipeline_run_id)
            super().__init__(**pipeline_run_response)

    def create(
        self,
        pipeline_run_name=None,
        description=None,
        pipeline_id=None,
        experiment_id=None,
        experiment_name=None,
        experiment_description=None,
        experiment_tag_list=None,
        parameter_list=None,
        instance_name=None,
        instance_count=1,
        boot_storage_size=50,
        nas_list=None,
        tag_list=None,
        wait=True,
    ):
        if not experiment_id:
            experiment_id = os.environ.get("EM_EXPERIMENT_ID")
        instance_list = easymaker.easymaker_config.api_sender.get_instance_list()
        response = easymaker.easymaker_config.api_sender.create_pipeline_run(
            PipelineRunCreateBody(
                pipeline_run_or_recurring_run_name=pipeline_run_name,
                description=description,
                pipeline_id=pipeline_id,
                experiment_id=experiment_id,
                experiment_name=experiment_name,
                experiment_description=experiment_description,
                experiment_tag_list=experiment_tag_list,
                parameter_list=parameter_list,
                flavor_id=utils.from_name_to_id(instance_list, instance_name, "instance"),
                instance_count=instance_count,
                boot_storage_size=boot_storage_size,
                nas_list=nas_list,
                tag_list=tag_list,
            )
        )
        super().__init__(**response)

        if wait:
            waiting_time_seconds = 0
            while self.pipeline_run_status_code != "COMPLETE":
                print(f"[AI EasyMaker] Pipeline run status : {self.pipeline_run_status_code} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                response = easymaker.easymaker_config.api_sender.get_pipeline_run_by_id(self.pipeline_run_id)
                super().__init__(**response)
                if "FAIL" in self.pipeline_run_status_code or "STOPPED" in self.pipeline_run_status_code:
                    raise exceptions.EasyMakerError("Pipeline run create failed.")
            print(f"[AI EasyMaker] Pipeline run create complete. pipeline_run_id: {self.pipeline_run_id}")
        else:
            print(f"[AI EasyMaker] Pipeline run create request complete. pipeline_run_id: {self.pipeline_run_id}")

        return self

    def stop(self):
        if self.pipeline_run_id:
            easymaker.easymaker_config.api_sender.stop_pipeline_run_by_id(self.pipeline_run_id)
            print(f"[AI EasyMaker] Pipeline run stop request complete. Pipeline run ID : {self.pipeline_run_id}")
        else:
            print("[AI EasyMaker] Pipeline run stop fail. pipeline_run_id is empty.")

    def delete(self):
        if self.pipeline_run_id:
            easymaker.easymaker_config.api_sender.delete_pipeline_run_by_id(self.pipeline_run_id)
            super().__init__()
            print(f"[AI EasyMaker] Pipeline run delete request complete. Pipeline run ID : {self.pipeline_run_id}")
        else:
            print("[AI EasyMaker] Failed to delete pipeline run. The pipeline_run_id is empty.")


def delete(pipeline_run_id: str):
    if pipeline_run_id:
        easymaker.easymaker_config.api_sender.delete_pipeline_run_by_id(pipeline_run_id)
        print(f"[AI EasyMaker] Pipeline run delete request complete. Pipeline run ID : {pipeline_run_id}")
    else:
        print("[AI EasyMaker] Failed to delete pipeline run. The pipeline_run_id is empty.")
