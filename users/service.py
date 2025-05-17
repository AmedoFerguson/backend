# services.py
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserService:
    def create_user(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

    def update_user(self, user_instance, validated_data):
        for attr, value in validated_data.items():
            setattr(user_instance, attr, value)
        user_instance.save()
        return user_instance
