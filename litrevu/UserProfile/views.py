from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user_model
from django.urls import reverse
from django.conf import settings
from UserProfile.forms import SearchingForm, TicketForm, ReviewForm
from UserProfile.models import Ticket, Review
from datetime import datetime
import pytz
import os

User = get_user_model()
PARIS_TZ = pytz.timezone("Europe/Paris")


# Gère la déconnexion et la redirection de l'utilisateur
@login_required
def log_out(request):
    logout(request)
    return redirect(reverse("auth"))


# Récupère les tickets et les reviews de l'utilisateur pour les intégrer dans une liste triée
# Retourne la liste triée
@login_required
def define_elements(request, subscriptions_users=None):
    if not subscriptions_users:
        tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")
        subscriptions_reviews = Review.objects.filter(user=request.user).order_by(
            "-time_created"
        )
        ticket_reviews = ""
    else:
        tickets = Ticket.objects.filter(user__in=subscriptions_users).order_by(
            "-time_created"
        )
        subscriptions_reviews = Review.objects.filter(
            user__in=subscriptions_users
        ).order_by("-time_created")
        ticket_reviews = Review.objects.filter(ticket__user=request.user)

    elements = []
    for ticket in tickets:
        elements.append(ticket)

    for review in subscriptions_reviews:
        elements.append(review)

    for other_review in ticket_reviews:
        if other_review not in elements:
            elements.append(other_review)

    sorted_elements = sorted(elements, key=lambda obj: obj.time_created, reverse=True)
    return sorted_elements


# Gère l'affichage de la section "flux"
@login_required
def flux(request):
    subscriptions_users = list(request.user.subscriptions.all())
    subscriptions_users.append(request.user)
    sorted_elements = define_elements(request, subscriptions_users)

    # Gère le clic sur le bouton "créer une critique" de chaque ticket
    # Redirige vers le gabarit "new-review/<int:ticket_id>/"
    if request.POST.get("create_review_button"):
        id_ticket = request.POST.get("create_review_button")
        return redirect(reverse("ticket_response", kwargs={"ticket_id": id_ticket}))

    return render(request, "UserProfile/flux-posts.html", {"elements": sorted_elements})


# Gère l'affichage de la section "posts"
@login_required
def posts(request):
    sorted_elements = define_elements(request)
    if request.method == "POST":

        # Gère le clic sur le bouton "supprimer" affiché au ticket
        if request.POST.get("delete-ticket"):
            id_ticket = request.POST.get("delete-ticket")
            if id_ticket:
                ticket_to_delete = Ticket.objects.get(id=id_ticket)
                document = ticket_to_delete.document
                if document and document.file:
                    file_path = os.path.join(settings.MEDIA_ROOT, str(document.file))
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                ticket_to_delete.delete()
                return redirect("posts")

        # Gère le clic sur le bouton "supprimer" affiché à la critique
        if request.POST.get("delete-review"):
            id_review = request.POST.get("delete-review")
            if id_review:
                review_to_delete = Review.objects.get(id=id_review)
                review_to_delete.delete()
                return redirect("posts")

        # Gère le clic sur le bouton "modifier" affiché au ticket
        if request.POST.get("modify_ticket_button"):
            id_ticket = request.POST.get("modify_ticket_button")
            return redirect(reverse("edit_ticket", kwargs={"ticket_id": id_ticket}))

        # Gère le clic sur le bouton "modifier" affiché à la critique
        if request.POST.get("modify_review_button"):
            id_review = request.POST.get("modify_review_button")
            review_qst = Review.objects.filter(id=id_review)
            for review in review_qst:
                ticket_qst = Ticket.objects.filter(id=review.ticket.id)
                for ticket in ticket_qst:
                    id_ticket = ticket.id
            return redirect(reverse("ticket_response", kwargs={"ticket_id": id_ticket}))

    return render(request, "UserProfile/flux-posts.html", {"elements": sorted_elements})


