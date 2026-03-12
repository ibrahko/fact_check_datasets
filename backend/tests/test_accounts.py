from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsAPITests(APITestCase):
    def test_register_login_refresh_and_profile(self):
        register_payload = {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret1234',
            'first_name': 'Alice',
            'last_name': 'Doe',
        }
        register_response = self.client.post('/api/accounts/register/', register_payload, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        token_response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'alice', 'password': 'secret1234'},
            format='json',
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', token_response.data)
        self.assertIn('refresh', token_response.data)

        refresh_response = self.client.post(
            reverse('token_refresh'),
            {'refresh': token_response.data['refresh']},
            format='json',
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")
        profile_response = self.client.get('/api/accounts/me/')
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data['username'], 'alice')

    def test_non_admin_cannot_list_users(self):
        user = get_user_model().objects.create_user(username='bob', password='secret1234')
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/accounts/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
