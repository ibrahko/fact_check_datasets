from django.conf import settings
from django.db import models


class FactCheck(models.Model):
    class Verdict(models.TextChoices):
        VRAI = 'VRAI', 'Vrai'
        FAUX = 'FAUX', 'Faux'
        PARTIELLEMENT_VRAI = 'PARTIELLEMENT_VRAI', 'Partiellement vrai'
        NON_VERIFIE = 'NON_VERIFIE', 'Non vérifié'

    title = models.CharField(max_length=255)
    content = models.TextField()
    source_url = models.URLField(blank=True)
    verdict = models.CharField(max_length=30, choices=Verdict.choices, default=Verdict.NON_VERIFIE)
    confidence_score = models.FloatField(default=0)
    explanation = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fact_checks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
