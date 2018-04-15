# import GraphDB
from graphdb import GraphDB

from main.models import Movie, Board

# initialize a database
# db = GraphDB('test_graph.db') # uses ':memory:' if no path
"""
from main.graphdb_test import *

boards = Board.objects.all()
movies = Movie.objects.all()
"""

for board in boards:
    for movie in board.movies.all():
        # db.store_relation(board.name, "contains_movie", movie.title)
        db.store_relation(movie.title, "in_board", board.name)
    print("board " + str(board.id) + " done") 


# SCRAPE ALL MOVIES DATA
"""
1.) Construct new full graph:

Boards
User - Movies
User - Actor
User - Director
User - Genre
Director
Actor
Actor - Genre
Director - Genre

Board size limit > 100 (Join smaller boards)

2.) On the fly creation
Genre
Actor - Genre
Director - Genre
Same actor and director
"""

