import re
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.contrib import messages

from .models import Note
from .forms import NoteForm


@login_required
def note_list(request: HttpRequest) -> HttpResponse:
    notes = request.user.notes.all()
    return render(request, "note/note_list.html", {"notes": notes})


@login_required
def note_detail(request: HttpRequest, slug) -> HttpResponse:
    note = get_object_or_404(Note, slug=slug)
    return render(request, "note/detail.html", {"note": note})


@login_required
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


@login_required
def note_edit(request: HttpRequest, slug) -> HttpResponse:
    if request.method == "POST":
        note_edit_form = NoteForm(
            instance=request.user.notes.get(slug=slug), data=request.POST
        )


        if note_edit_form.is_valid():
            note: Note = note_edit_form.save(commit=False)

            for user_note in Note.objects.filter(user=request.user).exclude(
                slug=note.slug
            ):
                if note.title == user_note.title:
                    messages.error(request, "This title is already exists")
                    return render(request, "note/edit.html", {"form": note_edit_form})

            note.slug = slugify(note_edit_form.cleaned_data["title"])
            note.save()

            return redirect(note.get_absolute_url())

    else:
        try:
            note_edit_form = NoteForm(instance=request.user.notes.get(slug=slug))
        except Note.DoesNotExist:
            return HttpResponseRedirect("/notes")

    return render(request, "note/edit.html", {"form": note_edit_form})


@login_required
def note_delete(request: HttpRequest, slug) -> HttpResponseRedirect:
    try:
        note_to_delete = request.user.notes.get(slug=slug)
        note_to_delete.delete()
    except Note.DoesNotExist:
        ...

    return HttpResponseRedirect("/notes")
