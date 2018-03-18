from django.db import models

# Create your models here.
class Genre(models.Model):  
    name = models.CharField(
        max_length=20, 
        blank=False)

    def __str__(self):
        return self.name


class Movie(models.Model):
    movie_id = models.IntegerField(
        blank=False,
        primary_key=True)
    imdb_id = models.CharField(
        blank=True,
        max_length=30)
    tmdb_id = models.CharField(
        blank=True,
        max_length=30)
    title = models.CharField(
        blank=False,
        max_length=30)
    genres = models.ManyToManyField(
        Genre,
        blank=True,
        related_name="movies",
        related_query_name="movie")
    
    def __str__(self):
        return self.title

 
class User(models.Model):
    user_id = models.IntegerField(
        blank=False,
        primary_key=True)
    movies = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="user")


class Rating(models.Model):
    rating = models.FloatField(
        blank=False)
    timestamp = models.DateTimeField(
        blank=False)
    movie = models.OneToOneField(
        Movie,
        on_delete=models.CASCADE,
        related_name="rating")
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="rating")


class Tag(models.Model):
    tag = models.CharField(
        blank=False,
        max_length=100)
    timestamp = models.DateTimeField(
        blank=False)
    movie = models.OneToOneField(
        Movie,
        on_delete=models.CASCADE,
        related_name="movie")
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user")
