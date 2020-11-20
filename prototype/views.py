from django.shortcuts import render
from django.http import HttpResponse

from .models import Ticket

# Create your views here.
def index(request):
    latest_tickets = Ticket.objects.order_by("-created_datetime")[:5]
    output = ", ".join([ticket.description for ticket in latest_tickets])
    return HttpResponse(output)

def ticket(request, ticket_id):
    # TODO: Add user authorisation here
    return HttpResponse("Ticket %s" % ticket_id)
