from django.urls import include, path
from . import views


app_name = "notes"

detail_patterns = [
    path("", views.note_detail, name="detail"),
    path("edit/", views.note_edit, name="edit"),
    path("delete/", views.note_delete, name="delete")
]

urlpatterns = [
    path("", views.note_list, name="list"),
    path("create/", views.note_create, name="create"),
    path("detail/<slug:slug>/", include(detail_patterns)),
]
