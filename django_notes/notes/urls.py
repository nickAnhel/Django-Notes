from django.urls import path
from . import views


app_name = "notes"

urlpatterns = [
    path("", views.note_list, name="list"),
    path("detail/<slug:slug>/", views.note_detail, name="detail"),
    path("create/", views.note_create, name="create"),
]
