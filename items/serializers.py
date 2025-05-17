from rest_framework import serializers
from .models import Laptop

class LaptopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laptop
        fields = '__all__'
        extra_kwargs = {
            'image_url': {'required': False},
        }
