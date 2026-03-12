from django.urls import path

from .views import FactCheckCreateView, FactCheckDetailView, FactCheckListView, UserFactChecksView

urlpatterns = [
    path('', FactCheckListView.as_view(), name='fact-check-list'),
    path('create/', FactCheckCreateView.as_view(), name='fact-check-create'),
    path('my-checks/', UserFactChecksView.as_view(), name='user-fact-checks'),
    path('<int:pk>/', FactCheckDetailView.as_view(), name='fact-check-detail'),
]
