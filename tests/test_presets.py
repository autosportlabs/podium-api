#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import podium_api
from podium_api.presets import (
    make_presets_get, make_preset_create, create_preset_redirect_handler,
    make_preset_get, make_preset_delete, make_preset_update
    )
from podium_api.types.preset import get_preset_from_json
from podium_api.types.redirect import get_redirect_from_json
from podium_api.types.token import PodiumToken
from mock import patch, Mock
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode

class TestPresetsGet(unittest.TestCase):

    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)

        self.result_json = {'id': 'test',
                            'URI': 'test/presets/test',
                            'name': 'test name',
                            'notes': 'test notes',
                            'preset_data': 'test preset data',
                            'mapping_type_id': 1234,
                            'private': True,
                            'rating': 4.5,
                            'mapping_type': 'test_mapping_type',
                            'created': '2018-03-02T16:23:00Z',
                            'updated': '2018-03-02T16:23:00Z'
                            }
        self.paged_preset_json = {'total': 1, 'presets': [self.result_json]}
        self.field_names = {'id': 'preset_id', 'URI': 'uri'}

    def check_results_preset(self):
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
        self.assertEqual(result.payload_name, 'presets')
        for preset in result.presets:
            self.result = preset
            self.check_results_preset()

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_no_params(self, mock_request):
        req = make_presets_get(
            self.token,
            endpoint='https://podium.live/api/v1/presets?start=20&per_page=20',
            expand=None,
            success_callback=self.success_cb)
        self.assertEqual(
            req.url, 'https://podium.live/api/v1/presets?start=20&per_page=20')

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_presets_get(self, mock_request):
        req = make_presets_get(self.token, start=0, per_page=100,
                              success_callback=self.success_cb)
        self.assertEqual(req._method, 'GET')
        self.assertTrue('https://podium.live/api/v1/presets?' in req.url)
        self.assertTrue('per_page=100' in req.url)
        self.assertTrue('start=0' in req.url)
        self.assertTrue('expand=True' in req.url)
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        #simulate successful request
        req.on_success()(req, self.paged_preset_json)
        self.check_results_paged_response()


    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_presets_get(self.token, start=0, per_page=100,
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
        req = make_presets_get(self.token, start=0, per_page=100,
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
        req = make_presets_get(self.token, start=0, per_page=100,
                              redirect_callback=redir_cb)
        #simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        #assert our lambda called the mock correctly
        redir_cb.assert_called_with(req, None,
                                    {'success_callback': None,
                                     'failure_callback': None,
                                     'progress_callback': None,
                                     'redirect_callback': redir_cb})

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_presets_get(self.token, start=0, per_page=100,
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


class TestPresetCreate(unittest.TestCase):

    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)
        self.result_json = {'location': 'test/presets/test1',
                            'object_type': 'preset'}
        self.field_names = {}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    def test_get_redirect_from_json(self):
        self.result = get_redirect_from_json(self.result_json, 'preset')
        self.check_results()

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_preset_create(self, mock_request):
        req = make_preset_create(self.token, 'name',
                                'notes',
                                'preset_data',
                                1234,
                                True,
                                redirect_callback=self.success_cb)
        self.assertEqual(req._method, 'POST')
        self.assertEqual(req.url, 'https://podium.live/api/v1/presets')
        self.assertEqual(
            req.req_body,
            urlencode({'preset[name]': 'name',
                       'preset[notes]': 'notes',
                       'preset[preset_data]': 'preset_data',
                       'preset[mapping_type_id]': 1234,
                       'preset[private]': True
                       }))
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
        req = make_preset_create(self.token, 'name',
                                 'notes',
                                 'preset',
                                 1234,
                                 True,
                                failure_callback=error_cb)
        #simulate calling the requests on_error
        req.on_error()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'error', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': create_preset_redirect_handler,
             '_redirect_callback': None}
        )

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_preset_create(self.token, 'name',
                                'notes',
                                'preset',
                                1234,
                                True,
                                failure_callback=error_cb)
        #simulate calling the requests on_failure
        req.on_failure()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'failure', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': create_preset_redirect_handler,
             '_redirect_callback': None}
        )

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_success_callback(self, mock_request):
        success_cb = Mock()
        req = make_preset_create(self.token, 'name',
                                'notes',
                                'preset',
                                1234,
                                True,
                                success_callback=success_cb)
        #simulate calling the requests on_success
        self.assertEqual(req.on_success, None)

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_preset_create(self.token, 'name',
                                'notes',
                                'preset',
                                1234,
                                True,
                                progress_callback=progress_cb)
        # simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(
            0, 10,
           {'success_callback': None,
            'failure_callback': None,
            'progress_callback': progress_cb,
            'redirect_callback': create_preset_redirect_handler,
            '_redirect_callback': None})

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestPresetDelete(unittest.TestCase):

    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)

    def check_results(self):
        self.assertEqual(self.result, 'https://podium.live/api/v1/presets/test')

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_preset_delete(self, mock_request):
        req = make_preset_delete(self.token,
                                'https://podium.live/api/v1/presets/test',
                                success_callback=self.success_cb)
        self.assertEqual(req._method, 'DELETE')
        self.assertEqual(req.url,
                         'https://podium.live/api/v1/presets/test')
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        #simulate successful request
        req.on_success()(req, {})
        self.check_results()

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_preset_delete(self.token,
                                'https://podium.live/api/v1/presets/test',
                                failure_callback=error_cb)
        #simulate calling the requests on_error
        req.on_error()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'error', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': None,
             'deleted_uri': 'https://podium.live/api/v1/presets/test'}
        )

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_preset_delete(self.token,
                                'https://podium.live/api/v1/presets/test',
                                failure_callback=error_cb)
        #simulate calling the requests on_failure
        req.on_failure()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'failure', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': None,
             'deleted_uri': 'https://podium.live/api/v1/presets/test'}
        )

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_preset_delete(self.token,
                                'https://podium.live/api/v1/presets/test',
                                redirect_callback=redir_cb)
        #simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        #assert our lambda called the mock correctly
        redir_cb.assert_called_with(
            req, None,
            {'success_callback': None,
             'failure_callback': None,
             'progress_callback': None,
             'redirect_callback': redir_cb,
             'deleted_uri': 'https://podium.live/api/v1/presets/test'}
        )

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_preset_delete(self.token,
                                'https://podium.live/api/v1/presets/test',
                                progress_callback=progress_cb)
        #simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        #assert our lambda called the mock correctly
        progress_cb.assert_called_with(
            0, 10,
           {'success_callback': None,
            'failure_callback': None,
            'progress_callback': progress_cb,
            'redirect_callback': None,
            'deleted_uri': 'https://podium.live/api/v1/presets/test'}
        )

    def tearDown(self):
        podium_api.unregister_podium_application()


