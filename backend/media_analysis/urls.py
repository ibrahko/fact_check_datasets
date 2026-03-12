from django.urls import path

from .views import MediaFileDetailView, MediaFileListView, MediaFileUploadView

urlpatterns = [
    path('upload/', MediaFileUploadView.as_view(), name='media-upload'),
    path('my-files/', MediaFileListView.as_view(), name='media-list'),
    path('<int:pk>/', MediaFileDetailView.as_view(), name='media-detail'),
]
