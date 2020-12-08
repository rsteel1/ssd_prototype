from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Company, Ticket, TicketComment


class CreateTicketFormClient(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateTicketFormClient, self).__init__(*args, **kwargs)
        self.helper = FormHelper

    class Meta:
        model = Ticket
        fields = ["steps", "description", "type", "priority"]

    def is_client_form(self):
        return True


class CreateTicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateTicketForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper

    class Meta:
        model = Ticket
        fields = ["steps", "description", "type", "priority", "company", "assignee"]

    def is_client_form(self):
        return False


class CreateTicketFormFactory:
    def __init__(self, profile):
        self.profile = profile

    def generate_form(self, *args):
        if self.profile.is_client():
            return CreateTicketFormClient(*args)
        else:
            return CreateTicketForm(*args)


class EditTicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditTicketForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper

    class Meta:
        model = Ticket
        fields = [
            "steps",
            "description",
            "status",
            "type",
            "priority",
            "company",
            "assignee",
        ]

    def clean(self):
        super(EditTicketForm, self).clean()

        cd = self.cleaned_data
        if self.instance.status == "OPEN" and cd.get("status") == "CLOSED":
            self.add_error(
                "status",
                "This status cannot be set yet. Please set to Resolved before Closed",
            )
        return cd


class AddCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper

    class Meta:
        model = TicketComment
        fields = ["description"]


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def clean(self):
        super(RegisterForm, self).clean()
        cd = self.cleaned_data
        domain = cd.get("email").split("@")[1]
        try:
            Company.objects.get(domain=domain)
        except ObjectDoesNotExist:
            self.add_error(
                "email",
                "This email domain is not registered to any company in our database.",
            )
        return cd
