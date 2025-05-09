from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def login_view(request):
    form = LoginForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            remember = form.cleaned_data.get("remember_me")

            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password")
                return render(request, "login.html", {"form": form})

            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)

                if not remember:
                    request.session.set_expiry(0)  

                return redirect("home")
            else:
                messages.error(request, "Invalid email or password")

    return render(request, "login.html", {"form": form})



def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})