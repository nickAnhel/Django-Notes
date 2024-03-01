from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import UserSignUpForm


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_creation_form = UserSignUpForm(data=request.POST)

        if user_creation_form.is_valid():
            user = user_creation_form.save()

            # Authenticate new user
            login(request, user)
            return HttpResponseRedirect("/notes")

    else:
        user_creation_form = UserSignUpForm()

    return render(request, "account/register.html", {"form": user_creation_form})
