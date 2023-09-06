from django.http import HttpResponse
from django.shortcuts import render

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