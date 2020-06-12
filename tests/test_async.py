import unittest
import podium_api
from podium_api.async import (get_json_header, make_request,
                              make_request_default,
                              make_request_custom_success)
from podium_api.types.exceptions import PodiumApplicationNotRegistered
from mock import patch, Mock
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


class TestMakeRequestDefault(unittest.TestCase):

    @patch('podium_api.async.UrlRequest.run')
    def test_endpoint(self, mock_request):
        req = make_request_default('test/test')
        self.assertEqual(req.url, 'test/test')
        self.assertEqual(req._method, "GET")
        self.assertEqual(req.req_body, None)
        self.assertEqual(req.req_headers, None)

    @patch('podium_api.async.UrlRequest.run')
    def test_method(self, mock_request):
        req = make_request_default('test/test', method="PUT")
        self.assertEqual(req._method, "PUT")

    @patch('podium_api.async.UrlRequest.run')
    def test_body(self, mock_request):
        req = make_request_default('test/test', body={"test1": "test2"})
        self.assertEqual(req.req_body,
                         urlencode({"test1": "test2"}))

    @patch('podium_api.async.UrlRequest.run')
    def test_params(self, mock_request):
        req = make_request_default('test/test', params={"test1": "test2"})
        self.assertEqual(req.url,
                         'test/test?' + urlencode({"test1": "test2"}))

    @patch('podium_api.async.UrlRequest.run')
    def test_params_with_params(self, mock_request):
        req = make_request_default('test/test?test3=test4',
            params={"test1": "test2"})
        self.assertEqual(
            req.url, 'test/test?test3=test4&' + urlencode({"test1": "test2"})
            )

    @patch('podium_api.async.UrlRequest.run')
    def test_header(self, mock_request):
        req = make_request_default('test/test', header={"test1": "test2"})
        self.assertEqual(req.req_headers, {"test1": "test2"})

    @patch('podium_api.async.UrlRequest.run')
    def test_success_callback(self, mock_request):
        success_cb = Mock()
        req = make_request_default('test/test', success_callback=success_cb)
        # simulate calling the requests on_success
        req.on_success()(req, {})
        # assert our lambda called the mock correctly
        success_cb.assert_called_with({},
                                      {'success_callback': success_cb,
                                       'failure_callback': None,
                                       'progress_callback': None,
                                       'redirect_callback': None})

    @patch('podium_api.async.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        req = make_request_default('test/test', failure_callback=error_cb)
        # simulate calling the requests on_success
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
        req = make_request_default('test/test', failure_callback=error_cb)
        # simulate calling the requests on_success
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
        req = make_request_default('test/test', redirect_callback=redir_cb)
        # simulate calling the requests on_success
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
        req = make_request_default('test/test', progress_callback=progress_cb)
        # simulate calling the requests on_success
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(0, 10,
                                       {'success_callback': None,
                                        'failure_callback': None,
                                        'progress_callback': progress_cb,
                                        'redirect_callback': None})

    @patch('podium_api.async.UrlRequest.run')
    def test_custom_data(self, mock_request):
        success_cb = Mock()
        req = make_request_default('test/test', success_callback=success_cb,
                                   data={"custom": "test"})
        # simulate calling the requests on_success
        req.on_success()(req, {})
        # assert our lambda called the mock correctly
        success_cb.assert_called_with({},
                                      {'success_callback': success_cb,
                                       'failure_callback': None,
                                       'progress_callback': None,
                                       'redirect_callback': None,
                                       'custom': 'test'})


class TestMakeRequestCustomSuccess(unittest.TestCase):

    @patch('podium_api.async.UrlRequest.run')
    def test_endpoint(self, mock_request):
        success_handler = Mock()
        req = make_request_custom_success('test/test', success_handler)
        self.assertEqual(req.url, 'test/test')
        self.assertEqual(req._method, "GET")
        self.assertEqual(req.req_body, None)
        self.assertEqual(req.req_headers, None)

    @patch('podium_api.async.UrlRequest.run')
    def test_method(self, mock_request):
        success_handler = Mock()
        req = make_request_custom_success('test/test', success_handler,
                                          method="PUT")
        self.assertEqual(req._method, "PUT")

    @patch('podium_api.async.UrlRequest.run')
    def test_body(self, mock_request):
        success_handler = Mock()
        req = make_request_custom_success('test/test', success_handler,
                                          body={"test1": "test2"})
        self.assertEqual(req.req_body,
                         urlencode({"test1": "test2"}))

    @patch('podium_api.async.UrlRequest.run')
    def test_header(self, mock_request):
        success_handler = Mock()
        req = make_request_custom_success('test/test', success_handler,
                                          header={"test1": "test2"})
        self.assertEqual(req.req_headers, {"test1": "test2"})

    @patch('podium_api.async.UrlRequest.run')
    def test_success_callback(self, mock_request):
        success_handler = Mock()
        req = make_request_custom_success('test/test', success_handler)
        # simulate calling the requests on_success
        req.on_success()(req, {})
        # assert our lambda called the mock correctly
        success_handler.assert_called_with(req, {},
                                           {'success_callback': None,
                                            'failure_callback': None,
                                            'progress_callback': None,
                                            'redirect_callback': None})

    @patch('podium_api.async.UrlRequest.run')
    def test_error_callback(self, mock_request):
        error_cb = Mock()
        success_handler = Mock()
        req = make_request_custom_success('test/test', success_handler,
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
        success_handler = Mock()
        error_cb = Mock()
        req = make_request_custom_success('test/test', success_handler,
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
        success_handler = Mock()
        redir_cb = Mock()
        req = make_request_custom_success('test/test', success_handler,
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
        success_handler = Mock()
        req = make_request_custom_success('test/test', success_handler,
                                          progress_callback=progress_cb)
        # simulate calling the requests on_progress
        req.on_progress()(req, 0, 10)
        # assert our lambda called the mock correctly
        progress_cb.assert_called_with(0, 10,
                                       {'success_callback': None,
                                        'failure_callback': None,
                                        'progress_callback': progress_cb,
                                        'redirect_callback': None})

    @patch('podium_api.async.UrlRequest.run')
    def test_custom_data(self, mock_request):
        success_handler = Mock()
        req = make_request_custom_success('test/test', success_handler,
                                          data={"custom": "test"})
        # simulate calling the requests on_success
        req.on_success()(req, {})
        # assert our lambda called the mock correctly
        success_handler.assert_called_with(req, {},
                                           {'success_callback': None,
                                            'failure_callback': None,
                                            'progress_callback': None,
                                            'redirect_callback': None,
                                            'custom': 'test'})


class TestMakeRequest(unittest.TestCase):

    @patch('podium_api.async.UrlRequest.run')
    def test_make_request(self, mock_request):
        req = make_request('test/test')
        self.assertEqual(req.url, 'test/test')
        self.assertEqual(req._method, "GET")
        self.assertEqual(req.req_body, None)
        self.assertEqual(req.req_headers, None)
        self.assertEqual(req.on_success, None)
        self.assertEqual(req.on_failure, None)
        self.assertEqual(req.on_error, None)
        self.assertEqual(req.on_progress, None)
        self.assertEqual(req.on_redirect, None)

    @patch('podium_api.async.UrlRequest.run')
    def test_make_request_method(self, mock_request):
        req = make_request('test/test', method="POST")
        self.assertEqual(req._method, "POST")

    @patch('podium_api.async.UrlRequest.run')
    def test_make_request_headers(self, mock_request):
        req = make_request('test/test', header={"test": "test2"})
        self.assertEqual(req.url, 'test/test')
        self.assertEqual(req.req_headers, {"test": "test2"})

    @patch('podium_api.async.UrlRequest.run')
    def test_make_request_body(self, mock_request):
        req = make_request('test/test', body={"test": "test2"})
        self.assertEqual(req.req_body,
                         urlencode({"test": "test2"}))

    @patch('podium_api.async.UrlRequest.run')
    def test_make_request_callbacks(self, mock_request):
        success_cb = Mock()
        failure_cb = Mock()
        error_cb = Mock()
        progress_cb = Mock()
        redirect_cb = Mock()
        req = make_request('test/test', body={"test": "test2"},
                           on_success=success_cb,
                           on_redirect=redirect_cb,
                           on_progress=progress_cb,
                           on_failure=failure_cb,
                           on_error=error_cb)
        # simulate calling the requests on_success
        req.on_success()(req, {})
        # assert our lambda called the mock correctly
        success_cb.assert_called_with(req, {}, None)
        # do the same for the rest of the callbacks
        req.on_failure()(req, {})
        failure_cb.assert_called_with(req, {}, None)
        req.on_error()(req, {})
        error_cb.assert_called_with(req, {}, None)
        req.on_redirect()(req, {})
        redirect_cb.assert_called_with(req, {}, None)
        req.on_progress()(req, 0, 10)
        progress_cb.assert_called_with(req, 0, 10, None)

    @patch('podium_api.async.UrlRequest.run')
    def test_forward_data_to_callbacks(self, mock_request):
        success_cb = Mock()
        failure_cb = Mock()
        error_cb = Mock()
        progress_cb = Mock()
        redirect_cb = Mock()
        req = make_request('test/test', body={"test": "test2"},
                           on_success=success_cb,
                           on_redirect=redirect_cb,
                           on_progress=progress_cb,
                           on_failure=failure_cb,
                           on_error=error_cb,
                           data={"test": "testdata"})
        # simulate calling the requests on_success
        req.on_success()(req, {})
        # assert our lambda called the mock correctly
        success_cb.assert_called_with(req, {}, {"test": "testdata"})
        # do the same for the rest of the callbacks
        req.on_failure()(req, {})
        failure_cb.assert_called_with(req, {}, {"test": "testdata"})
        req.on_error()(req, {})
        error_cb.assert_called_with(req, {}, {"test": "testdata"})
        req.on_redirect()(req, {})
        redirect_cb.assert_called_with(req, {}, {"test": "testdata"})
        req.on_progress()(req, 0, 10)
        progress_cb.assert_called_with(req, 0, 10, {"test": "testdata"})


class TestGetJsonHeader(unittest.TestCase):

    def test_get_header(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        header = get_json_header()
        self.assertEqual(header['Content-Type'],
                         "application/x-www-form-urlencoded")
        self.assertEqual(header['Authorization'], 'Basic test_id:test_secret')
        self.assertEqual(header['Accept'], "application/json")

    def test_get_header_no_register(self):
        podium_api.unregister_podium_application()
        with self.assertRaises(PodiumApplicationNotRegistered):
            get_json_header()

    def tearDown(self):
        podium_api.unregister_podium_application()
