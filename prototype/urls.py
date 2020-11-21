from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("ticket/<int:ticket_id>/", views.ticket, name="ticket"),
    path("ticket/create/", views.create_ticket, name="create_ticket"),
    path("ticket/edit/<int:ticket_id>/", views.edit_ticket, name="edit_ticket"),
    path("ticket/<int:ticket_id>/add_comment", views.add_comment, name="add_comment"),
    path("register/", views.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls"))
]