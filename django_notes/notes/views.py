from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .models import Note
from .forms import NoteCreateForm


def note_list(request: HttpRequest) -> HttpResponse:
    notes = Note.objects.all()

    return render(request, "note/note_list.html", {"notes": notes})


def note_detail(request: HttpRequest, slug) -> HttpResponse:
    note = get_object_or_404(Note, slug=slug)
    return render(request, "note/detail.html", {"note": note})


def note_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        note_create_form = NoteCreateForm(data=request.POST)

        if note_create_form.is_valid():
            new_note = note_create_form.save(commit=False)
            new_note.user = request.user
            new_note.slug = slugify(note_create_form.cleaned_data["title"])
            new_note.save()

            return redirect(new_note.get_absolute_url())

    else:
        note_create_form = NoteCreateForm()

    return render(request, "note/create.html", {"form": note_create_form})
