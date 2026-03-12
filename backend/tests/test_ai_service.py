from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from django.test import SimpleTestCase

from media_analysis.services import CheckIAService, DeepfakeDetector


class AIServiceTests(SimpleTestCase):
    def test_detect_ai_generated_text_with_mocked_openai(self):
        mock_client = Mock()
        mock_client.responses.create.return_value = SimpleNamespace(
            output_text='{"ai_probability":0.8,"rationale":"style"}'
        )
        detector = DeepfakeDetector(client=mock_client)

        result = detector.detect_ai_generated_text('Texte suspect')

        self.assertIn('raw_response', result)
        mock_client.responses.create.assert_called_once()

    def test_transcribe_audio_uses_whisper_and_text_detection(self):
        mock_client = Mock()
        mock_client.audio.transcriptions.create.return_value = SimpleNamespace(text='Bonjour le monde')
        detector = DeepfakeDetector(client=mock_client)
        detector.detect_ai_generated_text = Mock(return_value={'ai_probability': 0.2})

        audio_path = Path(__file__).parent / 'dummy.wav'
        audio_path.write_bytes(b'RIFF....WAVEfmt ')

        try:
            result = detector.transcribe_audio(audio_path)
        finally:
            audio_path.unlink(missing_ok=True)

        self.assertEqual(result['transcription'], 'Bonjour le monde')
        self.assertEqual(result['text_analysis']['ai_probability'], 0.2)

    def test_checkia_service_image_flow(self):
        detector = Mock()
        detector.analyze_image_metadata.return_value = {'manipulation_score': 0.6}
        detector.detect_image_artifacts.return_value = {'artifact_score': 0.4}

        service = CheckIAService(detector=detector)
        fake_media = SimpleNamespace(
            media_type='image',
            MediaType=SimpleNamespace(IMAGE='image', VIDEO='video', AUDIO='audio'),
            file=SimpleNamespace(path='/tmp/file.png'),
        )

        score, result = service.analyze_media(fake_media)

        self.assertEqual(score, 50.0)
        self.assertIn('metadata', result)
        self.assertIn('artifacts', result)
