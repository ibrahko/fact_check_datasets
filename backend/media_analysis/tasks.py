from decimal import Decimal

from celery import shared_task

from facts.models import FactCheck
from media_analysis.models import MediaFile
from media_analysis.services.ai_service import CheckIAService


def _to_decimal(value, default='0'):
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal(default)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def process_media_file(self, media_file_id: int):
    media_file = MediaFile.objects.select_related('fact_check').get(id=media_file_id)
    media_file.status = MediaFile.AnalysisStatus.PROCESSING
    media_file.save(update_fields=['status'])

    service = CheckIAService()

    try:
        if media_file.media_type == MediaFile.MediaType.IMAGE:
            result = service.analyze_image(media_file.file.path)
            media_file.deepfake_score = _to_decimal(result.get('deepfake_score', 0))
            media_file.analysis_result = result
            media_file.confidence = _to_decimal(result.get('deepfake_score', 0))
        elif media_file.media_type == MediaFile.MediaType.AUDIO:
            transcript = media_file.fact_check.raw_input
            result = service.analyze_audio_transcript(transcript)
            media_file.analysis_result = result
            media_file.deepfake_score = _to_decimal(result.get('confidence_score', 0))
            media_file.confidence = _to_decimal(result.get('confidence_score', 0))
        else:
            fallback_text = media_file.fact_check.raw_input
            result = service.analyze_text(fallback_text)
            media_file.analysis_result = result
            media_file.deepfake_score = _to_decimal(result.get('confidence_score', 0))
            media_file.confidence = _to_decimal(result.get('confidence_score', 0))

        media_file.status = MediaFile.AnalysisStatus.DONE
        media_file.save(update_fields=['analysis_result', 'deepfake_score', 'confidence', 'status'])
        return media_file.analysis_result
    except Exception as exc:
        media_file.status = MediaFile.AnalysisStatus.FAILED
        media_file.analysis_result = {'error': str(exc)}
        media_file.save(update_fields=['status', 'analysis_result'])
        raise


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def process_fact_check(self, fact_check_id: int):
    fact_check = FactCheck.objects.get(id=fact_check_id)
    service = CheckIAService()

    if fact_check.source_url:
        result = service.analyze_article(fact_check.source_url)
    else:
        result = service.analyze_text(fact_check.raw_input)

    fact_check.verdict = result.get('verdict', FactCheck.Verdict.UNKNOWN)
    fact_check.confidence_score = _to_decimal(result.get('confidence_score', 0))
    fact_check.ai_summary = result.get('explanation', '')
    fact_check.save(update_fields=['verdict', 'confidence_score', 'ai_summary', 'updated_at'])

    return {
        'fact_check_id': fact_check.id,
        'verdict': fact_check.verdict,
        'confidence_score': float(fact_check.confidence_score),
    }
