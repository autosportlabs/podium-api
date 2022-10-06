#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from mock import Mock, patch

import podium_api
from podium_api.events import (
    create_event_redirect_handler,
    make_event_create,
    make_event_delete,
    make_event_get,
    make_event_update,
    make_events_get,
)
from podium_api.types.event import get_event_from_json
from podium_api.types.redirect import get_redirect_from_json
from podium_api.types.token import PodiumToken

try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


class TestEventsGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {
            "id": "test",
            "URI": "test/events/test",
            "devices_uri": "test/devices",
            "title": "test title",
            "start_time": "test_time",
            "end_time": "test_end",
            "venue_uri": "test/venue",
            "private": False,
        }
        self.paged_event_json = {"total": 1, "events": [self.result_json]}
        self.field_names = {"id": "event_id", "URI": "uri"}

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

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_no_params(self, mock_request):
        req = make_events_get(
            self.token,
            endpoint="https://podium.live/api/v1/events?start=20&per_page=20",
            expand=None,
            success_callback=self.success_cb,
        )
        self.assertEqual(req.url, "https://podium.live/api/v1/events?start=20&per_page=20")

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_events_get(self, mock_request):
        req = make_events_get(self.token, start=0, per_page=100, success_callback=self.success_cb)
        self.assertEqual(req._method, "GET")
        self.assertTrue("https://podium.live/api/v1/events?" in req.url)
        self.assertTrue("per_page=100" in req.url)
        self.assertTrue("start=0" in req.url)
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
        req = make_events_get(self.token, start=0, per_page=100, failure_callback=error_cb)
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
        req = make_events_get(self.token, start=0, per_page=100, failure_callback=error_cb)
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
        req = make_events_get(self.token, start=0, per_page=100, redirect_callback=redir_cb)
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
        req = make_events_get(self.token, start=0, per_page=100, progress_callback=progress_cb)
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


class TestEventCreate(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {"location": "test/events/test1", "object_type": "event"}
        self.field_names = {}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_redirect_from_json(self):
        self.result = get_redirect_from_json(self.result_json, "event")
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_venue_id_option(self, mock_request):
        req = make_event_create(
            self.token, "test", "2016-06-28T00:00:00Z", "2016-06-29T00:00:00Z", venue_id="test_venue"
        )
        self.assertEqual(
            req.req_body,
            urlencode(
                {
                    "event[title]": "test",
                    "event[start_time]": "2016-06-28T00:00:00Z",
                    "event[end_time]": "2016-06-29T00:00:00Z",
                    "event[venue_id]": "test_venue",
                }
            ),
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_event_create(self, mock_request):
        req = make_event_create(
            self.token,
            "test",
            "2016-06-28T00:00:00Z",
            "2016-06-29T00:00:00Z",
            private=True,
            redirect_callback=self.success_cb,
        )
        self.assertEqual(req._method, "POST")
        self.assertEqual(req.url, "https://podium.live/api/v1/events")
        self.assertEqual(
            req.req_body,
            urlencode(
                {
                    "event[title]": "test",
                    "event[start_time]": "2016-06-28T00:00:00Z",
                    "event[end_time]": "2016-06-29T00:00:00Z",
                    "event[private]": "true",
                }
            ),
        )
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
        req = make_event_create(
            self.token, "test", "2016-06-28T00:00:00Z", "2016-06-29T00:00:00Z", failure_callback=error_cb
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
                "redirect_callback": create_event_redirect_handler,
                "_redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_event_create(
            self.token, "test", "2016-06-28T00:00:00Z", "2016-06-29T00:00:00Z", failure_callback=error_cb
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
                "redirect_callback": create_event_redirect_handler,
                "_redirect_callback": None,
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_success_callback(self, mock_request):
        success_cb = Mock()
        req = make_event_create(
            self.token, "test", "2016-06-28T00:00:00Z", "2016-06-29T00:00:00Z", success_callback=success_cb
        )
        # simulate calling the requests on_success
        self.assertEqual(req.on_success, None)

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_event_create(
            self.token, "test", "2016-06-28T00:00:00Z", "2016-06-29T00:00:00Z", progress_callback=progress_cb
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
                "redirect_callback": create_event_redirect_handler,
                "_redirect_callback": None,
            },
        )

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestEventDelete(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)

    def check_results(self):
        self.assertEqual(self.result, "https://podium.live/api/v1/events/test")

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_event_delete(self, mock_request):
        req = make_event_delete(self.token, "https://podium.live/api/v1/events/test", success_callback=self.success_cb)
        self.assertEqual(req._method, "DELETE")
        self.assertEqual(req.url, "https://podium.live/api/v1/events/test")
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, {})
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_event_delete(self.token, "https://podium.live/api/v1/events/test", failure_callback=error_cb)
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
                "deleted_uri": "https://podium.live/api/v1/events/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_event_delete(self.token, "https://podium.live/api/v1/events/test", failure_callback=error_cb)
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
                "deleted_uri": "https://podium.live/api/v1/events/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_event_delete(self.token, "https://podium.live/api/v1/events/test", redirect_callback=redir_cb)
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
                "deleted_uri": "https://podium.live/api/v1/events/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_event_delete(self.token, "https://podium.live/api/v1/events/test", progress_callback=progress_cb)
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
                "deleted_uri": "https://podium.live/api/v1/events/test",
            },
        )

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestEventGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)
        self.result_json = {
            "id": "test",
            "URI": "https://podium.live/api/v1/events/test",
            "devices_uri": "test/devices",
            "title": "test title",
            "start_time": "test_time",
            "end_time": "test_end",
            "venue_uri": "test_venue",
            "private": False,
        }
        self.field_names = {"id": "event_id", "URI": "uri"}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_no_params(self, mock_request):
        req = make_event_get(self.token, "https://podium.live/api/v1/events/test", expand=None)
        self.assertEqual(req.url, "https://podium.live/api/v1/events/test")

    def success_cb(self, result):
        self.result = result

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_event_get(self, mock_request):
        req = make_event_get(self.token, "https://podium.live/api/v1/events/test", success_callback=self.success_cb)
        self.assertEqual(req._method, "GET")
        self.assertEqual(req.url, "https://podium.live/api/v1/events/test?expand=True")
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, {"event": self.result_json})
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_event_get(self.token, "https://podium.live/api/v1/events/test", failure_callback=error_cb)
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
        req = make_event_get(self.token, "https://podium.live/api/v1/events/test", failure_callback=error_cb)
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
        req = make_event_get(self.token, "https://podium.live/api/v1/events/test", redirect_callback=redir_cb)
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
        req = make_event_get(self.token, "https://podium.live/api/v1/events/test", progress_callback=progress_cb)
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


