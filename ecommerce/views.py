from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.http import JsonResponse


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
    context = {"product": product}
    return render(request, "ecommerce/product.html", context)


def contact(request):
    return render(request, "ecommerce/contact.html")


@login_required(login_url="login")
def cart(request):
    return render(request, "ecommerce/cart.html")


@login_required(login_url="login")
def add_to_cart(request):
    if (
        request.method == "POST"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):
        product = Product.objects.get(id=request.POST["hidden_product_id"])
        user = request.user
        existing_cart = Cart.objects.filter(user=user).first()
        if existing_cart:
            existing_cart_item = CartItem.objects.filter(
                cart=existing_cart, product=product
            ).first()

            if existing_cart_item:
                existing_cart_item.quantity += 1
                existing_cart_item.save()
            else:
                cart = CartItem.objects.create(
                    cart=existing_cart, product=product, quantity=1
                )
                cart.save()
            return JsonResponse({"success": True})
        else:
            my_cart = Cart.objects.create(user=user)
            my_cart.save()
            my_cart = Cart.objects.filter(user=user).first()
            cart_items = CartItem.objects.create(
                cart=my_cart, product=product, quantity=1
            )
            cart_items.save()
            return JsonResponse({"success": True})

    return render(request, "ecommerce/products.html")


@login_required(login_url="login")
def cart_item_increase(request):
    if request.method == "POST":
        pass
    return render(request, "ecommerce/cart.html")


@login_required(login_url="login")
def orders(request):
    return render(request, "ecommerce/orders.html")
