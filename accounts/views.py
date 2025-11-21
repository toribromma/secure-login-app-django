from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

@require_http_methods(["GET", "POST"])
@ratelimit(key="ip", rate="5/m", block=True)
def login_view(request):
    if request.user.is_authenticated:
        return redirect("me")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("me")
    return render(request, "login.html", {"form": form})

@require_http_methods(["GET", "POST"])
@ratelimit(key="ip", rate="5/m", block=True)
def register_view(request):
    if request.user.is_authenticated:
        return redirect("me")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        messages.success(request, "Account created. Please log in.")
        return redirect("login")
    return render(request, "register.html", {"form": form})

@login_required
def me_view(request):
    return render(request, "me.html", {"user": request.user})

def logout_view(request):
    logout(request)
    return redirect("login")
