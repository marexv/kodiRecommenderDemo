import csv

from main.models import Genre, Movie, User, Rating, Tag, Board

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
            title=row[1]
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
        # if created:
        #     user.save()

        try:
            user.movies.add(row[1])
            user.save()
            print("added user and movie")
        except IntegrityError:
            print("multiple tags")
            continue

# Add actual tags:
with open(path_tags) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    next(csvReader, None)  # skip the headers
    for row in csvReader:
        try:
            tag, created = Tag.objects.get_or_create(
                tag=row[2].lower().strip())
            movie = Movie.objects.get(movie_id=int(row[1]))
            movie.tags.add(tag)
            user = User.objects.get(user_id=int(row[0]))
            user.tags.add(tag)
            print("tag saved " + str(csvReader.line_num))
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


with open(path_ratings) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    next(csvReader, None)  # skip the headers
    bulk = []
    for row in csvReader:
        bulk.append(
            Rating(
                rating=row[2],
                movie_id=int(row[1]),
                user_id=int(row[0])
            )
        )
        if csvReader.line_num%10 == 0: 
            try: 
                Rating.objects.bulk_create(bulk)
            except Exception as e:
                print("Error in ratings " + str(e))
            print("reseting bulk at " + str(csvReader.line_num))
            bulk=[]

# Natural boards tag-movie

# Natural boards movie-actor

# Creat boards - user Genre
for user in User.objects.all():
    for genre in Genre.objects.all():
        movies = user.movies.filter(genres__name=genre.name)
        if len(movies) > 3:
            board_name = str(user.user_id) + " " + str(genre.name)
            board, created = Board.objects.get_or_create(
                name=board_name
            )
            for movie in movies:
                board.movies.add(movie) 