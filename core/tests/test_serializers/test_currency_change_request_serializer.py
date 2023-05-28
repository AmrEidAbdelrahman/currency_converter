from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from core.serializers import CurrencyChangeRequestSerializer
from rest_framework.test import APITestCase


class CurrencyChangeRequestSerializerTests(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')

    def tearDown(self):
        self.test_user.delete()

    def test_currency_change_request_serializer_valid(self):
        serializer_data = {
            'source_currency': 'usd',
            'target_currency': 'eur',
            'value': 100
        }
        context = {'user': self.test_user}
        serializer = CurrencyChangeRequestSerializer(data=serializer_data, context=context)

        self.assertTrue(serializer.is_valid())

        currency_change_request = serializer.save()
        self.assertEqual(currency_change_request.user, self.test_user)
        self.assertEqual(currency_change_request.source_currency, 'usd')
        self.assertEqual(currency_change_request.target_currency, 'eur')
        self.assertEqual(currency_change_request.number_of_requests, 1)

    def test_currency_change_request_serializer_invalid_value(self):
        serializer_data = {
            'source_currency': 'usd',
            'target_currency': 'eur',
            'value': 0
        }
        context = {'user': self.test_user}
        serializer = CurrencyChangeRequestSerializer(data=serializer_data, context=context)

        self.assertFalse(serializer.is_valid())

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_currency_change_request_serializer_invalid_source_currency(self):
        serializer_data = {
            'source_currency': 'dsa',
            'target_currency': 'eur',
            'value': 1
        }
        context = {'user': self.test_user}
        serializer = CurrencyChangeRequestSerializer(data=serializer_data, context=context)

        self.assertFalse(serializer.is_valid())

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_currency_change_request_serializer_invalid_target_currency(self):
        serializer_data = {
            'source_currency': 'usd',
            'target_currency': 'qeq',
            'value': 1
        }
        context = {'user': self.test_user}
        serializer = CurrencyChangeRequestSerializer(data=serializer_data, context=context)

        self.assertFalse(serializer.is_valid())

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
