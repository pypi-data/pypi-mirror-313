from abc import ABC, abstractmethod
from time import time

from oic.oauth2 import Client, OauthMessageFactory, CCAccessTokenRequest, AccessTokenResponse
from oic.oauth2.message import MessageTuple
from oic.utils.authn.client import CLIENT_AUTHN_METHOD


class _CCMessageFactory(OauthMessageFactory):
    """Client Credentials Request Factory."""
    token_endpoint = MessageTuple(CCAccessTokenRequest, AccessTokenResponse)


class AccessTokenGenerator(ABC):
    @abstractmethod
    def generate(self) -> str:
        raise NotImplementedError


class StaticTokenGenerator(AccessTokenGenerator):
    _static_access_token: str

    def __init__(self, access_token: str, **kwargs):  # noqa - allow extra, unused keyed arguments
        super().__init__()
        self._static_access_token = access_token

    def generate(self) -> str:
        return self._static_access_token


class ClientTokenGenerator(AccessTokenGenerator):
    _oidc_issuer: str
    _oidc_request_args: dict
    _cached_response: dict

    def __init__(self, oidc_issuer: str, oidc_config: dict, **kwargs):  # noqa - allow extra, unused keyed arguments
        super().__init__()
        self._oidc_issuer = oidc_issuer
        self._oidc_request_args = self._oidc_request_args(oidc_config)
        self._cached_response = dict()

    @staticmethod
    def _oidc_request_args(oidc_config):
        request_args = oidc_config.copy()

        if 'scope' in request_args and request_args['scope'] is None:
            del request_args['scope']

        return request_args

    def generate(self) -> str:
        is_in_cache = 'access_token' in self._cached_response and 'expires_at' in self._cached_response

        if is_in_cache and self._cached_response['expires_at'] > time():
            return self._cached_response['access_token']

        client = Client(client_authn_method=CLIENT_AUTHN_METHOD, message_factory=_CCMessageFactory)
        client.provider_config(self._oidc_issuer)

        resp = client.do_access_token_request(request_args=self._oidc_request_args)
        self._cached_response = {
            'access_token': resp.get('access_token'),
            # Internally, ensure the access tokens have at least half their lifetime remaining.
            'expires_at': int(time()) + int(resp.get('expires_in')) / 2
        }

        return resp.get('access_token')
