import operator
from collections import Counter
from random import randrange, uniform

from django.db.models import Count

from main.models import Board, Movie

# Create your views here.
def get_recommendations(movie, steps=1000, alpha=0.5):
    boards = Board.objects.annotate(Count('movies')).filter(movies=movie).order_by('-movies__count')
    starting_node = boards[0]
    board_node = starting_node
    
    movies = {}
    
    for step in range(steps):    
        movies_in_board = board_node.movies.all()
        next_movie_index = randrange(0, len(movies_in_board))
        movie_node = movies_in_board[next_movie_index]
        try:
            movies[movie_node] = movies[movie_node] +1
        except KeyError:
            movies[movie_node] = 1
        except Exception as e:
            print("Exception " + str(e))
        
        boards_containging_movie = movie_node.boards.all()
        next_board_index = randrange(0, len(boards_containging_movie))
        board_node = boards_containging_movie[next_board_index]
        
        if uniform(0,1) < 0.5:
            board_node = starting_node
    
    sorted_movies = sorted(
                        movies.items(),
                        key=operator.itemgetter(1),
                        reverse=True)
    
    sorted_movies = sorted_movies[:10]
    
    sorted_movies_titles = [movie[0].title for movie in sorted_movies]

    return sorted_movies_titles