from rest_framework import serializers

from .models import FactCheck


class FactCheckSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FactCheck
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
