from typing import Any, List, Optional
import json
import time
from datetime import timedelta
import os

import easymaker
from easymaker.api.request_body import PipelineRecurringRunCreateBody
from easymaker.common.base_model.easymaker_base_model import EasyMakerBaseModel
from easymaker.common import constants, exceptions, utils


class PipelineRecurringRun(EasyMakerBaseModel):
    pipeline_recurring_run_id: Optional[str] = None
    pipeline_recurring_run_name: Optional[str] = None
    pipeline_recurring_run_status_code: Optional[str] = None
    pipeline: Optional[Any] = None
    experiment: Optional[Any] = None
    pipeline_recurring_run: Optional[Any] = None
    flavor: Optional[Any] = None
    instance_count: Optional[Any] = None
    boot_storage: Optional[Any] = None
    nas_list: Optional[List[Any]] = None
    parameter_list: Optional[List[Any]] = None
    schedule_periodic_minutes: Optional[Any] = None
    schedule_cron_expression: Optional[Any] = None
    max_concurrency_count: Optional[Any] = None
    schedule_start_datetime: Optional[Any] = None
    schedule_end_datetime: Optional[Any] = None
    use_catchup: Optional[Any] = None

    def __init__(self, pipeline_recurring_run_id: str = None):
        if pipeline_recurring_run_id:
            pipeline_recurring_run_response = easymaker.easymaker_config.api_sender.get_pipeline_recurring_run_by_id(pipeline_recurring_run_id)
            super().__init__(**pipeline_recurring_run_response)

    def create(
        self,
        pipeline_recurring_run_name=None,
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
        schedule_periodic_minutes=None,
        schedule_cron_expression=None,
        max_concurrency_count=1,
        schedule_start_datetime=None,
        schedule_end_datetime=None,
        use_catchup=True,
        wait=True,
    ):
        if not experiment_id:
            experiment_id = os.environ.get("EM_EXPERIMENT_ID")
        if not schedule_cron_expression and not schedule_periodic_minutes:
            raise exceptions.EasyMakerError("Either schedule_cron_expression or schedule_periodic_minutes must be provided.")

        instance_list = easymaker.easymaker_config.api_sender.get_instance_list()
        response = easymaker.easymaker_config.api_sender.create_pipeline_recurring_run(
            PipelineRecurringRunCreateBody(
                pipeline_run_or_recurring_run_name=pipeline_recurring_run_name,
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
                schedule_periodic_minutes=schedule_periodic_minutes,
                schedule_cron_expression=schedule_cron_expression,
                max_concurrency_count=max_concurrency_count,
                schedule_start_datetime=schedule_start_datetime,
                schedule_end_datetime=schedule_end_datetime,
                use_catchup=use_catchup,
            )
        )
        super().__init__(**response)

        if wait:
            waiting_time_seconds = 0
            while self.pipeline_recurring_run_status_code != "ENABLED":
                print(f"[AI EasyMaker] Pipeline recurring run status : {self.pipeline_recurring_run_status_code} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                response = easymaker.easymaker_config.api_sender.get_pipeline_recurring_run_by_id(self.pipeline_recurring_run_id)
                super().__init__(**response)
                if self.pipeline_recurring_run_status_code == "CREATE_FAILED":
                    raise exceptions.EasyMakerError("Pipeline recurring run create failed.")
            print(f"[AI EasyMaker] Pipeline recurring run create complete. pipeline_recurring_run_id: {self.pipeline_recurring_run_id}")
        else:
            print(f"[AI EasyMaker] Pipeline recurring run create request complete. pipeline_recurring_run_id: {self.pipeline_recurring_run_id}")

        return self

    def stop(self):
        if self.pipeline_recurring_run_id:
            easymaker.easymaker_config.api_sender.stop_pipeline_recurring_run_by_id(self.pipeline_recurring_run_id)
            print(f"[AI EasyMaker] Pipeline recurring run stop request complete. Pipeline recurring run ID : {self.pipeline_recurring_run_id}")
        else:
            print("[AI EasyMaker] Pipeline recurring run stop fail. pipeline_recurring_run_id is empty.")

    def start(self):
        if self.pipeline_recurring_run_id:
            easymaker.easymaker_config.api_sender.start_pipeline_recurring_run_by_id(self.pipeline_recurring_run_id)
            print(f"[AI EasyMaker] Pipeline recurring run start request complete. Pipeline recurring run ID : {self.pipeline_recurring_run_id}")
        else:
            print("[AI EasyMaker] Pipeline recurring run start fail. pipeline_recurring_run_id is empty.")

    def delete(self):
        if self.pipeline_recurring_run_id:
            easymaker.easymaker_config.api_sender.delete_pipeline_recurring_run_by_id(self.pipeline_recurring_run_id)
            super().__init__()
            print(f"[AI EasyMaker] Pipeline recurring run delete request complete. Pipeline recurring run ID : {self.pipeline_recurring_run_id}")
        else:
            print("[AI EasyMaker] Failed to delete pipeline recurring run. The pipeline_recurring_run_id is empty.")


def delete(pipeline_recurring_run_id: str):
    if pipeline_recurring_run_id:
        easymaker.easymaker_config.api_sender.delete_pipeline_recurring_run_by_id(pipeline_recurring_run_id)
        print(f"[AI EasyMaker] Pipeline recurring run delete request complete. Pipeline recurring run ID : {pipeline_recurring_run_id}")
    else:
        print("[AI EasyMaker] Failed to delete pipeline recurring run. The pipeline_recurring_run_id is empty.")
