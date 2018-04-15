import json

from django.http import HttpResponse
from django.shortcuts import render

from main.models import Movie
from main.forms import movieForm

from main.graph_as_dict import get_recommendations

# Create your views here.
def autocomplete(request):
    """Function for autocompleting search form."""
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

                # Chanege Algorithms here:
                recommendations = get_recommendations(movie)

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