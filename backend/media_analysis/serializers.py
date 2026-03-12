from rest_framework import serializers

from .models import MediaFile


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = '__all__'
        read_only_fields = ['id', 'deepfake_score', 'confidence', 'analysis_result', 'status', 'created_at']


class MediaFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['fact_check', 'media_type', 'file']
