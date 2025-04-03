from django.contrib import admin
from .models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "document", "time_created")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "headline", "get_ticket_name", "user", "time_created")

    def get_ticket_name(self, obj):
        return obj.ticket.title

    get_ticket_name.short_description = "Associated Ticket Name"


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
