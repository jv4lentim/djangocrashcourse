from django.shortcuts import render, redirect

from django.forms import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.
@unauthenticated_user
def registerCustomer(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')

            return redirect('/login')

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginCustomer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # It gets from the input fields at the login template

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Incorrect password or username, try again')

    context = {

    }
    return render(request, 'accounts/login.html', context)

def logoutCustomer(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='login')
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    total_delivered_orders = orders.filter(status='Delivered').count()
    total_pending_orders = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'total_delivered_orders': total_delivered_orders,
        'total_pending_orders': total_pending_orders
    }

    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {
        'form': form
    }
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Customers(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    orders = customer.order_set.all()

    orderFilter = OrderFilter(request.GET, queryset=orders)
    orders = orderFilter.qs

    data = {
        'customer': customer,
        'orders': orders,
        'orderFilter': orderFilter
    }

    return render(request, 'accounts/customer.html', data)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, customer_id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    
    customer = Customer.objects.get(pk=customer_id)

    formset = OrderFormSet(instance=customer, queryset=Order.objects.none())
    # form     = OrderForm(initial={'customer': customer})
    
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'form': formset
    }
    
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, order_id):

    order   = Order.objects.get(pk=order_id)
    form    = OrderForm(instance=order)

    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, order_id):

    order   = Order.objects.get(pk=order_id)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'order': order
    }
    return render(request, 'accounts/delete.html', context)
