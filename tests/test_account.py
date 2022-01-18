#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import podium_api
from podium_api.account import make_account_get
from podium_api.types.account import get_account_from_json
from podium_api.types.token import PodiumToken
from mock import patch, Mock
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode

class TestAccountRequest(unittest.TestCase):

    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {'id': 'test', 'username': 'test_user',
                            'email': "test@test.test",
                            'devices_uri': 'test/devices',
                            'exports_uri': 'test/exports',
                            'streams_uri': 'test/streams',
                            'user_uri': 'test/user',
                            'events_uri': 'test/events'}
        self.field_names = {'id': 'account_id'}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_account_from_json(self):
        self.result = get_account_from_json(self.result_json)
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_params(self, mock_request):
        req = make_account_get(self.token,
                               expand=True,
                               success_callback=self.success_cb)
        self.assertEqual(req._method, "GET")
        self.assertEqual(req.url,
                         "https://podium.live/api/v1/account?expand=True")

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_account(self, mock_request):
        req = make_account_get(self.token,
                               success_callback=self.success_cb)
        self.assertEqual(req._method, "GET")
        self.assertEqual(req.url,
                         "https://podium.live/api/v1/account?expand=False")
        self.assertEqual(req.req_headers['Content-Type'],
                         "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], "application/json")
        #simulate successful request
        req.on_success()(req, {'account': self.result_json})
        self.check_results()


    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_account_get(self.token,
                                   failure_callback=error_cb)
        #simulate calling the requests on_error
        req.on_error()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with('error', {},
                                    {'success_callback': None,
                                     'failure_callback': error_cb,
                                     'progress_callback': None,
                                     'redirect_callback': None})

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_account_get(self.token,
                                   failure_callback=error_cb)
        #simulate calling the requests on_failure
        req.on_failure()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with('failure', {},
                                    {'success_callback': None,
                                     'failure_callback': error_cb,
                                     'progress_callback': None,
                                     'redirect_callback': None})

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_account_get(self.token,
                               redirect_callback=redir_cb)
        #simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        #assert our lambda called the mock correctly
        redir_cb.assert_called_with(req, None,
                                    {'success_callback': None,
                                     'redirect_callback': redir_cb,
                                     'progress_callback': None,
                                     'failure_callback': None})

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_account_get(self.token,
                                   progress_callback=progress_cb)
        #simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        #assert our lambda called the mock correctly
        progress_cb.assert_called_with(0, 10,
                                       {'success_callback': None,
                                        'failure_callback': None,
                                        'progress_callback': progress_cb,
                                        'redirect_callback': None})

    def tearDown(self):
        podium_api.unregister_podium_application()
