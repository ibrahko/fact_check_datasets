from pathlib import Path

from .deepfake_detector import DeepfakeDetector


class CheckIAService:
    def __init__(self, detector=None):
        self.detector = detector or DeepfakeDetector()

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
            text_analysis = result['audio'].get('text_analysis', {})
            score = text_analysis.get('ai_probability', 0.0)
        else:
            score = 0.0

        return round(score * 100, 2), result
