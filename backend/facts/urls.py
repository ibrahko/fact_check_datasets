from rest_framework.routers import DefaultRouter

from .views import FactCheckViewSet

router = DefaultRouter()
router.register('', FactCheckViewSet, basename='fact-check')

urlpatterns = router.urls
