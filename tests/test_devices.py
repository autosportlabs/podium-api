#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from mock import Mock, patch

import podium_api
from podium_api.devices import (
    create_device_redirect_handler,
    make_device_create,
    make_device_delete,
    make_device_get,
    make_device_update,
)
from podium_api.types.device import get_device_from_json
from podium_api.types.redirect import get_redirect_from_json
from podium_api.types.token import PodiumToken

try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


class TestDeviceCreate(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {"location": "test/devices/test1", "object_type": "device"}
        self.field_names = {}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_redirect_from_json(self):
        self.result = get_redirect_from_json(self.result_json, "device")
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_device_create(self, mock_request):
        req = make_device_create(self.token, "test", True, "avatar.jpg", "avatar_data", redirect_callback=self.success_cb)
        self.assertEqual(req._method, "POST")
        self.assertEqual(req.url, "https://podium.live/api/v1/devices")
        self.assertEqual(req.req_body, urlencode({"device[name]": "test", "device[private]": 1, "device[avatar_name]": "avatar.jpg", "device[avatar_data]": "avatar_data"}))
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
        req = make_device_create(self.token, "test", True, "avatar.jpg", "avatar_data", failure_callback=error_cb)
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
                "redirect_callback": create_device_redirect_handler,
                "_redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_device_create(self.token, "test", True, "avatar.jpg", "avatar_data", failure_callback=error_cb)
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
                "redirect_callback": create_device_redirect_handler,
                "_redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_success_callback(self, mock_request):
        success_cb = Mock()
        req = make_device_create(self.token, "test", True, "avatar.jpg", "avatar_data", success_callback=success_cb)
        # simulate calling the requests on_success
        self.assertEqual(req.on_success, None)

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_device_create(self.token, "test", True, "avatar.jpg", "avatar_data", progress_callback=progress_cb)
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
                "redirect_callback": create_device_redirect_handler,
                "_redirect_callback": None,
            },
        )

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestDeviceDelete(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)

    def check_results(self):
        self.assertEqual(self.result, "https://podium.live/api/v1/devices/test")

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_device_delete(self, mock_request):
        req = make_device_delete(
            self.token, "https://podium.live/api/v1/devices/test", success_callback=self.success_cb
        )
        self.assertEqual(req._method, "DELETE")
        self.assertEqual(req.url, "https://podium.live/api/v1/devices/test")
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, {})
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_device_delete(self.token, "https://podium.live/api/v1/devices/test", failure_callback=error_cb)
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
                "deleted_uri": "https://podium.live/api/v1/devices/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_device_delete(self.token, "https://podium.live/api/v1/devices/test", failure_callback=error_cb)
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
                "deleted_uri": "https://podium.live/api/v1/devices/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_device_delete(self.token, "https://podium.live/api/v1/devices/test", redirect_callback=redir_cb)
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
                "deleted_uri": "https://podium.live/api/v1/devices/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_device_delete(self.token, "https://podium.live/api/v1/devices/test", progress_callback=progress_cb)
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
                "deleted_uri": "https://podium.live/api/v1/devices/test",
            },
        )

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestDeviceGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {
            "id": "test",
            "URI": "https://podium.live/api/v1/devices/test",
            "serial": "test_serial",
            "private": False,
            "name": "test_device",
            "avatar_url": "https://avatar_url/image.jpg",
        }
        self.field_names = {"id": "device_id", "URI": "uri"}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_account_from_json(self):
        self.result = get_device_from_json(self.result_json)
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_device_get(self, mock_request):
        req = make_device_get(self.token, "https://podium.live/api/v1/devices/test", success_callback=self.success_cb)
        self.assertEqual(req._method, "GET")
        self.assertEqual(req.url, "https://podium.live/api/v1/devices/test?expand=True")
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, {"device": self.result_json})
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_device_get(self.token, "https://podium.live/api/v1/devices/test", failure_callback=error_cb)
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
        req = make_device_get(self.token, "https://podium.live/api/v1/devices/test", failure_callback=error_cb)
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
        req = make_device_get(self.token, "https://podium.live/api/v1/devices/test", redirect_callback=redir_cb)
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
        req = make_device_get(self.token, "https://podium.live/api/v1/devices/test", progress_callback=progress_cb)
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


class TestDeviceUpdate(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_no_params(self, mock_request):
        req = make_device_update(self.token, "https://podium.live/api/v1/devices/test")
        self.assertEqual(req.req_body, urlencode({}))
        self.assertEqual(req.url, "https://podium.live/api/v1/devices/test")

    def success_cb(self, result, uri):
        self.result = result
        self.uri = uri

    def check_results(self):
        self.assertEqual(self.result, {"message": "Update success"})
        self.assertEqual(self.uri, "https://podium.live/api/v1/devices/test")

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_device_update(self, mock_request):
        req = make_device_update(
            self.token, "https://podium.live/api/v1/devices/test", name="new_title", success_callback=self.success_cb
        )
        self.assertEqual(req._method, "PUT")
        self.assertEqual(req.req_body, urlencode({"device[name]": "new_title"}))
        self.assertEqual(req.url, "https://podium.live/api/v1/devices/test")
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, {"message": "Update success"})
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_device_update(
            self.token, "https://podium.live/api/v1/devices/test", name="new_title", failure_callback=error_cb
        )
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
                "updated_uri": "https://podium.live/api/v1/devices/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_device_update(
            self.token, "https://podium.live/api/v1/devices/test", name="new_title", failure_callback=error_cb
        )
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
                "updated_uri": "https://podium.live/api/v1/devices/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_device_update(
            self.token, "https://podium.live/api/v1/devices/test", name="new_title", redirect_callback=redir_cb
        )
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
                "updated_uri": "https://podium.live/api/v1/devices/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_device_update(
            self.token, "https://podium.live/api/v1/devices/test", name="new_title", progress_callback=progress_cb
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
                "updated_uri": "https://podium.live/api/v1/devices/test",
            },
        )

    def tearDown(self):
        podium_api.unregister_podium_application()
