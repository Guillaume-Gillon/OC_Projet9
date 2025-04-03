from django.core.exceptions import ValidationError
from django import forms
from UserAccounts.models import NewUser


def check_email_unique(value):
    if NewUser.objects.filter(email=value).exists():
        raise ValidationError("Cette adresse e-mail est déjà utilisée.")


def check_username_unique(value):
    if NewUser.objects.filter(username=value).exists():
        raise ValidationError("Ce nom d'utilisateur n'est pas disponible.")


def check_username_exists(value):
    if not NewUser.objects.filter(username=value).exists():
        raise ValidationError("Ce nom d'utilisateur n'existe pas.")


class InscrptionForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        validators=[check_username_unique],
        error_messages={
            "required": "Merci d'entrer un nom d'utilisateur",
        },
    )
    first_name = forms.CharField(
        max_length=20,
        error_messages={
            "required": "Merci d'entrer votre prénom.",
        },
    )
    last_name = forms.CharField(
        max_length=20,
        error_messages={
            "required": "Merci d'entrer votre nom.",
        },
    )
    email = forms.EmailField(
        validators=[check_email_unique],
        error_messages={
            "required": "Merci d'entrer une adresse mail.",
            "invalid": "Merci d'entrer une adresse mail valide",
        },
    )
    password = forms.CharField(
        min_length=14,
        widget=forms.PasswordInput(),
        error_messages={
            "min_length": "Merci d'entrer au moins 14 caractères.",
            "required": "Merci d'entrer un mot de passe.",
        },
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            "min_length": "Merci d'entrer au moins 14 caractères.",
            "required": "Merci d'entrer un mot de passe.",
        },
    )


class ConnexionForm(forms.Form):
    username = forms.CharField(max_length=20, validators=[check_username_exists])
    password = forms.CharField(
        min_length=14,
        widget=forms.PasswordInput(),
        error_messages={
            "min_length": "Merci d'entrer au moins 14 caractères.",
            "required": "Merci d'entrer votre mot de passe",
        },
    )
