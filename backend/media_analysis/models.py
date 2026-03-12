from django.db import models

from facts.models import FactCheck


class MediaFile(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Vidéo'
        AUDIO = 'audio', 'Audio'

    class AnalysisStatus(models.TextChoices):
        PENDING = 'pending', 'En attente'
        PROCESSING = 'processing', 'En traitement'
        DONE = 'done', 'Terminé'
        FAILED = 'failed', 'Échec'

    fact_check = models.ForeignKey(FactCheck, on_delete=models.CASCADE, related_name='media_files')
    media_type = models.CharField(max_length=20, choices=MediaType.choices)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    deepfake_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    analysis_result = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=AnalysisStatus.choices, default=AnalysisStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type} - {self.status}"
