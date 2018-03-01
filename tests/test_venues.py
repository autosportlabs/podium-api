#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import podium_api
from podium_api.types.venue import get_venue_from_json
from podium_api.venues import make_venue_get, make_venues_get
from podium_api.types.token import PodiumToken
from mock import patch, Mock
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


class TestVenuesGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)
        self.result_json = {
            'URI': 'test/venues',
            'id': '1234',
        }
        self.paged_event_json = {'total': 1, 'venues': [self.result_json]}
        self.field_names = {'id': 'venue_id', 'URI': 'uri'}

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
        self.assertEqual(result.payload_name, 'venues')
        for venue in result.venues:
            self.result = venue
            self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.async.UrlRequest.run')
    def test_venues_get(self, mock_request):
        req = make_venues_get(
            self.token,
            'test/venues',
            success_callback=self.success_cb
        )
        self.assertEqual(req._method, 'GET')
        self.assertTrue(
            'test/venues' in req.url
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
        req = make_venues_get(
            self.token,
            'test/venues',
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
        req = make_venues_get(
            self.token,
            'test/venues',
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
        req = make_venues_get(
            self.token,
            'test/venues',
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
        req = make_venues_get(
            self.token,
            'test/venues',
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


class TestVenueGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)
        self.result_json = {
            'URI': 'test/venues/1234',
            'id': '1234',
        }
        self.field_names = {'id': 'venue_id', 'URI': 'uri'}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_venue_from_json(self):
        self.result = get_venue_from_json(self.result_json)
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.async.UrlRequest.run')
    def test_venue_get(self, mock_request):
        req = make_venue_get(
            self.token,
            'test/venues/1234',
            success_callback=self.success_cb)
        self.assertEqual(req._method, 'GET')
        self.assertEqual(
            req.url, 'test/venues/1234?expand=True'
        )
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        # simulate successful request
        req.on_success()(req, {'venue': self.result_json})
        self.check_results()

    @patch('podium_api.async.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_venue_get(
            self.token,
            'test/venues/1234',
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
        req = make_venue_get(
            self.token,
            'test/venues/1234',
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
        req = make_venue_get(
            self.token,
            'test/venues/1234',
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
        req = make_venue_get(
            self.token,
            'test/venues/1234',
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

