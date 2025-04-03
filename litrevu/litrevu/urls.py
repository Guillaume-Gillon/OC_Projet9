"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from UserAccounts import views as AuthViews
from UserProfile import views as ProfileViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", AuthViews.auth, name="auth"),
    path("sign-up/", AuthViews.sign_up, name="sign-up"),
    path("waiting-page/", AuthViews.waiting_page, name="waiting_page"),
    path("flux/", ProfileViews.flux, name="flux"),
    path("posts/", ProfileViews.posts, name="posts"),
    path("subscriptions/", ProfileViews.subscriptions, name="subscriptions"),
    path("logout/", ProfileViews.log_out, name="logout"),
    path("new-ticket/", ProfileViews.new_ticket, name="new_ticket"),
    path("new-ticket/<int:ticket_id>/", ProfileViews.new_ticket, name="edit_ticket"),
    path("new-review/", ProfileViews.new_review, name="new_review"),
    path(
        "new-review/<int:ticket_id>/", ProfileViews.new_review, name="ticket_response"
    ),
    path("success/", ProfileViews.success, name="success"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
