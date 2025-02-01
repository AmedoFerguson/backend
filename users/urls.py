from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Регистрация
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),  # Логин
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
    path('auth/users/<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),  # Убедитесь, что это правильный путь
    path('user/', views.UserDetailView.as_view(), name='user-detail'),  # Получение текущего пользователя
    path('users/<int:pk>/', views.UserByIdDetailView.as_view(), name='user-by-id'),  # Получение пользователя по ID
]
