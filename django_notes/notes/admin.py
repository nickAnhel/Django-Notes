from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "created"]
    ordering = ["created"]
    prepopulated_fields = {"slug": ("title",)}