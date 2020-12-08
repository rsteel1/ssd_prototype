from django.contrib import admin

# Register your models here.
from .models import Company, Ticket, TicketComment, Profile

admin.site.register(Company)
admin.site.register(Ticket)
admin.site.register(TicketComment)
admin.site.register(Profile)