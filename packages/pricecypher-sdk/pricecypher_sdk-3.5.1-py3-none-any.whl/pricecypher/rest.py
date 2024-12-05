import json
import os
import socket
from datetime import datetime
from random import randint
from time import sleep

import requests
from marshmallow import Schema, EXCLUDE

from .exceptions import HttpException, RateLimitException

UNKNOWN_ERROR = 'pricecypher.sdk.internal.unknown'

# Mapping from (wildcard) domains to IP addresses to resolve manually.
dns_cache = {}
# Keep track of original getaddrinfo function to use for domain names not in our custom cache.
prv_getaddrinfo = socket.getaddrinfo


def is_ipv4(s):
    """ Check whether the given address is an IPv4 address. """
    return ':' not in s


def add_custom_dns(domain, port, ip):
    """
    Add a custom DNS record to our local cache, such that requests for the given domain and port are resolved to the
    given ip address.
    ."""
    # See docs for tuple format: https://docs.python.org/2/library/socket.html#socket.getaddrinfo
    if is_ipv4(ip):
        value = (socket.AddressFamily.AF_INET, 1, 6, '', (ip, port))
    else:  # ipv6
        value = (socket.AddressFamily.AF_INET6, 1, 6, '', (ip, port, 0, 0))

    dns_cache[domain] = [value]


def new_getaddrinfo(*args):
    """
    Define a patched function that will replace the original `socket.getaddrinfo` function.
    This patched function will first check if the given host or its wildcard host is included in our local cache.
    If so, it resolves the address to the custom IP in our cache. Otherwise, the original getaddrinfo is used instead.
    """
    # Find host in given arguments and split it into parts.
    host = args[0]
    host_parts = host.split('.')

    if len(host_parts) < 1:
        return prv_getaddrinfo(*args)

    # Replace first part of domain with * such that we can also look for the wildcard host in our local cache.
    host_parts[0] = '*'
    host_wildcard = '.'.join(host_parts)

    try:
        # Try to find original host in cache first, if not present also try to find its wildcard version.
        return dns_cache.get(host, False) or dns_cache[host_wildcard]
    except KeyError:
        # If both the given host and its wildcard version are not present in cache, fallback to original function.
        return prv_getaddrinfo(*args)


# Patch the getaddrinfo function to use our local cache iff custom overwrite environment variables are set.
if 'CUSTOM_DNS_DOMAIN' in os.environ and 'CUSTOM_DNS_IP' in os.environ:
    # Patch getaddrinfo function.
    socket.getaddrinfo = new_getaddrinfo
    # Find the custom domain and IP to set in cache.
    custom_domain = os.environ.get('CUSTOM_DNS_DOMAIN')
    custom_ip = os.environ.get('CUSTOM_DNS_IP')

    # Add custom DNS rules to our local cache.
    add_custom_dns(custom_domain, 80, custom_ip)
    add_custom_dns(custom_domain, 443, custom_ip)


class RestClientOptions(object):
    """
    Configuration object for RestClient.
    Used for configuring additional RestClient options, such as rate-limit retries.

    :param float or tuple[float,float] timeout: (optional) Change the requests connect and read timeout (in seconds).
        Pass a tuple to specify both values separately or a float to set both to it.
        (defaults to 300.0 (5 minutes) for both)
    :param int retries: (optional) In the event an API request returns a 429 response header (indicating rate-limit
        has been hit), the RestClient will retry the request this many times using an exponential backoff strategy,
        before raising a RateLimitException.
        (defaults to 3)
    """

    def __init__(self, timeout=None, retries=None):
        self.timeout = 300.0
        self.retries = 3
        self.verify = True

        if timeout is not None:
            self.timeout = timeout

        if retries is not None:
            self.retries = retries

        if 'SSL_VERIFY' in os.environ:
            self.verify = os.environ.get('SSL_VERIFY').lower() == 'true'


