from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MediaFile
from .serializers import MediaFileSerializer
from .services import CheckIAService


class MediaFileViewSet(viewsets.ModelViewSet):
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    ai_service_class = CheckIAService

    def get_queryset(self):
        return MediaFile.objects.filter(fact_check__user=self.request.user)

    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        media = self.get_object()
        media.status = MediaFile.AnalysisStatus.PROCESSING
        media.save(update_fields=['status'])

        try:
            score, result = self.ai_service_class().analyze_media(media)
            media.deepfake_score = score
            media.analysis_result = result
            media.status = MediaFile.AnalysisStatus.DONE
            media.save(update_fields=['deepfake_score', 'analysis_result', 'status'])
        except Exception as exc:  # noqa: BLE001
            media.status = MediaFile.AnalysisStatus.FAILED
            media.analysis_result = {'error': str(exc)}
            media.save(update_fields=['status', 'analysis_result'])
            return Response(media.analysis_result, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(media)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reanalyze(self, request, pk=None):
        return self.analyze(request, pk)
