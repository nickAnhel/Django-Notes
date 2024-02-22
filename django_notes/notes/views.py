import re
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .models import Note
from .forms import NoteForm


def note_list(request: HttpRequest) -> HttpResponse:
    notes = Note.objects.all()  # .filter(user=request.user)
    return render(request, "note/note_list.html", {"notes": notes})


def note_detail(request: HttpRequest, slug) -> HttpResponse:
    note = get_object_or_404(Note, slug=slug)
    return render(request, "note/detail.html", {"note": note})


def note_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        note_create_form = NoteForm(data=request.POST)

        if note_create_form.is_valid():
            new_note: Note = note_create_form.save(commit=False)
            new_note.user = request.user

            for user_note in Note.objects.filter(user=request.user):
                if user_note.title.startswith(new_note.title):
                    if re.search(r"\x28\d{1,}\x29", user_note.title):
                        new_note.title += (
                            f" ({int(user_note.title[:-1].split('(')[-1]) + 1})"
                        )
                    else:
                        new_note.title += " (1)"

            new_note.slug = slugify(new_note.title)
            new_note.save()

            return redirect(new_note.get_absolute_url())

    else:
        note_create_form = NoteForm()

    return render(request, "note/create.html", {"form": note_create_form})


def note_edit(request: HttpRequest, slug) -> HttpResponse:
    if request.method == "POST":
        note_edit_form = NoteForm(
            instance=Note.objects.get(slug=slug), data=request.POST
        )

        if note_edit_form.is_valid():
            note: Note = note_edit_form.save(commit=False)
            note.slug = slugify(note_edit_form.cleaned_data["title"])
            note.save()

            return redirect(note.get_absolute_url())

    else:
        note_edit_form = NoteForm(instance=Note.objects.get(slug=slug))

    return render(request, "note/edit.html", {"form": note_edit_form})
