from rest_framework import serializers

from .models import FactCheck


class FactCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactCheck
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'verdict', 'confidence_score', 'ai_summary']


class FactCheckCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactCheck
        fields = ['title', 'source_url', 'raw_input', 'content_type', 'is_public']
