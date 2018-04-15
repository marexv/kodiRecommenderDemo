"""
Contains all functions for loading .csv data to DB via Django ORM.

from main.load_db import *
"""
import csv
import itertools
import datetime

from pprint import pprint

from django.db import IntegrityError

from main.models import Genre, Movie, User, Rating, Tag, Board
from django.db.models import Count


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
    """Save all genres to genres table."""
    for genre in genres:
        genre = str(genre).strip().lower()
        if not Genre.objects.filter(name=genre).exists():
            new_genre = Genre(name=genre)
            new_genre.save()


def save_movies(path_movies = 'csvData/movies.csv'):
    """Save all movies to movies table, add relations to all genres."""
    with open(path_movies) as csvDataFile:
        """Save all movies to DB and add relations to genres."""
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
    """Helper function for adding genre relations to movie."""
    genre_objects = Genre.objects.all()
    for genre in genres:
        try:
            key = genre_objects.get(name=genre).pk
            movie.genres.add(key)
        except Genre.DoesNotExist:
            continue
    print("saved movie " + str(movie.movie_id))
    movie.save()


def save_users_from_tags(path_tags = 'csvData/tags.csv'):
    """Save all users to DB and add movies that they watched."""
    with open(path_tags) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        next(csvReader, None)  # skip the headers
        for row in csvReader:
            user, created = User.objects.get_or_create(user_id=row[0]) 
            try:
                user.movies.add(row[1])
                user.save()
                print("added user and movie")
            except IntegrityError:
                print("multiple tags")
                continue


def save_tags(path_tags = 'csvData/tags.csv'):
    """Save all tags that user assigned to movies."""
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


def save_users_from_ratings(path_ratings = 'csvData/ratings.csv'):
    """Save all users to DB and add movies that they watched."""
    with open(path_ratings) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        next(csvReader, None)  # skip the headers
        for row in csvReader:
            user, created = User.objects.get_or_create(user_id=row[0])
            if created:
                user.save()
                print("added user")
            try:
                user.movies.add(row[1])
                user.save()
                print("added movie")
            except IntegrityError:
                print("multiple ratings")


def save_ratings(path_ratings = 'csvData/ratings.csv'):
    """Save all ratings with realtion: user-rating-movie."""
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


def create_boards_user_genre():
    """Create a board containing each users movies with same genre."""
    for user in User.objects.all():
        for genre in Genre.objects.all():
            movies = user.movies.filter(genres__name=genre.name)
            if len(movies) > 3: # This limit can be removed if we join small boards later
                board_name = str(user.user_id) + " " + str(genre.name)
                board, created = Board.objects.get_or_create(
                    name=board_name
                )
                for movie in movies:
                    board.movies.add(movie)

#####################################################################
# Not implemeted in database. Implemented just in graph dictionary: #
#####################################################################

def create_boards_for_same_series():
    """Crate boards taht contain all movies from one franchise."""
    movies = list(Movie.objects.all())
    new_boards_graph = {}

    for counter, movie in enumerate(movies):
        new_board = []
        new_board.append(movie)
        other_movies = movies.remove(movie)
        for other in movies[counter+1:]:
            new_title_1 = movie.title.replace("-", " ").lower().split(" ")[:2]
            new_title_2 = other.title.replace("-", " ").lower().split(" ")[:2]
            if new_title_1 == new_title_2:
                new_board.append(other)

        if len(new_board) > 2:
            name = "Series Board {}".format(" ".join(new_title_1))
            new_movies = [movie.title for movie in new_board]
            new_boards_graph[name] = new_movies
            print("Crated new board: {}, with {} movies".format(
                                                            name, 
                                                            len(new_movies)))
    
    return new_boards_graph


def join_boards():
    """Join multiple smaller boards into bigger ones."""
    joined_boards_graph = {}
    boards_to_remove = []
    for genre in genres:
        candidates = Board.objects.filter(
                        name__contains=genre
                    ).annotate(
                        movie=Count('movies')
                    ).filter(movie__lt=6)
        # print("{}:".format(genre))
        # pprint(candidates)

        movies = []
        for board in candidates:
            boards_to_remove.append(board.name)
            for movie in board.movies.all():
                movies.append(movie)

        name = "merged {} board".format(genre)
        movies = set(movies)

        joined_boards_graph[name] = [movie.title for movie in movies]
    
    return joined_boards_graph, boards_to_remove

def remove_boards_from_graph(
        graph: dict, 
        boards_to_remove: list):

    for board in boards_to_remove:
        movies = graph[board]
        for movie in movies:
            try:
                graph[movie].remove(board)
            except Exception as e:
                print("failed to remove {}, from {}".format(
                    board, board
                ))
        del(graph[board])
    
    return graph
