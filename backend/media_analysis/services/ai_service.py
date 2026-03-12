import base64
import json
import logging
import os
from typing import Any

import requests
from bs4 import BeautifulSoup
from openai import OpenAI

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
        "Observe l'image et identifie les indices techniques de manipulation: "
        "textures incohérentes, artefacts, lumières impossibles, ombres anormales, "
        "bords de composition, incohérences anatomiques. "
        "Réponds UNIQUEMENT en JSON avec: is_manipulated (bool), deepfake_score (0-100), explanation (français)."
    )

    AUDIO_SYSTEM_PROMPT = (
        "Tu es un expert en désinformation audio. "
        "Analyse la transcription pour détecter les allégations douteuses, les manipulations rhétoriques, "
        "les contradictions et l'absence de preuves. "
        "Réponds UNIQUEMENT en JSON avec: verdict (true|false|mixed|unknown), confidence_score (0-100), "
        "explanation (français), sources_suggested (liste)."
    )

    def __init__(self) -> None:
        api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=api_key)

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
        response = self.client.chat.completions.create(
            model='gpt-4o',
            temperature=0.2,
            response_format={'type': 'json_object'},
            messages=[
                {'role': 'system', 'content': self.TEXT_SYSTEM_PROMPT},
                {
                    'role': 'user',
                    'content': (
                        "Vérifie les faits de ce contenu et attribue un verdict argumenté:\n\n"
                        f"{text}"
                    ),
                },
            ],
        )
        content = response.choices[0].message.content or '{}'
        return self._parse_json_response(content)

    def analyze_article(self, url: str) -> dict[str, Any]:
        page = requests.get(url, timeout=15)
        page.raise_for_status()

        soup = BeautifulSoup(page.text, 'html.parser')
        paragraphs = [p.get_text(' ', strip=True) for p in soup.find_all('p')]
        article_text = '\n'.join([p for p in paragraphs if p])

        if not article_text:
            return {
                'verdict': 'unknown',
                'confidence_score': 0,
                'explanation': "Impossible d'extraire le contenu textuel de l'article.",
                'sources_suggested': [],
            }

        return self.analyze_text(article_text[:12000])

    def analyze_image(self, image_path: str) -> dict[str, Any]:
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
                        {'type': 'text', 'text': "Analyse cette image pour détecter une manipulation."},
                        {
                            'type': 'image_url',
                            'image_url': {'url': f"data:image/jpeg;base64,{encoded_image}"},
                        },
                    ],
                },
            ],
        )

        content = response.choices[0].message.content or '{}'
        parsed = self._parse_json_response(content)
        return {
            'is_manipulated': bool(parsed.get('is_manipulated', False)),
            'deepfake_score': parsed.get('deepfake_score', 0),
            'explanation': parsed.get('explanation', ''),
        }

    def analyze_audio_transcript(self, transcript: str) -> dict[str, Any]:
        response = self.client.chat.completions.create(
            model='gpt-4o',
            temperature=0.2,
            response_format={'type': 'json_object'},
            messages=[
                {'role': 'system', 'content': self.AUDIO_SYSTEM_PROMPT},
                {
                    'role': 'user',
                    'content': (
                        "Analyse cette transcription audio et identifie les signaux de désinformation:\n\n"
                        f"{transcript}"
                    ),
                },
            ],
        )

        content = response.choices[0].message.content or '{}'
        return self._parse_json_response(content)
