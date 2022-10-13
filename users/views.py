from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, RegisterForm, UserChangeForm

User = get_user_model()


def register_user_profile(request):
    if request.user.is_authenticated:
        return redirect("feed_page_view")
    else:
        form = RegisterForm(data=request.POST or None, files=request.FILES or None)
        if form.is_valid():
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get("password1")
            user_cre = form.save(commit=False)
            user_cre.set_password(password)
            if not User.objects.all().exists():
                user_cre.is_staff = True
                user_cre.is_superuser = True
            user_cre.save()
            user_cre = authenticate(phone_number=phone_number, password=password)
            login(request, user_cre)
            return redirect("feed_page_view")
        return render(request, "signup.html", {"form": form})


def login_user_profile(request):
    if request.user.is_authenticated:
        return redirect("feed_page_view")
    else:
        form = LoginForm(request=request, data=request.POST or None)
        if form.is_valid():
            phone_number = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user_cre = authenticate(phone_number=phone_number, password=password)
            login(request, user_cre)
            if "next" in request.POST:
                next_url = request.POST.get("next")
                return redirect(next_url)
            else:
                return redirect("feed_page_view")
        return render(request, "index.html", {"form": form})


def logout_user_profile(request):
    if not request.user.is_authenticated:
        raise Http404()
    else:
        logout(request)
        return redirect("login_user_profile")


@login_required
def update_user_profile(request):
    instance = get_object_or_404(User, id=request.user.id)
    form = UserChangeForm(
        data=request.POST or None, files=request.FILES or None, instance=instance
    )
    if form.is_valid():
        form.save()
        return redirect("update_user_profile")
    return render(request, "user.html", {"form": form})
