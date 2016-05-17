import unittest
import podium_api
from podium_api.exceptions import PodiumApplicationAlreadyRegistered

class TestRegisterApplication(unittest.TestCase):

    def test_register(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        self.assertEqual(podium_api.PODIUM_APP.app_id, 'test_id')
        self.assertEqual(podium_api.PODIUM_APP.app_secret, 'test_secret')

    def test_register_twice(self):
        podium_api.register_podium_application('test_id', 'test_secret')
        with self.assertRaises(PodiumApplicationAlreadyRegistered):
            podium_api.register_podium_application('test_id2', 'test_secret2')

    def tearDown(self):
        podium_api.unregister_podium_application()
