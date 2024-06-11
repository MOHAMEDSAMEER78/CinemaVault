# movies/models.py
from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    imdb_id = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    release_date = models.CharField(max_length=100)
    poster_url = models.URLField()

class MovieList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_public = models.BooleanField(default=False)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name
