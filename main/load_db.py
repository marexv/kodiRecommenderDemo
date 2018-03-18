import csv

from main.models import Genre, Movie, User, Rating, Tag

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
        
path_movies = 'csvData/tags.csv'