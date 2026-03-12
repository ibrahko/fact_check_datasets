from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from media_analysis.tasks import process_fact_check

from .models import FactCheck
from .serializers import FactCheckSerializer


class FactCheckViewSet(viewsets.ModelViewSet):
    serializer_class = FactCheckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FactCheck.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='auto-check')
    def auto_check(self, request, pk=None):
        fact_check = self.get_object()
        process_fact_check.delay(fact_check.id)
        return Response(
            {'detail': 'Vérification automatique lancée.', 'fact_check_id': fact_check.id},
            status=status.HTTP_202_ACCEPTED,
        )
