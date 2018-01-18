#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import podium_api
from podium_api.eventdevices import (
    make_eventdevice_create, create_eventdevice_redirect_handler,
    make_eventdevices_get, make_eventdevice_delete, make_eventdevice_get,
    make_livestreams_get, make_eventdevice_update)
from podium_api.types.eventdevice import get_eventdevice_from_json
from podium_api.types.redirect import get_redirect_from_json
from podium_api.types.token import PodiumToken
from mock import patch, Mock

try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


class TestEventDeviceCreate(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)
        self.result_json = {
            'location': 'https://podium.live/api/v1/events/'
                        'test_event/devices/test_device',
            'object_type': 'eventdevice'
        }
        self.field_names = {}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_redirect_from_json(self):
        self.result = get_redirect_from_json(self.result_json, 'eventdevice')
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.async.UrlRequest.run')
    def test_eventdevice_create(self, mock_request):
        req = make_eventdevice_create(self.token, 'test_event',
                                      'test_device', "test name",
                                      redirect_callback=self.success_cb)
        self.assertEqual(req._method, 'POST')
        self.assertEqual(req.url,
                         'https://podium.live/api/v1/events/test_event/devices')
        self.assertEqual(
            req.req_body,
            urlencode({'eventdevice[device_id]': 'test_device',
                       'eventdevice[name]': 'test name'})
        )
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        # simulate response header
        req._resp_headers = self.result_json
        # simulate successful request
        req.on_redirect()(req, {})
        self.check_results()

    @patch('podium_api.async.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_eventdevice_create(self.token, 'test_event',
                                      'test_device', "test name",
                                      failure_callback=error_cb)
        # simulate calling the requests on_error
        req.on_error()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'error', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': create_eventdevice_redirect_handler,
             '_redirect_callback': None}
        )

    @patch('podium_api.async.UrlRequest.run')
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_eventdevice_create(self.token, 'test_event',
                                      'test_device', "test name",
                                      failure_callback=error_cb)
        # simulate calling the requests on_failure
        req.on_failure()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'failure', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': create_eventdevice_redirect_handler,
             '_redirect_callback': None}
        )

    @patch('podium_api.async.UrlRequest.run')
    def test_success_callback(self, mock_request):
        success_cb = Mock()
        req = make_eventdevice_create(self.token, 'test_event',
                                      'test_device', "test name",
                                      success_callback=success_cb)
        # simulate calling the requests on_success
        self.assertEqual(req.on_success, None)

    @patch('podium_api.async.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_eventdevice_create(self.token, 'test_event',
                                      'test_device', "test name",
                                      progress_callback=progress_cb)
        # simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(
            0, 10,
            {'success_callback': None,
             'failure_callback': None,
             'progress_callback': progress_cb,
             'redirect_callback': create_eventdevice_redirect_handler,
             '_redirect_callback': None})

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestEventDevicesGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)
        self.result_json = {
            'id': 'test_event_id',
            'URI': 'https://podium.live/api/v1/events/'
                   'test_event/devices/test_device',
            'device_uri': 'https://podium.live/api/v1/devices/test_device',
            'name': 'test name',
            'laps_uri': 'test/laps',
            'user_uri': 'test/user',
            'event_uri': 'test/event',
            'channels': [],
            }
        self.paged_event_json = {'total': 1, 'eventdevices': [self.result_json]}
        self.field_names = {'id': 'eventdevice_id', 'URI': 'uri'}

    def check_results_individual(self):
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
        self.assertEqual(result.payload_name, 'eventdevices')
        for eventdevice in result.eventdevices:
            self.result = eventdevice
            self.check_results_individual()

    def test_get_eventdevice_from_json(self):
        self.result = get_eventdevice_from_json(self.result_json)
        self.check_results_individual()

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.async.UrlRequest.run')
    def test_events_get(self, mock_request):
        req = make_eventdevices_get(self.token, event_id="test_event",
                                    per_page=100, start=0,
                                    success_callback=self.success_cb)
        self.assertEqual(req._method, 'GET')
        self.assertTrue(
            'https://podium.live/api/v1/events/test_event/devices' in req.url
        )
        self.assertTrue('per_page=100' in req.url)
        self.assertTrue('start=0' in req.url)
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
    def test_livestreams_get(self, mock_request):
        req = make_livestreams_get(self.token,
                                    per_page=100, start=0,
                                    success_callback=self.success_cb)
        self.assertEqual(req._method, 'GET')
        self.assertTrue(
            'https://podium.live/api/v1/livestreams' in req.url
        )
        self.assertTrue('per_page=100' in req.url)
        self.assertTrue('start=0' in req.url)
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
        req = make_eventdevices_get(self.token, event_id="test_event",
                                    per_page=100, start=0,
                                    failure_callback=error_cb)
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
        req = make_eventdevices_get(self.token, event_id="test_event",
                                    per_page=100, start=0,
                                    failure_callback=error_cb)
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
        req = make_eventdevices_get(self.token, event_id="test_event",
                                    per_page=100, start=0,
                                    redirect_callback=redir_cb)
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
        req = make_eventdevices_get(self.token, event_id="test_event",
                                    per_page=100, start=0,
                                    progress_callback=progress_cb)
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


