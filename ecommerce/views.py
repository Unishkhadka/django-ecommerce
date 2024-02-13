from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *


def error_404(request, exception):
    return render(request, "ecommerce/404.html")


def index(request):
    return render(request, "ecommerce/index.html")


def products(request):
    q = request.GET.get("search_query")
    if q:
        products = Product.objects.filter(product_name__icontains=q)
    else:
        products = Product.objects.all()

    context = {"products": products}
    return render(request, "ecommerce/products.html", context)

def single_product(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product':product}
    return render(request, "ecommerce/product.html", context)

def contact(request):
    return render(request, "ecommerce/contact.html")


@login_required(login_url="login")
def cart(request):
    return render(request, "ecommerce/cart.html")


@login_required(login_url="login")
def orders(request):
    return render(request, "ecommerce/orders.html")
