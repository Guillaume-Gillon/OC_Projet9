/* Les données passées dans la fonction proviennent des gabarits (attributs de données) */
function open_modal_window(title, data, image, infos) {
    let modal_title = document.getElementById("modal-title")
    modal_title.textContent = title

    let modal_image = document.getElementById("modal-image")
    modal_image.src = image

    let modal_infos = document.getElementById("modal-infos")
    modal_infos.textContent = infos

    let window = document.getElementById("modal-window")
    window.className = "display-modal-window"

    /* Déclaration du bouton de validation et du formulaire associé */
    let validation_button = document.getElementById("validation_button")
    let validation_form = document.getElementById("validation-form")

    /* Pour ajouter une nouvelle fonctionnalité à la modale,
    déclarer ici un bouton de validation en fonction du contexte */
    let logout_button = document.getElementById("logout-button-modal")
    let cancel_ticket_button = document.getElementById("cancel-ticket-button-modal")
    let cancel_subscription_button = document.getElementById("cancel-subscription-button-modal")

    /* Définition de la classe par défaut "hidden" pour chaque bouton
    et pour le formulaire de validation */
    validation_form.className = "hidden"
    logout_button.className = "hidden"
    cancel_ticket_button.className = "hidden"
    cancel_subscription_button.className = "hidden"

    /* Pour ajouter un nouveau bouton de validation redirigeant vers un url (balise <a> du gabarit base.html),
    ajouter un case ci-dessous */
    switch (title) {
        case "Déconnexion":
            logout_button.className = "button modal-button-a"
            break
        case "Annuler l'inscription":
            cancel_subscription_button.className = "button modal-button-a"
            break
        case "Annuler la saisie":
            cancel_ticket_button.className = "button modal-button-a"
            break

        /*
        Pour ajouter une nouvelle fonction au bouton de validation de formulaire (balise <button> du gabarit base.html),
        ajouter un "case" ci-dessous.

        - L'attribut "name" permet à la vue de cibler le bouton.
        - L'attribut "value" passe les données à la vue.
        */
        case "Annuler l'abonnement":
            validation_form.className = ""
            validation_button.setAttribute("name", "delete-subscription")
            validation_button.setAttribute("value", data)
            break
        case "Bloquer l'utilisateur":
            validation_form.className = ""
            validation_button.setAttribute("name", "lock-subscriber")
            validation_button.setAttribute("value", data)
            break
        case "Débloquer l'utilisateur":
            validation_form.className = ""
            validation_button.setAttribute("name", "unlock-subscriber")
            validation_button.setAttribute("value", data)
            break
        case "Supprimer le ticket":
            validation_form.className = ""
            validation_button.setAttribute("name", "delete-ticket")
            validation_button.setAttribute("value", data)
            break
        case "Supprimer la critique":
            validation_form.className = ""
            validation_button.setAttribute("name", "delete-review")
            validation_button.setAttribute("value", data)
            break
        

    }
}

function close_modal_window() {
    let window = document.getElementById("modal-window")
    window.className = "hidden-modal-window"
}