from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("orders/", orders, name="orders"),
    path("admin-products/", admin_products, name="admin-products"),
    path("edit-product/<str:pk>", edit_product, name="edit-product"),
    path("add-product/", add_product, name="add-product"),
    path("customers/", customers, name="customers"),
    ]