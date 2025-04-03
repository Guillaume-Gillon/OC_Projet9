from django import forms
from .models import Ticket, Review


# Formulaire de recherche d'utilisateur pour nouvel abonnement
class SearchingForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Entrez le nom de l'utilisateur",
                "class": "userprofile-text-field",
                "aria-label": "Nom d'utilisateur",
            }
        ),
    )


# Formulaire pour créer un nouveau ticket
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ("user",)
        widgets = {
            "description": forms.Textarea,
            "document": forms.FileInput(attrs={"class": "hidden"}),
        }


# Formulaire pour créer une nouvelle critique
class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        label="Choisissez une note",
        widget=forms.RadioSelect,
        choices=[(i, i) for i in range(6)],
    )

    class Meta:
        model = Review
        exclude = (
            "user",
            "ticket",
        )
        widgets = {"body": forms.Textarea}
