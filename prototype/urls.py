from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("ticket/<int:pk>/", views.TicketView.as_view(), name="ticket"),
    path("ticket/create/", views.create_ticket, name="create_ticket"),
    path("register/", views.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls"))
]