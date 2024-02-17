from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("orders/", orders, name="orders"),
    path("admin-products/", admin_products, name="admin-products"),
    path("edit-product/<str:pk>", edit_product, name="edit-product"),
    path("customers/", customers, name="customers"),
    ]