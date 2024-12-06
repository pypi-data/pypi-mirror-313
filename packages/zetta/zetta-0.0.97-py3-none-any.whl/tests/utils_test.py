# Copyright ZettaBlock Labs 2024
import requests
import unittest
from unittest.mock import patch
from zetta._utils.connections import check_api_status

class TestConnections(unittest.TestCase):
    @patch('zetta._utils.connections.requests.get')
    def test_check_api_status(self, mock_get):
        mock_get.return_value.status_code = 200
        self.assertEqual(check_api_status('testnet'), {"status": "testnet API is up and running"})
        mock_get.return_value.status_code = 404
        self.assertEqual(check_api_status('testnet'), {"status": "testnet API is down", "status_code": 404})
        mock_get.side_effect = requests.exceptions.RequestException("Connection Error")
        self.assertEqual(check_api_status('testnet'), {"status": "testnet API is down", "error": "Connection Error"})
