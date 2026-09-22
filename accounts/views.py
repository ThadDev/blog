from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .form import LoginForm


# Create your views here.
def login(request):
    if request.method == "GET":
        return render(
            request,
            "post/login.html",
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
            return redirect("user_detail", id=user.id)

        return HttpResponse("Invalid credentials", status=401)

    return render(
        request,
        "post/login.html",
        {"form": form}
    )