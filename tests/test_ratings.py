#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import podium_api
from podium_api.ratings import (
    make_rating_create, create_rating_redirect_handler,
    )
from podium_api.types.rating import get_rating_from_json
from podium_api.types.redirect import get_redirect_from_json
from podium_api.types.token import PodiumToken
from mock import patch, Mock
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode

class TestRatingCreate(unittest.TestCase):

    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)
        self.result_json = {'location': 'test/rateable_type/ratings',
                            'object_type': 'rating'}
        self.field_names = {}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_redirect_from_json(self):
        self.result = get_redirect_from_json(self.result_json, 'rating')
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_rating_create(self, mock_request):
        req = make_rating_create(self.token, 'rateable_type',
                                1234,
                                2,
                                redirect_callback=self.success_cb)
        self.assertEqual(req._method, 'POST')
        self.assertEqual(req.url, 'https://podium.live/api/v1/rateable_type/1234/ratings')
        self.assertEqual(
            req.req_body,
            urlencode({'rating[rating]': 2}))
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        #simulate response header
        req._resp_headers = self.result_json
        #simulate successful request
        req.on_redirect()(req, {})
        self.check_results()


    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_rating_create(self.token, 'rateable_type',
                                1234,
                                2,
                                failure_callback=error_cb)
        #simulate calling the requests on_error
        req.on_error()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'error', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': create_rating_redirect_handler,
             '_redirect_callback': None}
        )

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_rating_create(self.token, 'rateable_type',
                                1234,
                                2,
                                failure_callback=error_cb)
        #simulate calling the requests on_failure
        req.on_failure()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'failure', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': create_rating_redirect_handler,
             '_redirect_callback': None}
        )

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_success_callback(self, mock_request):
        success_cb = Mock()
        req = make_rating_create(self.token, 'rateable_type',
                                1234,
                                2,
                                success_callback=success_cb)
        #simulate calling the requests on_success
        self.assertEqual(req.on_success, None)

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_rating_create(self.token, 'rateable_type',
                                1234,
                                2,
                                progress_callback=progress_cb)
        # simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(
            0, 10,
           {'success_callback': None,
            'failure_callback': None,
            'progress_callback': progress_cb,
            'redirect_callback': create_rating_redirect_handler,
            '_redirect_callback': None})

    def tearDown(self):
        podium_api.unregister_podium_application()
