from unittest.mock import Mock

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from facts.models import FactCheck


@pytest.mark.django_db
def test_auth_register_login_logout_flow(monkeypatch):
    client = APIClient()

    register_response = client.post(
        '/api/accounts/register/',
        {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecretPass123!',
            'password_confirm': 'SecretPass123!',
        },
        format='json',
    )
    assert register_response.status_code == status.HTTP_201_CREATED

    login_response = client.post(
        '/api/accounts/login/',
        {'username': 'newuser', 'password': 'SecretPass123!'},
        format='json',
    )
    assert login_response.status_code == status.HTTP_200_OK
    refresh = login_response.data['tokens']['refresh']
    access = login_response.data['tokens']['access']

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    logout_response = client.post('/api/accounts/logout/', {'refresh': refresh}, format='json')
    assert logout_response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_upload_and_analyze_media(auth_client, fact_check, image_upload_file, monkeypatch):
    delay_mock = Mock()
    monkeypatch.setattr('media_analysis.views.process_media_file.delay', delay_mock)

    upload_response = auth_client.post(
        '/api/media/upload/',
        {'fact_check': fact_check.id, 'media_type': 'image', 'file': image_upload_file},
    )
    assert upload_response.status_code == status.HTTP_201_CREATED
    delay_mock.assert_called_once()

    media_id = upload_response.data['id']
    analyze_response = auth_client.post(f'/api/media/{media_id}/analyze/')
    assert analyze_response.status_code == status.HTTP_202_ACCEPTED


@pytest.mark.django_db
def test_text_analysis_endpoint(auth_client, monkeypatch):
    fake_result = {
        'verdict': 'true',
        'confidence_score': 88,
        'explanation': 'Les affirmations principales sont corroborées.',
        'sources_suggested': ['https://example.org/source-1'],
    }
    monkeypatch.setattr('media_analysis.views.CheckIAService.analyze_text', lambda self, content: fake_result)

    response = auth_client.post('/api/media/analysis/text/', {'content': 'Un article à vérifier.'}, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['verdict'] == 'VRAI'
    assert response.data['score'] == 88


@pytest.mark.django_db
def test_trending_fact_checks_endpoint(user):
    for idx in range(12):
        FactCheck.objects.create(
            user=user,
            title=f'Fact #{idx}',
            raw_input='payload',
            content_type=FactCheck.ContentType.ARTICLE,
            is_public=idx % 2 == 0,
        )

    response = APIClient().get('/api/facts/trending/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) <= 10
    assert all(item['is_public'] for item in response.data)