# Gère l'affichage de la section "abonnements"
# user_error contient un message d'erreur personnalisé
@login_required
def subscriptions(request):
    user_error = ""
    searching_form = SearchingForm(request.POST or None)

    # Si le bouton "supprimer l'abonnement" est cliqué
    if request.POST.get("delete-subscription"):
        id_user = request.POST.get("delete-subscription")
        user_to_unsubscribe = User.objects.get(id=id_user)
        request.user.subscriptions.remove(user_to_unsubscribe)

    # Si le bouton "bloquer l'abonné" est cliqué
    if request.POST.get("lock-subscriber"):
        id_user_to_lock = request.POST.get("lock-subscriber")
        user_to_lock = User.objects.get(id=id_user_to_lock)
        request.user.subscribers.remove(user_to_lock)
        actual_user = User.objects.get(username=request.user)
        if user_to_lock.username not in actual_user.locked_users:
            actual_user.locked_users.append(user_to_lock.username)
            actual_user.save()
            return redirect(reverse("subscriptions"))

    # Si le bouton "débloquer l'abonné" est cliqué
    if request.POST.get("unlock-subscriber"):
        username_to_unlock = request.POST.get("unlock-subscriber")
        user_to_unlock = User.objects.get(username=username_to_unlock)
        actual_user = User.objects.get(username=request.user)
        if user_to_unlock.username in actual_user.locked_users:
            actual_user.locked_users.remove(user_to_unlock.username)
            actual_user.save()
            return redirect(reverse("subscriptions"))

    elif searching_form.is_valid():
        username = searching_form.cleaned_data["username"]
        try:
            user_found = User.objects.get(username__iexact=username)
            # Gestion du cas où l'utilisateur souhaite s'abonner à lui même
            if request.user.username == user_found.username:
                user_error = "Vous ne pouvez pas vous abonner à vous même."
            elif request.user.username in user_found.locked_users:
                user_error = f"{user_found.username} n'autorise pas cette action."
            else:
                request.user.subscriptions.add(user_found)
        except User.DoesNotExist:
            user_error = f"L'utilisateur '{username}' n'existe pas."

    else:
        if searching_form.errors:
            user_error = "Merci d'entrer un nom d'utilisateur."

    return render(
        request,
        "UserProfile/subscriptions.html",
        {
            "searching_form": searching_form,
            "user_error": user_error,
        },
    )


# Gère la recherche de ticket en DB et l'instance de formulaire associé
@login_required
def init_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        ticket = None
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
    else:
        ticket_form = TicketForm(instance=ticket)
    ticket_form.fields["title"].label = "Titre"

    return ticket, ticket_form


# Gère l'affichage de la section "créer un ticket" et "modifier un ticket"
@login_required
def new_ticket(request, ticket_id=None):

    data = init_ticket(request, ticket_id)
    ticket = data[0]
    ticket_form = data[1]

    if ticket_form.is_valid():
        ticket = ticket_form.save(commit=False)
        ticket.user = request.user

        # Si le ticket existe dans la DB, on intègre la date de modification
        if ticket_id:
            ticket.time_modified = datetime.now(PARIS_TZ)
        ticket.save()
        return redirect(reverse("success"))

    return render(
        request,
        "UserProfile/new-ticket.html",
        {"ticket": ticket, "ticket_form": ticket_form},
    )


# Gère l'affichage de la section "créer une critique" et "modifier une critique"
@login_required
def new_review(request, ticket_id=None):

    # Initialisation du ticket objet de la critique et du formulaire associé
    data = init_ticket(request, ticket_id)
    ticket = data[0]
    ticket_form = data[1]

    # Dans le contexte de l'application, un ticket ne peut avoir qu'une seule critique
    # On utilise donc review_set.first() pour sélectionner la première review associée au ticket
    try:
        review = ticket.review_set.first()
    except AttributeError:
        review = None

    # Le formulaire de review prend en paramètre une instance de review
    # Cela permet de modifier une review liée à un ticket
    if request.method == "POST":
        review_form = ReviewForm(request.POST, instance=review)
    else:
        review_form = ReviewForm(instance=review)

    # Personnalisation des labels du formulaire
    review_form.fields["headline"].label = "Votre avis"
    review_form.fields["body"].label = "Détails"

    # Si la review en cours est associée à un ticket ou si elle est une réponse à un ticket
    # Alors verouillage des champs du ticket pour empêcher une modification de celui-ci
    if ticket_id:
        ticket_form.fields["title"].widget.attrs["readonly"] = True
        ticket_form.fields["description"].widget.attrs["readonly"] = True

    if ticket_form.is_valid() and review_form.is_valid():

        # Si le ticket vient d'être créé, sauvegarde et récupération de l'objet ticket
        if not ticket_id:
            ticket_to_save = ticket_form.save(commit=False)
            ticket_to_save.user = request.user
            ticket_to_save.save()
            ticket = Ticket.objects.get(id=ticket_to_save.id)

        review_to_save = review_form.save(commit=False)

        # Si la review existe, alors on intègre la date de modification
        if review_to_save.time_created:
            review_to_save.time_modified = datetime.now(PARIS_TZ)

        review_to_save.ticket = ticket
        review_to_save.user = request.user
        review_to_save.save()

        return redirect(reverse("success"))

    return render(
        request,
        "UserProfile/new-review.html",
        {
            "ticket": ticket,
            "ticket_form": ticket_form,
            "review_form": review_form,
        },
    )


# Gère l'affichage de la page de confirmation
@login_required
def success(request):
    return render(request, "UserProfile/success.html")
