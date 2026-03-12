import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from facts.models import FactCheck


TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class MediaAnalysisAPITests(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='mediauser', password='secret1234')
        self.client.force_authenticate(user=self.user)
        self.fact = FactCheck.objects.create(
            user=self.user,
            title='Fact media',
            raw_input='input',
            content_type='image',
        )

    def _image_file(self):
        tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        Image.new('RGB', (10, 10), color='red').save(tmp.name, format='PNG')
        with open(tmp.name, 'rb') as f:
            payload = f.read()
        return SimpleUploadedFile('test.png', payload, content_type='image/png')

    def test_upload_analyze_reanalyze(self):
        upload_response = self.client.post(
            '/api/media/',
            {'fact_check': self.fact.id, 'media_type': 'image', 'file': self._image_file()},
        )
        self.assertEqual(upload_response.status_code, status.HTTP_201_CREATED)

        media_id = upload_response.data['id']
        analyze_response = self.client.post(f'/api/media/{media_id}/analyze/')
        self.assertEqual(analyze_response.status_code, status.HTTP_200_OK, analyze_response.data)
        self.assertIn('analysis_result', analyze_response.data)

        reanalyze_response = self.client.post(f'/api/media/{media_id}/reanalyze/')
        self.assertEqual(reanalyze_response.status_code, status.HTTP_200_OK)
