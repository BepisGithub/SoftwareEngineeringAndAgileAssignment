from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Movie


def index(request):
    # TODO: add pagination
    movies = Movie.objects.all()
    template_path = 'movie/index.html'
    context = {
        'movies': movies
    }

    return render(request, template_path, context)


def display(request, id):
    movie = get_object_or_404(Movie, id=id)
    template_path = 'movie/display.html'
    context = {
        'movie': movie
    }

    return render(request, template_path, context)