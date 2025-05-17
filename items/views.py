from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Laptop
from .serializers import LaptopSerializer
from .utils import upload_image_to_imgur


class LaptopListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        laptops = Laptop.objects.all()
        serializer = LaptopSerializer(laptops, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED
            )

        data = request.data.copy()
        data["owner"] = request.user.id

        image_file = request.FILES.get("image")
        if image_file:
            try:
                image_url = upload_image_to_imgur(image_file)
                data["image_url"] = image_url
            except Exception as e:
                return Response({"error": f"Image upload failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LaptopSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LaptopRetrieveUpdateDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            laptop = Laptop.objects.get(pk=pk)
        except Laptop.DoesNotExist:
            return Response({"error": "Laptop not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = LaptopSerializer(laptop)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            laptop = Laptop.objects.get(pk=pk)
        except Laptop.DoesNotExist:
            return Response({"error": "Laptop not found"}, status=status.HTTP_404_NOT_FOUND)

        if laptop.owner != request.user:
            return Response(
                {"error": "You do not have permission to edit this laptop."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data.copy()

        image_file = request.FILES.get("image")
        if image_file:
            try:
                image_url = upload_image_to_imgur(image_file)
                data["image_url"] = image_url
            except Exception as e:
                return Response({"error": f"Image upload failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LaptopSerializer(laptop, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            laptop = Laptop.objects.get(pk=pk)
        except Laptop.DoesNotExist:
            return Response({"error": "Laptop not found"}, status=status.HTTP_404_NOT_FOUND)

        if laptop.owner != request.user:
            return Response(
                {"error": "You do not have permission to delete this laptop."},
                status=status.HTTP_403_FORBIDDEN,
            )

        laptop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
