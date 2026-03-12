from rest_framework import serializers

from .models import FactCheck


class FactCheckSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FactCheck
        fields = [
            'id',
            'title',
            'content',
            'source_url',
            'verdict',
            'confidence_score',
            'explanation',
            'created_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class FactCheckCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactCheck
        fields = ['title', 'content', 'source_url']
