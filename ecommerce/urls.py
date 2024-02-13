from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("products/", products, name="products"),
    path("contact/", contact, name="contact"),
    path("cart/", cart, name="cart"),
    path("orders/", orders, name="orders"),
    path("search/", search_view, name="search"),
]
