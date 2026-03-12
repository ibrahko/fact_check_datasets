from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from media_analysis.tasks import process_fact_check

from .models import FactCheck
from .serializers import FactCheckCreateSerializer, FactCheckSerializer


class FactCheckViewSet(viewsets.ModelViewSet):
    serializer_class = FactCheckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FactCheck.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return FactCheckCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fact_check = serializer.save(user=request.user)
        output = FactCheckSerializer(fact_check, context=self.get_serializer_context())
        return Response(output.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='auto-check')
    def auto_check(self, request, pk=None):
        fact_check = self.get_object()
        process_fact_check.delay(fact_check.id)
        return Response(
            {'detail': 'Vérification automatique lancée.', 'fact_check_id': fact_check.id},
            status=status.HTTP_202_ACCEPTED,
        )


class FactCheckListView(generics.ListAPIView):
    serializer_class = FactCheckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FactCheck.objects.filter(user=self.request.user)


class FactCheckDetailView(generics.RetrieveAPIView):
    serializer_class = FactCheckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FactCheck.objects.filter(user=self.request.user)


class FactCheckCreateView(generics.CreateAPIView):
    serializer_class = FactCheckCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fact_check = serializer.save(user=request.user)
        return Response(FactCheckSerializer(fact_check).data, status=status.HTTP_201_CREATED)


class UserFactChecksView(generics.ListAPIView):
    serializer_class = FactCheckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FactCheck.objects.filter(user=self.request.user)
