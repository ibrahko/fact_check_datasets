from rest_framework import generics, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MediaFile
from .serializers import MediaFileSerializer, MediaFileUploadSerializer
from .services.ai_service import CheckIAService
from .tasks import process_media_file


class TextAnalysisInputSerializer(serializers.Serializer):
    url = serializers.URLField(required=False, allow_blank=True)
    content = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if not attrs.get('url') and not attrs.get('content'):
            raise serializers.ValidationError('url ou content est requis.')
        return attrs


class MediaFileUploadView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MediaFile.objects.filter(fact_check__user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return MediaFileUploadSerializer
        return MediaFileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        media_file = serializer.save()
        process_media_file.delay(media_file.id)
        return Response(MediaFileSerializer(media_file).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='analyze')
    def analyze(self, request, pk=None):
        media_file = self.get_object()
        media_file.status = MediaFile.AnalysisStatus.PENDING
        media_file.save(update_fields=['status'])
        process_media_file.delay(media_file.id)
        return Response(
            {'detail': 'Analyse lancée.', 'media_file_id': media_file.id},
            status=status.HTTP_202_ACCEPTED,
        )

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


class MediaFileListView(generics.ListAPIView):
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MediaFile.objects.filter(fact_check__user=self.request.user)


class MediaFileDetailView(generics.RetrieveAPIView):
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MediaFile.objects.filter(fact_check__user=self.request.user)


class MediaFileCreateView(generics.CreateAPIView):
    serializer_class = MediaFileUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        media_file = serializer.save()
        process_media_file.delay(media_file.id)
        return Response(MediaFileSerializer(media_file).data, status=status.HTTP_201_CREATED)


class TextAnalysisView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TextAnalysisInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = CheckIAService()

        if serializer.validated_data.get('url'):
            result = service.analyze_article(serializer.validated_data['url'])
        else:
            result = service.analyze_text(serializer.validated_data.get('content', ''))

        verdict_mapping = {
            'true': 'VRAI',
            'false': 'FAUX',
            'mixed': 'INCERTAIN',
            'unknown': 'INCERTAIN',
        }
        return Response(
            {
                'verdict': verdict_mapping.get(str(result.get('verdict', 'unknown')).lower(), 'INCERTAIN'),
                'score': max(0, min(100, int(float(result.get('confidence_score', 0) or 0)))),
                'explanation': result.get('explanation', ''),
                'sources': result.get('sources_suggested', []),
            }
        )
