from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Laptop
from .serializers import LaptopSerializer
from .utils import upload_image_to_imgur


class LaptopService:

    @staticmethod
    def get_all_laptops():
        return Laptop.objects.all()

    @staticmethod
    def get_laptop_by_id(pk):
        try:
            return Laptop.objects.get(pk=pk)
        except Laptop.DoesNotExist:
            return None

    @staticmethod
    def create_laptop(data, user, image_file=None):
        data = data.copy()
        data["owner"] = user.id

        if image_file:
            image_url = LaptopService.upload_image(image_file)
            data["image_url"] = image_url

        serializer = LaptopSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data, None
        return None, serializer.errors

    @staticmethod
    def update_laptop(laptop, data, image_file=None):
        data = data.copy()
        if image_file:
            image_url = LaptopService.upload_image(image_file)
            data["image_url"] = image_url

        serializer = LaptopSerializer(laptop, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data, None
        return None, serializer.errors

    @staticmethod
    def delete_laptop(laptop):
        laptop.delete()

    @staticmethod
    def upload_image(image_file):
        try:
            return upload_image_to_imgur(image_file)
        except Exception as e:
            raise Exception(f"Image upload failed: {str(e)}")


class LaptopListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        laptops = LaptopService.get_all_laptops()
        serializer = LaptopSerializer(laptops, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        image_file = request.FILES.get("image")
        laptop_data, errors = LaptopService.create_laptop(request.data, request.user, image_file)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(laptop_data, status=status.HTTP_201_CREATED)


class LaptopRetrieveUpdateDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        laptop = LaptopService.get_laptop_by_id(pk)
        if not laptop:
            return Response({"error": "Laptop not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LaptopSerializer(laptop)
        return Response(serializer.data)

    def put(self, request, pk):
        laptop = LaptopService.get_laptop_by_id(pk)
        if not laptop:
            return Response({"error": "Laptop not found"}, status=status.HTTP_404_NOT_FOUND)

        if laptop.owner != request.user:
            return Response(
                {"error": "You do not have permission to edit this laptop."},
                status=status.HTTP_403_FORBIDDEN,
            )

        image_file = request.FILES.get("image")
        updated_data, errors = LaptopService.update_laptop(laptop, request.data, image_file)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(updated_data)

    def delete(self, request, pk):
        laptop = LaptopService.get_laptop_by_id(pk)
        if not laptop:
            return Response({"error": "Laptop not found"}, status=status.HTTP_404_NOT_FOUND)

        if laptop.owner != request.user:
            return Response(
                {"error": "You do not have permission to delete this laptop."},
                status=status.HTTP_403_FORBIDDEN,
            )

        LaptopService.delete_laptop(laptop)
        return Response(status=status.HTTP_204_NO_CONTENT)
