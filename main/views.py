import json
import operator
from collections import Counter
from random import randrange, uniform

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from main.models import Board, Movie
from main.forms import movieForm

# Create your views here.
def get_recommendations(movie, steps=1000, alpha=0.5):
    boards = Board.objects.annotate(Count('movies')).filter(movies=movie).order_by('-movies__count')
    starting_node = boards[0]
    board_node = starting_node
    #
    movies = {}
    #
    for step in range(steps):
        #
        movies_in_board = board_node.movies.all()
        next_movie_index = randrange(0, len(movies_in_board))
        movie_node = movies_in_board[next_movie_index]
        try:
            movies[movie_node] = movies[movie_node] +1
        except KeyError:
            movies[movie_node] = 1
        except Exception as e:
            print("Exception " + str(e))
        #
        boards_containging_movie = movie_node.boards.all()
        next_board_index = randrange(0, len(boards_containging_movie))
        board_node = boards_containging_movie[next_board_index]
        #
        if uniform(0,1) < 0.5:
            board_node = starting_node
    #
    sorted_movies = sorted(movies.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_movies


def autocomplete(request):
    """Autocomplete fbid field in form used to send transaction notification.
    
    Function needed for webservice simulation page

    Search by name, surname, username
    """
    data = request.GET
    term = data.get("term")

    if term:
        movies = Movie.objects.filter(title__icontains=term)
    else:
        movies = Movie.objects.all()
    
    results = []
    for movie in movies:
        movies_json = {}
        movies_json['id'] = movie.movie_id
        movies_json['label'] = movie.title
        movies_json['value'] = movie.title
        results.append(movies_json)
    
    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def index(request):
    if request.method == 'POST':
        form = movieForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            form = movieForm()
            if Movie.objects.filter(title=title).exists():
                movie = Movie.objects.filter(title=title)[0]

                recommendations = get_recommendations(movie)[:10]
                recommendations = [movie[0].title for movie in recommendations]

                return render(
                            request,
                            "main/index.html", 
                            {"form":form,
                             "status": "Here are your recommendations",
                             "anchor" : "recommender",
                             "recommendations":recommendations})
            else:
                return render(request, 
                              "main/index.html", 
                              {"form": form,
                               "status": "Movie not found",
                               "anchor" : "page-top",
                               "recommendations": None})
        else:
            print("form is not valid")       
    else:
        form = movieForm()

    return render(
        request,
        'main/index.html',
        {"form": form,
         "status": None,
         "anchor" : "page-top",
         "recommendations": None})