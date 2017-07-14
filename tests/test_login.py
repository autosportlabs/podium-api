#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import podium_api
from podium_api.login import make_login_post
from podium_api.types.token import get_token_from_json
from mock import patch, Mock
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode
    
class TestLoginRequest(unittest.TestCase):

    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')

    def success_cb(self, token):
        self.token = token

    @patch('podium_api.async.UrlRequest.run')
    def test_login(self, mock_request):
        req = make_login_post("test", "test1",
                              success_callback=self.success_cb)
        self.assertEqual(req._method, "POST")
        self.assertEqual(req.url, 'https://podium.live/oauth/token')
        self.assertEqual(req.req_body,
                         urlencode({"grant_type": "password",
                                    "username": "test",
                                    "password": "test1"}))
        self.assertEqual(req.req_headers['Content-Type'],
                         "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers['Authorization'],
                         'Basic test_id:test_secret')
        self.assertEqual(req.req_headers['Accept'], "application/json")
        #simlate access token return
        req.on_success()(req, {"access_token": "blah5", "token_type": "blah4",
                               "created_at": 1})
        #check Token object returned in success_cb
        self.assertEqual(self.token.token, "blah5")
        self.assertEqual(self.token.token_type, "blah4")
        self.assertEqual(self.token.created, 1)

    def test_get_token_from_json(self):
        json = {'access_token': 'test_token', 'token_type': 'test_type',
                'created_at': 1}
        token = get_token_from_json(json)
        self.assertEqual(token.token, "test_token")
        self.assertEqual(token.token_type, "test_type")
        self.assertEqual(token.created, 1)

    @patch('podium_api.async.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_login_post("test", "test1",
                              failure_callback=error_cb)
        #simulate calling the requests on_error
        req.on_error()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with('error', {}, 
                                    {'success_callback': None,
                                     'failure_callback': error_cb,
                                     'progress_callback': None,
                                     'redirect_callback': None})

    @patch('podium_api.async.UrlRequest.run')
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_login_post("test", "test1",
                              failure_callback=error_cb)
        #simulate calling the requests on_failure
        req.on_failure()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with('failure', {}, 
                                    {'success_callback': None,
                                     'failure_callback': error_cb,
                                     'progress_callback': None,
                                     'redirect_callback': None})

    @patch('podium_api.async.UrlRequest.run')
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_login_post("test", "test1",
                              redirect_callback=redir_cb)
        #simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        #assert our lambda called the mock correctly
        redir_cb.assert_called_with(req, None, 
                                    {'success_callback': None,
                                     'failure_callback': None,
                                     'progress_callback': None,
                                     'redirect_callback': redir_cb})

    @patch('podium_api.async.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_login_post("test", "test1",
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
