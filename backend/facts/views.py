from rest_framework import permissions, viewsets

from .models import FactCheck
from .serializers import FactCheckSerializer


class FactCheckViewSet(viewsets.ModelViewSet):
    serializer_class = FactCheckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FactCheck.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
