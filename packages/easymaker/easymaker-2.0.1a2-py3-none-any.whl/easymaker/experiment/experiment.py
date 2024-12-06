import time
from datetime import timedelta
from typing import Any, List, Optional

import easymaker
from easymaker.api.request_body import ExperimentCreateBody
from easymaker.common import constants, exceptions
from easymaker.common.base_model.easymaker_base_model import EasyMakerBaseModel


class Experiment(EasyMakerBaseModel):
    experiment_id: Optional[str] = None
    experiment_name: Optional[str] = None
    experiment_status_code: Optional[str] = None
    tensorboard_access_uri: Optional[str] = None

    def __init__(self, experiment_id: str = None):
        if experiment_id:
            response = easymaker.easymaker_config.api_sender.get_experiment_by_id(experiment_id)
            super().__init__(**response)

    def create(
        self,
        experiment_name: str,
        description: Optional[str] = None,
        tag_list: Optional[List[Any]] = None,
        wait: Optional[bool] = True,
    ):
        """
        Args:
            experiment_name (str): Experiment name
            experiment_description (str): Experiment description
            tag_list (list): [{"tagKey": "sample","tagValue": "sample"}]
            wait (bool): wait for the job to complete
        Returns:
            experiment_id
        """
        try:
            experiment_id = get_id_by_name(experiment_name=experiment_name)
            print(f"[AI EasyMaker] Experiment '{experiment_name}' already exists. experiment_id: {experiment_id}")

            response = easymaker.easymaker_config.api_sender.get_experiment_by_id(experiment_id)
            super().__init__(**response)
            return self
        except ValueError:
            pass

        response = easymaker.easymaker_config.api_sender.create_experiment(
            ExperimentCreateBody(
                experiment_name=experiment_name,
                description=description,
                tag_list=tag_list,
            )
        )
        super().__init__(**response)
        if wait:
            waiting_time_seconds = 0
            while self.experiment_status_code != "ACTIVE":
                print(f"[AI EasyMaker] Experiment upload status: {self.experiment_status_code} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
                time.sleep(constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS)
                waiting_time_seconds += constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS
                response = easymaker.easymaker_config.api_sender.get_experiment_by_id(self.experiment_id)
                super().__init__(**response)
                if "FAIL" in self.experiment_status_code == "CREATE_FAILED":
                    raise exceptions.EasyMakerError("Experiment create failed.")
            print(f"[AI EasyMaker] Experiment create complete. experiment_id: {self.experiment_id}")
        else:
            print(f"[AI EasyMaker] Experiment create request complete. experiment_id: {self.experiment_id}")

        return self

    def delete(self):
        if self.experiment_id:
            response = easymaker.easymaker_config.api_sender.delete_experiment_by_id(self.experiment_id)
            super().__init__()
            print(f"[AI EasyMaker] Experiment delete request complete. Experiment ID : {self.experiment_id}")
        else:
            print("[AI EasyMaker] Failed to delete experiment. The experiment_id is empty.")


def delete(experiment_id: str):
    if experiment_id:
        easymaker.easymaker_config.api_sender.delete_experiment_by_id(experiment_id)
        print(f"[AI EasyMaker] Experiment delete request complete. Experiment ID : {experiment_id}")
    else:
        print("[AI EasyMaker] Failed to delete experiment. The experiment_id is empty.")


def get_id_by_name(experiment_name: str):
    experiments = get_list(experiment_name_list=[experiment_name])

    if not experiments:
        raise ValueError(f"[AI EasyMaker] No experiment is found with name {experiment_name}.")

    if len(experiments) > 1:
        raise ValueError(f"[AI EasyMaker] Multiple experiments is found with name {experiment_name}.")

    return experiments[0]["id"]


def get_list(
    experiment_id_list: Optional[List[str]] = None,
    experiment_name_list: Optional[List[str]] = None,
) -> list[dict]:
    return easymaker.easymaker_config.api_sender.get_experiment_list(
        experiment_name_list=experiment_name_list,
        experiment_id_list=experiment_id_list,
    )
