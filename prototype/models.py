from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    PRIORITY_CHOICES = [(1, "High"), (2, "Medium"), (3, "Low")]
    TYPE_CHOICES = [("DEV", "Development"), ("TEST", "Testing"), ("PROD", "Production")]
    STATUS_CHOICES = [("OPEN", "Open"), ("RES", "Resolved"), ("CLOSED", "Closed")]

    description = models.TextField()
    created_datetime = models.DateField(auto_now=True)
    type = models.CharField(choices=TYPE_CHOICES, default="DEV", max_length=20)
    status = models.CharField(choices=STATUS_CHOICES, default="OPEN", max_length=15)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="created_tickets", null=True
    )
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="assigned_tickets", null=True
    )

    def __str__(self):
        return f"Ticket {str(self.id)}"


class TicketComment(models.Model):
    description = models.TextField()
    created_at = models.DateField(auto_now=True)

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.description