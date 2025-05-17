from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import (
    RegisterView,
    MyTokenObtainPairView,
    UserInfoView,
    UserTokenInfoView,
    UpdateUserView,
    UserDetailView,
    UserByIdDetailView,
    UserUpdateView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('user/', UserInfoView.as_view(), name='user-info'),
    path('user/token/', UserTokenInfoView.as_view(), name='user-token-info'),
    path('user/update/', UpdateUserView.as_view(), name='user-update'),

    path('auth/users/<int:pk>/', UserUpdateView.as_view(), name='user-update-by-id'),
    path('user/detail/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/', UserByIdDetailView.as_view(), name='user-by-id'),
]
