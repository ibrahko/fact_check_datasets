from django.contrib import admin

from .models import FactCheck


@admin.register(FactCheck)
class FactCheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content_type', 'verdict', 'confidence_score', 'created_at']
    list_filter = ['content_type', 'verdict', 'created_at']
    search_fields = ['title', 'raw_input', 'source_url']
