import hashlib
import io
import os
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageStat

try:
    import cv2
except ImportError:  # pragma: no cover
    cv2 = None

from openai import OpenAI


class DeepfakeDetector:
    def __init__(self, client=None, model='gpt-4o-mini', whisper_model='whisper-1'):
        if client is not None:
            self.client = client
        elif os.getenv('OPENAI_API_KEY'):
            self.client = OpenAI()
        else:
            self.client = None
        self.model = model
        self.whisper_model = whisper_model

    def analyze_image_metadata(self, image_path):
        image = Image.open(image_path)
        exif = image.getexif() or {}

        suspicious = 0
        flags = []
        software = exif.get(305)
        if software:
            software_str = str(software).lower()
            if any(token in software_str for token in ['photoshop', 'gimp', 'stable diffusion', 'midjourney']):
                suspicious += 0.35
                flags.append(f"Logiciel d'édition détecté: {software}")

        if exif and not exif.get(306):
            suspicious += 0.15
            flags.append('Date EXIF absente malgré métadonnées présentes')

        if not exif:
            suspicious += 0.20
            flags.append('Aucune métadonnée EXIF détectée')

        return {
            'manipulation_score': min(1.0, round(suspicious, 3)),
            'flags': flags,
            'exif_size': len(exif),
        }

    def detect_image_artifacts(self, image_path):
        image = Image.open(image_path).convert('RGB')

        buffer = io.BytesIO()
        image.save(buffer, 'JPEG', quality=80)
        recompressed = Image.open(io.BytesIO(buffer.getvalue())).convert('RGB')
        diff = ImageChops.difference(image, recompressed)
        diff_stat = ImageStat.Stat(diff)
        diff_mean = sum(diff_stat.mean) / len(diff_stat.mean)

        edges = image.filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        edge_mean = sum(edge_stat.mean) / len(edge_stat.mean)

        compression_score = min(1.0, diff_mean / 32.0)
        splice_score = max(0.0, min(1.0, (edge_mean - 20.0) / 80.0))

        return {
            'artifact_score': round((compression_score * 0.6) + (splice_score * 0.4), 3),
            'compression_signal': round(compression_score, 3),
            'splice_signal': round(splice_score, 3),
        }

    def analyze_video_frames(self, video_path):
        if cv2 is None:
            return {'frame_anomaly_score': 0.0, 'frames_analyzed': 0, 'warning': 'opencv-python non installé'}

        cap = cv2.VideoCapture(str(video_path))
        total = 0
        anomaly_values = []
        prev_hash = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            total += 1
            if total % 5 != 0:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.Laplacian(gray, cv2.CV_64F).var()
            frame_hash = hashlib.sha1(gray.tobytes()).hexdigest()[:16]

            hash_jump = 1.0 if prev_hash and frame_hash[:8] == prev_hash[:8] else 0.0
            blur_anomaly = max(0.0, min(1.0, (120.0 - blur) / 120.0))
            anomaly_values.append((blur_anomaly * 0.8) + (hash_jump * 0.2))
            prev_hash = frame_hash

        cap.release()
        avg = sum(anomaly_values) / len(anomaly_values) if anomaly_values else 0.0
        return {'frame_anomaly_score': round(avg, 3), 'frames_analyzed': len(anomaly_values), 'raw_frames': total}

    def transcribe_audio(self, audio_path):
        if self.client is None:
            text = ''
            return {'transcription': text, 'text_analysis': self.detect_ai_generated_text(text)}

        with Path(audio_path).open('rb') as audio_file:
            transcript = self.client.audio.transcriptions.create(model=self.whisper_model, file=audio_file)

        text = transcript.text if hasattr(transcript, 'text') else str(transcript)
        text_analysis = self.detect_ai_generated_text(text)
        return {'transcription': text, 'text_analysis': text_analysis}

    def detect_ai_generated_text(self, text):
        prompt = (
            'Analyse le texte suivant et retourne uniquement un JSON compact avec '
            'les clés ai_probability (0..1) et rationale.\nTexte:\n'
            f'{text}'
        )
        if self.client is not None:
            response = self.client.responses.create(model=self.model, input=prompt, temperature=0)
            output_text = response.output_text if hasattr(response, 'output_text') else ''
        else:
            output_text = ''

        if not output_text:
            length_penalty = min(1.0, len(text.split()) / 400)
            punctuation_ratio = text.count('.') / max(1, len(text.split()))
            score = min(1.0, (0.35 * length_penalty) + (0.65 * min(1.0, punctuation_ratio * 10)))
            return {'ai_probability': round(score, 3), 'rationale': 'Heuristique locale'}

        return {'raw_response': output_text}
