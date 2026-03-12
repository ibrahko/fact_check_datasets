from django.conf import settings
from django.db import models


class FactCheck(models.Model):
    class ContentType(models.TextChoices):
        ARTICLE = 'article', 'Article'
        BLOG = 'blog', 'Blog'
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Vidéo'
        AUDIO = 'audio', 'Audio'

    class Verdict(models.TextChoices):
        TRUE = 'true', 'Vrai'
        FALSE = 'false', 'Faux'
        MIXED = 'mixed', 'Mitigé'
        UNKNOWN = 'unknown', 'Inconnu'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fact_checks')
    title = models.CharField(max_length=255)
    source_url = models.URLField(blank=True)
    raw_input = models.TextField()
    content_type = models.CharField(max_length=20, choices=ContentType.choices)
    is_public = models.BooleanField(default=True)
    ai_summary = models.TextField(blank=True)
    verdict = models.CharField(max_length=20, choices=Verdict.choices, default=Verdict.UNKNOWN)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.verdict})"
