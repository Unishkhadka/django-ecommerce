from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
import requests
import json
from django.core.paginator import Paginator
from .models import *


def error_404(request, exception):
    return render(request, "ecommerce/404.html")


def index(request):
    """http://localhost:8000/?pidx=6Y3erRKfCqSStkzAzFmA7b&transaction_id=RkcfL8abKMRwrXF6oqNSFg&tidx=RkcfL8abKMRwrXF6oqNSFg&amount=100000&total_amount=100000&mobile=98XXXXX001&status=Completed&purchase_order_id=4235&purchase_order_name=Test%20Product"""

    # get status from  url update status to completed if completed
    # save billing address
    return render(request, "ecommerce/index.html")


def products(request):
    q = request.GET.get("search_query")
    if q:
        p = Product.objects.filter(
            Q(product_name__icontains=q) | Q(category__category_name__icontains=q)
        )
    else:
        p = Product.objects.all()
        q=''

    paginator = Paginator(p, 3)
    pg_no = request.GET.get("page")
    page_obj = paginator.get_page(pg_no)
    total_pages = range(1, paginator.num_pages + 1)
    avail_pages = paginator.num_pages>1
    context = {'query':q,"avail_pages":avail_pages,"total_pages": total_pages, "page_obj": page_obj}
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
def payment(request):
    if request.method == "POST":
        fname = request.POST.get("First Name")
        lname = request.POST.get("Last Name")
        email = request.POST.get("Email")
        address = request.POST.get("Address")
        address2 = request.POST.get("Address2")
        state = request.POST.get("State")
        zip = request.POST.get("zip code")

        for key, value in request.POST.items():
            if not value:
                messages.error(request, f"Please enter {key}")
                return redirect("checkout")
        order = Order.objects.create(user=request.user)
        BillingAddress.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            address=address,
            address2=address2,
            state=state,
            zip_code=zip,
            user=request.user,
            order=order,
        )
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    my_order = Order.objects.get(user=request.user)
    for item in cart_items:
        OrderItem.objects.create(
            order=my_order, product=item.product, quantity=item.quantity
        )
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    price = 0
    for item in cart_items:
        price += item.product.price * item.quantity
    payload = {
        "purchase_order_id": "4235",
        "amount": 100000,
        "website_url": "http://localhost:8000",
        "return_url": "http://localhost:8000/",
        "purchase_order_name": "Test Product",
    }

    headers = {"Authorization": "Key 8eb5e556328c47f2a2a4a7c9b3511b32"}

    response = requests.post(url, json=payload, headers=headers)
    res = response.json()
    if response.status_code == 200:
        # NOTE: create order
        # create order items where order = order, products and amount will come from cart items
        # create payment user=user, order=order, amount=price, default initiated
        return redirect(res["payment_url"])
    return render(request, "ecommerce/checkout.html")


@login_required(login_url="login")
def orders(request):
    return render(request, "ecommerce/orders.html")


@login_required(login_url="login")
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    price = 0
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        price += item.product.price * item.quantity
    context = {"items": cart_items, "price": price}
    return render(request, "ecommerce/checkout.html", context)
