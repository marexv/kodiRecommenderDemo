"""
Contains code for implementing movie graph as python dict.

* DEV file path: "graph.json"
* PROD file path: "/home/markoprcac/kodiRecommenderDemo/graph.json"
"""

import json
import random
import operator

from fuzzywuzzy import fuzz
from pprint import pprint

from django.conf import settings

from main.models import Movie, Board
from main.load_db import (join_boards, 
                          create_boards_for_same_series,
                          remove_boards_from_graph)

"""
Run locally in console:

from main.graph_as_dict import *

boards = Board.objects.all()
movies = Movie.objects.all()

# Get sample movie ...
movie = random.choice(Movie.objects.all())

# or choose one
movie = Movie.objects.all()[0]

# Creat graph...
graph = create_or_update_graph(boards=boards, movies=movies)
graph = add_additional_boards(graph)
save_graph_to_json(graph)
 
# OR load graph.
graph = read_graph_form_json()

get_recommendations(movie, graph, steps=1000, alpha=0.8)
"""

def create_or_update_graph(
    boards=None,
    movies=None,
    graph={}):
    """Create or update graph form DB models."""
    if boards is not None:
        for board in boards:
            try:   
                movies_in_board = []
                for movie in board.movies.all():  
                    movies_in_board.append(movie.title)
                graph[board.name] = movies_in_board
                print('board {0} done'.format(board.pk))
            except Exception as e:
                print(str(e))

    if movies is not None:
        for movie in movies:
            try:
                boards_containing_movie = []
                for board in movie.boards.all():
                    boards_containing_movie.append(board.name)
                graph[movie.title] = boards_containing_movie
                print('movie {0} done'.format(movie.pk))
            except Exception as e:
                print(str(e))

    return graph


def add_additional_boards(graph={}):
    print("Inital lenght: {}".format(len(graph)))
    graph1, merged_boards = join_boards()
    graph.update(graph1)
    print("Mid-update lenght {}".format(len(graph)))
    graph = remove_boards_from_graph(graph, merged_boards)
    print("After redundant removal lenght {}".format(len(graph)))
    graph2 = create_boards_for_same_series()
    graph.update(graph2)
    print("Final length {}".format(len(graph)))
    return graph


if settings.DEBUG:
   # Local path
   file_path = "graph.json"
else:
    # Path for PROD
    file_path = "/home/markoprcac/kodiRecommenderDemo/graph.json"


def save_graph_to_json(graph: dict, file_path=file_path):
    """Save dict representing movie graph to JSON file."""
    with open(file_path, "w") as fp:
        json.dump(graph, fp, sort_keys=True, indent=4)


def read_graph_form_json(file_path=file_path):
    """Load dict from JSON."""
    with open(file_path, "r") as fp:
        data = json.load(fp)
    return data


def get_board_with_most_movies(boards):
    """Return board with most movies form passed board."""
    return sorted(boards, key=lambda k: len(boards[k]), reverse=True)[0]


def get_recommendations(movie: Movie, graph={}, steps=1000, alpha=0.5):
    """Get recommendetions by performing BASIC
       random walk on movie graph represented as dict."""

    if len(graph) == 0:
        graph = read_graph_form_json()
    
    movies = {}
    starting_movie = movie.title
    movie = starting_movie
    for step in range(steps):
        # Get random board containing movie.        
        board = random.choice(graph[movie])
        # Get random movie contained in board.
        movie = random.choice(graph[board])
        # Cave movie to dict and increase counter if it's repeating.
        try:
            movies[movie] = movies[movie] +1
        except KeyError:
            movies[movie] = 1
        except Exception as e:
            print("Exception " + str(e))
        # Control how far away from movie do you want to go.
        if random.uniform(0,1) < alpha:
            movie = starting_movie
    
    # Sort the movies by number of visitis. Here we could implement some other
    # sorting function.
    
    if starting_movie in movies:
        del movies[starting_movie]

    movies = check_for_merged_boards(movies=movies,
                                     graph=graph,
                                     starting_movie=starting_movie)

    sorted_movies = sorted(
                        movies.items(),
                        key=operator.itemgetter(1),
                        reverse=True)

    # Take top 10 movies.
    sorted_movies = sorted_movies[:10]

    # Return just a list of titles without view counts.
    sorted_movies_titles = [movie[0] for movie in sorted_movies]

    return sorted_movies_titles


# Helper functions:
def get_same_series_by_name_matching(
        movies: dict,
        starting_movie: str,
        threshold: int,
        weight: int):
    print("BEFORE NAME WEIGHT")
    pprint(movies)
    for key, value in movies.items():
        if fuzz.token_set_ratio(starting_movie[:12], key[:12]) > threshold:
            value += weight
    print("AFTER")
    pprint(movies)
    return movies

def check_for_merged_boards(
        movies: dict,
        graph: dict,
        starting_movie: str):
    new_title_1 = starting_movie.replace("-", " ").lower().split(" ")[:2]
    name = "Series Board {}".format(" ".join(new_title_1))
    if name in graph:
        for movie in graph[name]:
            try:
                movies[movie] = movies[movie] + 7
            except KeyError:
                movies[movie] = 10

    return movies