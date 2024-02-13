from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def error_404(request, exception):
    return render(request, "ecommerce/404.html")

def index(request):
    return render(request, "ecommerce/index.html")

def search_view(request):
    if request.method == "GET":
        q = request.GET.get('search_query')
        return render(request,"ecommerce/products.html")

def products(request):
    return render(request, "ecommerce/products.html")

def contact(request):
    return render(request, "ecommerce/contact.html")

@login_required(login_url="login")
def cart(request):
    return render(request, "ecommerce/cart.html")

@login_required(login_url="login")
def orders(request):
    return render(request, "ecommerce/orders.html")
    