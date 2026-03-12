from django.contrib import admin

from .models import MediaFile


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'fact_check', 'media_type', 'status', 'deepfake_score', 'created_at']
    list_filter = ['media_type', 'status', 'created_at']
