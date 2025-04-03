from django.contrib.auth.models import AbstractUser
from django.db import models


class NewUser(AbstractUser):
    subscriptions = models.ManyToManyField(
        "self", symmetrical=False, related_name="subscribers", blank=True
    )
    locked_users = models.JSONField(default=list, blank=True)
