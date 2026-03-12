from rest_framework import serializers

from .models import MediaFile


class MediaFileSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MediaFile
        fields = [
            'id',
            'file',
            'media_type',
            'file_url',
            'deepfake_score',
            'confidence',
            'analysis_result',
            'status',
            'fact_check',
            'uploaded_by',
            'created_at',
        ]
        read_only_fields = ['id', 'uploaded_by', 'created_at', 'deepfake_score', 'confidence', 'analysis_result', 'status']


class MediaFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['file', 'media_type', 'file_url', 'fact_check']
