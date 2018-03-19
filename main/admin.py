from django.contrib import admin
from .models import Genre, Movie, User, Tag, Rating, Board

# Register your models here.
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Rating)
admin.site.register(Board)
