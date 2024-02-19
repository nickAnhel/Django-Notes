from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .models import Note
from .forms import NoteForm


def note_list(request: HttpRequest) -> HttpResponse:
    notes = Note.objects.all()

    return render(request, "note/note_list.html", {"notes": notes})


def note_detail(request: HttpRequest, slug) -> HttpResponse:
    try:
        note = get_object_or_404(Note, slug=slug)
    except MultipleObjectsReturned:
        notes = list(Note.objects.filter(slug=slug))
        i = 0
        for note in notes:
            note.slug += f"-{i + 1}"
            note.save()
            i += 1

        note = notes[0]

    return render(request, "note/detail.html", {"note": note})


def note_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        note_create_form = NoteForm(data=request.POST)

        if note_create_form.is_valid():
            new_note = note_create_form.save(commit=False)
            new_note.user = request.user
            new_note.slug = slugify(note_create_form.cleaned_data["title"])
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
            note = note_edit_form.save(commit=False)
            note.slug = slugify(note_edit_form.cleaned_data["title"])
            note.save()

    else:
        note_edit_form = NoteForm(instance=Note.objects.get(slug=slug))

    return render(request, "note/edit.html", {"form": note_edit_form})
