from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Laptop
from .serializers import LaptopSerializer
from .utils import upload_image_to_imgur
from rest_framework import serializers


class LaptopListCreateView(generics.ListCreateAPIView):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        data = self.request.data.copy()

        image_file = self.request.FILES.get("image")
        if image_file:
            try:
                image_url = upload_image_to_imgur(image_file)
                data["image_url"] = image_url
            except Exception as e:
                raise serializers.ValidationError({"image": f"Image upload failed: {str(e)}"})

        serializer.save(owner=self.request.user, **data)


class LaptopRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ['PUT', 'DELETE'] and obj.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to modify this laptop.")
        return obj

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        image_file = request.FILES.get("image")
        if image_file:
            try:
                image_url = upload_image_to_imgur(image_file)
                data["image_url"] = image_url
            except Exception as e:
                return Response({"error": f"Image upload failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
