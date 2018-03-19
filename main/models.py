from django.db import models

# Create your models here.
class Genre(models.Model):  
    name = models.CharField(
        max_length=20, 
        blank=False)

    def __str__(self):
        return self.name


class Rating(models.Model):
    rating = models.FloatField(
        blank=False)

class Tag(models.Model):
    tag = models.CharField(
        blank=False,
        max_length=200)

    def __str__(self):
        return self.tag

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
    ratings = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="movies",
        related_query_name="movie")
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="movies",
        related_query_name="movie")
    
    def __str__(self):
        return self.title

 
class User(models.Model):
    user_id = models.IntegerField(
        blank=False,
        primary_key=True)
    movies = models.ManyToManyField(
        Movie,
        related_name="users",
        related_query_name="user")
    ratings = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="users",
        related_query_name="user")
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="users",
        related_query_name="user")
    
    def __str__(self):
        return "user " + str(self.user_id)


class Board(models.Model):
    name = models.CharField(
        default="default board",
        max_length=140)
    movies = models.ManyToManyField(
        Movie,
        related_name="boards",
        related_query_name="board"
    )

    def __str__(self):
        return "user " + str(self.name)