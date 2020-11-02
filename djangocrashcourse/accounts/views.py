from django.shortcuts import render
from .models import *

# Create your views here.
def Home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    total_delivered_orders = orders.filter(status='Delivered').count()
    total_pending_orders = orders.filter(status='Pending').count()

    data = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_delivered_orders': total_delivered_orders,
        'total_pending_orders': total_pending_orders
    }

    return render(request, 'accounts/dashboard.html', data)

def Products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})

def Customers(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    orders = customer.order_set.all()

    data = {
        'customer': customer,
        'orders': orders
    }

    return render(request, 'accounts/customer.html', data)
