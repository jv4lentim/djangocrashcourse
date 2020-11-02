from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('products/', views.Products, name="products"),
    path('customer/<int:customer_id>/', views.Customers, name="customer")
]
