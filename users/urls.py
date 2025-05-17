from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),  # Регистрация
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),  # Логин
    path('token/refresh/', views.MyTokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
    path('auth/users/<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),  # Обновление пользователя
    path('user/', views.UserDetailView.as_view(), name='user-detail'),  # Текущий пользователь
    path('users/<int:pk>/', views.UserByIdDetailView.as_view(), name='user-by-id'),  # Пользователь по ID
]
