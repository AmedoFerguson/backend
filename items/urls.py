from django.urls import path
from .views import LaptopModelsListView  
from .views import LaptopListCreateView, LaptopRetrieveUpdateDestroyView

urlpatterns = [
    path('items/', LaptopListCreateView.as_view(), name='laptop-list-create'),
    path('items/<int:pk>/', LaptopRetrieveUpdateDestroyView.as_view(), name='laptop-detail'),
    path('items/models/', LaptopModelsListView.as_view(), name='laptop-models'),  
]
