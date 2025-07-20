import json
import threading

import requests


class StandardUrlRequest:
    def __init__(
        self,
        url,
        method="GET",
        req_body=None,
        req_headers=None,
        on_success=None,
        on_failure=None,
        on_error=None,
        on_redirect=None,
        on_progress=None,
        **kwargs
    ):
        self._url = url
        self._method = method
        self._body = req_body
        self._headers = req_headers or {}
        self._on_success = on_success
        self._on_failure = on_failure
        self._on_error = on_error
        self._on_redirect = on_redirect
        self._on_progress = on_progress

        # Start the request in a separate thread so callbacks fire “asynchronously”
        thread = threading.Thread(target=self._run)
        thread.daemon = True
        thread.start()

    def _run(self):
        try:
            # We do not implement chunked progress or true redirects:
            # we simply make one HTTP call, parse JSON, and call on_success or on_failure
            resp = requests.request(
                self._method, self._url, headers=self._headers, data=self._body, allow_redirects=False
            )

            # If you want to support on_redirect, check 3xx codes:
            if 300 <= resp.status_code < 400 and self._on_redirect:
                self._on_redirect(self, resp.json() if self._can_parse_json(resp) else resp.text)
                return

            # If status_code is 200–299, treat as success, else failure
            if 200 <= resp.status_code < 300:
                parsed = resp.json() if self._can_parse_json(resp) else resp.text
                if self._on_success:
                    self._on_success(self, parsed)
            else:
                parsed = resp.json() if self._can_parse_json(resp) else resp.text
                if self._on_failure:
                    self._on_failure(self, parsed)

        except Exception as e:
            # Any exception (network error, JSON parse error, etc.) → on_error
            if self._on_error:
                self._on_error(self, e)

    def _can_parse_json(self, resp):
        ct = resp.headers.get("Content-Type", "")
        return "application/json" in ct

    @property
    def _resp_headers(self):
        # Not implemented; for backward compatibility you could store resp.headers
        return {}

    @property
    def result(self):
        # You could cache the JSON or .text before calling callbacks if you want
        return None

    @property
    def status_code(self):
        return None
