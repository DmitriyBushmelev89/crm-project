from django.urls import path
from .views import ClientListCreateView
from .views import ClientGetUpdateView
from .views import ProductListCreateView
from .views import ProductGetUpdateDestroyView
from .views import OrderListCreateView
from .views import OrdersGetUpdateDestroyView


urlpatterns = [
    path('clients/', ClientListCreateView.as_view()),
    path('clients/<int:pk>/', ClientGetUpdateView.as_view()),
    path('products/', ProductListCreateView.as_view()),
    path('products/<int:pk>/', ProductGetUpdateDestroyView.as_view()),
    path('orders/', OrderListCreateView.as_view()),
    path('orders/<int:pk>/', OrdersGetUpdateDestroyView.as_view())
    ]