from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("products/", products, name="products"),
    path("contact/", contact, name="contact"),
    path("cart/", cart, name="cart"),
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    path("orders/", orders, name="orders"),
    path("products/", products, name="search"),
    path("product/<str:pk>", single_product, name="product"),
]
