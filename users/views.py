
from email import message
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from posts.models import Author


from users.forms import UserForm
from main.functions import generate_form_errors

# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)

                return HttpResponseRedirect("/")

        context = {
            "title": "Login",
            "error": True,
            "message": "Invalid username or password"
        }
        return render(request, "users/login.html", context)
    else:
        context = {
            "title": "Login",

        }
        return render(request, "users/login.html", context)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("web:index"))


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            user= User.objects.create_user(
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                    email=instance.email,
                    password=instance.password,
                    username=instance.username
                )
            Author.objects.create(
                    name=instance.first_name,
                    user=user
                )

            user = authenticate(
                request, username=instance.username, password=instance.password)
            auth_login(request, user)

            return HttpResponseRedirect(reverse('web:index'))
        else:
            message = generate_form_errors(form)
            form = UserForm()
            context = {
                "title": "Signup",
                "error": True,
                "form": form,
                "message": message
            }
            return render(request, "users/signup.html", context)
    else:
        form = UserForm()
        context = {
            'title': "Signup",
            "form": form,
        }
        return render(request, "users/signup.html", context=context)
