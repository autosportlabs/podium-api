#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from mock import Mock, patch

import podium_api
from podium_api.friendships import (
    create_friendship_redirect_handler,
    make_friendship_create,
    make_friendship_delete,
    make_friendship_get,
    make_friendships_get,
)
from podium_api.types.friendship import get_friendship_from_json
from podium_api.types.redirect import get_redirect_from_json
from podium_api.types.token import PodiumToken

try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


class TestFriendshipCreate(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {"location": "test/friendships/1", "object_type": "friendship"}
        self.field_names = {}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_redirect_from_json(self):
        self.result = get_redirect_from_json(self.result_json, "friendship")
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_friendship_create(self, mock_request):
        req = make_friendship_create(self.token, 1, redirect_callback=self.success_cb)
        self.assertEqual(req._method, "POST")
        self.assertEqual(req.url, "https://podium.live/api/v1/friendships")
        self.assertEqual(req.req_body, urlencode({"friendship[user_id]": "1"}))
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
        req = make_friendship_create(self.token, 1, failure_callback=error_cb)
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
                "redirect_callback": create_friendship_redirect_handler,
                "_redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_friendship_create(self.token, 1, failure_callback=error_cb)
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
                "redirect_callback": create_friendship_redirect_handler,
                "_redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_success_callback(self, mock_request):
        success_cb = Mock()
        req = make_friendship_create(self.token, 1, success_callback=success_cb)
        # simulate calling the requests on_success
        self.assertEqual(req.on_success, None)

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_friendship_create(self.token, 1, progress_callback=progress_cb)
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
                "redirect_callback": create_friendship_redirect_handler,
                "_redirect_callback": None,
            },
        )

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestFriendshipDelete(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)

    def check_results(self):
        self.assertEqual(self.result, "https://podium.live/api/v1/friendships/1")

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_friendship_delete(self, mock_request):
        req = make_friendship_delete(
            self.token, "https://podium.live/api/v1/friendships/1", success_callback=self.success_cb
        )
        self.assertEqual(req._method, "DELETE")
        self.assertEqual(req.url, "https://podium.live/api/v1/friendships/1")
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, {})
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_friendship_delete(self.token, "https://podium.live/api/v1/friendships/1", failure_callback=error_cb)
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
                "deleted_uri": "https://podium.live/api/v1/friendships/1",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_friendship_delete(self.token, "https://podium.live/api/v1/friendships/1", failure_callback=error_cb)
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
                "deleted_uri": "https://podium.live/api/v1/friendships/1",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_friendship_delete(self.token, "https://podium.live/api/v1/friendships/1", redirect_callback=redir_cb)
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
                "deleted_uri": "https://podium.live/api/v1/friendships/1",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_friendship_delete(
            self.token, "https://podium.live/api/v1/friendships/1", progress_callback=progress_cb
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
                "deleted_uri": "https://podium.live/api/v1/friendships/1",
            },
        )

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestFriendshipsGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {
            "id": "test",
            "URI": "test/users/test",
            "username": "test_user",
            "description": None,
            "avatar_url": "test/avatar/img.png",
            "links": None,
            "friendships_uri": "test/friendships",
            "followers_uri": "test/followers",
            "friendship_uri": "https://podium.live/api/v1/friendships/1",
            "profile_image_url": "test/avatar/img.png",
            "events_uri": "test/events",
            "venues_uri": "test/venues",
        }
        self.paged_event_json = {"total": 1, "users": [self.result_json]}
        self.field_names = {"id": "user_id", "URI": "uri"}

    def check_results_user(self):
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
        self.assertEqual(result.payload_name, "users")
        for user in result.users:
            self.result = user
            self.check_results_user()

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_friendships_get(self, mock_request):
        req = make_friendships_get(
            self.token, "https://podium.live/api/v1/user/friendships", success_callback=self.success_cb
        )
        self.assertEqual(req._method, "GET")
        self.assertTrue("https://podium.live/api/v1/user/friendships" in req.url)
        self.assertTrue("expand=True" in req.url)
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, self.paged_event_json)
        self.check_results_paged_response()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_friendships_get(self.token, "https://podium.live/api/v1/user/friendships", failure_callback=error_cb)
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
        req = make_friendships_get(self.token, "https://podium.live/api/v1/user/friendships", failure_callback=error_cb)
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
        req = make_friendships_get(
            self.token, "https://podium.live/api/v1/user/friendships", redirect_callback=redir_cb
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
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_friendships_get(
            self.token, "https://podium.live/api/v1/user/friendships", progress_callback=progress_cb
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


class TestFriendshipGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {
            "id": 1,
            "user_uri": "test/user/user_uri",
            "user_id": 2,
            "friend_id": 3,
            "friend_uri": "test/user/friend_uri",
        }
        self.field_names = {"id": "friendship_id"}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_account_from_json(self):
        self.result = get_friendship_from_json(self.result_json)
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_friendship_get(self, mock_request):
        req = make_friendship_get(
            self.token, "https://podium.live/api/v1/friendships/test", success_callback=self.success_cb
        )
        self.assertEqual(req._method, "GET")
        self.assertEqual(req.url, "https://podium.live/api/v1/friendships/test?expand=True")
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, {"friendship": self.result_json})
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_friendship_get(self.token, "https://podium.live/api/v1/friendships/test", failure_callback=error_cb)
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
        req = make_friendship_get(self.token, "https://podium.live/api/v1/friendships/test", failure_callback=error_cb)
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
        req = make_friendship_get(self.token, "https://podium.live/api/v1/friendships/test", redirect_callback=redir_cb)
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
        req = make_friendship_get(
            self.token, "https://podium.live/api/v1/friendships/test", progress_callback=progress_cb
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
