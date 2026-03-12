from rest_framework.routers import DefaultRouter

from .views import MediaFileUploadView

router = DefaultRouter()
router.register('', MediaFileUploadView, basename='media-file')

urlpatterns = router.urls
