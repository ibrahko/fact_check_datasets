from django.conf import settings
from django.db import models

from facts.models import FactCheck


class MediaFile(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'IMAGE', 'Image'
        AUDIO = 'AUDIO', 'Audio'
        VIDEO = 'VIDEO', 'Vidéo'
        ARTICLE = 'ARTICLE', 'Article'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        PROCESSING = 'PROCESSING', 'En cours'
        COMPLETED = 'COMPLETED', 'Terminé'
        FAILED = 'FAILED', 'Échec'

    file = models.FileField(upload_to='media_uploads/%Y/%m/%d/')
    media_type = models.CharField(max_length=10, choices=MediaType.choices)
    file_url = models.URLField(blank=True)
    deepfake_score = models.FloatField(null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    analysis_result = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    fact_check = models.ForeignKey(
        FactCheck,
        on_delete=models.SET_NULL,
        related_name='media_files',
        null=True,
        blank=True,
    )
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='media_files')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.media_type} - {self.status}"
