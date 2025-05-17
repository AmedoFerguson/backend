# views.py (ООП подход)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Laptop
from .serializers import LaptopSerializer
from .utils import upload_image_to_imgur


class LaptopService:
    def list_laptops(self):
        return Laptop.objects.all()

    def create_laptop(self, data, user, image_file=None):
        data = data.copy()
        data["owner"] = user.id

        if image_file:
            image_url = upload_image_to_imgur(image_file)
            data["image_url"] = image_url

        serializer = LaptopSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

    def get_laptop(self, pk):
        try:
            return Laptop.objects.get(pk=pk)
        except Laptop.DoesNotExist:
            return None

    def update_laptop(self, laptop, data, image_file=None):
        data = data.copy()

        if image_file:
            image_url = upload_image_to_imgur(image_file)
            data["image_url"] = image_url

        serializer = LaptopSerializer(laptop, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer


class LaptopListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    service = LaptopService()

    def get(self, request):
        laptops = self.service.list_laptops()
        serializer = LaptopSerializer(laptops, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        image_file = request.FILES.get("image")

        try:
            serializer = self.service.create_laptop(request.data, request.user, image_file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LaptopRetrieveUpdateDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    service = LaptopService()

    def get(self, request, pk):
        laptop = self.service.get_laptop(pk)
        if not laptop:
            return Response({"error": "Laptop not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = LaptopSerializer(laptop)
        return Response(serializer.data)

    def put(self, request, pk):
        laptop = self.service.get_laptop(pk)
        if not laptop:
            return Response({"error": "Laptop not found"}, status=status.HTTP_404_NOT_FOUND)

        if laptop.owner != request.user:
            return Response({"error": "You do not have permission to edit this laptop."}, status=status.HTTP_403_FORBIDDEN)

        image_file = request.FILES.get("image")

        try:
            serializer = self.service.update_laptop(laptop, request.data, image_file)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        laptop = self.service.get_laptop(pk)
        if not laptop:
            return Response({"error": "Laptop not found"}, status=status.HTTP_404_NOT_FOUND)

        if laptop.owner != request.user:
            return Response({"error": "You do not have permission to delete this laptop."}, status=status.HTTP_403_FORBIDDEN)

        laptop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)