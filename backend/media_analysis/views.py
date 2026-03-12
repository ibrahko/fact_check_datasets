from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MediaFile
from .serializers import MediaFileSerializer
from .tasks import process_media_file


class MediaFileUploadView(viewsets.ModelViewSet):
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MediaFile.objects.filter(fact_check__user=self.request.user)

    def perform_create(self, serializer):
        media_file = serializer.save()
        process_media_file.delay(media_file.id)

    @action(detail=True, methods=['post'], url_path='reanalyze')
    def reanalyze(self, request, pk=None):
        media_file = self.get_object()
        media_file.status = MediaFile.AnalysisStatus.PENDING
        media_file.save(update_fields=['status'])
        process_media_file.delay(media_file.id)
        return Response(
            {'detail': 'Réanalyse lancée.', 'media_file_id': media_file.id},
            status=status.HTTP_202_ACCEPTED,
        )
