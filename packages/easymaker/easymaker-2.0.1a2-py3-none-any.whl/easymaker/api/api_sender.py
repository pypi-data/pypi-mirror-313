import os
import ssl
from typing import List, Optional

import requests
from requests.adapters import HTTPAdapter, Retry
from requests.sessions import Session
from urllib3 import poolmanager

from easymaker.api.request_body import (
    BatchInferenceBody,
    EndpointCreateBody,
    ExperimentCreateBody,
    HyperparameterTuningCreateBody,
    ModelCreateBody,
    PipelineRecurringRunCreateBody,
    PipelineRunCreateBody,
    PipelineUploadBody,
    StageCreateBody,
    TrainingCreateBody,
)
from easymaker.common import constants, exceptions


class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        self.poolmanager = poolmanager.PoolManager(num_pools=connections, maxsize=maxsize, block=block, ssl_context=ctx)


class ApiSender:
    def __init__(self, region, appkey, secret_key=None):

        if os.environ.get("EM_PROFILE") and os.environ.get("EM_PROFILE") != "real":
            self._easymakerApiUrl = constants.EASYMAKER_DEV_API_URL.format(region, os.environ.get("EM_PROFILE")).rstrip("/")
            if os.environ.get("EM_PROFILE") == "local":
                self._easymakerApiUrl = "http://127.0.0.1:10090".rstrip("/")
        else:
            self._easymakerApiUrl = constants.EASYMAKER_API_URL.format(region).rstrip("/")

        self._appkey = appkey
        self._secret_key = secret_key

        self.session = Session()
        self.session.mount("https://", TLSAdapter(max_retries=Retry(total=3, backoff_factor=1, status_forcelist=Retry.RETRY_AFTER_STATUS_CODES)))
        self.session.headers.update(self._get_headers())

        if not os.environ.get("EM_PROFILE") in ["local", "test"]:
            try:
                requests.get(self._easymakerApiUrl + "/nhn-api-gateway")
            except Exception:
                raise exceptions.EasyMakerRegionError("Invalid region")

    def _isSuccessful(self, response):
        isSuccess = response["header"]["isSuccessful"]
        if not isSuccess:
            raise exceptions.EasyMakerError(response)

        return isSuccess

    def _get_headers(self):
        if os.environ.get("EM_TOKEN"):
            headers = {"X-EasyMaker-Token": os.environ.get("EM_TOKEN")}
        else:
            headers = {"X-Secret-Key": self._secret_key}
        headers["Accept-Language"] = "en"
        return headers

    def get_objectstorage_token(self, tenant_id=None, username=None, password=None):

        if os.environ.get("EM_TOKEN"):
            response = self.session.get(f'{self._easymakerApiUrl}/token/v1.0/appkeys/{self._appkey}/groups/{os.environ.get("EM_GROUP_ID")}/iaas-token').json()
            self._isSuccessful(response)
            return response
        else:
            if tenant_id and username and password:
                token_url = constants.OBJECT_STORAGE_TOKEN_URL
                req_header = {"Content-Type": "application/json"}
                body = {"auth": {"tenantId": tenant_id, "passwordCredentials": {"username": username, "password": password}}}
                response = self.session.post(token_url, headers=req_header, json=body).json()
                return response
            else:
                raise exceptions.EasyMakerError(f"Invalid object storage username/password")

    def get_instance_list(self):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/flavors").json()
        self._isSuccessful(response)

        flavor_dict_list = []
        for flavor in response["flavorList"]:
            flavor_dict_list.append({"id": flavor["id"], "name": flavor["name"]})
        return flavor_dict_list

    def get_image_list(self):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/images").json()
        self._isSuccessful(response)

        image_dict_list = []
        for image in response["imageList"]:
            if image["groupTypeCode"] == "TRAINING":
                image_dict_list.append({"id": image["imageId"], "name": image["imageName"]})
        return image_dict_list

    def get_algorithm_list(self):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/algorithms").json()
        self._isSuccessful(response)

        algorithm_dict_list = []
        image_dict = {image["id"]: image["name"] for image in self.get_image_list()}

        for algorithm in response["algorithmList"]:
            algorithm_dict_list.append({"id": algorithm["algorithmId"], "name": algorithm["algorithmName"], "availableTrainingImageList": [image_dict[algorithm["cpuTrainingImageId"]], image_dict[algorithm["gpuTrainingImageId"]]]})

        return algorithm_dict_list

    def get_experiment_list(
        self,
        experiment_id_list: Optional[List[str]] = None,
        experiment_name_list: Optional[List[str]] = None,
    ) -> list[dict]:
        params = {}
        if experiment_id_list:
            params["experimentIdList"] = ",".join(experiment_id_list)
        if experiment_name_list:
            params["experimentNameList"] = ",".join(experiment_name_list)

        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/experiments", params=params).json()
        self._isSuccessful(response)

        dict_list = []
        for experiment in response["experimentList"]:
            dict_list.append({"id": experiment["experimentId"], "name": experiment["experimentName"]})
        return dict_list

    def create_experiment(self, body: ExperimentCreateBody):
        response = self.session.post(
            f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/experiments",
            json=body.model_dump(),
        ).json()
        self._isSuccessful(response)

        return response["experiment"]

    def get_experiment_by_id(self, experiment_id):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/experiments/{experiment_id}").json()
        self._isSuccessful(response)

        return response["experiment"]

    def delete_experiment_by_id(self, experiment_id):
        response = self.session.delete(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/experiments/{experiment_id}").json()
        self._isSuccessful(response)

        return response

    def run_training(self, body: TrainingCreateBody):
        response = self.session.post(
            f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/trainings",
            json=body.model_dump(),
        ).json()

        self._isSuccessful(response)
        return response["training"]

    def get_training_list(self):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/trainings").json()
        self._isSuccessful(response)

        dict_list = []
        for training in response["trainingList"]:
            dict_list.append({"id": training["trainingId"], "name": training["trainingName"]})
        return dict_list

    def get_training_by_id(self, training_id):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/trainings/{training_id}").json()
        self._isSuccessful(response)

        return response["training"]

    def delete_training_by_id(self, training_id):
        response = self.session.delete(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/trainings/{training_id}").json()
        self._isSuccessful(response)

        return response

    def run_hyperparameter_tuning(self, body: HyperparameterTuningCreateBody):
        response = self.session.post(
            f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/hyperparameter-tunings",
            json=body.model_dump(),
        ).json()

        self._isSuccessful(response)
        return response["hyperparameterTuning"]

    def get_hyperparameter_tuning_list(self):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/hyperparameter-tunings").json()
        self._isSuccessful(response)

        dict_list = []
        for training in response["hyperparameterTuningList"]:
            dict_list.append({"id": training["hyperparameterTuningId"], "name": training["hyperparameterTuningName"]})
        return dict_list

    def get_hyperparameter_tuning_by_id(self, hyperparameter_tuning_id):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/hyperparameter-tunings/{hyperparameter_tuning_id}").json()
        self._isSuccessful(response)

        return response["hyperparameterTuning"]

    def delete_hyperparameter_tuning_by_id(self, hyperparameter_tuning_id):
        response = self.session.delete(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/hyperparameter-tunings/{hyperparameter_tuning_id}").json()
        self._isSuccessful(response)

        return response

    def create_model(self, body: ModelCreateBody):
        response = self.session.post(
            f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/models",
            json=body.model_dump(),
        ).json()
        self._isSuccessful(response)

        return response["model"]

    def get_model_list(self):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/models").json()
        self._isSuccessful(response)

        dict_list = []
        for model in response["modelList"]:
            dict_list.append({"id": model["modelId"], "name": model["modelName"]})
        return dict_list

    def get_model_by_id(self, model_id):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/models/{model_id}").json()
        self._isSuccessful(response)

        return response["model"]

    def delete_model_by_id(self, model_id):
        response = self.session.delete(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/models/{model_id}").json()
        self._isSuccessful(response)

        return response

    def create_endpoint(self, body: EndpointCreateBody):
        response = self.session.post(
            f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/endpoints",
            json=body.model_dump(),
        ).json()
        self._isSuccessful(response)

        return response["endpoint"]

    def create_stage(self, body: StageCreateBody):
        response = self.session.post(
            f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/endpoint-stages",
            json=body.model_dump(),
        ).json()
        self._isSuccessful(response)

        return response["endpointStage"]

    def get_endpoint_list(self):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/endpoints").json()
        self._isSuccessful(response)

        return response["endpointList"]

    def get_endpoint_by_id(self, endpoint_id):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/endpoints/{endpoint_id}").json()
        self._isSuccessful(response)

        return response["endpoint"]

    def get_endpoint_stage_list(self, endpoint_id):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/endpoint-stages", params={"endpointId": endpoint_id}).json()
        self._isSuccessful(response)

        return response["endpointStageList"]

    def get_endpoint_stage_by_id(self, endpoint_stage_id):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/endpoint-stages/{endpoint_stage_id}").json()
        self._isSuccessful(response)

        return response["endpointStage"]

    def get_endpoint_model_list(self, endpoint_stage_id):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/endpoint-models", params={"endpointStageId": endpoint_stage_id}).json()
        self._isSuccessful(response)

        return response["endpointModelList"]

    def get_endpoint_model_by_id(self, endpoint_model_id):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/endpoint-models/{endpoint_model_id}").json()
        self._isSuccessful(response)

        return response["endpointModel"]

    def delete_endpoint_by_id(self, endpoint_id):
        response = self.session.delete(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/endpoints/{endpoint_id}").json()
        self._isSuccessful(response)

        return response

    def delete_endpoint_stage_by_id(self, endpoint_stage_id):
        response = self.session.delete(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/endpoint-stages/{endpoint_stage_id}").json()
        self._isSuccessful(response)

        return response

    def delete_endpoint_model_by_id(self, endpoint_model_id):
        response = self.session.delete(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/endpoint-models/{endpoint_model_id}").json()
        self._isSuccessful(response)

        return response

    def run_batch_inference(self, body: BatchInferenceBody):
        response = self.session.post(
            f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/batch-inferences",
            json=body.model_dump(),
        ).json()

        self._isSuccessful(response)
        return response["batchInference"]

    def get_batch_inference_list(self):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/batch-inferences").json()
        self._isSuccessful(response)

        dict_list = []
        for batch_inference in response["batchInferenceList"]:
            dict_list.append(
                {
                    "id": batch_inference["batchInferenceId"],
                    "name": batch_inference["batchInferenceName"],
                }
            )
        return dict_list

    def get_batch_inference_by_id(self, batch_inference_id):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/batch-inferences/{batch_inference_id}").json()
        self._isSuccessful(response)

        return response["batchInference"]

    def delete_batch_inference_by_id(self, batch_inference_id):
        response = self.session.delete(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/batch-inferences/{batch_inference_id}").json()
        self._isSuccessful(response)

        return response

    def send_logncrash(self, logncrash_body):
        response = self.session.post(constants.LOGNCRASH_URL, json=logncrash_body).json()
        return response

    # Pipeline
    def upload_pipeline(self, body: PipelineUploadBody):
        response = self.session.post(
            f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/pipelines/upload",
            json=body.model_dump(),  # camel case로 변환
        ).json()
        self._isSuccessful(response)

        return response["pipeline"]

    def get_pipeline_by_id(self, pipeline_id):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/pipelines/{pipeline_id}").json()
        self._isSuccessful(response)

        return response["pipeline"]

    def delete_pipeline_by_id(self, pipeline_id):
        response = self.session.delete(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/pipelines/{pipeline_id}").json()
        self._isSuccessful(response)

        return response

    # Pipeline Run
    def get_pipeline_run_by_id(self, pipeline_run_id):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/pipeline-runs/{pipeline_run_id}").json()
        self._isSuccessful(response)

        return response["pipelineRun"]

    def create_pipeline_run(self, body: PipelineRunCreateBody):
        response = self.session.post(
            f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/pipeline-runs",
            json=body.model_dump(),
        ).json()
        self._isSuccessful(response)

        return response["pipelineRun"]

    def stop_pipeline_run_by_id(self, pipeline_run_id):
        response = self.session.put(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/pipeline-runs/{pipeline_run_id}/stop").json()
        self._isSuccessful(response)

        return response

    def delete_pipeline_run_by_id(self, pipeline_run_id):
        response = self.session.delete(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/pipeline-runs/{pipeline_run_id}").json()
        self._isSuccessful(response)

        return response

    # Pipeline Recurring Run
    def get_pipeline_recurring_run_by_id(self, pipeline_recurring_run_id):
        response = self.session.get(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/pipeline-recurring-runs/{pipeline_recurring_run_id}").json()
        self._isSuccessful(response)

        return response["pipelineRecurringRun"]

    def create_pipeline_recurring_run(self, body: PipelineRecurringRunCreateBody):
        response = self.session.post(
            f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/pipeline-runs",
            json=body.model_dump(),
        ).json()
        self._isSuccessful(response)

        return response["pipelineRecurringRun"]

    def stop_pipeline_recurring_run_by_id(self, pipeline_recurring_run_id):
        response = self.session.put(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/pipeline-recurring-runs/{pipeline_recurring_run_id}/stop").json()
        self._isSuccessful(response)

        return response

    def start_pipeline_recurring_run_by_id(self, pipeline_recurring_run_id):
        response = self.session.put(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/pipeline-recurring-runs/{pipeline_recurring_run_id}/start").json()
        self._isSuccessful(response)

        return response

    def delete_pipeline_recurring_run_by_id(self, pipeline_recurring_run_id):
        response = self.session.delete(f"{self._easymakerApiUrl}/v1.0/appkeys/{self._appkey}/pipeline-recurring-runs/{pipeline_recurring_run_id}").json()
        self._isSuccessful(response)

        return response
