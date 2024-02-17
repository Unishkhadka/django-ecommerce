from django.shortcuts import render


def dashboard(request):
    return render(request, "admins/dashboard.html")


def orders(request):
    return render(request, "admins/orders.html")


def admin_products(request):
    return render(request, "admins/admin-products.html")


def customers(request):
    return render(request, "admins/customers.html")
