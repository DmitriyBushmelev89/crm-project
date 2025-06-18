from django.urls import path
from .views import ClientCreateView
from .views import ClientGetView

urlpatterns = [
    path('clients/', ClientCreateView.as_view()),
    path('clients/<int:pk>/', ClientGetView.as_view()),
]