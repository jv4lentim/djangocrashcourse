from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home),
    path('products/', views.Products),
    path('customer/', views.Customer)
]
