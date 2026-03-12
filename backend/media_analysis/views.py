from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import MediaFile
from .serializers import MediaFileSerializer, MediaFileUploadSerializer


class MediaFileUploadView(generics.CreateAPIView):
    serializer_class = MediaFileUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        media_file = serializer.save(uploaded_by=request.user)
        return Response(MediaFileSerializer(media_file).data, status=status.HTTP_201_CREATED)


class MediaFileDetailView(generics.RetrieveAPIView):
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MediaFile.objects.select_related('uploaded_by', 'fact_check').filter(uploaded_by=self.request.user)


class MediaFileListView(generics.ListAPIView):
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MediaFile.objects.select_related('uploaded_by', 'fact_check').filter(uploaded_by=self.request.user)
