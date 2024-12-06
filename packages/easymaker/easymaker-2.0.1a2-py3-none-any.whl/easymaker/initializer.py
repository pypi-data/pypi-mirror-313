# -*- coding: utf-8 -*-

import logging
import os
from typing import Optional

from easymaker.api.api_sender import ApiSender
from easymaker.common import constants

_LOGGER = logging.getLogger(__name__)


class _Config:
    """Stores common parameters and options for API calls."""

    def __init__(self):
        self._appkey = os.environ.get("EM_APPKEY")
        self._region = os.environ.get("EM_REGION")
        self._user_id = None
        self._secret_key = None
        self.api_sender = None
        if os.environ.get("EM_APPKEY") and os.environ.get("EM_REGION"):
            self.api_sender = ApiSender(self._region, self._appkey)

    def init(
        self,
        *,
        appkey: Optional[str] = None,
        region: Optional[str] = None,
        secret_key: Optional[str] = None,
        profile: Optional[str] = None,
        experiment_id: Optional[str] = None,
    ):
        """
        Args:
            appkey (str): easymaker appkey
            region (str): region (kr1, ..)
            secret_key (str): easymaker secret key
            profile (str): easymaker profile (alpha, beta)
        """
        _LOGGER.debug("EasyMaker Config init")
        if appkey:
            self._appkey = appkey
            os.environ["EM_APPKEY"] = appkey
        if region:
            self._region = region
            os.environ["EM_REGION"] = region
        if secret_key:
            self._secret_key = secret_key
            os.environ["EM_SECRET_KEY"] = secret_key
        if profile:
            os.environ["EM_PROFILE"] = profile
        if experiment_id:
            os.environ["EM_EXPERIMENT_ID"] = experiment_id

        self.api_sender = ApiSender(region, appkey, secret_key)

    @property
    def appkey(self) -> str:
        return self._appkey

    @property
    def region(self) -> str:
        return self._region or constants.DEFAULT_REGION

    @property
    def secret_key(self) -> str:
        return self._secret_key


# global config to store init parameters: easymaker.init(appkey=..., region=...)
global_config = _Config()
