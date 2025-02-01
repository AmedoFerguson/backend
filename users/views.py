from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer, CustomUserUpdateSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import AccessToken  # Импортируйте AccessToken


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class TokenRefreshView(TokenRefreshView):
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


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        # Проверяем, что токен есть в заголовке
        token = request.headers.get('Authorization', None)
        if token:
            try:
                access_token = AccessToken(token.split()[1])  # Разделяем токен и извлекаем его
                user_id = access_token['user_id']  # Извлекаем user_id из токена
                
                # Проверяем, что ID пользователя совпадает с тем, что в URL
                if user_id != pk:
                    return Response({"detail": "Нет прав для обновления данных другого пользователя."},
                                    status=status.HTTP_403_FORBIDDEN)

                # Извлекаем пользователя из базы
                user = get_user_model().objects.get(id=user_id)
                
                # Применяем сериализатор с частичным обновлением
                serializer = CustomUserUpdateSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Токен не найден."}, status=status.HTTP_400_BAD_REQUEST)


class UserByIdDetailView(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
