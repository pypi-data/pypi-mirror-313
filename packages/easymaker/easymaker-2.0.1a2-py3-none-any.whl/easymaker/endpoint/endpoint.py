import time
from datetime import timedelta
from typing import Any, List, Optional

import requests

import easymaker
from easymaker.api.request_body import EndpointCreateBody, StageCreateBody
from easymaker.common import constants, exceptions, utils
from easymaker.common.base_model.easymaker_base_model import EasyMakerBaseModel
from easymaker.endpoint import ApiSpec
from easymaker.endpoint import utils as endpoint_utils


class Endpoint(EasyMakerBaseModel):
    endpoint_id: Optional[str] = None
    endpoint_name: Optional[str] = None
    endpoint_status_code: Optional[str] = None
    apigw_app_key: Optional[str] = None
    apigw_region: Optional[str] = None
    apigw_service_id: Optional[str] = None
    image: Optional[Any] = None
    boot_storage: Optional[Any] = None
    data_storage_list: Optional[List[Any]] = None
    endpoint_stage_list: Optional[List[Any]] = None
    default_stage: Optional[Any] = None

    def __init__(self, endpoint_id: str = None, response: dict = None):
        if response:
            super().__init__(**response)
        elif endpoint_id:
            response = easymaker.easymaker_config.api_sender.get_endpoint_by_id(endpoint_id)
            super().__init__(**response)
            self.default_stage = get_default_endpoint_stage(endpoint_id=self.endpoint_id)

    def create(
        self,
        endpoint_name: Optional[str],
        endpoint_model_resource_list: List[Any],
        instance_name: Optional[str],
        instance_count: int = 1,
        description: Optional[str] = None,
        tag_list: Optional[List[Any]] = None,
        use_log: Optional[bool] = False,
        wait: Optional[bool] = True,
        autoscaler_enable: Optional[bool] = False,
        autoscaler_min_node_count: Optional[int] = 1,
        autoscaler_max_node_count: Optional[int] = 10,
        autoscaler_scale_down_enable: Optional[bool] = True,
        autoscaler_scale_down_util_threshold: Optional[int] = 50,
        autoscaler_scale_down_unneeded_time: Optional[int] = 10,
        autoscaler_scale_down_delay_after_add: Optional[int] = 10,
    ):
        """
        Returns:
            endpoint_id(str)
        """
        instance_list = easymaker.easymaker_config.api_sender.get_instance_list()
        response = easymaker.easymaker_config.api_sender.create_endpoint(
            EndpointCreateBody(
                endpoint_name=endpoint_name,
                description=description,
                flavor_id=utils.from_name_to_id(instance_list, instance_name, "instance"),
                endpoint_model_resource_list=endpoint_model_resource_list,
                node_count=instance_count,
                tag_list=tag_list,
                use_log=use_log,
                ca_enable=autoscaler_enable,
                ca_min_node_count=autoscaler_min_node_count,
                ca_max_node_count=autoscaler_max_node_count,
                ca_scale_down_enable=autoscaler_scale_down_enable,
                ca_scale_down_util_thresh=autoscaler_scale_down_util_threshold,
                ca_scale_down_unneeded_time=autoscaler_scale_down_unneeded_time,
                ca_scale_down_delay_after_add=autoscaler_scale_down_delay_after_add,
            )
        )
        super().__init__(**response)
        if wait:
            waiting_time_seconds = 0
            while self.endpoint_status_code != "ACTIVE":
                print(f"[AI EasyMaker] Endpoint create status : {self.endpoint_status_code} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                response = easymaker.easymaker_config.api_sender.get_endpoint_by_id(self.endpoint_id)
                super().__init__(**response)
                if "FAIL" in self.endpoint_status_code:
                    raise exceptions.EasyMakerError("Endpoint create failed.")

            self.default_stage = get_default_endpoint_stage(endpoint_id=self.endpoint_id)
            while self.default_stage.endpoint_stage_status_code != "ACTIVE":
                print(f"[AI EasyMaker] Endpoint stage create status : {self.default_stage.endpoint_stage_status_code} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                self.default_stage = EndpointStage(self.default_stage.endpoint_stage_id)
                if "FAIL" in self.default_stage.endpoint_stage_status_code:
                    raise exceptions.EasyMakerError("Endpoint Stage create failed.")

            print(f"[AI EasyMaker] Endpoint create complete. endpoint_id: {self.endpoint_id}, default_stage.endpoint_stage_id: {self.default_stage.endpoint_stage_id}")
        else:
            print(f"[AI EasyMaker] Endpoint create request complete. endpoint_id: {self.endpoint_id}")
        return self

    def predict(self, model_id, json=None, api_spec: ApiSpec = ApiSpec.auto):
        if self.default_stage:
            endpoint_model = next((x for x in self.default_stage.endpoint_model_list if x["modelId"] == model_id), {})
            model_name = endpoint_model.get("model", {}).get("modelName")
            endpoint_url = "https://" + self.default_stage.apigw_stage_url

            if api_spec == ApiSpec.auto:
                api_spec = endpoint_utils.get_api_spec(json)

            resource_uri = endpoint_model.get("apigwResourceUri", endpoint_utils.get_inference_url(api_spec, model_name))
            response = requests.post(f"{endpoint_url}{resource_uri}", json=json).json()
            return response

    def get_stage_list(self):
        return get_endpoint_stage_list(self.endpoint_id)

    def delete(self):
        if self.endpoint_id:
            easymaker.easymaker_config.api_sender.delete_endpoint_by_id(self.endpoint_id)
            super().__init__()
            print(f"[AI EasyMaker] Endpoint delete request complete. Endpoint ID : {self.endpoint_id}")
        else:
            print("[AI EasyMaker] Failed to delete endpoint. The endpoint_id is empty.")


def get_endpoint_list() -> List[Endpoint]:
    endpoint_list_response = easymaker.easymaker_config.api_sender.get_endpoint_list()
    endpoint_list = []
    for endpoint_response in endpoint_list_response:
        endpoint_list.append(Endpoint(response=endpoint_response))
    return endpoint_list


def delete_endpoint(endpoint_id: str):
    if endpoint_id:
        easymaker.easymaker_config.api_sender.delete_endpoint_by_id(endpoint_id)
        print(f"[AI EasyMaker] Endpoint delete request complete. Endpoint ID : {endpoint_id}")
    else:
        print("[AI EasyMaker] Failed to delete endpoint. The endpoint_id is empty.")


class EndpointStage(EasyMakerBaseModel):
    endpoint_stage_id: Optional[str] = None
    endpoint_id: Optional[str] = None
    endpoint_stage_name: Optional[str] = None
    endpoint_stage_status_code: Optional[str] = None
    apigw_stage_id: Optional[str] = None
    apigw_stage_name: Optional[str] = None
    log_and_crash_app_key: Optional[str] = None
    flavor: Optional[Any] = None
    auto_scaler: Optional[Any] = None
    node_count: Optional[int] = None
    is_active_node_group_status: Optional[bool] = None
    is_cluster_latest: Optional[bool] = None
    expired_datetime: Optional[str] = None
    apigw_stage_url: Optional[str] = None
    deploy_status: Optional[str] = None
    default_stage: Optional[bool] = None
    pod_count: Optional[int] = None
    endpoint: Optional[Any] = None
    endpoint_model_list: Optional[List[Any]] = None

    def __init__(self, endpoint_stage_id: str = None, response: dict = None):
        if response:
            super().__init__(**response)
        elif endpoint_stage_id:
            response = easymaker.easymaker_config.api_sender.get_endpoint_stage_by_id(endpoint_stage_id)
            super().__init__(**response)

    def create(
        self,
        stage_name: Optional[str],
        endpoint_id: Optional[str],
        endpoint_instance_name: Optional[str],
        endpoint_model_resource_list: List[Any],
        endpoint_instance_count: int = 1,
        stage_description: Optional[str] = None,
        tag_list: Optional[List[Any]] = None,
        use_log: Optional[bool] = False,
        autoscaler_enable: Optional[bool] = False,
        autoscaler_min_node_count: Optional[int] = 1,
        autoscaler_max_node_count: Optional[int] = 10,
        autoscaler_scale_down_enable: Optional[bool] = True,
        autoscaler_scale_down_util_threshold: Optional[int] = 50,
        autoscaler_scale_down_unneeded_time: Optional[int] = 10,
        autoscaler_scale_down_delay_after_add: Optional[int] = 10,
        wait: Optional[bool] = True,
    ):
        """
        Returns:
            endpoint_stage_id(str)
        """
        instance_list = easymaker.easymaker_config.api_sender.get_instance_list()
        response = easymaker.easymaker_config.api_sender.create_stage(
            StageCreateBody(
                endpoint_id=endpoint_id,
                apigw_stage_name=stage_name,
                description=stage_description,
                flavor_id=utils.from_name_to_id(instance_list, endpoint_instance_name, "instance"),
                endpoint_model_resource_list=endpoint_model_resource_list,
                node_count=endpoint_instance_count,
                tag_list=tag_list,
                use_log=use_log,
                ca_enable=autoscaler_enable,
                ca_min_node_count=autoscaler_min_node_count,
                ca_max_node_count=autoscaler_max_node_count,
                ca_scale_down_enable=autoscaler_scale_down_enable,
                ca_scale_down_util_thresh=autoscaler_scale_down_util_threshold,
                ca_scale_down_unneeded_time=autoscaler_scale_down_unneeded_time,
                ca_scale_down_delay_after_add=autoscaler_scale_down_delay_after_add,
            )
        )
        super().__init__(**response)
        if wait:
            waiting_time_seconds = 0
            while self.endpoint_stage_status_code != "ACTIVE":
                print(f"[AI EasyMaker] Endpoint stage create status : {self.endpoint_stage_status_code} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                response = easymaker.easymaker_config.api_sender.get_endpoint_stage_by_id(self.endpoint_stage_id)
                super().__init__(**response)
                if "FAIL" in self.endpoint_stage_status_code:
                    raise exceptions.EasyMakerError("Endpoint stage create failed.")
            print(f"[AI EasyMaker] Endpoint stage create complete. endpoint_stage_id: {self.endpoint_stage_id}")
        else:
            print(f"[AI EasyMaker] Endpoint stage create request complete. endpoint_stage_id: {self.endpoint_stage_id}")

        return self

    def predict(self, model_id, json=None, api_spec: ApiSpec = ApiSpec.auto):
        endpoint_model = next((x for x in self.endpoint_model_list if x["modelId"] == model_id), {})
        model_name = endpoint_model.get("model", {}).get("modelName")
        endpoint_url = "https://" + self.apigw_stage_url

        if api_spec == ApiSpec.auto:
            api_spec = endpoint_utils.get_api_spec(json)

        resource_uri = endpoint_model.get("apigwResourceUri", endpoint_utils.get_inference_url(api_spec, model_name))
        response = requests.post(f"{endpoint_url}{resource_uri}", json=json).json()
        return response

    def delete(self):
        if self.endpoint_stage_id:
            easymaker.easymaker_config.api_sender.delete_endpoint_stage_by_id(self.endpoint_stage_id)
            super().__init__()
            print(f"[AI EasyMaker] Endpoint stage delete request complete. Endpoint stage ID : {self.endpoint_stage_id}")
        else:
            print("[AI EasyMaker] Failed to delete endpoint stage. The endpoint_stage_id is empty.")


def get_endpoint_stage_list(endpoint_id) -> List[EndpointStage]:
    endpoint_stage_list_response = easymaker.easymaker_config.api_sender.get_endpoint_stage_list(endpoint_id)
    endpoint_stage_list = []
    for endpoint_stage_response in endpoint_stage_list_response:
        endpoint_stage_list.append(EndpointStage(response=endpoint_stage_response))
    return endpoint_stage_list


def get_default_endpoint_stage(endpoint_id) -> EndpointStage:
    endpoint_stage_list = get_endpoint_stage_list(endpoint_id)

    for endpoint_stage in endpoint_stage_list:
        if endpoint_stage.default_stage:
            return endpoint_stage
    return EndpointStage()


def delete_endpoint_stage(endpoint_stage_id: str):
    if endpoint_stage_id:
        easymaker.easymaker_config.api_sender.delete_endpoint_stage_by_id(endpoint_stage_id)
        print(f"[AI EasyMaker] Endpoint stage delete request complete. Endpoint stage ID : {endpoint_stage_id}")
    else:
        print("[AI EasyMaker] Failed to delete endpoint stage. The endpoint_stage_id is empty.")


class EndpointModel(EasyMakerBaseModel):
    endpoint_model_id: Optional[str]
    endpoint_id: Optional[str]
    endpoint_model_status_code: Optional[str]
    endpoint_stage_id: Optional[str]
    model_id: Optional[str]
    image_id: Optional[str]
    stage: Optional[Any]
    model: Optional[Any]
    running_pod_count: Optional[int]
    pod_count: Optional[int]

    def __init__(self, endpoint_model_id: str = None, response: dict = None):
        if response:
            super().__init__(**response)
        elif endpoint_model_id:
            response = easymaker.easymaker_config.api_sender.get_endpoint_model_by_id(endpoint_model_id)
            super().__init__(**response)

    def delete(self):
        if self.endpoint_model_id:
            easymaker.easymaker_config.api_sender.delete_endpoint_model_by_id(self.endpoint_model_id)
            super().__init__()


def get_endpoint_model_list(endpoint_model_id):
    endpoint_model_list_response = easymaker.easymaker_config.api_sender.get_endpoint_model_list(endpoint_model_id)
    endpoint_model_list = []
    for endpoint_model_response in endpoint_model_list_response:
        endpoint_model_list.append(EndpointModel(response=endpoint_model_response))
    return endpoint_model_list


def delete_endpoint_model(endpoint_model_id: str):
    if endpoint_model_id:
        easymaker.easymaker_config.api_sender.delete_endpoint_model_by_id(endpoint_model_id)
