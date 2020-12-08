from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.views import generic
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import Ticket, Company, TicketComment
from .forms import AddCommentForm, CreateTicketFormFactory, RegisterForm, EditTicketForm

# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "prototype/index.html"
    context_object_name = "tickets"

    def get_queryset(self):
        user = self.request.user
        if user.profile.role == "CLIENT":
            return Ticket.objects.filter(
                company=self.request.user.profile.company
            ).order_by("-created_datetime")
        return Ticket.objects.order_by("-created_datetime")


def access_allowed(request, ticket):
    if (
        request.user.profile.is_client()
        and ticket.company != request.user.profile.company
    ):
        return False
    else:
        return True


@login_required
def ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if not access_allowed(request, ticket):
        return HttpResponseForbidden()

    comments = TicketComment.objects.filter(ticket_id=ticket_id)
    return render(
        request,
        template_name="prototype/ticket_detail.html",
        context={"ticket": ticket, "comments": comments},
    )


@login_required
def create_ticket(request):
    factory = CreateTicketFormFactory(request.user.profile)
    if request.method == "POST":
        form = factory.generate_form(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            cd = form.cleaned_data
            print(cd)
            if request.user.profile.is_client():
                new_ticket.company = request.user.profile.company
            else:
                new_ticket.company = cd.get("company")
                new_ticket.assignee = cd.get("assignee")
            new_ticket.author = request.user
            new_ticket.save()
            return redirect("/")
    else:
        form = factory.generate_form()
    return render(request, "prototype/create_ticket.html", context={"form": form})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if not access_allowed(request, ticket) or request.user.profile.is_client():
        return HttpResponseForbidden()

    form = EditTicketForm(request.POST or None, instance=ticket)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("/")
    return render(request, "prototype/edit_ticket.html", context={"form": form})


@login_required
def add_comment(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if not access_allowed(request, ticket):
        return HttpResponseForbidden()

    if request.method == "POST":
        form = AddCommentForm(request.POST)
        if form.is_valid():
            print("FORM VALID")
            new_comment = form.save(commit=False)
            new_comment.ticket = ticket
            new_comment.author = request.user
            new_comment.save()
            return redirect("ticket", ticket_id=ticket_id)
    else:
        form = AddCommentForm()
    return render(request, "prototype/add_comment.html", context={"form": form})


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
            if user.profile.company.name == "Safari Security":
                user.profile.role = "STAFF"
            user.save()
            password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", context={"form": form})