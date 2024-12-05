from typing import Union, Any

from better_abc import ABCMeta, abstract_attribute


class BaseEndpoint(metaclass=ABCMeta):
    """
    Default environment request param of the underlying data intake to query. Use `None` for latest intake.
    NB: Class property.
    """
    default_environment_key = None

    """ Instance prop. The base URL of the endpoint. """
    base_url: str = abstract_attribute()
    """ Instance prop. The default keys of the parameters to include (if a value is set) in the request parameters. """
    param_keys: iter = set()

    def _url(self, path: Union[None, str, list[str]] = None):
        """
        Get URL composed of the base URL in this endpoint with the given path appended.

        :param None or str or list[str] path: path or path components to append to the base URL.
        :return: Base URL with given path appended. Different path components will be joined using a '/'.
        :rtype: str
        """
        if path is None:
            return self.base_url
        if type(path) is list:
            path = '/'.join(str(s).strip('/') for s in path)
        else:
            path = path.strip('/')
        return f'{self.base_url.strip("/")}/{path}'

    def _find_request_params(self, **kwargs) -> dict[str, Any]:
        """
        Constructs a dict containing the request parameters that should be included in the HTTP request.
        The possible request param keys can be given using keyword argument `keys`, falling back to `self.param_keys`.
        Only keys with a corresponding value which is not None, are included in the request params.
        :key keys: possible / "allowed" request parameter keys. Defaults to `self.param_keys` if not provided.
        :param kwargs: For each request param key, optionally a value that should be used for the request parameter.
        :return: Dictionary of request parameters.
        """
        keys = kwargs.get('keys', self.param_keys)
        params = {}

        for key in keys:
            value = kwargs.get(key)

            if value is None:
                continue

            params[key] = value

        if 'environment' in keys and 'environment' not in params and self.default_environment_key:
            params['environment'] = self.default_environment_key

        return params
