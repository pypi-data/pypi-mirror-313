from typing import Any, List, Optional
import base64
import json
import time
from datetime import timedelta

import easymaker
from easymaker.api.request_body import PipelineUploadBody
from easymaker.common.base_model.easymaker_base_model import EasyMakerBaseModel
from easymaker.common import constants, exceptions


class Pipeline(EasyMakerBaseModel):
    pipeline_id: Optional[str] = None
    pipeline_name: Optional[str] = None
    pipeline_parameter_spec_list: Optional[List[Any]] = None
    pipeline_status_code: Optional[str] = None
    pipeline_spec_manifest: Optional[Any] = None

    def __init__(self, pipeline_id: str = None):
        if pipeline_id:
            pipeline_response = easymaker.easymaker_config.api_sender.get_pipeline_by_id(pipeline_id)
            super().__init__(**pipeline_response)

    def upload(
        self,
        pipeline_name,
        pipeline_spec_manifest_path,
        description,
        tag_list,
        wait=True,
    ):

        with open(pipeline_spec_manifest_path, "rb") as file:
            pipeline_spec_manifest = file.read()
        base64_pipeline_spec_manifest = base64.b64encode(pipeline_spec_manifest).decode("utf-8")

        response = easymaker.easymaker_config.api_sender.upload_pipeline(
            PipelineUploadBody(
                pipeline_name=pipeline_name,
                base64_pipeline_spec_manifest=base64_pipeline_spec_manifest,
                description=description,
                tag_list=tag_list,
            )
        )
        super().__init__(**response)

        if wait:
            waiting_time_seconds = 0
            while self.pipeline_status_code != "ACTIVE":
                print(f"[AI EasyMaker] Pipeline upload status : {self.pipeline_status_code} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                response = easymaker.easymaker_config.api_sender.get_pipeline_by_id(self.pipeline_id)
                super().__init__(**response)
                if self.pipeline_status_code == "CREATE_FAILED":
                    raise exceptions.EasyMakerError("Pipeline upload failed.")
            print(f"[AI EasyMaker] Pipeline upload complete. Pipeline ID : {self.pipeline_id}")
        else:
            print(f"[AI EasyMaker] Pipeline upload request complete. Pipeline ID : {self.pipeline_id}")

        return self

    def delete(self):
        if self.pipeline_id:
            easymaker.easymaker_config.api_sender.delete_pipeline_by_id(self.pipeline_id)
            super().__init__()
            print(f"[AI EasyMaker] Pipeline delete request complete. Pipeline ID : {self.pipeline_id}")
        else:
            print("[AI EasyMaker] Failed to delete pipeline. The pipeline_id is empty.")


def delete(pipeline_id: str):
    if pipeline_id:
        easymaker.easymaker_config.api_sender.delete_pipeline_by_id(pipeline_id)
        print(f"[AI EasyMaker] Pipeline delete request complete. Pipeline ID : {pipeline_id}")
    else:
        print("[AI EasyMaker] Failed to delete pipeline. The pipeline_id is empty.")
