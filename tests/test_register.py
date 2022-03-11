import unittest

import podium_api


class TestRegisterApplication(unittest.TestCase):
    def test_register(self):
        podium_api.register_podium_application("test_id", "test_secret")
        self.assertEqual(podium_api.PODIUM_APP.app_id, "test_id")
        self.assertEqual(podium_api.PODIUM_APP.app_secret, "test_secret")

    def tearDown(self):
        podium_api.unregister_podium_application()
