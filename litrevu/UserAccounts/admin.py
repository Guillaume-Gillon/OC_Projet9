from django.contrib import admin
from UserAccounts.models import NewUser


class UsersAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "last_login", "is_superuser")


admin.site.register(NewUser, UsersAdmin)
