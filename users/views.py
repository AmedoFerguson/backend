from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

from .serializers import (
    CustomUserSerializer,
    CustomTokenObtainPairSerializer,
    CustomUserUpdateSerializer,
)


User = get_user_model()


# ==== Сервісний клас ====

class UserService:
    @staticmethod
    def validate_update_permission(token: str, user_id_to_edit: int) -> None:
        """
        Перевіряє, чи користувач має право редагувати дані.
        """
        if not token:
            raise PermissionError("Токен не знайдено.")

        try:
            # Витяг id з токену
            access_token = AccessToken(token.split()[1])
            user_id = access_token['user_id']
            if user_id != int(user_id_to_edit):
                raise PermissionError("Немає прав для редагування даних іншого користувача.")
        except Exception as e:
            raise PermissionError(f"Помилка перевірки токена: {str(e)}")


# ==== Реєстрація ====

class RegisterUserView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()


# ==== Отримання токена ====

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    pass


# ==== Деталі поточного користувача ====

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Повертає інформацію про поточного користувача.
        """
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
        }
        return Response(data)


# ==== Оновлення користувача ====

class UserUpdateView(UpdateAPIView):
    serializer_class = CustomUserUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        user_id_to_edit = kwargs.get('pk')

        try:
            UserService.validate_update_permission(token, user_id_to_edit)
        except PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        return self.partial_update(request, *args, **kwargs)


# ==== Перегляд користувача по ID ====

class UserByIdDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
