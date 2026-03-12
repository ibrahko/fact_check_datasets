from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FactCheckCreateView,
    FactCheckDetailView,
    FactCheckListView,
    FactCheckViewSet,
    TrendingFactChecksView,
    UserFactChecksView,
)

router = DefaultRouter()
router.register('', FactCheckViewSet, basename='fact-check')

urlpatterns = [
    path('list/', FactCheckListView.as_view(), name='fact-check-list'),
    path('create/', FactCheckCreateView.as_view(), name='fact-check-create'),
    path('my-checks/', UserFactChecksView.as_view(), name='user-fact-checks'),
    path('trending/', TrendingFactChecksView.as_view(), name='trending-fact-checks'),
    path('detail/<int:pk>/', FactCheckDetailView.as_view(), name='fact-check-detail'),
    path('', include(router.urls)),
]
