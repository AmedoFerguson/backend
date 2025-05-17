from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.LaptopListCreateView.as_view(), name='laptop-list-create'),
    path('items/<int:pk>/', views.LaptopRetrieveUpdateDeleteView.as_view(), name='laptop-detail'),
]
