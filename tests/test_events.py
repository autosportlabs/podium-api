#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import podium_api
from podium_api.events import make_events_get
from podium_api.types.event import get_event_from_json
from podium_api.types.token import PodiumToken
from unittest.mock import patch, Mock
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode
    
class TestAccountRequest(unittest.TestCase):

    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {'id': 'test',
                            'URI': 'test/events/test',
                            'devices_uri': 'test/devices',
                            'title': 'test title',
                            'start_time': 'test_time',
                            'end_time': 'test_end',
                            'venue_uri': "test/venue",
                            'private': False,
                            }
        self.paged_event_json = {"total": 1, 'events': [self.result_json]}
        self.field_names = {'id': 'event_id', 'URI': 'uri'}

    def check_results_event(self):
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
        self.assertEqual(result.payload_name, "events")
        for event in result.events:
            self.result = event
            self.check_results_event()

    def test_get_account_from_json(self):
        self.result = get_event_from_json(self.result_json)
        self.check_results_event()

    @patch('podium_api.async.UrlRequest.run')
    def test_no_params(self, mock_request):
        req = make_events_get(
            self.token,
            endpoint='https://podium.live/api/v1/events?start=20&per_page=20',
            success_callback=self.success_cb)
        self.assertEqual(
            req.url, 'https://podium.live/api/v1/events?start=20&per_page=20')
        
    def success_cb(self, result):
        self.result = result

    @patch('podium_api.async.UrlRequest.run')
    def test_account(self, mock_request):
        req = make_events_get(self.token, start=0, per_page=100,
                              success_callback=self.success_cb)
        self.assertEqual(req._method, "GET")
        self.assertTrue('https://podium.live/api/v1/events?' in req.url)
        self.assertTrue('per_page=100' in req.url)
        self.assertTrue('start=0' in req.url)
        self.assertTrue('expand=False' in req.url)
        self.assertEqual(req.req_headers['Content-Type'],
                         "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], "application/json")
        #simulate successful request
        req.on_success()(req, self.paged_event_json)
        self.check_results_paged_response()


    @patch('podium_api.async.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_events_get(self.token, start=0, per_page=100,
                              failure_callback=error_cb)
        #simulate calling the requests on_error
        req.on_error()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with('error', {}, 
                                    {'success_callback': None,
                                     'failure_callback': error_cb,
                                     'progress_callback': None})

    @patch('podium_api.async.UrlRequest.run')
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_events_get(self.token, start=0, per_page=100,
                              failure_callback=error_cb)
        #simulate calling the requests on_failure
        req.on_failure()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with('failure', {}, 
                                    {'success_callback': None,
                                     'failure_callback': error_cb,
                                     'progress_callback': None})

    @patch('podium_api.async.UrlRequest.run')
    def test_redirect_callback(self, mock_request):
        error_cb = Mock()
        req = make_events_get(self.token, start=0, per_page=100,
                              failure_callback=error_cb)
        #simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with('redirect', {}, 
                                    {'success_callback': None,
                                     'failure_callback': error_cb,
                                     'progress_callback': None})

    @patch('podium_api.async.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_events_get(self.token, start=0, per_page=100,
                              progress_callback=progress_cb)
        #simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        #assert our lambda called the mock correctly
        progress_cb.assert_called_with(0, 10, 
                                       {'success_callback': None,
                                        'failure_callback': None,
                                        'progress_callback': progress_cb})

    def tearDown(self):
        podium_api.unregister_podium_application()
