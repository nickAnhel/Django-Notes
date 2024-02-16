from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["-created"])]
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("notes:detail", args=[self.slug])
