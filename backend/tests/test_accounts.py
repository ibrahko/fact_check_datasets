from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsAPITests(APITestCase):
    def test_register_and_login(self):
        register_payload = {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'SecretPass123!',
            'password_confirm': 'SecretPass123!',
        }
        register_response = self.client.post('/api/accounts/register/', register_payload, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        login_response = self.client.post(
            '/api/accounts/login/',
            {'username': 'alice', 'password': 'SecretPass123!'},
            format='json',
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', login_response.data)

    def test_profile_endpoint_authenticated(self):
        user = get_user_model().objects.create_user(username='bob', password='SecretPass123!')
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/accounts/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'bob')
