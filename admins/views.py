from django.shortcuts import render, redirect
from ecommerce.models import *

def is_admin(request):
    return True if request.user.is_staff else False

def dashboard(request):
    if not is_admin(request):
        return redirect("index")
    return render(request, "admins/dashboard.html")

def orders(request):
    if not is_admin(request):
        return redirect("index")
    return render(request, "admins/orders.html")

def admin_products(request):
    if not is_admin(request):
        return redirect("index")
    if request.method == "POST":
        product_id = request.POST['product_id']  
        product = Product.objects.get(id=product_id)
        Product.delete(product)
    products = Product.objects.all()
    context = {'products':products}
    return render(request, "admins/admin-products.html", context)

def edit_product(request, pk):
    if not is_admin(request):
        return redirect("index")
    product = Product.objects.get(id=pk)
    categories = Category.objects.all()
    context = {'product':product, 'categories':categories}
    return render(request, "admins/edit_product.html", context)

def customers(request):
    if not is_admin(request):
        return redirect("index")
    if request.method == "POST":
        customer_id = request.POST['customer_id']  
        customer = User.objects.get(id=customer_id)
        User.delete(customer)
    customers = User.objects.all()
    context = {'customers':customers}
    return render(request, "admins/customers.html", context)
