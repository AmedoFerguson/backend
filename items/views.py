from rest_framework import status, permissions, generics
from rest_framework.response import Response
from .models import Laptop
from .serializers import LaptopSerializer
from .utils import upload_image_to_imgur
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers


class LaptopPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 24

class LaptopListCreateView(generics.ListCreateAPIView):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LaptopPagination

    def perform_create(self, serializer):
        image_file = self.request.FILES.get("image")
        data = self.request.data.copy()

        if image_file:
            result = upload_image_to_imgur(image_file)
            if not result.startswith("http"):
                raise serializers.ValidationError({"image_url": f"Не вдалося завантажити зображення: {result}"})
            data["image_url"] = result

        serializer.save(owner=self.request.user, **data)

class LaptopRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        laptop = self.get_object()
        if laptop.owner != self.request.user:
            raise permissions.PermissionDenied("У вас немає прав для редагування цього ноутбука")

        image_file = self.request.FILES.get("image")
        data = self.request.data.copy()

        if image_file:
            result = upload_image_to_imgur(image_file)
            if not result.startswith("http"):
                raise serializers.ValidationError({"image_url": f"Не вдалося завантажити зображення: {result}"})
            data["image_url"] = result

        serializer.save(**data)

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise permissions.PermissionDenied("У вас немає прав для видалення цього ноутбука")
        instance.delete()
