from abc import ABC, abstractmethod
from typing import Any

from pricecypher.dataclasses import PredictResult
from pricecypher.enums import AccessTokenGrantType
from .base_handler import BaseHandler


class InferenceHandler(BaseHandler, ABC):
    """
    The abstract InferenceHandler class serves as an interaction contract such that by extending it with its
        methods implemented, a "real-time" (api) handler can be created that performs model inference for a dataset,
        which can then be used in a generalized yet controlled setting.
    NB: This class should be used for "short" running tasks only (i.e. finish in less than 30 seconds), as it must (at
        least) be usable to handle HTTP requests (using the access token provided in such underlying request).
    """

    def get_allowed_access_token_grant_types(self) -> set[AccessTokenGrantType]:
        return {AccessTokenGrantType.STATIC}

    def set_access_token(self, access_token):
        """
        Set the static access token that will then be returned each time {self._get_access_token()} is called.
        NB: Since this InferenceHandler is intended to handle "real-time" API requests, the access token of the caller
            of that underlying API should be used during the handling of the "task". I.e., the runtime executing this
            InferenceHandler has to explicitly set this access token within a handler instance. Note that a M2M access
            token should not be used for this since that would lead to privilege escalating vulnerabilities.
        """
        self.set_token_generator(AccessTokenGrantType.STATIC.get_generator(access_token=access_token))

    @abstractmethod
    def handle(self, user_input: dict[str, Any]) -> PredictResult:
        raise NotImplementedError
