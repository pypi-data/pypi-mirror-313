import json
import unittest

import mock
import requests

from pricecypher.exceptions import RateLimitException, HttpException
from pricecypher.rest import RestClient, RestClientOptions


class TestRest(unittest.TestCase):
    TIMEOUT_DEF = 300.0

    @classmethod
    def setUpClass(cls):
        cls.low_timeout_options = RestClientOptions(0.00001)
        cls.tuple_timeout_options = RestClientOptions((10, 2))
        cls.static_response_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def test_get_can_timeout(self):
        rc = RestClient(jwt='a-token', options=self.low_timeout_options)

        with self.assertRaises(requests.exceptions.Timeout):
            rc.get('https://google.com')

    def test_post_can_timeout(self):
        rc = RestClient(jwt='a-token', options=self.low_timeout_options)

        with self.assertRaises(requests.exceptions.Timeout):
            rc.post('https://google.com')

    def test_put_can_timeout(self):
        rc = RestClient(jwt='a-token', options=self.low_timeout_options)

        with self.assertRaises(requests.exceptions.Timeout):
            rc.put('https://google.com')

    def test_patch_can_timeout(self):
        rc = RestClient(jwt='a-token', options=self.low_timeout_options)

        with self.assertRaises(requests.exceptions.Timeout):
            rc.patch('https://google.com')

    def test_delete_can_timeout(self):
        rc = RestClient(jwt='a-token', options=self.low_timeout_options)

        with self.assertRaises(requests.exceptions.Timeout):
            rc.delete('https://google.com')

    @mock.patch('requests.get')
    def test_get_custom_timeout(self, mock_get):
        rc = RestClient(jwt='a-token', options=self.tuple_timeout_options)
        headers = self.static_response_headers | {
            'Authorization': 'Bearer a-token',
        }
        mock_get.return_value.text = '["a", "b"]'
        mock_get.return_value.status_code = 200

        rc.get('the-url')
        mock_get.assert_called_with('the-url', params=None, headers=headers, timeout=(10, 2), verify=True)

    @mock.patch('requests.post')
    def test_post_custom_timeout(self, mock_post):
        rc = RestClient(jwt='a-token', options=self.tuple_timeout_options)
        headers = self.static_response_headers | {
            'Authorization': 'Bearer a-token',
        }
        mock_post.return_value.text = '["a", "b"]'
        mock_post.return_value.status_code = 200

        rc.post('the-url')
        mock_post.assert_called_with('the-url', data='null', headers=headers, timeout=(10, 2), verify=True)

    @mock.patch('requests.put')
    def test_put_custom_timeout(self, mock_put):
        rc = RestClient(jwt='a-token', options=self.tuple_timeout_options)
        headers = self.static_response_headers | {'Authorization': 'Bearer a-token'}

        mock_put.return_value.text = '["a", "b"]'
        mock_put.return_value.status_code = 200

        rc.put('the-url')
        mock_put.assert_called_with('the-url', json=None, headers=headers, timeout=(10, 2), verify=True)

    @mock.patch('requests.patch')
    def test_patch_custom_timeout(self, mock_patch):
        rc = RestClient(jwt='a-token', options=self.tuple_timeout_options)
        headers = self.static_response_headers | {'Authorization': 'Bearer a-token'}

        mock_patch.return_value.text = '["a", "b"]'
        mock_patch.return_value.status_code = 200

        rc.patch('the-url')
        mock_patch.assert_called_with('the-url', json=None, headers=headers, timeout=(10, 2), verify=True)

    @mock.patch('requests.delete')
    def test_delete_custom_timeout(self, mock_delete):
        rc = RestClient(jwt='a-token', options=self.tuple_timeout_options)
        headers = self.static_response_headers | {'Authorization': 'Bearer a-token'}

        mock_delete.return_value.text = '["a", "b"]'
        mock_delete.return_value.status_code = 200

        rc.delete('the-url')
        mock_delete.assert_called_with('the-url', params={}, json=None, headers=headers, timeout=(10, 2), verify=True)

    @mock.patch('requests.get')
    def test_get(self, mock_get):
        rc = RestClient(jwt='a-token')
        headers = self.static_response_headers | {'Authorization': 'Bearer a-token'}

        mock_get.return_value.text = '["a", "b"]'
        mock_get.return_value.status_code = 200

        response = rc.get('the-url')
        mock_get.assert_called_with('the-url', params=None, headers=headers, timeout=self.TIMEOUT_DEF, verify=True)

        self.assertEqual(response, ['a', 'b'])

        response = rc.get(url='the/url', params={'A': 'param', 'B': 'param'})
        mock_get.assert_called_with('the/url', params={'A': 'param',
                                                       'B': 'param'},
                                    headers=headers, timeout=self.TIMEOUT_DEF, verify=True)
        self.assertEqual(response, ['a', 'b'])

        mock_get.return_value.text = ''
        response = rc.get('the/url')
        self.assertEqual(response, '')

    @mock.patch('requests.get')
    def test_get_errors(self, mock_get):
        rc = RestClient(jwt='a-token')

        mock_get.return_value.text = '{"statusCode": 999,' \
                                     ' "errorCode": "code",' \
                                     ' "message": "message"}'
        mock_get.return_value.status_code = 999

        with self.assertRaises(HttpException) as context:
            rc.get('the/url')

        self.assertEqual(context.exception.status_code, 999)
        self.assertEqual(context.exception.code, 'code')
        self.assertEqual(context.exception.message, 'message')

    @mock.patch('requests.get')
    def test_get_rate_limit_error(self, mock_get):
        options = RestClientOptions(retries=0)
        rc = RestClient(jwt='a-token', options=options)
        rc._skip_sleep = True

        mock_get.return_value.text = '{"statusCode": 429,' \
                                     ' "errorCode": "code",' \
                                     ' "message": "message"}'
        mock_get.return_value.status_code = 429
        mock_get.return_value.headers = {
            'x-ratelimit-limit': '3',
            'x-ratelimit-remaining': '6',
            'x-ratelimit-reset': '9',
        }

        with self.assertRaises(HttpException) as context:
            rc.get('the/url')

        self.assertEqual(context.exception.status_code, 429)
        self.assertEqual(context.exception.code, 'code')
        self.assertEqual(context.exception.message, 'message')
        self.assertIsInstance(context.exception, RateLimitException)
        self.assertEqual(context.exception.reset_at, 9)

        self.assertEqual(rc._metrics['retries'], 0)

    @mock.patch('requests.get')
    def test_get_rate_limit_error_without_headers(self, mock_get):
        options = RestClientOptions(retries=1)
        rc = RestClient(jwt='a-token', options=options)

        mock_get.return_value.text = '{"statusCode": 429,' \
                                     ' "errorCode": "code",' \
                                     ' "message": "message"}'
        mock_get.return_value.status_code = 429

        mock_get.return_value.headers = {}
        with self.assertRaises(HttpException) as context:
            rc.get('the/url')

        self.assertEqual(context.exception.status_code, 429)
        self.assertEqual(context.exception.code, 'code')
        self.assertEqual(context.exception.message, 'message')
        self.assertIsInstance(context.exception, RateLimitException)
        self.assertEqual(context.exception.reset_at, -1)

        self.assertEqual(rc._metrics['retries'], 1)

    @mock.patch('requests.get')
    def test_get_rate_limit_custom_retries(self, mock_get):
        options = RestClientOptions(retries=5)
        rc = RestClient(jwt='a-token', options=options)
        rc._skip_sleep = True

        mock_get.return_value.text = '{"statusCode": 429,' \
                                     ' "errorCode": "code",' \
                                     ' "message": "message"}'
        mock_get.return_value.status_code = 429
        mock_get.return_value.headers = {
            'x-ratelimit-limit': '3',
            'x-ratelimit-remaining': '6',
            'x-ratelimit-reset': '9',
        }

        with self.assertRaises(HttpException) as context:
            rc.get('the/url')

        self.assertEqual(context.exception.status_code, 429)
        self.assertEqual(context.exception.code, 'code')
        self.assertEqual(context.exception.message, 'message')
        self.assertIsInstance(context.exception, RateLimitException)
        self.assertEqual(context.exception.reset_at, 9)

        self.assertEqual(rc._metrics['retries'], 5)
        self.assertEqual(rc._metrics['retries'], len(rc._metrics['backoff']))

    @mock.patch('requests.get')
    def test_get_rate_limit_invalid_retries_below_min(self, mock_get):
        options = RestClientOptions(retries=-1)
        rc = RestClient(jwt='a-token', options=options)
        rc._skip_sleep = True

        mock_get.return_value.text = '{"statusCode": 429,' \
                                     ' "errorCode": "code",' \
                                     ' "message": "message"}'
        mock_get.return_value.status_code = 429
        mock_get.return_value.headers = {
            'x-ratelimit-limit': '3',
            'x-ratelimit-remaining': '6',
            'x-ratelimit-reset': '9',
        }

        with self.assertRaises(HttpException) as context:
            rc.get('the/url')

        self.assertEqual(context.exception.status_code, 429)
        self.assertEqual(context.exception.code, 'code')
        self.assertEqual(context.exception.message, 'message')
        self.assertIsInstance(context.exception, RateLimitException)
        self.assertEqual(context.exception.reset_at, 9)

        self.assertEqual(rc._metrics['retries'], 0)

    @mock.patch('requests.get')
    def test_get_rate_limit_retries_use_exponential_backoff(self, mock_get):
        options = RestClientOptions(retries=10)
        rc = RestClient(jwt='a-token', options=options)
        rc._skip_sleep = True

        mock_get.return_value.text = '{"statusCode": 429,' \
                                     ' "errorCode": "code",' \
                                     ' "message": "message"}'
        mock_get.return_value.status_code = 429
        mock_get.return_value.headers = {
            'x-ratelimit-limit': '3',
            'x-ratelimit-remaining': '6',
            'x-ratelimit-reset': '9',
        }

        with self.assertRaises(HttpException) as context:
            rc.get('the/url')

        self.assertEqual(context.exception.status_code, 429)
        self.assertEqual(context.exception.code, 'code')
        self.assertEqual(context.exception.message, 'message')
        self.assertIsInstance(context.exception, RateLimitException)
        self.assertEqual(context.exception.reset_at, 9)

        self.assertEqual(rc._metrics['retries'], 10)
        self.assertEqual(rc._metrics['retries'], len(rc._metrics['backoff']))

        base_backoff = [0]
        base_backoff_sum = 0
        final_backoff = 0

        for i in range(0, 9):
            backoff = 100 * 2 ** i
            base_backoff.append(backoff)
            base_backoff_sum += backoff

        for backoff in rc._metrics['backoff']:
            final_backoff += backoff

        # Assert that exponential backoff is happening.
        self.assertGreaterEqual(rc._metrics['backoff'][1], rc._metrics['backoff'][0])
        self.assertGreaterEqual(rc._metrics['backoff'][2], rc._metrics['backoff'][1])
        self.assertGreaterEqual(rc._metrics['backoff'][3], rc._metrics['backoff'][2])
        self.assertGreaterEqual(rc._metrics['backoff'][4], rc._metrics['backoff'][3])
        self.assertGreaterEqual(rc._metrics['backoff'][5], rc._metrics['backoff'][4])
        self.assertGreaterEqual(rc._metrics['backoff'][6], rc._metrics['backoff'][5])
        self.assertGreaterEqual(rc._metrics['backoff'][7], rc._metrics['backoff'][6])
        self.assertGreaterEqual(rc._metrics['backoff'][8], rc._metrics['backoff'][7])
        self.assertGreaterEqual(rc._metrics['backoff'][9], rc._metrics['backoff'][8])

        # Ensure jitter is being applied.
        self.assertNotEqual(rc._metrics['backoff'][1], base_backoff[1])
        self.assertNotEqual(rc._metrics['backoff'][2], base_backoff[2])
        self.assertNotEqual(rc._metrics['backoff'][3], base_backoff[3])
        self.assertNotEqual(rc._metrics['backoff'][4], base_backoff[4])
        self.assertNotEqual(rc._metrics['backoff'][5], base_backoff[5])
        self.assertNotEqual(rc._metrics['backoff'][6], base_backoff[6])
        self.assertNotEqual(rc._metrics['backoff'][7], base_backoff[7])
        self.assertNotEqual(rc._metrics['backoff'][8], base_backoff[8])
        self.assertNotEqual(rc._metrics['backoff'][9], base_backoff[9])

        # Ensure subsequent delay is never less than the minimum.
        self.assertGreaterEqual(rc._metrics['backoff'][1], rc.MIN_REQUEST_RETRY_DELAY())
        self.assertGreaterEqual(rc._metrics['backoff'][2], rc.MIN_REQUEST_RETRY_DELAY())
        self.assertGreaterEqual(rc._metrics['backoff'][3], rc.MIN_REQUEST_RETRY_DELAY())
        self.assertGreaterEqual(rc._metrics['backoff'][4], rc.MIN_REQUEST_RETRY_DELAY())
        self.assertGreaterEqual(rc._metrics['backoff'][5], rc.MIN_REQUEST_RETRY_DELAY())
        self.assertGreaterEqual(rc._metrics['backoff'][6], rc.MIN_REQUEST_RETRY_DELAY())
        self.assertGreaterEqual(rc._metrics['backoff'][7], rc.MIN_REQUEST_RETRY_DELAY())
        self.assertGreaterEqual(rc._metrics['backoff'][8], rc.MIN_REQUEST_RETRY_DELAY())
        self.assertGreaterEqual(rc._metrics['backoff'][9], rc.MIN_REQUEST_RETRY_DELAY())

        # Ensure delay is never more than the maximum.
        self.assertLessEqual(rc._metrics['backoff'][0], rc.MAX_REQUEST_RETRY_DELAY())
        self.assertLessEqual(rc._metrics['backoff'][1], rc.MAX_REQUEST_RETRY_DELAY())
        self.assertLessEqual(rc._metrics['backoff'][2], rc.MAX_REQUEST_RETRY_DELAY())
        self.assertLessEqual(rc._metrics['backoff'][3], rc.MAX_REQUEST_RETRY_DELAY())
        self.assertLessEqual(rc._metrics['backoff'][4], rc.MAX_REQUEST_RETRY_DELAY())
        self.assertLessEqual(rc._metrics['backoff'][5], rc.MAX_REQUEST_RETRY_DELAY())
        self.assertLessEqual(rc._metrics['backoff'][6], rc.MAX_REQUEST_RETRY_DELAY())
        self.assertLessEqual(rc._metrics['backoff'][7], rc.MAX_REQUEST_RETRY_DELAY())
        self.assertLessEqual(rc._metrics['backoff'][8], rc.MAX_REQUEST_RETRY_DELAY())
        self.assertLessEqual(rc._metrics['backoff'][9], rc.MAX_REQUEST_RETRY_DELAY())

        # Ensure total delay sum is never more than 10s.
        self.assertLessEqual(final_backoff, 10000)

    @mock.patch('requests.post')
    def test_post(self, mock_post):
        rc = RestClient(jwt='a-token')
        headers = self.static_response_headers | {'Authorization': 'Bearer a-token'}

        mock_post.return_value.text = '{"a": "b"}'

        data = {'some': 'data'}
        j_data = '{"some": "data"}'

        mock_post.return_value.status_code = 200
        response = rc.post('the/url', data=data)
        mock_post.assert_called_with('the/url', data=j_data, headers=headers, timeout=self.TIMEOUT_DEF, verify=True)

        self.assertEqual(response, {'a': 'b'})

    @mock.patch('requests.post')
    def test_post_errors(self, mock_post):
        rc = RestClient(jwt='a-token')

        mock_post.return_value.text = '{"statusCode": 999,' \
                                      ' "errorCode": "code",' \
                                      ' "message": "message"}'
        mock_post.return_value.status_code = 999

        with self.assertRaises(HttpException) as context:
            rc.post('the-url')

        self.assertEqual(context.exception.status_code, 999)
        self.assertEqual(context.exception.code, 'code')
        self.assertEqual(context.exception.message, 'message')

    @mock.patch('requests.post')
    def test_post_errors_with_no_message_property(self, mock_post):
        rc = RestClient(jwt='a-token')

        mock_post.return_value.text = json.dumps({
            "statusCode": 999,
            "errorCode": "code",
            "error": "error"
        })
        mock_post.return_value.status_code = 999

        with self.assertRaises(HttpException) as context:
            rc.post('the-url')

        self.assertEqual(context.exception.status_code, 999)
        self.assertEqual(context.exception.code, 'code')
        self.assertEqual(context.exception.message, 'error')

    @mock.patch('requests.post')
    def test_post_errors_with_no_message_or_error_property(self, mock_post):
        rc = RestClient(jwt='a-token')

        mock_post.return_value.text = json.dumps({
            "statusCode": 999,
            "errorCode": "code"
        })
        mock_post.return_value.status_code = 999

        with self.assertRaises(HttpException) as context:
            rc.post('the-url')

        self.assertEqual(context.exception.status_code, 999)
        self.assertEqual(context.exception.code, 'code')
        self.assertEqual(context.exception.message, '')

    @mock.patch('requests.post')
    def test_post_errors_with_message_and_error_property(self, mock_post):
        rc = RestClient(jwt='a-token')

        mock_post.return_value.text = json.dumps({
            "statusCode": 999,
            "errorCode": "code",
            "error": "error",
            "message": "message"
        })
        mock_post.return_value.status_code = 999

        with self.assertRaises(HttpException) as context:
            rc.post('the-url')

        self.assertEqual(context.exception.status_code, 999)
        self.assertEqual(context.exception.code, 'code')
        self.assertEqual(context.exception.message, 'message')

    @mock.patch('requests.post')
    def test_post_error_with_code_property(self, mock_post):
        rc = RestClient(jwt='a-token')

        for error_status in [400, 500, None]:
            mock_post.return_value.status_code = error_status
            mock_post.return_value.text = '{"errorCode": "e0",' \
                                          '"message": "desc"}'

            with self.assertRaises(HttpException) as context:
                rc.post('the-url')

            self.assertEqual(context.exception.status_code, error_status)
            self.assertEqual(context.exception.code, 'e0')
            self.assertEqual(context.exception.message, 'desc')

    @mock.patch('requests.post')
    def test_post_error_with_no_error_code(self, mock_post):
        rc = RestClient(jwt='a-token')

        for error_status in [400, 500, None]:
            mock_post.return_value.status_code = error_status
            mock_post.return_value.text = '{"message": "desc"}'

            with self.assertRaises(HttpException) as context:
                rc.post('the-url')

            self.assertEqual(context.exception.status_code, error_status)
            self.assertEqual(context.exception.code, 'pricecypher.sdk.internal.unknown')
            self.assertEqual(context.exception.message, 'desc')

    @mock.patch('requests.post')
    def test_post_error_with_text_response(self, mock_post):
        rc = RestClient(jwt='a-token')

        for error_status in [400, 500, None]:
            mock_post.return_value.status_code = error_status
            mock_post.return_value.text = 'there has been a terrible error'

            with self.assertRaises(HttpException) as context:
                rc.post('the-url')

            self.assertEqual(context.exception.status_code, error_status)
            self.assertEqual(context.exception.code, 'pricecypher.sdk.internal.unknown')
            self.assertEqual(context.exception.message, 'there has been a terrible error')

    @mock.patch('requests.post')
    def test_post_error_with_no_response_text(self, mock_post):
        rc = RestClient(jwt='a-token')

        for error_status in [400, 500, None]:
            mock_post.return_value.status_code = error_status
            mock_post.return_value.text = None

            with self.assertRaises(HttpException) as context:
                rc.post('the-url')

            self.assertEqual(context.exception.status_code, error_status)
            self.assertEqual(context.exception.code, 'pricecypher.sdk.internal.unknown')
            self.assertEqual(context.exception.message, '')

    @mock.patch('requests.post')
    def test_file_post_content_type_is_none(self, mock_post):
        rc = RestClient(jwt='a-token')
        headers = {'Authorization': 'Bearer a-token', 'Accept': 'application/json'}
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = 'Success'

        data = {'some': 'data'}
        files = [mock.Mock()]

        rc.file_post('the-url', data=data, files=files)

        mock_post.assert_called_once_with('the-url', data=data, files=files, headers=headers, timeout=self.TIMEOUT_DEF,
                                          verify=True)

    @mock.patch('requests.put')
    def test_put(self, mock_put):
        rc = RestClient(jwt='a-token')
        headers = self.static_response_headers | {'Authorization': 'Bearer a-token'}

        mock_put.return_value.text = '["a", "b"]'
        mock_put.return_value.status_code = 200

        data = {'some': 'data'}

        response = rc.put(url='the-url', data=data)
        mock_put.assert_called_with('the-url', json=data, headers=headers, timeout=self.TIMEOUT_DEF, verify=True)

        self.assertEqual(response, ['a', 'b'])

    @mock.patch('requests.put')
    def test_put_errors(self, mock_put):
        rc = RestClient(jwt='a-token')

        mock_put.return_value.text = '{"statusCode": 999,' \
                                     ' "errorCode": "code",' \
                                     ' "message": "message"}'
        mock_put.return_value.status_code = 999

        with self.assertRaises(HttpException) as context:
            rc.put(url='the/url')

        self.assertEqual(context.exception.status_code, 999)
        self.assertEqual(context.exception.code, 'code')
        self.assertEqual(context.exception.message, 'message')

    @mock.patch('requests.patch')
    def test_patch(self, mock_patch):
        rc = RestClient(jwt='a-token')
        headers = self.static_response_headers | {'Authorization': 'Bearer a-token'}

        mock_patch.return_value.text = '["a", "b"]'
        mock_patch.return_value.status_code = 200

        data = {'some': 'data'}

        response = rc.patch(url='the-url', data=data)
        mock_patch.assert_called_with('the-url', json=data, headers=headers, timeout=self.TIMEOUT_DEF, verify=True)

        self.assertEqual(response, ['a', 'b'])

    @mock.patch('requests.patch')
    def test_patch_errors(self, mock_patch):
        rc = RestClient(jwt='a-token')

        mock_patch.return_value.text = '{"statusCode": 999,' \
                                       ' "errorCode": "code",' \
                                       ' "message": "message"}'
        mock_patch.return_value.status_code = 999

        with self.assertRaises(HttpException) as context:
            rc.patch(url='the/url')

        self.assertEqual(context.exception.status_code, 999)
        self.assertEqual(context.exception.code, 'code')
        self.assertEqual(context.exception.message, 'message')

    @mock.patch('requests.delete')
    def test_delete(self, mock_delete):
        rc = RestClient(jwt='a-token')
        headers = self.static_response_headers | {'Authorization': 'Bearer a-token'}

        mock_delete.return_value.text = '["a", "b"]'
        mock_delete.return_value.status_code = 200

        response = rc.delete(url='the-url/ID')
        mock_delete.assert_called_with('the-url/ID', headers=headers, params={}, json=None, timeout=self.TIMEOUT_DEF,
                                       verify=True)

        self.assertEqual(response, ['a', 'b'])

    @mock.patch('requests.delete')
    def test_delete_with_body_and_params(self, mock_del):
        rc = RestClient(jwt='a-token')
        headers = self.static_response_headers | {'Authorization': 'Bearer a-token'}

        mock_del.return_value.text = '["a", "b"]'
        mock_del.return_value.status_code = 200

        data = {'some': 'data'}
        params = {'A': 'param', 'B': 'param'}

        response = rc.delete(url='the-url/ID', params=params, data=data)
        mock_del.assert_called_with('the-url/ID', headers=headers, params=params, json=data, timeout=self.TIMEOUT_DEF,
                                    verify=True)

        self.assertEqual(response, ['a', 'b'])

    @mock.patch('requests.delete')
    def test_delete_errors(self, mock_delete):
        rc = RestClient(jwt='a-token')

        mock_delete.return_value.text = '{"statusCode": 999,' \
                                        ' "errorCode": "code",' \
                                        ' "message": "message"}'
        mock_delete.return_value.status_code = 999

        with self.assertRaises(HttpException) as context:
            rc.delete(url='the-url')

        self.assertEqual(context.exception.status_code, 999)
        self.assertEqual(context.exception.code, 'code')
        self.assertEqual(context.exception.message, 'message')

    def test_disabled_telemetry(self):
        rc = RestClient(jwt='a-token')
        expected_headers = self.static_response_headers | {'Authorization': 'Bearer a-token'}

        self.assertEqual(rc.base_headers, expected_headers)
