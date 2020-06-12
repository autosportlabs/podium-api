#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import podium_api
from podium_api.racestat import (
    make_racestat_create, create_racestat_redirect_handler,
    make_alertmessage_get
    )
from podium_api.types.redirect import get_redirect_from_json
from podium_api.types.alertmessage import get_racestat_from_json
from podium_api.types.token import PodiumToken
from mock import patch, Mock
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


class TestRacestatCreate(unittest.TestCase):

    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)
        self.result_json = {'location': 'test/racestat/1',
                            'object_type': 'racestat'}
        self.field_names = {}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_redirect_from_json(self):
        self.result = get_redirect_from_json(self.result_json, 'racestat')
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.async.UrlRequest.run')
    def test_racestat_create(self, mock_request):
        req = make_racestat_create(token=self.token, event_id=1, device_id=2, message='pit now', priority=1,
                                     redirect_callback=self.success_cb)
        self.assertEqual(req._method, 'POST')
        self.assertEqual(req.url, 'https://podium.live/api/v1/events/1/devices/2/racestat')
        self.assertEqual(
            req.req_body,
            urlencode({'racestat[comp_number]': '1234', 'racestat[comp_class]': 'P1',
                       'racestat[total_laps]': 10, 'racestat[last_lap_time]': 1.234,
                       'racestat[position_overall]': 3, 'racestat[position_in_class]': 2,
                       'racestat[comp_number_ahead]': '456', 'racestat[comp_number_behind]': '789',
                       'racestat[gap_to_ahead]': 11.11, 'racestat[gap_to_behind]': 22.22,
                       'racestat[laps_to_ahead]': 11, 'racestat[laps_to_behind]': 22,
                        })
            )
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        # simulate response header
        req._resp_headers = self.result_json
        # simulate successful request
        req.on_redirect()(req, {})
        self.check_results()

    @patch('podium_api.async.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_alertmessage_create(token=self.token, event_id=1, device_id=2, message='pit now', priority=1,
                                     failure_callback=error_cb)
        # simulate calling the requests on_error
        req.on_error()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'error', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': create_alertmessage_redirect_handler,
             '_redirect_callback': None}
        )

    @patch('podium_api.async.UrlRequest.run')
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_alertmessage_create(token=self.token, event_id=1, device_id=2, message='pit now', priority=1,
                                     failure_callback=error_cb)
        # simulate calling the requests on_failure
        req.on_failure()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'failure', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': create_alertmessage_redirect_handler,
             '_redirect_callback': None}
        )

    @patch('podium_api.async.UrlRequest.run')
    def test_success_callback(self, mock_request):
        success_cb = Mock()
        req = make_alertmessage_create(token=self.token, event_id=1, device_id=2, message='pit now', priority=1,
                                     success_callback=success_cb)
        # simulate calling the requests on_success
        self.assertEqual(req.on_success, None)

    @patch('podium_api.async.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_alertmessage_create(token=self.token, event_id=1, device_id=2, message='pit now', priority=1,
                                     progress_callback=progress_cb)
        # simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(
            0, 10,
           {'success_callback': None,
            'failure_callback': None,
            'progress_callback': progress_cb,
            'redirect_callback': create_alertmessage_redirect_handler,
            '_redirect_callback': None})

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestAlertmessagesGet(unittest.TestCase):

    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)
        self.result_json = {
            'id': '11',
            'URI': 'test/alertmessage_uri',
            'send_time': '2018-09-18T10:35:25Z',
            'ack_time': "2018-10-18T10:35:25Z",
            'message': 'pit nao',
            'priority': '1',
            'sender_id': '12',
            'eventdevice_uri': 'test/eventdevice_uri',
            'device_uri': 'test/device_uri',
            'user_uri':'test/user_uri'
            }
        self.paged_event_json = {'total': 1, 'alertmessages': [self.result_json]}
        self.field_names = {'id': 'alertmessage_id', 'URI': 'uri'}

    def check_results_alertmessage(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def check_results_paged_response(self):
        result = self.result
        self.assertEqual(result.total, 1)
        self.assertEqual(result.next_uri, None)
        self.assertEqual(result.prev_uri, None)
        self.assertEqual(result.payload_name, 'alertmessages')
        for user in result.alertmessages:
            self.result = user
            self.check_results_alertmessage()

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.async.UrlRequest.run')
    def test_alertmessages_get(self, mock_request):
        req = make_alertmessages_get(
            token=self.token,
            endpoint='https://podium.live/api/v1/events/3/devices/3/alertmessages',
            success_callback=self.success_cb
            )
        self.assertEqual(req._method, 'GET')
        self.assertTrue(
            'https://podium.live/api/v1/events/3/devices/3/alertmessages' in req.url
            )
        self.assertTrue('expand=True' in req.url)
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        # simulate successful request
        req.on_success()(req, self.paged_event_json)
        self.check_results_paged_response()

    @patch('podium_api.async.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_alertmessages_get(
            token=self.token,
            endpoint='https://podium.live/api/v1/events/3/devices/3/alertmessages',
            failure_callback=error_cb
            )
        # simulate calling the requests on_error
        req.on_error()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with('error', {},
                                    {'success_callback': None,
                                     'failure_callback': error_cb,
                                     'progress_callback': None,
                                     'redirect_callback': None})

    @patch('podium_api.async.UrlRequest.run')
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_alertmessages_get(
            token=self.token,
            endpoint='https://podium.live/api/v1/events/3/devices/3/alertmessages',
            failure_callback=error_cb
            )
        # simulate calling the requests on_failure
        req.on_failure()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with('failure', {},
                                    {'success_callback': None,
                                     'failure_callback': error_cb,
                                     'progress_callback': None,
                                     'redirect_callback': None})

    @patch('podium_api.async.UrlRequest.run')
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_alertmessages_get(
            token=self.token,
            endpoint='https://podium.live/api/v1/events/3/devices/3/alertmessages',
            redirect_callback=redir_cb
            )
        # simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        # assert our lambda called the mock correctly
        redir_cb.assert_called_with(req, None,
                                    {'success_callback': None,
                                     'failure_callback': None,
                                     'progress_callback': None,
                                     'redirect_callback': redir_cb})

    @patch('podium_api.async.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_alertmessages_get(
            token=self.token,
            endpoint='https://podium.live/api/v1/events/3/devices/3/alertmessages',
            progress_callback=progress_cb
            )
        # simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(0, 10,
                                       {'success_callback': None,
                                        'failure_callback': None,
                                        'progress_callback': progress_cb,
                                        'redirect_callback': None})

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestAlertmessageGet(unittest.TestCase):

    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)
        self.result_json = {
            'id': '11',
            'URI': 'test/alertmessage_uri',
            'send_time': '2018-09-18T10:35:25Z',
            'ack_time': "2018-10-18T10:35:25Z",
            'message': 'pit nao',
            'priority': '1',
            'sender_id': '12',
            'eventdevice_uri': 'test/eventdevice_uri',
            'device_uri': 'test/device_uri',
            'user_uri':'test/user_uri'
            }

        self.field_names = {'id': 'alertmessage_id', 'URI':'uri'}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_alertmessage_from_json(self):
        self.result = get_alertmessage_from_json(self.result_json)
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.async.UrlRequest.run')
    def test_alertmessage_get(self, mock_request):
        req = make_alertmessage_get(
            self.token,
            'http://localhost:3000/api/v1/events/3/devices/3/alertmessages/8',
            success_callback=self.success_cb)
        self.assertEqual(req._method, 'GET')
        self.assertEqual(
            req.url, 'http://localhost:3000/api/v1/events/3/devices/3/alertmessages/8?expand=True'
            )
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        # simulate successful request
        req.on_success()(req, {'alertmessage': self.result_json})
        self.check_results()

    @patch('podium_api.async.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_alertmessage_get(
            self.token,
            'http://localhost:3000/api/v1/events/3/devices/3/alertmessages/8',
            failure_callback=error_cb
            )
        # simulate calling the requests on_error
        req.on_error()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with('error', {},
                                    {'success_callback': None,
                                     'failure_callback': error_cb,
                                     'progress_callback': None,
                                     'redirect_callback': None})

    @patch('podium_api.async.UrlRequest.run')
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_alertmessage_get(
            self.token,
            'http://localhost:3000/api/v1/events/3/devices/3/alertmessages/8',
            failure_callback=error_cb
            )
        # simulate calling the requests on_failure
        req.on_failure()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with('failure', {},
                                    {'success_callback': None,
                                     'failure_callback': error_cb,
                                     'progress_callback': None,
                                     'redirect_callback': None})

    @patch('podium_api.async.UrlRequest.run')
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_alertmessage_get(
            self.token,
            'http://localhost:3000/api/v1/events/3/devices/3/alertmessages/8',
            redirect_callback=redir_cb
            )
        # simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        # assert our lambda called the mock correctly
        redir_cb.assert_called_with(req, None,
                                    {'success_callback': None,
                                     'failure_callback': None,
                                     'progress_callback': None,
                                     'redirect_callback': redir_cb})

    @patch('podium_api.async.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_alertmessage_get(
            self.token,
            'http://localhost:3000/api/v1/events/3/devices/3/alertmessages/8',
            progress_callback=progress_cb
            )
        # simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(0, 10,
                                       {'success_callback': None,
                                        'failure_callback': None,
                                        'progress_callback': progress_cb,
                                        'redirect_callback': None})

    def tearDown(self):
        podium_api.unregister_podium_application()
