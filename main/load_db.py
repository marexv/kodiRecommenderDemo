import csv

from main.models import Genre, Movie, User, Rating, Tag

from django.db import IntegrityError

import datetime

genres = [
 "action",
 "adventure",
 "animation",
 "childrens",
 "comedy",
 "crime",
 "documentary",
 "drama",
 "fantasy",
 "film-noir",
 "horror",
 "musical",
 "mystery",
 "romance",
 "sci-fi",
 "thriller",
 "war",
 "western",
]

def save_genre(genres):
    for genre in genres:
        genre = str(genre).strip().lower()
        if not Genre.objects.filter(name=genre).exists():
            new_genre = Genre(name=genre)
            new_genre.save()
        
path_movies = 'csvData/movies.csv'
 
# Save movies:
with open(path_movies) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    next(csvReader, None)  # skip the headers
    for row in csvReader:
        movie = Movie(
            movie_id=row[0],
            title = row[1]            
        )
        movie.save()
        genres = row[2].lower().replace("|", " ").split()
        add_genre_to_movie(movie, genres)
        
def add_genre_to_movie(movie, genres):
    genre_objects = Genre.objects.all()
    for genre in genres:
        try:
            key = genre_objects.get(name=genre).pk
            movie.genres.add(key)
        except Genre.DoesNotExist:
            continue
    print("saved movie " + str(movie.movie_id))
    movie.save()
        
path_tags = 'csvData/tags.csv'

with open(path_tags) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    next(csvReader, None)  # skip the headers
    for row in csvReader:
        user, created = User.objects.get_or_create(user_id=row[0])
        if created:
            user.save()
        
        try:
            user.movies.add(row[1])
            user.save()
            print("added user and movie")
        except IntegrityError:
            print("multiple tags")
            continue

with open(path_tags) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    next(csvReader, None)  # skip the headers
    for row in csvReader:
        try:
            new_tag = Tag(
                tag=row[2],
                timestamp=datetime.datetime.fromtimestamp(row[3])
                user=row[0],
                movie=row[1]
            )
            new_tag.save()
            print("tag saved")
        except Exception as e:
            print("Exception: " + str(e))


path_ratings = 'csvData/ratings.csv'

with open(path_ratings) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    next(csvReader, None)  # skip the headers
    for row in csvReader:
        user, created = User.objects.get_or_create(user_id=row[0])
        if created:
            user.save()
        
        try:
            user.movies.add(row[1])
            user.save()
            print("added user and movie")
        except IntegrityError:
            print("multiple ratings")
            continue