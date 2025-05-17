# views.py (ООП-подход)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView
from .serializers import (
    CustomUserSerializer,
    CustomTokenObtainPairSerializer,
    CustomUserUpdateSerializer
)
from .services import UserService


class BaseUserView(APIView):
    permission_classes = [IsAuthenticated]
    user_service_class = UserService

    def get_user_service(self):
        return self.user_service_class()


class RegisterView(APIView):
    def post(self, request):
        user_service = UserService()
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = user_service.create_user(serializer.validated_data)
            return Response(CustomUserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class TokenRefreshView(TokenRefreshView):
    pass


class UserDetailView(BaseUserView):
    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })


class UserUpdateView(BaseUserView):
    def patch(self, request, pk):
        if request.user.id != pk:
            return Response({"detail": "Нет прав для обновления другого пользователя."}, status=status.HTTP_403_FORBIDDEN)
        user_service = self.get_user_service()
        updated_user = user_service.update_user(request.user, request.data)
        return Response(CustomUserSerializer(updated_user).data, status=status.HTTP_200_OK)


class UserByIdDetailView(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class IsAdminView(BaseUserView):
    def get(self, request):
        return Response({"is_admin": request.user.is_staff})
