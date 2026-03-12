from django.urls import path

from .views import ProfileView, RegisterView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', ProfileView.as_view(), name='profile'),
    path('', UserListView.as_view(), name='user-list'),
]
