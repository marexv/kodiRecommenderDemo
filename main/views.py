from django.shortcuts import render

from main.models import Movie, Board

from random import randrange, uniform
# Create your views here.

# Algorithm

steps = 5000
movie_id = 1

# Get first movie:
try:
    movie = Movie.objects.get(movie_id=movie_id)
except Exception:
    movie = None

# Choose board with biggest number of movies for starting board.
boards = Board.objects.annotate(Count('movies')).filter(movies=movie).order_by('-movies__count')
starting_node = boards[0]

board_node = starting_node
# Random walk:
movies = {}
for step in range(steps):
    #
    movies_in_board = board_node.movies.all()
    next_movie_index = randrange(0, len(movies_in_board))
    movie_node = movies_in_board[next_movie_index]
    try:
        movies[movie_node] = movies[movie_node] +1
    except Exception as e:
        print(str(e))
        movies[movie_node] = 1
    #
    boards_containging_movie = movie_node.boards.all()
    next_board_index = randrange(0, len(boards_containging_movie))
    board_node = boards_containging_movie[next_board_index]
    #
    if uniform(0,1) < 0.5:
        board_node = starting_node


import operator

sorted_movies = sorted(movies.items(), key=operator.itemgetter(1), reverse=True)

from collections import Counter

a = dict(Counter(movies))