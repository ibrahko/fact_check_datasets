from django.urls import path

from .views import ChangePasswordView, LoginView, LogoutView, ProfileView, RegisterView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('me/', ProfileView.as_view(), name='profile-me'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('', UserListView.as_view(), name='user-list'),
]
