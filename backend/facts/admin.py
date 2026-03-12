from django.contrib import admin

from .models import FactCheck


@admin.register(FactCheck)
class FactCheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'verdict', 'confidence_score', 'created_by', 'created_at']
    list_filter = ['verdict', 'created_at']
    search_fields = ['title', 'content', 'source_url']