class TestEventDeviceDelete(unittest.TestCase):

    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)

    def check_results(self):
        self.assertEqual(
            self.result,
            'https://podium.live/api/v1/events/test_event/devices/test_device'
        )

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.async.UrlRequest.run')
    def test_event_delete(self, mock_request):
        req = make_eventdevice_delete(
            self.token,
            'https://podium.live/api/v1/events/test_event/devices/test_device',
            success_callback=self.success_cb
        )
        self.assertEqual(req._method, 'DELETE')
        self.assertEqual(
            req.url,
            'https://podium.live/api/v1/events/test_event/devices/test_device'
        )
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        # simulate successful request
        req.on_success()(req, {})
        self.check_results()

    @patch('podium_api.async.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_eventdevice_delete(
            self.token,
            'https://podium.live/api/v1/events/test_event/devices/test_device',
            failure_callback=error_cb
        )
        # simulate calling the requests on_error
        req.on_error()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'error', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': None,
             'deleted_uri': 'https://podium.live/api/v1/events/'
                            'test_event/devices/test_device'}
        )

    @patch('podium_api.async.UrlRequest.run')
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_eventdevice_delete(
            self.token,
            'https://podium.live/api/v1/events/test_event/devices/test_device',
            failure_callback=error_cb
        )
        # simulate calling the requests on_failure
        req.on_failure()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'failure', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': None,
             'deleted_uri': 'https://podium.live/api/v1/events/'
                            'test_event/devices/test_device'}
        )

    @patch('podium_api.async.UrlRequest.run')
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_eventdevice_delete(
            self.token,
            'https://podium.live/api/v1/events/test_event/devices/test_device',
            redirect_callback=redir_cb
        )
        # simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        # assert our lambda called the mock correctly
        redir_cb.assert_called_with(
            req, None,
            {'success_callback': None,
             'failure_callback': None,
             'progress_callback': None,
             'redirect_callback': redir_cb,
             'deleted_uri': 'https://podium.live/api/v1/events/'
                            'test_event/devices/test_device'}
        )

    @patch('podium_api.async.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_eventdevice_delete(
            self.token,
            'https://podium.live/api/v1/events/test_event/devices/test_device',
            progress_callback=progress_cb
        )
        # simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(
            0, 10,
            {'success_callback': None,
             'failure_callback': None,
             'progress_callback': progress_cb,
             'redirect_callback': None,
             'deleted_uri': 'https://podium.live/api/v1/events/'
                            'test_event/devices/test_device'}
        )

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestEventDeviceGet(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)
        self.result_json = {
            'id': 'test_event_id',
            'URI': 'https://podium.live/api/v1/events/'
                   'test_event/devices/test_device',
            'device_uri': 'https://podium.live/api/v1/devices/test_device',
            'name': 'test name',
            'laps_uri': 'test/laps',
            'channels': [],
        }
        self.field_names = {'id': 'eventdevice_id', 'URI': 'uri'}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.async.UrlRequest.run')
    def test_event_get(self, mock_request):
        req = make_eventdevice_get(self.token,
                                   'https://podium.live/api/v1/events/'
                                   'test_event/devices/test_device',
                                   success_callback=self.success_cb)
        self.assertEqual(req._method, 'GET')
        self.assertEqual(req.url,
                         'https://podium.live/api/v1/events/'
                         'test_event/devices/test_device?expand=True')
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        # simulate successful request
        req.on_success()(req, {'eventdevice': self.result_json})
        self.check_results()

    @patch('podium_api.async.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_eventdevice_get(self.token,
                                   'https://podium.live/api/v1/events/'
                                   'test_event/devices/test_device',
                                   failure_callback=error_cb)
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
        req = make_eventdevice_get(self.token,
                                   'https://podium.live/api/v1/events/'
                                   'test_event/devices/test_device',
                                   failure_callback=error_cb)
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
        req = make_eventdevice_get(self.token,
                                   'https://podium.live/api/v1/events/'
                                   'test_event/devices/test_device',
                                   redirect_callback=redir_cb)
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
        req = make_eventdevice_get(self.token,
                                   'https://podium.live/api/v1/events/'
                                   'test_event/devices/test_device',
                                   progress_callback=progress_cb)
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


