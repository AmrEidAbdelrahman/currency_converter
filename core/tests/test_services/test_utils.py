import unittest
from unittest.mock import Mock
from core.services.utils import Utils


class UtilsTests(unittest.TestCase):

    def test_get_latest_exchange_rates_success(self):
        source_currency = 'usd'
        target_currency = 'eur'
        value = 100
        converted_amount = Utils.get_latest_exchange_rates(source_currency, target_currency, value)
        self.assertIsNotNone(converted_amount)

    def test_get_latest_exchange_rates_failed_request(self):
        source_currency = 'kjh'
        target_currency = 'eur'
        value = 100

        with self.assertRaises(Exception):
            Utils.get_latest_exchange_rates(source_currency, target_currency, value)

    def create_response_mock(self, json_data, status_code):
        response_mock = Mock()
        response_mock.json.return_value = json_data
        response_mock.status_code = status_code
        return response_mock
