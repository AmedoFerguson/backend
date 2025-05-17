from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from users.serializers import (
    CustomUserSerializer,
    CustomTokenObtainPairSerializer,
    CustomUserUpdateSerializer
)

User = get_user_model()


class UserInfoMixin:
    def get_user_data(self, user):
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_staff,
        }


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.copy()
        data['password'] = make_password(data.get('password'))
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserInfoView(UserInfoMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = self.get_user_data(user)
        return Response(data, status=status.HTTP_200_OK)


class UserTokenInfoView(UserInfoMixin, APIView):
    def post(self, request):
        token_str = request.data.get("token")

        if not token_str:
            return Response({"error": "Токен не передано."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = AccessToken(token_str)
            user_id = token.get("user_id")
            user = User.objects.get(id=user_id)
        except Exception:
            return Response({"error": "Недійсний токен."}, status=status.HTTP_401_UNAUTHORIZED)

        data = self.get_user_data(user)
        return Response(data, status=status.HTTP_200_OK)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = CustomUserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserByIdDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "Користувача не знайдено."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "Користувача не знайдено."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)