import pytest
from django.contrib.auth import get_user_model

from facts.models import FactCheck
from media_analysis.models import MediaFile


@pytest.mark.django_db
def test_user_model_defaults():
    user = get_user_model().objects.create_user(username='alice', password='SecretPass123!')

    assert user.role == get_user_model().Role.USER
    assert str(user) == 'alice'


@pytest.mark.django_db
def test_factcheck_model_fields(user):
    fact = FactCheck.objects.create(
        user=user,
        title='Titre',
        raw_input='Texte brut',
        content_type=FactCheck.ContentType.BLOG,
        is_public=False,
    )

    assert fact.verdict == FactCheck.Verdict.UNKNOWN
    assert fact.is_public is False
    assert 'Titre' in str(fact)


@pytest.mark.django_db
def test_mediafile_model_str_and_status(fact_check, image_upload_file):
    media = MediaFile.objects.create(
        fact_check=fact_check,
        media_type=MediaFile.MediaType.IMAGE,
        file=image_upload_file,
    )

    assert media.status == MediaFile.AnalysisStatus.PENDING
    assert 'image' in str(media)
