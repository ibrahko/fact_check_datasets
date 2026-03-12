from rest_framework.routers import DefaultRouter

from .views import MediaFileViewSet

router = DefaultRouter()
router.register('', MediaFileViewSet, basename='media-file')

urlpatterns = router.urls
