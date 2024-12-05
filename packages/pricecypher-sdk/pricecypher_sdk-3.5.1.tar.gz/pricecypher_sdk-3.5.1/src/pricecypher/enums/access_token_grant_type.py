from enum import Enum

from pricecypher.oidc import AccessTokenGenerator
from pricecypher.oidc.auth import StaticTokenGenerator, ClientTokenGenerator


class AccessTokenGrantType(Enum):
    """
    We refer to a 'static' access token when the token does not change during a single execution of an event handler.
    The 'client_credentials' grant type can be used by event handlers that can potentially run for a longer time
    than the lifetime of a single access token. Though, it may not be used by event handlers that are triggered by a
    user directly.
    """
    STATIC = 'static'
    CLIENT_CREDENTIALS = 'client_credentials'

    def get_generator(self, **kwargs) -> AccessTokenGenerator:
        match self:
            case AccessTokenGrantType.STATIC:
                return StaticTokenGenerator(**kwargs)
            case AccessTokenGrantType.CLIENT_CREDENTIALS:
                return ClientTokenGenerator(**kwargs)
