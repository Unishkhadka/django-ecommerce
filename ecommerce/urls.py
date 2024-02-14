from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("products/", products, name="products"),
    path("cart/", cart, name="cart"),
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    path("cart-item-decrease/", cart_item_decrease, name="cart-item-decrease"),
    path("delete-cart/", cart_item_delete, name="delete-cart"),
    path("checkout/", checkout, name="checkout"),
    path("payment/", payment, name="payment"),
    path("orders/", orders, name="orders"),
    path("products/", products, name="search"),
    path("product/<str:pk>", single_product, name="product"),
]