from django.contrib import admin

# Register your models here.
from .models import Company
from .models import Ticket
from .models import TicketComment

admin.site.register(Company)
admin.site.register(Ticket)
admin.site.register(TicketComment)