from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer, CustomUserUpdateSerializer
from rest_framework_simplejwt.tokens import AccessToken


class RegisterUserView(CreateAPIView):
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()


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
        if not token:
            return Response({"detail": "Токен не найден."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            access_token = AccessToken(token.split()[1])
            user_id = access_token['user_id']
            if user_id != int(kwargs['pk']):
                return Response({"detail": "Нет прав для обновления данных другого пользователя."},
                                status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return self.partial_update(request, *args, **kwargs)


class UserByIdDetailView(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
