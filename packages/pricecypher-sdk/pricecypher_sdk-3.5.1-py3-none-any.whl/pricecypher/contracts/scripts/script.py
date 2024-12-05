import warnings
from abc import ABC, abstractmethod
from typing import Any, Optional, Callable

from pricecypher.contracts import BaseHandler
from pricecypher.enums import AccessTokenGrantType


class Script(BaseHandler, ABC):
    """
    The abstract Script class serves as an interaction contract specifically intended for internal tasks being triggered
    by the PriceCypher Engine itself. Such tasks are expected to (potentially) have a longer execution time. For
    instance, it is designed to allow tasks to run for a longer time than the lifetime of a single access token.

    NB: This class should not be used for handling events that are being triggered by a user directly. This, as these
    tasks generally make use of machine-to-machine tokens for authorisation. Indirect triggers by a user (like e.g.
    starting an intake workflow) should be possible only after proper authorisation has been performed separately.
    """

    def set_oidc_client_credentials(self, oidc_issuer, oidc_config):
        """
        Set the OIDC (client) details that the script uses to issue new access tokens (following the client_credentials
        grant type).

        :param oidc_issuer: The OIDC Issuer used to issue new access tokens. It must expose a "well-known" OpenID
        Configuration (used to determine, for instance, the token endpoint).
        :param oidc_config: Dictionary containing all request arguments used when issuing new access tokens.
            NB: If a `scope` key is specified, it will be included in the token request only if the value is not empty.
        """
        self.set_token_generator(AccessTokenGrantType.CLIENT_CREDENTIALS.get_generator(
            oidc_issuer=oidc_issuer,
            oidc_config=oidc_config,
        ))

    @property
    def config(self):
        warnings.warn('Use of the public `config` property is deprecated. Please use protected `self._config` instead.')
        return self._config

    @property
    def dataset_id(self):
        warnings.warn('Use of the public `dataset_id` property is deprecated. Please use protected `self._dataset_id`.')
        return self._dataset_id

    @property
    def settings(self) -> dict[str, Any]:
        warnings.warn('Use of the public `settings` property is deprecated. Please use protected `self._settings`.')
        return self._settings.__dict__

    @abstractmethod
    def get_scope_dependencies(self) -> list[dict[str, Any]]:
        """
        Fetch the scopes that the script will use and requires to be present in the dataset.

        NB: All required config is assumed to be present.

        :return: List of required scopes, where each is a dictionary containing either
            a 'representation' or a 'scope_id'.
        """
        raise NotImplementedError

    def handle(self, user_input: dict[str, Any]) -> any:
        return self.execute('all', self._get_access_token, user_input)

    @abstractmethod
    def execute(
            self,
            business_cell_id: Optional[int],
            get_bearer_token: Callable[[], str],
            user_input: dict[Any: Any],
    ) -> Any:
        """
        Execute the script

        NB: All required config and scopes are assumed to be present.

        :param business_cell_id: Business cell to execute the script for, or None if running the script for all.
        :param get_bearer_token: Function that can be invoked to retrieve an access token.
        :param user_input: Dictionary of additional json-serializable input provided by the caller of the script.
        :return: Any json-serializable results the script outputs.
        """
        raise NotImplementedError
