# urls.py
from django.urls import path
from .views import (
    RegisterView,
    MyTokenObtainPairView,
    TokenRefreshView,
    UserDetailView,
    UserUpdateView,
    UserByIdDetailView,
    IsAdminView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/users/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/', UserByIdDetailView.as_view(), name='user-by-id'),
    path('admin-check/', IsAdminView.as_view(), name='admin-check'),
]
