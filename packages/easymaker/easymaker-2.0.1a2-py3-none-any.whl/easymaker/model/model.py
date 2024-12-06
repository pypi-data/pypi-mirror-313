import time
from datetime import timedelta
from typing import Any, List, Optional

import easymaker
from easymaker.api.request_body import ModelCreateBody
from easymaker.common import constants, exceptions
from easymaker.common.base_model.easymaker_base_model import EasyMakerBaseModel


class Model(EasyMakerBaseModel):
    model_id: Optional[str] = None
    model_name: Optional[str] = None  # TODO. model_name이 BaseModel 예약어라 충돌이나는데 어떻게 처리할지 확인 필요
    model_status_code: Optional[str] = None
    training: Optional[Any] = None
    hyperparameter_tuning: Optional[Any] = None
    framework_version: Optional[str] = None
    model_type_code: Optional[str] = None
    model_upload_uri: Optional[str] = None

    def __init__(self, model_id: str = None):
        if model_id:
            response = easymaker.easymaker_config.api_sender.get_model_by_id(model_id)
            super().__init__(**response)

    def create(
        self,
        model_name: str,
        training_id: Optional[str] = None,
        hyperparameter_tuning_id: Optional[str] = None,
        description: Optional[str] = None,
        parameter_list: Optional[List[Any]] = None,
        tag_list: Optional[List[Any]] = None,
        wait: Optional[bool] = True,
    ):
        """
        Args:
            model_name (str): Model name
            training_id (str): Training ID
            hyperparameter_tuning_id (str): Hyperparameter Tuning ID
            description (str): Model description
            tag_list (list): tags
        Returns:
            Model
        """
        response = easymaker.easymaker_config.api_sender.create_model(
            ModelCreateBody(
                model_name=model_name,
                training_id=training_id,
                hyperparameter_tuning_id=hyperparameter_tuning_id,
                description=description,
                parameter_list=parameter_list,
                tag_list=tag_list,
            )
        )
        super().__init__(**response)
        if wait:
            waiting_time_seconds = 0
            while self.model_status_code != "ACTIVE":
                print(f"[AI EasyMaker] Model create status : {self.model_status_code} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                response = easymaker.easymaker_config.api_sender.get_model_by_id(self.model_id)
                super().__init__(**response)
                if "FAIL" in self.model_status_code:
                    raise exceptions.EasyMakerError("Model create failed.")

            print(f"[AI EasyMaker] Model create complete. model_id: {self.model_id}")
        else:
            print(f"[AI EasyMaker] Model create complete. model_id: {self.model_id}")
        return self

    def create_by_model_upload_uri(
        self,
        model_name: str,
        model_type_code: Optional[str] = None,
        model_upload_uri: Optional[str] = None,
        description: Optional[str] = None,
        parameter_list: Optional[List[Any]] = None,
        tag_list: Optional[List[Any]] = None,
        wait: Optional[bool] = True,
    ):
        """
        Args:
            model_name (str): Model name
            model_type_code (str): easymaker.TENSORFLOW or easymaker.PYTORCH or easymaker.SCIKIT_LEARN
            model_upload_uri (str): model upload uri (NHN Cloud Object Storage or NAS)
            description (str): Model description
            parameter_list (list): model parameter list
            tag_list (list): tags
        Returns:
            Model
        """
        response = easymaker.easymaker_config.api_sender.create_model(
            ModelCreateBody(
                model_name=model_name,
                model_type_code=model_type_code,
                model_upload_uri=model_upload_uri,
                description=description,
                parameter_list=parameter_list,
                tag_list=tag_list,
            )
        )
        super().__init__(**response)
        if wait:
            waiting_time_seconds = 0
            while self.model_status_code != "ACTIVE":
                print(f"[AI EasyMaker] Model create status : {self.model_status_code} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                response = easymaker.easymaker_config.api_sender.get_model_by_id(self.model_id)
                super().__init__(**response)
                if "FAIL" in self.model_status_code:
                    raise exceptions.EasyMakerError("Model create failed.")

            print(f"[AI EasyMaker] Model create complete. model_id: {self.model_id}")
        else:
            print(f"[AI EasyMaker] Model create complete. model_id: {self.model_id}")
        return self

    def create_hugging_face_model(
        self,
        model_name: str,
        description: Optional[str] = None,
        parameter_list: Optional[List[Any]] = None,
        tag_list: Optional[List[Any]] = None,
        wait: Optional[bool] = True,
    ):
        """
        Args:
            model_name (str): Model name
            parameter_list (list): model parameter list
            description (str): Model description
            tag_list (list): tags
        Returns:
            Model
        """
        response = easymaker.easymaker_config.api_sender.create_model(
            ModelCreateBody(
                model_name=model_name,
                model_type_code=easymaker.HUGGING_FACE,
                description=description,
                parameter_list=parameter_list,
                tag_list=tag_list,
            )
        )
        super().__init__(**response)
        if wait:
            waiting_time_seconds = 0
            while self.model_status_code != "ACTIVE":
                print(f"[AI EasyMaker] Model create status : {self.model_status_code} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                response = easymaker.easymaker_config.api_sender.get_model_by_id(self.model_id)
                super().__init__(**response)
                if "FAIL" in self.model_status_code:
                    raise exceptions.EasyMakerError("Model create failed.")

            print(f"[AI EasyMaker] Model create complete. model_id: {self.model_id}")
        else:
            print(f"[AI EasyMaker] Model create complete. model_id: {self.model_id}")
        return self

    def delete(self):
        if self.model_id:
            easymaker.easymaker_config.api_sender.delete_model_by_id(self.model_id)
            super().__init__()


def delete(model_id: str):
    if model_id:
        easymaker.easymaker_config.api_sender.delete_model_by_id(model_id)
