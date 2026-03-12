from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import FactCheck
from .serializers import FactCheckCreateSerializer, FactCheckSerializer


class FactCheckListView(generics.ListAPIView):
    queryset = FactCheck.objects.select_related('created_by').all()
    serializer_class = FactCheckSerializer
    permission_classes = [permissions.IsAuthenticated]


class FactCheckDetailView(generics.RetrieveAPIView):
    queryset = FactCheck.objects.select_related('created_by').all()
    serializer_class = FactCheckSerializer
    permission_classes = [permissions.IsAuthenticated]


class FactCheckCreateView(generics.CreateAPIView):
    serializer_class = FactCheckCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fact_check = serializer.save(created_by=request.user)
        return Response(FactCheckSerializer(fact_check).data, status=status.HTTP_201_CREATED)


class UserFactChecksView(generics.ListAPIView):
    serializer_class = FactCheckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FactCheck.objects.select_related('created_by').filter(created_by=self.request.user)
