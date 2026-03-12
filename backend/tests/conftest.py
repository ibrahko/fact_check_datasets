import tempfile

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from facts.models import FactCheck


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        username='tester',
        email='tester@example.com',
        password='SecretPass123!',
    )


@pytest.fixture
def auth_client(user):
    from rest_framework.test import APIClient

    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def fact_check(user):
    return FactCheck.objects.create(
        user=user,
        title='Fact test',
        source_url='https://example.com/post',
        raw_input='Contenu de vérification',
        content_type=FactCheck.ContentType.ARTICLE,
        is_public=True,
    )


@pytest.fixture
def image_upload_file():
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    Image.new('RGB', (12, 12), color='blue').save(tmp.name, format='PNG')
    with open(tmp.name, 'rb') as file_handler:
        data = file_handler.read()
    return SimpleUploadedFile('sample.png', data, content_type='image/png')