class RestClient(object):
    """
    Provides simple methods for handling all RESTful api endpoints.

    :param str jwt: JWT token used to authorize requests to the APIs.
    :param RestClientOptions options: (optional) Pass an instance of RestClientOptions to configure additional
        RestClient options, such as rate-limit retries.
    """

    def __init__(self, jwt, options: RestClientOptions = None):
        if options is None:
            options = RestClientOptions()

        self.options = options
        self.jwt = jwt

        self._metrics = {'retries': 0, 'backoff': []}
        self._skip_sleep = False

        self.base_headers = {
            'Authorization': f'Bearer {self.jwt}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    # Returns the maximum amount of jitter to introduce in milliseconds (100ms)
    def MAX_REQUEST_RETRY_JITTER(self):
        return 100

    # Returns the maximum delay window allowed (1000ms)
    def MAX_REQUEST_RETRY_DELAY(self):
        return 1000

    # Returns the minimum delay window allowed (100ms)
    def MIN_REQUEST_RETRY_DELAY(self):
        return 100

    # Returns HTTP status codes on which to attempt retries
    def RETRIABLE_STATUS_CODES(self):
        return [408, 425, 429, 502, 503, 504]

    def _retry(self, make_request):
        # Track the API request attempt number
        attempt = 0

        # Reset the metrics tracker
        self._metrics = {'retries': 0, 'backoff': []}

        # Floor the retries at 0.
        retries = max(0, self.options.retries)

        while True:
            # Increment attempt number
            attempt += 1

            # Issue the request
            response = make_request()

            if response.status_code not in self.RETRIABLE_STATUS_CODES():
                break

            # Try to find Retry After header in response, which specifies the number of seconds we should wait.
            wait = response.headers.get('Retry-After')

            # break iff no retry needed
            if retries <= 0 or attempt > retries:
                break

            if wait is not None:
                # Wait for 3 seconds more than how long we should wait, just to be sure.
                wait = 1000 * (int(wait) + 3)
            else:
                # No Retry After header. Apply an exponential backoff for subsequent attempts, using this formula:
                # max(
                #   MIN_REQUEST_RETRY_DELAY,
                #   min(MAX_REQUEST_RETRY_DELAY, (100ms * (2 ** attempt - 1)) + random_bet(1, MAX_REQUEST_RETRY_JITTER))
                # )`

                # Increases base delay by (100ms * (2 ** attempt - 1))
                wait = 100 * 2 ** (attempt - 1)

                # Introduces jitter to the base delay; increases delay between 1ms to MAX_REQUEST_RETRY_JITTER (100ms)
                wait += randint(1, self.MAX_REQUEST_RETRY_JITTER())

                # Is never more than MAX_REQUEST_RETRY_DELAY (1s)
                wait = min(self.MAX_REQUEST_RETRY_DELAY(), wait)

                # Is never less than MIN_REQUEST_RETRY_DELAY (100ms)
                wait = max(self.MIN_REQUEST_RETRY_DELAY(), wait)

            self._metrics['retries'] = attempt
            self._metrics['backoff'].append(wait)

            # Skip calling sleep() when running unit tests
            if self._skip_sleep is False:
                # sleep() functions in seconds, so convert the milliseconds formula above accordingly
                sleep(wait / 1000)

        # Return the final Response
        return response

    def get(self, url, params=None, schema: Schema = None):
        headers = self.base_headers.copy()
        response = self._retry(lambda: requests.get(
            url,
            params=params, headers=headers, timeout=self.options.timeout, verify=self.options.verify
        ))

        return self._process_response(response, schema)

    def post(self, url, data=None, schema: Schema = None):
        headers = self.base_headers.copy()
        j_data = json.dumps(data, cls=JsonEncoder)
        response = self._retry(lambda: requests.post(
            url,
            data=j_data, headers=headers, timeout=self.options.timeout, verify=self.options.verify
        ))

        return self._process_response(response, schema)

    def file_post(self, url, data=None, files=None):
        headers = self.base_headers.copy()
        headers.pop('Content-Type', None)

        response = self._retry(lambda: requests.post(
            url,
            data=data, files=files, headers=headers, timeout=self.options.timeout, verify=self.options.verify
        ))
        return self._process_response(response)

    def patch(self, url, data=None):
        headers = self.base_headers.copy()

        response = self._retry(lambda: requests.patch(
            url,
            json=data, headers=headers, timeout=self.options.timeout, verify=self.options.verify
        ))
        return self._process_response(response)

    def put(self, url, data=None):
        headers = self.base_headers.copy()

        response = self._retry(lambda: requests.put(
            url,
            json=data, headers=headers, timeout=self.options.timeout, verify=self.options.verify
        ))
        return self._process_response(response)

    def delete(self, url, params=None, data=None):
        headers = self.base_headers.copy()
        params = params or {}

        response = self._retry(
            lambda: requests.delete(
                url,
                headers=headers, params=params, json=data, timeout=self.options.timeout, verify=self.options.verify
            ))
        return self._process_response(response)

    def _process_response(self, response, schema=None):
        return self._parse(response, schema).content()

    def _parse(self, response, schema=None):
        if not response.text:
            return EmptyResponse(response.status_code)
        try:
            return JsonResponse(response, schema)
        except ValueError:
            return PlainResponse(response)


class Response(object):
    def __init__(self, status_code, content, headers):
        self._status_code = status_code
        self._content = content
        self._headers = headers

    def content(self):
        if self._is_error():
            msg = self._error_message()

            if self._status_code == 429:
                reset_at = int(self._headers.get('x-ratelimit-reset', '-1'))
                raise RateLimitException(message=msg, error_code=self._error_code(), reset_at=reset_at)

            raise HttpException(message=msg, status_code=self._status_code, error_code=self._error_code())
        else:
            return self._content

    def _is_error(self):
        return self._status_code is None or self._status_code >= 400

    # Force implementation in subclasses
    def _error_code(self):
        raise NotImplementedError

    def _error_message(self):
        raise NotImplementedError


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class JsonResponse(Response):
    def __init__(self, response, schema: Schema = None):
        if schema is not None and response.status_code < 400:
            content = schema.loads(json_data=response.text, unknown=EXCLUDE)
        else:
            content = json.loads(response.text)
        super(JsonResponse, self).__init__(response.status_code, content, response.headers)

    def _error_code(self):
        if 'errorCode' in self._content:
            return self._content.get('errorCode')
        elif 'error' in self._content:
            return self._content.get('error')
        else:
            return UNKNOWN_ERROR

    def _error_message(self):
        message = self._content.get('message', '')
        if message is not None and message != '':
            return message
        return self._content.get('error', '')


class PlainResponse(Response):
    def __init__(self, response):
        super(PlainResponse, self).__init__(response.status_code, response.text, response.headers)

    def _error_code(self):
        return UNKNOWN_ERROR

    def _error_message(self):
        return self._content


class EmptyResponse(Response):
    def __init__(self, status_code):
        super(EmptyResponse, self).__init__(status_code, '', {})

    def _error_code(self):
        return UNKNOWN_ERROR

    def _error_message(self):
        return ''
