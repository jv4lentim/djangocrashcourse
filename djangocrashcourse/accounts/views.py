from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request, 'accounts/dashboard.html')

def Products(request):
    return render(request, 'accounts/products.html')

def Customer(request):
    return render(request, 'accounts/customer.html')