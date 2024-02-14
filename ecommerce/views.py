from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q


def error_404(request, exception):
    return render(request, "ecommerce/404.html")


def index(request):
    return render(request, "ecommerce/index.html")


def products(request):
    q = request.GET.get("search_query")
    if q:
        products = Product.objects.filter(
            Q(product_name__icontains=q) | Q(category__category_name__icontains=q)
        )
    else:
        products = Product.objects.all()

    context = {"products": products}
    return render(request, "ecommerce/products.html", context)


def single_product(request, pk):
    product = Product.objects.get(id=pk)
    context = {"product": product}
    return render(request, "ecommerce/product.html", context)


@login_required(login_url="/login")
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart)
    context = {"cart": cart_items}
    return render(request, "ecommerce/cart.html", context)


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
def cart_item_decrease(request):
    if request.method == "POST":
        id = request.POST.get("hidden_product_id")
        product = Product.objects.get(id=id)
        existing_cart_item = CartItem.objects.filter(product=product).first()
        print(existing_cart_item.quantity)
        if existing_cart_item:
            if existing_cart_item.quantity > 1:
                existing_cart_item.quantity -= 1
                existing_cart_item.save()
            else:
                existing_cart_item.delete()
            return redirect("cart")

        return JsonResponse({"success": True})

    return render(request, "ecommerce/cart.html")


@login_required(login_url="login")
def cart_item_delete(request):
    if request.method == "POST":
        id = request.POST.get("hidden-cart-id")
        CartItem.objects.filter(product__id=id).delete()
        return redirect("cart")
    return render(request, "ecommerce/cart.html")


@login_required(login_url="login")
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    price = 0
    cart_items = CartItem.objects.filter(cart=cart)
    print(cart_items)
    for item in cart_items:
        price += item.product.price * item.quantity
    context = {"items": cart_items, "price": price}
    return render(request, "ecommerce/checkout.html", context)


@login_required(login_url="login")
def orders(request):
    return render(request, "ecommerce/orders.html")


@login_required(login_url="login")
def payment(request):
    URL = "https://a.khalti.com/api/v2/epayment/initiate/"
    cart = Cart.objects.get(user=request.user)
    price = 0
    cart_items = CartItem.objects.filter(cart=cart)
    print(cart_items)
    for item in cart_items:
        price += item.product.price * item.quantity
    payload = {
        "return_url": "http://127.0.0.1:8000/",
        "website_url": "http://127.0.0.1:8000/",
        "amount": price,
        "purchase_order_id": cart.id,
        "purchase_order_name": "test",
        "customer_info": {
            "name": request.user.full_name,
            "email": request.user.email,
            "phone": "9811496763",
        }
    }
    if request.method == "POST":
        pass
    return render(request, "ecommerce/checkout.html")
