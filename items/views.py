from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Laptop
from .serializers import LaptopSerializer
from .utils import upload_image_to_imgur

class BaseLaptopView(APIView):
    def get_laptop(self, pk):
        try:
            return Laptop.objects.get(pk=pk)
        except Laptop.DoesNotExist:
            return None

    def handle_image_upload(self, image_file):
        try:
            return upload_image_to_imgur(image_file)
        except Exception as e:
            return str(e)


class LaptopListCreateView(BaseLaptopView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        laptops = Laptop.objects.all()
        serializer = LaptopSerializer(laptops, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Потрібна автентифікація"}, status=status.HTTP_401_UNAUTHORIZED
            )

        data = request.data.copy()
        data["owner"] = request.user.id

        image_file = request.FILES.get("image")
        if image_file:
            result = self.handle_image_upload(image_file)
            if result.startswith("http"):
                data["image_url"] = result
            else:
                return Response({"error": f"Не вдалося завантажити зображення: {result}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LaptopSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LaptopRetrieveUpdateDeleteView(BaseLaptopView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        laptop = self.get_laptop(pk)
        if not laptop:
            return Response({"error": "Ноутбук не знайдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = LaptopSerializer(laptop)
        return Response(serializer.data)

    def put(self, request, pk):
        laptop = self.get_laptop(pk)
        if not laptop:
            return Response({"error": "Ноутбук не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        if laptop.owner != request.user:
            return Response(
                {"error": "У вас немає прав для редагування цього ноутбука"},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data.copy()
        image_file = request.FILES.get("image")
        if image_file:
            result = self.handle_image_upload(image_file)
            if result.startswith("http"):
                data["image_url"] = result
            else:
                return Response({"error": f"Не вдалося завантажити зображення: {result}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LaptopSerializer(laptop, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        laptop = self.get_laptop(pk)
        if not laptop:
            return Response({"error": "Ноутбук не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        if laptop.owner != request.user:
            return Response(
                {"error": "У вас немає прав для видалення цього ноутбука"},
                status=status.HTTP_403_FORBIDDEN,
            )

        laptop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
