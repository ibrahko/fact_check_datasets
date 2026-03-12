from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MediaFileCreateView, MediaFileDetailView, MediaFileListView, MediaFileUploadView, TextAnalysisView

router = DefaultRouter()
router.register('', MediaFileUploadView, basename='media-file')

urlpatterns = [
    path('upload/', MediaFileCreateView.as_view(), name='media-upload'),
    path('analysis/text/', TextAnalysisView.as_view(), name='text-analysis'),
    path('my-files/', MediaFileListView.as_view(), name='media-list'),
    path('detail/<int:pk>/', MediaFileDetailView.as_view(), name='media-detail'),
    path('', include(router.urls)),
]
