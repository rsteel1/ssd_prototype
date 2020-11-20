from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.views import generic
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import Ticket, Company
from .forms import CreateTicketFormFactory, RegisterForm

# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "prototype/index.html"
    context_object_name = "tickets"

    def get_queryset(self):
        user = self.request.user
        if user.profile.role == "CLIENT":
            return Ticket.objects.filter(company=self.request.user.profile.company).order_by("-created_datetime")
        return Ticket.objects.order_by("-created_datetime")

class TicketView(generic.DetailView):
    model = Ticket
    template_name = "prototype/ticket_detail.html"
    context_object_name = "ticket"

@login_required
def create_ticket(request):
    factory = CreateTicketFormFactory(request.user.profile)
    if (request.method == "POST"):
        form = factory.generate_form(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            cd = form.cleaned_data
            print(cd)
            if not request.user.profile.is_client():
                new_ticket.company = request.user.profile.company
            else:
                new_ticket.company = cd.get["company"]
                new_ticket.assignee = cd.get["assignee"]
            new_ticket.author = request.user
            new_ticket.save()
            return redirect("/")
    else:
        form = factory.generate_form()
    return render(request, "prototype/create_ticket.html", context={"form": form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email_domain = form.cleaned_data.get("email").split("@")[1]
            company = Company.objects.get(domain=email_domain)
            user = form.save()
            user.refresh_from_db()
            user.profile.company_id = company.id
            user.profile.save()
            user.save()
            password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", context={"form": form})

def ticket(request, ticket_id):
    # TODO: Add user authorisation here
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, "")
    
