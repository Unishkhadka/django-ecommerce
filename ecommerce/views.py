from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum
from django.db.models import Q
import requests
import json
from .models import *
import math


def error_404(request, exception):
    return render(request, "ecommerce/404.html")

def index(request):
    if request.method == "GET":
        # Fetch query parameters
        status = request.GET.get('status')
        purchase_order_id = request.GET.get('purchase_order_id')
        
        # Check if the status is 'Completed'
        if status == 'Completed' and purchase_order_id:
            # Update the status of the corresponding payment
            try:
                payment = Payment.objects.get(order__id=purchase_order_id)
                payment.status = 'success'  # Assuming the status field in Payment model
                payment.save()
            except Payment.DoesNotExist:
                # Handle case where no corresponding payment is found
                pass
        else:
            pass

    # Render the index page (you can adjust this based on your requirements)
    return render(request, "ecommerce/index.html")


def products(request):
    q = request.GET.get("search_query")
    if q:
        p = Product.objects.filter(
            Q(product_name__icontains=q) | Q(category__category_name__icontains=q)
        )
    else:
        p = Product.objects.all()
        q = ""

    paginator = Paginator(p, 3)
    pg_no = request.GET.get("page")
    page_obj = paginator.get_page(pg_no)
    total_pages = range(1, paginator.num_pages + 1)
    avail_pages = paginator.num_pages > 1
    context = {
        "query": q,
        "avail_pages": avail_pages,
        "total_pages": total_pages,
        "page_obj": page_obj,
    }
    return render(request, "ecommerce/products.html", context)


def single_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        review = Review()
        review.product = product
        review.review = request.POST.get("review")
        review.user = request.user
        review.rating = request.POST.get("rating")
        review.save()
    reviews = Review.objects.filter(product=product)
    total = Review.objects.aggregate(total=Sum("rating"))["total"]
    if reviews.count() > 0:
        average_rating = math.floor(total / reviews.count())
    else:
        average_rating = 0
    context = {"product": product, "reviews": reviews, "average_rating": average_rating}
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
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    my_order, created = Order.objects.get_or_create(user=request.user)
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    price = 0
    for item in cart_items:
        price += item.product.price * item.quantity
    payload = {
        "purchase_order_id": my_order.id,
        "amount": price,
        "website_url": "http://localhost:8000",
        "return_url": "http://localhost:8000/",
        "purchase_order_name": "Test Product",
    }

    headers = {"Authorization": "Key 8eb5e556328c47f2a2a4a7c9b3511b32"}

    response = requests.post(url, json=payload, headers=headers)
    res = response.json()

    for item in cart_items:
        OrderItem.objects.create(
            order=my_order, product=item.product, quantity=item.quantity
        )
    if response.status_code == 200:
        BillingAddress.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            address=address,
            address2=address2,
            state=state,
            zip_code=zip,
            user=request.user,
            order=my_order,
            payment=payment
        )
        payment = Payment(order=my_order, pidx=res['pidx'], amount=price, user=request.user)
        payment.save()
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
