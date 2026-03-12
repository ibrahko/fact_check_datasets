from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from facts.models import FactCheck


class FactCheckAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='user1', password='secret1234')
        self.other = get_user_model().objects.create_user(username='user2', password='secret1234')
        self.client.force_authenticate(user=self.user)

    def test_factcheck_crud(self):
        payload = {
            'title': 'Titre test',
            'source_url': 'https://example.com/article',
            'raw_input': 'Contenu à vérifier',
            'content_type': 'article',
        }
        create_response = self.client.post('/api/facts/', payload, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        fact_id = create_response.data['id']

        list_response = self.client.get('/api/facts/')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        update_response = self.client.patch(f'/api/facts/{fact_id}/', {'title': 'Titre maj'}, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['title'], 'Titre maj')

        delete_response = self.client.delete(f'/api/facts/{fact_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permissions_only_owner_sees_own_facts(self):
        FactCheck.objects.create(
            user=self.user,
            title='A',
            raw_input='x',
            content_type='article',
        )
        FactCheck.objects.create(
            user=self.other,
            title='B',
            raw_input='y',
            content_type='article',
        )

        response = self.client.get('/api/facts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'A')
