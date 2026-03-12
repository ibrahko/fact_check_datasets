from django.urls import path

from .views import ProfileView, UserListView

urlpatterns = [
    path('me/', ProfileView.as_view(), name='profile'),
    path('', UserListView.as_view(), name='user-list'),
]
