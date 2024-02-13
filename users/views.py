from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from users.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# @user_passes_test()
def login_page(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password )

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials!")

    return render(request, "users/login.html")

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password != cpassword:
            messages.error(request, "Password and Confirm password doesn't match.")
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email not available!")
        else:
            created_user = CustomUser.objects.create_user(email=email, full_name=name, password=password)
            login(request, created_user)
            return redirect("index")

    return render(request, "users/signup.html")

@login_required(login_url="login")
def logout_user(request):
    logout(request)
    message = messages.success(request,"User logged out!")
    context = {'message':message}
    return render(request, "ecommerce/index.html", context)
