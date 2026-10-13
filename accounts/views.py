from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from .form import LoginForm


# Create your views here.
def login(request):
    if request.method == "GET":
        return render(
            request,
            "auth/login.html",
            {"form": LoginForm()}
        )

    form = LoginForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("post:post_list")

        return HttpResponse("Invalid credentials", status=401)

    return render(
        request,
        "auth/login.html",
        {"form": form}
    )
def user_detail(request, id):
    user = get_object_or_404(User,id=id)
    return render(request,"auth/user_detail.html",{"user":user})

import random





def send_reset_code(request):

    email = "thaddevstudios@gmail.com"

    code = str(random.randint(1000, 9999))

    send_mail(
        subject="Your Password Reset Code",
        message=f"Your password reset code is {code}.",
        from_email=None,
        recipient_list=[email],
    )

    return HttpResponse("Reset code sent!")





def signin():
    ...