class TestEventUpdate(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.token = PodiumToken("test_token", "test_type", 1)

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_no_params(self, mock_request):
        req = make_event_update(self.token, "https://podium.live/api/v1/events/test")
        self.assertEqual(req.req_body, urlencode({"event[venue_id]": ""}))
        self.assertEqual(req.url, "https://podium.live/api/v1/events/test")

    def success_cb(self, result, uri):
        self.result = result
        self.uri = uri

    def check_results(self):
        self.assertEqual(self.result, {"message": "Update success"})
        self.assertEqual(self.uri, "https://podium.live/api/v1/events/test")

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_event_update(self, mock_request):
        req = make_event_update(
            self.token,
            "https://podium.live/api/v1/events/test",
            title="new_title",
            private=True,
            success_callback=self.success_cb,
        )
        self.assertEqual(req._method, "PUT")
        self.assertEqual(
            req.req_body, urlencode({"event[title]": "new_title", "event[venue_id]": "", "event[private]": "true"})
        )
        self.assertEqual(req.url, "https://podium.live/api/v1/events/test")
        self.assertEqual(req.req_headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(req.req_headers["Authorization"], "Bearer {}".format(self.token.token))
        self.assertEqual(req.req_headers["Accept"], "application/json")
        # simulate successful request
        req.on_success()(req, {"message": "Update success"})
        self.check_results()

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_event_update(
            self.token, "https://podium.live/api/v1/events/test", title="new_title", failure_callback=error_cb
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
                "updated_uri": "https://podium.live/api/v1/events/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_event_update(
            self.token, "https://podium.live/api/v1/events/test", title="new_title", failure_callback=error_cb
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
                "updated_uri": "https://podium.live/api/v1/events/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_event_update(
            self.token, "https://podium.live/api/v1/events/test", title="new_title", redirect_callback=redir_cb
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
                "updated_uri": "https://podium.live/api/v1/events/test",
            },
        )

    @patch("podium_api.asyncreq.UrlRequest.run")
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_event_update(
            self.token, "https://podium.live/api/v1/events/test", title="new_title", progress_callback=progress_cb
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
                "updated_uri": "https://podium.live/api/v1/events/test",
            },
        )

    def tearDown(self):
        podium_api.unregister_podium_application()
