from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class FactsAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='factuser', password='secret1234')
        self.client.force_authenticate(user=self.user)

    def test_create_and_list_fact_checks(self):
        payload = {
            'title': 'Vérifier une info',
            'source_url': 'https://example.com/news',
            'raw_input': 'Le contenu à analyser',
            'content_type': 'article',
        }
        create_response = self.client.post('/api/facts/create/', payload, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        list_response = self.client.get('/api/facts/my-checks/')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(list_response.data), 1)
