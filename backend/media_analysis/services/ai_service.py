import base64
import json
import logging
import os
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from openai import OpenAI

from .deepfake_detector import DeepfakeDetector

logger = logging.getLogger(__name__)


class CheckIAService:
    """Service centralisant les appels OpenAI pour l'analyse de contenu."""

    TEXT_SYSTEM_PROMPT = (
        "Tu es Check-IA, un assistant expert en fact-checking francophone. "
        "Analyse rigoureusement les affirmations du texte, signale les incohérences, "
        "les manques de contexte et les éléments potentiellement trompeurs. "
        "Tu dois répondre UNIQUEMENT en JSON valide avec les champs: "
        "verdict (true|false|mixed|unknown), confidence_score (0-100), "
        "explanation (texte en français), sources_suggested (liste de 3 à 5 sources crédibles à consulter)."
    )
    IMAGE_SYSTEM_PROMPT = (
        "Tu es un analyste en forensic visuel et détection de deepfake. "
        "Observe l'image et identifie les indices techniques de manipulation. "
        "Réponds UNIQUEMENT en JSON avec: is_manipulated, deepfake_score, explanation."
    )
    AUDIO_SYSTEM_PROMPT = (
        "Tu es un expert en désinformation audio. "
        "Réponds UNIQUEMENT en JSON avec: verdict, confidence_score, explanation, sources_suggested."
    )

    def __init__(self, detector=None) -> None:
        api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.detector = detector or DeepfakeDetector(client=self.client)

    def _parse_json_response(self, content: str) -> dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning('Réponse OpenAI non JSON, retour format par défaut.')
            return {
                'verdict': 'unknown',
                'confidence_score': 0,
                'explanation': content,
                'sources_suggested': [],
            }

    def analyze_text(self, text: str) -> dict[str, Any]:
        if self.client is None:
            return {
                'verdict': 'unknown',
                'confidence_score': 0,
                'explanation': 'Clé OpenAI absente.',
                'sources_suggested': [],
            }
        response = self.client.chat.completions.create(
            model='gpt-4o',
            temperature=0.2,
            response_format={'type': 'json_object'},
            messages=[
                {'role': 'system', 'content': self.TEXT_SYSTEM_PROMPT},
                {'role': 'user', 'content': f"Vérifie les faits de ce contenu:\n\n{text}"},
            ],
        )
        return self._parse_json_response(response.choices[0].message.content or '{}')

    def analyze_article(self, url: str) -> dict[str, Any]:
        page = requests.get(url, timeout=15)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, 'html.parser')
        article_text = '\n'.join([p.get_text(' ', strip=True) for p in soup.find_all('p') if p.get_text(strip=True)])
        if not article_text:
            return {
                'verdict': 'unknown',
                'confidence_score': 0,
                'explanation': "Impossible d'extraire le contenu textuel de l'article.",
                'sources_suggested': [],
            }
        return self.analyze_text(article_text[:12000])

    def analyze_image(self, image_path: str) -> dict[str, Any]:
        if self.client is None:
            return {'is_manipulated': False, 'deepfake_score': 0, 'explanation': 'Clé OpenAI absente.'}
        with open(image_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        response = self.client.chat.completions.create(
            model='gpt-4o',
            temperature=0.1,
            response_format={'type': 'json_object'},
            messages=[
                {'role': 'system', 'content': self.IMAGE_SYSTEM_PROMPT},
                {
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': 'Analyse cette image pour détecter une manipulation.'},
                        {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{encoded_image}'}},
                    ],
                },
            ],
        )
        parsed = self._parse_json_response(response.choices[0].message.content or '{}')
        return {
            'is_manipulated': bool(parsed.get('is_manipulated', False)),
            'deepfake_score': parsed.get('deepfake_score', 0),
            'explanation': parsed.get('explanation', ''),
        }

    def analyze_audio_transcript(self, transcript: str) -> dict[str, Any]:
        if self.client is None:
            return {
                'verdict': 'unknown',
                'confidence_score': 0,
                'explanation': 'Clé OpenAI absente.',
                'sources_suggested': [],
            }
        response = self.client.chat.completions.create(
            model='gpt-4o',
            temperature=0.2,
            response_format={'type': 'json_object'},
            messages=[
                {'role': 'system', 'content': self.AUDIO_SYSTEM_PROMPT},
                {'role': 'user', 'content': f'Analyse cette transcription audio:\n\n{transcript}'},
            ],
        )
        return self._parse_json_response(response.choices[0].message.content or '{}')

    def analyze_media(self, media_file):
        path = Path(media_file.file.path)
        result = {}
        if media_file.media_type == media_file.MediaType.IMAGE:
            result['metadata'] = self.detector.analyze_image_metadata(path)
            result['artifacts'] = self.detector.detect_image_artifacts(path)
            score = (result['metadata']['manipulation_score'] + result['artifacts']['artifact_score']) / 2
        elif media_file.media_type == media_file.MediaType.VIDEO:
            result['video'] = self.detector.analyze_video_frames(path)
            score = result['video'].get('frame_anomaly_score', 0.0)
        elif media_file.media_type == media_file.MediaType.AUDIO:
            result['audio'] = self.detector.transcribe_audio(path)
            score = result['audio'].get('text_analysis', {}).get('ai_probability', 0.0)
        else:
            score = 0.0
        return round(score * 100, 2), result
