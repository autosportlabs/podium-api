#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from mock import Mock, patch

import podium_api
from podium_api.types.token import PodiumToken
from podium_api.types.user import get_user_from_json
from podium_api.users import make_user_get, make_user_update

try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


class TestUserGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {
            "id": "test",
            "URI": "test/users/test",
            "username": "test_user",
            "name": "test_name",
            "description": None,
            "avatar_url": "test/avatar/img.png",
            "links": None,
            "permalink": "test_user_permalink",
            "friendships_uri": "test/friendships",
            "followers_uri": "test/followers",
            "friendship_uri": None,
            "profile_image_url": "test/avatar/img.png",
            "events_uri": "test/events",
            "venues_uri": "test/venues",
        }
        self.field_names = {"id": "user_id", "URI": "uri"}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_account_from_json(self):
        self.result = get_user_from_json(self.result_json)
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_params(self, mock_request):
        req = make_user_get(
            self.token, "https://podium.live/api/v1/users/test", expand=True, success_callback=self.success_cb
        )
        self.assertEqual(req._method, "GET")
        self.assertEqual(req.url, "https://podium.live/api/v1/users/test?expand=True")

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_account(self, mock_request):
        req = make_user_get(self.token, "https://podium.live/api/v1/users/test", success_callback=self.success_cb)
        self.assertEqual(req._method, "GET")
        self.assertEqual(req.url, "https://podium.live/api/v1/users/test?expand=False")
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, {"user": self.result_json})
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_user_get(self.token, "https://podium.live/api/v1/users/test", failure_callback=error_cb)
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
        req = make_user_get(self.token, "https://podium.live/api/v1/users/test", failure_callback=error_cb)
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
        req = make_user_get(self.token, "https://podium.live/api/v1/users/test", redirect_callback=redir_cb)
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
        req = make_user_get(self.token, "https://podium.live/api/v1/users/test", progress_callback=progress_cb)
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


class TestUserUpdate(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_no_params(self, mock_request):
        req = make_user_update(self.token, "https://podium.live/api/v1/users/test")
        self.assertEqual(req.req_body, urlencode({}))
        self.assertEqual(req.url, "https://podium.live/api/v1/users/test")

    def success_cb(self, result, uri):
        self.result = result
        self.uri = uri

    def check_results(self):
        self.assertEqual(self.result, {"message": "Update success"})
        self.assertEqual(self.uri, "https://podium.live/api/v1/users/test")

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_device_update(self, mock_request):
        req = make_user_update(
            self.token, "https://podium.live/api/v1/users/test", name="new_name", success_callback=self.success_cb
        )
        self.assertEqual(req._method, "PUT")
        self.assertEqual(req.req_body, urlencode({"user[name]": "new_name"}))
        self.assertEqual(req.url, "https://podium.live/api/v1/users/test")
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, {"message": "Update success"})
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_user_update(
            self.token, "https://podium.live/api/v1/users/test", name="new_name", failure_callback=error_cb
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
                "updated_uri": "https://podium.live/api/v1/users/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_user_update(
            self.token, "https://podium.live/api/v1/users/test", name="new_name", failure_callback=error_cb
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
                "updated_uri": "https://podium.live/api/v1/users/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_user_update(
            self.token, "https://podium.live/api/v1/users/test", name="new_name", redirect_callback=redir_cb
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
                "updated_uri": "https://podium.live/api/v1/users/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_user_update(
            self.token, "https://podium.live/api/v1/users/test", name="new_title", progress_callback=progress_cb
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
                "updated_uri": "https://podium.live/api/v1/users/test",
            },
        )

    def tearDown(self):
        podium_api.unregister_podium_application()
