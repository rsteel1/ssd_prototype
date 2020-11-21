from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
User._meta.get_field("first_name").blank = False
User._meta.get_field("first_name").null = False
User._meta.get_field("last_name").blank = False
User._meta.get_field("last_name").null = False


class Company(models.Model):
    name = models.CharField(max_length=256)
    domain = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    ROLE_CHOICES = [("STAFF", "Staff"), ("CLIENT", "Client")]
    role = models.CharField(choices=ROLE_CHOICES, default="CLIENT", max_length=10)

    def is_client(self):
        return self.role == "CLIENT"

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Ticket(models.Model):
    PRIORITY_CHOICES = [(1, "High"), (2, "Medium"), (3, "Low")]
    TYPE_CHOICES = [("DEV", "Development"), ("TEST", "Testing"), ("PROD", "Production")]
    STATUS_CHOICES = [("OPEN", "Open"), ("RES", "Resolved"), ("CLOSED", "Closed")]

    description = models.TextField(default="")
    steps = models.TextField(default="")
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

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.description