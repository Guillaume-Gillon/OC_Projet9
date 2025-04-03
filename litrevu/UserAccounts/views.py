from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse
from UserAccounts.forms import ConnexionForm, InscrptionForm

User = get_user_model()


# Gestion de l'authentification utilisateur
def auth(request):
    form = ConnexionForm(request.POST or None)
    login_error = ""

    if form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )

        if user is not None:
            login(request, user)
            return redirect(reverse("flux"))
        else:
            login_error = "Nom d'utilisateur ou mot de passe incorrect."

    return render(
        request, "UserAccounts/auth.html", {"form": form, "login_error": login_error}
    )


# Gestion de l'inscription utilisateur
def sign_up(request):
    form = InscrptionForm(request.POST or None)

    if form.is_valid():
        if form.cleaned_data["password"] == form.cleaned_data["password_confirmation"]:
            User.objects.create_user(
                username=form.cleaned_data["username"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            return redirect(reverse("waiting_page"))

    return render(request, "UserAccounts/sign-up.html", {"form": form})


def waiting_page(request):
    return render(request, "UserAccounts/waiting-page.html")