class TestPresetGet(unittest.TestCase):

    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)
        self.result_json = {'id': 'test',
                            'URI': 'https://podium.live/api/v1/presets/test',
                            'name': 'name',
                            'notes': 'notes',
                            'preset_data': 'preset_data',
                            'mapping_type_id': 1234,
                            'private': True,
                            'rating': 3.5
                            }
        self.field_names = {'id': 'preset_id', 'URI': 'uri'}

    def check_results(self):
        for key in self.result_json:
            if key in self.field_names:
                rkey = self.field_names[key]
            else:
                rkey = key
            self.assertEqual(getattr(self.result, rkey), self.result_json[key])

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_no_params(self, mock_request):
        req = make_preset_get(self.token,
                             'https://podium.live/api/v1/presets/test',
                             expand=None)
        self.assertEqual(req.url, 'https://podium.live/api/v1/presets/test')

    def success_cb(self, result):
        self.result = result

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_preset_get(self, mock_request):
        req = make_preset_get(self.token,
                             'https://podium.live/api/v1/presets/test',
                             success_callback=self.success_cb)
        self.assertEqual(req._method, 'GET')
        self.assertEqual(req.url,
                         'https://podium.live/api/v1/presets/test?expand=True')
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        #simulate successful request
        req.on_success()(req, {'preset': self.result_json})
        self.check_results()

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_preset_get(self.token,
                             'https://podium.live/api/v1/presets/test',
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
        req = make_preset_get(self.token,
                             'https://podium.live/api/v1/presets/test',
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
        req = make_preset_get(self.token,
                             'https://podium.live/api/v1/presets/test',
                             redirect_callback=redir_cb)
        #simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        #assert our lambda called the mock correctly
        redir_cb.assert_called_with(req, None,
                                    {'success_callback': None,
                                     'failure_callback': None,
                                     'progress_callback': None,
                                     'redirect_callback': redir_cb})

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_preset_get(self.token,
                             'https://podium.live/api/v1/presets/test',
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


class TestPresetUpdate(unittest.TestCase):

    def setUp(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.token = PodiumToken('test_token', 'test_type', 1)


    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_no_params(self, mock_request):
        req = make_preset_update(self.token,
                                'https://podium.live/api/v1/presets/test')
        self.assertEqual(req.req_body, urlencode({}))
        self.assertEqual(req.url, 'https://podium.live/api/v1/presets/test')

    def success_cb(self, result, uri):
        self.result = result
        self.uri = uri

    def check_results(self):
        self.assertEqual(self.result, {'message': 'Update success'})
        self.assertEqual(self.uri, 'https://podium.live/api/v1/presets/test')

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_preset_update(self, mock_request):
        req = make_preset_update(self.token,
                                'https://podium.live/api/v1/presets/test',
                                name='new name',
                                notes='new notes',
                                preset_data='new preset',
                                mapping_type_id=5678,
                                private=True,
                                success_callback=self.success_cb)
        self.assertEqual(req._method, 'PUT')
        self.assertEqual(req.req_body,
                         urlencode({'preset[name]': 'new name',
                                    'preset[notes]': 'new notes',
                                    'preset[preset_data]': 'new preset',
                                    'preset[mapping_type_id]': 5678,
                                    'preset[private]': True}))
        self.assertEqual(req.url,
                         'https://podium.live/api/v1/presets/test')
        self.assertEqual(req.req_headers['Content-Type'],
                         'application/x-www-form-urlencoded')
        self.assertEqual(req.req_headers['Authorization'],
                         'Bearer {}'.format(self.token.token))
        self.assertEqual(req.req_headers['Accept'], 'application/json')
        #simulate successful request
        req.on_success()(req, {'message': 'Update success'})
        self.check_results()

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_preset_update(self.token,
                                'https://podium.live/api/v1/presets/test',
                                name='new name',
                                notes='new notes',
                                preset_data='new preset',
                                mapping_type_id = 5678,
                                private=True,
                                failure_callback=error_cb)
        #simulate calling the requests on_error
        req.on_error()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'error', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': None,
             'updated_uri': 'https://podium.live/api/v1/presets/test'}
        )

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_failure_callback(self, mock_request):
        error_cb = Mock()
        req = make_preset_update(self.token,
                                'https://podium.live/api/v1/presets/test',
                                name='new name',
                                notes='new notes',
                                preset_data='new preset',
                                mapping_type_id = 5678,
                                private=True,
                                failure_callback=error_cb)
        #simulate calling the requests on_failure
        req.on_failure()(req, {})
        #assert our lambda called the mock correctly
        error_cb.assert_called_with(
            'failure', {},
            {'success_callback': None,
             'failure_callback': error_cb,
             'progress_callback': None,
             'redirect_callback': None,
             'updated_uri': 'https://podium.live/api/v1/presets/test'}
        )

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_redirect_callback(self, mock_request):
        redir_cb = Mock()
        req = make_preset_update(self.token,
                                'https://podium.live/api/v1/presets/test',
                                name='new name',
                                notes='new notes',
                                preset_data='new preset',
                                mapping_type_id = 5678,
                                private=True,
                                redirect_callback=redir_cb)
        #simulate calling the requests on_redirect
        req.on_redirect()(req, {})
        #assert our lambda called the mock correctly
        redir_cb.assert_called_with(
            req, None,
            {'success_callback': None,
             'failure_callback': None,
             'progress_callback': None,
             'redirect_callback': redir_cb,
             'updated_uri': 'https://podium.live/api/v1/presets/test'}
        )

    @patch('podium_api.asyncreq.UrlRequest.run')
    def test_progress_callback(self, mock_request):
        progress_cb = Mock()
        req = make_preset_update(self.token,
                                'https://podium.live/api/v1/presets/test',
                                name='new name',
                                notes='new notes',
                                preset_data='new preset',
                                mapping_type_id = 5678,
                                private=True,
                                progress_callback=progress_cb)
        #simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        #assert our lambda called the mock correctly
        progress_cb.assert_called_with(
            0, 10,
           {'success_callback': None,
            'failure_callback': None,
            'progress_callback': progress_cb,
            'redirect_callback': None,
            'updated_uri': 'https://podium.live/api/v1/presets/test'}
        )

    def tearDown(self):
        podium_api.unregister_podium_application()
