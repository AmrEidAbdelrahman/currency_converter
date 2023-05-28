from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import CurrencyChangeRequest


class CurrencyConverterViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def tearDown(self):
        self.user.delete()

    def test_convert_currency(self):
        currency_change_request = CurrencyChangeRequest.objects.create(
            user=self.user,
            source_currency='usd',
            target_currency='eur',
            number_of_requests=1
        )

        url = reverse('convert_currency')
        data = {
            'source_currency': 'usd',
            'target_currency': 'eur',
            'value': 100
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        currency_change_request.refresh_from_db()
        self.assertEqual(currency_change_request.number_of_requests, 2)

    def test_convert_currency_invalid_value(self):
        url = reverse('convert_currency')
        data = {
            'source_currency': 'usd',
            'target_currency': 'eur',
            'value': 0  # Value must be greater than 0
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)  # Ensure the validation error message is returned

    def test_convert_currency_invalid_source_currency(self):
        url = reverse('convert_currency')
        data = {
            'source_currency': 'gpl',
            'target_currency': 'eur',
            'value': 1
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('source_currency', response.data)  # Ensure the validation error message is returned

    def test_convert_currency_invalid_target_currency(self):
        url = reverse('convert_currency')
        data = {
            'source_currency': 'usd',
            'target_currency': 'gpl',
            'value': 1
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('target_currency', response.data)  # Ensure the validation error message is returned
