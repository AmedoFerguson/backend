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


class UserService:
    @staticmethod
    def validate_update_permission(token, user_id_to_edit):
        if not token:
            raise PermissionError("Токен не найден.")
        try:
            access_token = AccessToken(token.split()[1])
            user_id = access_token['user_id']
            if user_id != int(user_id_to_edit):
                raise PermissionError("Нет прав для обновления данных другого пользователя.")
        except Exception as e:
            raise PermissionError(str(e))


class RegisterUserView(CreateAPIView):
    serializer_class = CustomUserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    pass


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return Response(data)


class UserUpdateView(UpdateAPIView):
    serializer_class = CustomUserUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = get_user_model().objects.all()
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        user_id_to_edit = kwargs.get('pk')

        try:
            UserService.validate_update_permission(token, user_id_to_edit)
        except PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        return self.partial_update(request, *args, **kwargs)


class UserByIdDetailView(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
