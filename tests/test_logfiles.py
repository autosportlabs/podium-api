#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from mock import Mock, patch

import podium_api
from podium_api.logfiles import (
    create_logfile_redirect_handler,
    make_logfile_create,
    make_logfile_get,
    make_logfile_new,
    make_logfiles_get,
)
from podium_api.types.logfile import get_logfile_from_json
from podium_api.types.redirect import get_redirect_from_json
from podium_api.types.token import PodiumToken

try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


class TestLogfileCreate(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {"location": "test/logfiles/1", "object_type": "logfile"}
        self.field_names = {}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_redirect_from_json(self):
        self.result = get_redirect_from_json(self.result_json, "logfile")
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_logfile_create(self, mock_request):
        req = make_logfile_create(self.token, file_key="12345", eventdevice_id=123, redirect_callback=self.success_cb)
        self.assertEqual(req._method, "POST")
        self.assertEqual(req.url, "https://podium.live/api/v1/logfiles")
        self.assertEqual(req.req_body, urlencode({"logfile[file_key]": "12345", "logfile[eventdevice_id]": 123}))
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate response header
        req._resp_headers = self.result_json
        # simulate successful request
        req.on_redirect()(req, {})
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_logfile_create(self.token, file_key="12345", eventdevice_id=123, failure_callback=error_cb)
        # simulate calling the requests on_error
        req.on_error()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            "error",
            {},
            {
                "success_callback": None,
                "failure_callback": error_cb,
                "progress_callback": None,
                "redirect_callback": create_logfile_redirect_handler,
                "_redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_logfile_create(self.token, file_key="12345", eventdevice_id=123, failure_callback=error_cb)
        # simulate calling the requests on_failure
        req.on_failure()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            "failure",
            {},
            {
                "success_callback": None,
                "failure_callback": error_cb,
                "progress_callback": None,
                "redirect_callback": create_logfile_redirect_handler,
                "_redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_success_callback(self, mock_request):
        success_cb = Mock()
        req = make_logfile_create(self.token, file_key="12345", eventdevice_id=123, success_callback=success_cb)
        # simulate calling the requests on_success
        self.assertEqual(req.on_success, None)

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_logfile_create(self.token, file_key="12345", eventdevice_id=123, progress_callback=progress_cb)
        # simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(
            0,
            10,
            {
                "success_callback": None,
                "failure_callback": None,
                "progress_callback": progress_cb,
                "redirect_callback": create_logfile_redirect_handler,
                "_redirect_callback": None,
            },
        )

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestLogfileNew(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {
            "upload_url": "test/upload/url",
            "file_key": 12345,
            "eventdevice_id": 123,
            "status": -1,
        }
        self.field_names = {
            "upload_url": "upload_url",
            "file_key": "file_key",
            "eventdevice_id": "eventdevice_id",
            "status": "status",
        }

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_logfile_from_json(self):
        self.result = get_logfile_from_json(self.result_json)
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_logfile_new(self, mock_request):
        req = make_logfile_new(
            self.token,
            device_id=1234,
            event_id=5678,
            success_callback=self.success_cb,
        )
        self.assertEqual(req._method, "GET")
        self.assertEqual(req.url, "https://podium.live/api/v1/logfiles/new?device_id=1234&event_id=5678")
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, {"logfile": self.result_json})
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_logfile_new(self.token, device_id=1234, event_id=5678, failure_callback=error_cb)
        # simulate calling the requests on_error
        req.on_error()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            "error",
            {},
            {
                "success_callback": None,
                "failure_callback": error_cb,
                "progress_callback": None,
                "redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_logfile_new(self.token, device_id=1234, event_id=5678, failure_callback=error_cb)
        # simulate calling the requests on_failure
        req.on_failure()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            "failure",
            {},
            {
                "success_callback": None,
                "failure_callback": error_cb,
                "progress_callback": None,
                "redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_logfile_new(self.token, device_id=1234, event_id=5678, redirect_callback=redir_cb)
        # simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        # assert our lambda called the mock correctly
        redir_cb.assert_called_with(
            req,
            None,
            {
                "success_callback": None,
                "failure_callback": None,
                "progress_callback": None,
                "redirect_callback": redir_cb,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_logfile_new(
            self.token,
            device_id=1234,
            event_id=5678,
            progress_callback=progress_cb,
        )
        # simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(
            0,
            10,
            {
                "success_callback": None,
                "failure_callback": None,
                "progress_callback": progress_cb,
                "redirect_callback": None,
            },
        )

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestLogfileGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {
            "id": 111,
            "URI": "https://podium.live/api/v1/logfile/111",
            "file_key": "123456",
            "eventdevice_id": 1234,
            "status": 2,
            "event_id": 333,
            "event_url": "https://podium.live/api/v1/events/222",
            "device_id": 444,
            "device_url": "https://podium.live/api/v1/devices/333",
            "created": "2023-09-04T09:38:18Z",
        }
        self.field_names = {
            "id": "id",
            "URI": "URI",
            "file_key": "file_key",
            "eventdevice_id": "eventdevice_id",
            "status": "status",
            "event_id": "event_id",
            "event_url": "event_url",
            "device_id": "device_id",
            "device_url": "device_url",
            "created": "created",
        }

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_account_from_json(self):
        self.result = get_logfile_from_json(self.result_json)
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_logfile_get(self, mock_request):
        req = make_logfile_get(self.token, "https://podium.live/api/v1/logfiles/test", success_callback=self.success_cb)
        self.assertEqual(req._method, "GET")
        self.assertEqual(req.url, "https://podium.live/api/v1/logfiles/test?expand=True")
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, {"logfile": self.result_json})
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_logfile_get(self.token, "https://podium.live/api/v1/logfiles/111", failure_callback=error_cb)
        # simulate calling the requests on_error
        req.on_error()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            "error",
            {},
            {
                "success_callback": None,
                "failure_callback": error_cb,
                "progress_callback": None,
                "redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_logfile_get(self.token, "https://podium.live/api/v1/logfiles/111", failure_callback=error_cb)
        # simulate calling the requests on_failure
        req.on_failure()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            "failure",
            {},
            {
                "success_callback": None,
                "failure_callback": error_cb,
                "progress_callback": None,
                "redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_logfile_get(self.token, "https://podium.live/api/v1/logfiles/111", redirect_callback=redir_cb)
        # simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        # assert our lambda called the mock correctly
        redir_cb.assert_called_with(
            req,
            None,
            {
                "success_callback": None,
                "failure_callback": None,
                "progress_callback": None,
                "redirect_callback": redir_cb,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_logfile_get(self.token, "https://podium.live/api/v1/logfiles/111", progress_callback=progress_cb)
        # simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(
            0,
            10,
            {
                "success_callback": None,
                "failure_callback": None,
                "progress_callback": progress_cb,
                "redirect_callback": None,
            },
        )

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestLogfilesGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)

        self.result_json = {
            "id": 111,
            "URI": "https://podium.live/api/v1/logfile/111",
            "file_key": "123456",
            "eventdevice_id": 1234,
            "status": 2,
            "event_id": 333,
            "event_url": "https://podium.live/api/v1/events/222",
            "device_id": 444,
            "device_url": "https://podium.live/api/v1/devices/333",
            "created": "2023-09-04T09:38:18Z",
        }
        self.field_names = {
            "id": "id",
            "URI": "URI",
            "file_key": "file_key",
            "eventdevice_id": "eventdevice_id",
            "status": "status",
            "event_id": "event_id",
            "event_url": "event_url",
            "device_id": "device_id",
            "device_url": "device_url",
            "created": "created",
        }

        self.paged_logfile_json = {"total": 1, "logfiles": [self.result_json]}

    def check_results_logfile(self):
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
        self.assertEqual(result.payload_name, "logfiles")
        for logfile in result.logfiles:
            self.result = logfile
            self.check_results_logfile()

    def test_get_logfile_from_json(self):
        self.result = get_logfile_from_json(self.result_json)
        self.check_results_logfile()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_no_params(self, mock_request):
        req = make_logfiles_get(
            self.token,
            expand=None,
            success_callback=self.success_cb,
        )
        self.assertEqual(req.url, "https://podium.live/api/v1/logfiles")

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_logfiles_get(self, mock_request):
        req = make_logfiles_get(self.token, start=0, per_page=100, success_callback=self.success_cb)
        self.assertEqual(req._method, "GET")
        self.assertTrue("https://podium.live/api/v1/logfiles?" in req.url)
        self.assertTrue("per_page=100" in req.url)
        self.assertTrue("start=0" in req.url)
        self.assertTrue("expand=True" in req.url)
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, self.paged_logfile_json)
        self.check_results_paged_response()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_logfiles_get(self.token, start=0, per_page=100, failure_callback=error_cb)
        # simulate calling the requests on_error
        req.on_error()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            "error",
            {},
            {
                "success_callback": None,
                "failure_callback": error_cb,
                "progress_callback": None,
                "redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_logfiles_get(self.token, start=0, per_page=100, failure_callback=error_cb)
        # simulate calling the requests on_failure
        req.on_failure()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            "failure",
            {},
            {
                "success_callback": None,
                "failure_callback": error_cb,
                "progress_callback": None,
                "redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_logfiles_get(self.token, start=0, per_page=100, redirect_callback=redir_cb)
        # simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        # assert our lambda called the mock correctly
        redir_cb.assert_called_with(
            req,
            None,
            {
                "success_callback": None,
                "failure_callback": None,
                "progress_callback": None,
                "redirect_callback": redir_cb,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_logfiles_get(self.token, start=0, per_page=100, progress_callback=progress_cb)
        # simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(
            0,
            10,
            {
                "success_callback": None,
                "failure_callback": None,
                "progress_callback": progress_cb,
                "redirect_callback": None,
            },
        )

    def tearDown(self):
        podium_api.unregister_podium_application()
