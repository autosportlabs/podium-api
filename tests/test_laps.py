#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import podium_api
from podium_api.types.lap import get_lap_from_json
from podium_api.laps import make_lap_get, make_laps_get
from podium_api.types.token import PodiumToken
from mock import patch, Mock
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


class TestLapsGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)
        self.result_json = {
            'URI': 'test/events/test1/devices/test2/laps',
            'raw_data_uri': 'test/raw/data/uri',
            'lap_number': '1',
            'end_time': 'testtime',
            'aggregates': ['test'],
            'lap_time': 2.5,
        }
        self.paged_event_json = {'total': 1, 'laps': [self.result_json]}
        self.field_names = {'URI': 'uri'}

    def check_results(self):
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
        self.assertEqual(result.payload_name, 'laps')
        for lap in result.laps:
            self.result = lap
            self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.async.UrlRequest.run')
    def test_laps_get(self, mock_request):
        req = make_laps_get(
            self.token,
            'test/events/test1/devices/test2/laps',
            success_callback=self.success_cb
        )
        self.assertEqual(req._method, 'GET')
        self.assertTrue(
            'test/events/test1/devices/test2/laps' in req.url
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
        req = make_laps_get(
            self.token,
            'test/events/test1/devices/test2/laps',
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
        req = make_laps_get(
            self.token,
            'test/events/test1/devices/test2/laps',
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
        req = make_laps_get(
            self.token,
            'test/events/test1/devices/test2/laps',
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
        req = make_laps_get(
            self.token,
            'test/events/test1/devices/test2/laps',
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


class TestFriendshipGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)
        self.result_json = {
            'URI': 'test/events/test1/devices/test2/laps/1',
            'raw_data_uri': 'test/raw/data/uri',
            'lap_number': '1',
            'end_time': 'testtime',
            'aggregates': ['test'],
            'lap_time': 2.5,
        }
        self.field_names = {'URI': 'uri'}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_account_from_json(self):
        self.result = get_lap_from_json(self.result_json)
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.async.UrlRequest.run')
    def test_lap_get(self, mock_request):
        req = make_lap_get(
            self.token,
            'test/events/test1/devices/test2/laps/1',
            success_callback=self.success_cb)
        self.assertEqual(req._method, 'GET')
        self.assertEqual(
            req.url, 'test/events/test1/devices/test2/laps/1?expand=True'
        )
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        # simulate successful request
        req.on_success()(req, {'lap': self.result_json})
        self.check_results()

    @patch('podium_api.async.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_lap_get(
            self.token,
            'test/events/test1/devices/test2/laps/1',
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
        req = make_lap_get(
            self.token,
            'test/events/test1/devices/test2/laps/1',
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
        req = make_lap_get(
            self.token,
            'test/events/test1/devices/test2/laps/1',
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
        req = make_lap_get(
            self.token,
            'test/events/test1/devices/test2/laps/1',
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

