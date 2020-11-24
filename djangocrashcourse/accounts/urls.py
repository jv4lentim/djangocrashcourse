from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('products/', views.Products, name="products"),
    path('customer/<int:customer_id>/', views.Customers, name="customer"),
    path('user/', views.userPage, name="user_page"),
    path('account/', views.accountSettings, name="account"),

    path('create_order/<int:customer_id>', views.createOrder, name="create_order"),
    path('update_order/<int:order_id>', views.updateOrder, name="update_order"),
    path('delete_order/<int:order_id>', views.deleteOrder, name="delete_order"),

    path('register/', views.registerCustomer, name="register_customer"),
    path('login/', views.loginCustomer, name="login"),
    path('logout/', views.logoutCustomer, name="logout_customer")
]
