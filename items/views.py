from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Laptop
from .serializers import LaptopSerializer
from .utils import upload_image_to_imgur


class LaptopService:
    @staticmethod
    def upload_image(image_file):
        if image_file:
            return upload_image_to_imgur(image_file)
        return None

    @staticmethod
    def check_owner(laptop, user):
        return laptop.owner == user


class LaptopListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        laptops = Laptop.objects.all()
        serializer = LaptopSerializer(laptops, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data["owner"] = request.user.pk

        image_file = request.FILES.get("image")
        if image_file:
            try:
                image_url = LaptopService.upload_image(image_file)
                if image_url:
                    data["image_url"] = image_url
            except Exception as e:
                return Response({"detail": f"Image upload failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LaptopSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LaptopRetrieveUpdateDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Laptop, pk=pk)

    def get(self, request, pk):
        laptop = self.get_object(pk)
        serializer = LaptopSerializer(laptop)
        return Response(serializer.data)

    def put(self, request, pk):
        laptop = self.get_object(pk)

        if not LaptopService.check_owner(laptop, request.user):
            return Response({"detail": "You do not have permission to edit this laptop."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        image_file = request.FILES.get("image")
        if image_file:
            try:
                image_url = LaptopService.upload_image(image_file)
                if image_url:
                    data["image_url"] = image_url
            except Exception as e:
                return Response({"detail": f"Image upload failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LaptopSerializer(laptop, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        laptop = self.get_object(pk)

        if not LaptopService.check_owner(laptop, request.user):
            return Response({"detail": "You do not have permission to delete this laptop."}, status=status.HTTP_403_FORBIDDEN)

        laptop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