class TestEventDeviceUpdate(unittest.TestCase):
    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)

    def success_cb(self, result, uri):
        self.result = result
        self.uri = uri

    def check_results(self):
        self.assertEqual(self.result, {'message': 'Update success'})
        self.assertEqual(self.uri, 'https://podium.live/api/v1/events/'
                                   'test_event/devices/test_device')

    @patch('podium_api.async.UrlRequest.run')
    def test_event_update(self, mock_request):
        req = make_eventdevice_update(
            self.token,
            'https://podium.live/api/v1/events/test_event/devices/test_device',
            name='new_name',
            success_callback=self.success_cb
        )
        self.assertEqual(req._method, 'PUT')
        self.assertEqual(req.req_body,
                         urlencode({'eventdevice[name]': 'new_name'}))
        self.assertEqual(req.url,
                         'https://podium.live/api/v1/events/'
                         'test_event/devices/test_device')
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        # simulate successful request
        req.on_success()(req, {'message': 'Update success'})
        self.check_results()

    @patch('podium_api.async.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_eventdevice_update(
            self.token,
            'https://podium.live/api/v1/events/test_event/devices/test_device',
            name='new_name',
            failure_callback=error_cb)
        # simulate calling the requests on_error
        req.on_error()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'error', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': None,
             'updated_uri': 'https://podium.live/api/v1/events/'
                            'test_event/devices/test_device'}
        )

    @patch('podium_api.async.UrlRequest.run')
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_eventdevice_update(
            self.token,
            'https://podium.live/api/v1/events/test_event/devices/test_device',
            name='new_name',
            failure_callback=error_cb)
        # simulate calling the requests on_failure
        req.on_failure()(req, {})
        # assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'failure', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': None,
             'updated_uri': 'https://podium.live/api/v1/events/'
                            'test_event/devices/test_device'}
        )

    @patch('podium_api.async.UrlRequest.run')
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_eventdevice_update(
            self.token,
            'https://podium.live/api/v1/events/test_event/devices/test_device',
            name='new_name',
            redirect_callback=redir_cb)
        # simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        # assert our lambda called the mock correctly
        redir_cb.assert_called_with(
            req, None,
            {'success_callback': None,
             'failure_callback': None,
             'progress_callback': None,
             'redirect_callback': redir_cb,
             'updated_uri': 'https://podium.live/api/v1/events/'
                            'test_event/devices/test_device'}
        )

    @patch('podium_api.async.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_eventdevice_update(
            self.token,
            'https://podium.live/api/v1/events/test_event/devices/test_device',
            name='new_name',
            progress_callback=progress_cb)
        # simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(
            0, 10,
            {'success_callback': None,
             'failure_callback': None,
             'progress_callback': progress_cb,
             'redirect_callback': None,
             'updated_uri': 'https://podium.live/api/v1/events/'
                            'test_event/devices/test_device'}
        )

    def tearDown(self):
        podium_api.unregister_podium_application()
