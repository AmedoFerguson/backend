from django.urls import path
from .views import LaptopListCreateView, LaptopRetrieveUpdateDeleteView

urlpatterns = [
    path('items/', LaptopListCreateView.as_view(), name='laptop-list-create'),
    path('items/<int:pk>/', LaptopRetrieveUpdateDeleteView.as_view(), name='laptop-detail'),
]
