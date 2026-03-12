from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Utilisateur'
        ANALYST = 'analyst', 'Analyste'
        ADMIN = 'admin', 'Administrateur'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return self.username
