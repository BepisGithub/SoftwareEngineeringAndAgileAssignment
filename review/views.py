from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from movie.models import Movie
from .models import Review


def movie_reviews(request, id):
    movie = get_object_or_404(Movie, id=id)
    reviews = Review.objects.filter(movie_id=movie)
    template_path = 'review/movie_reviews.html'
    context = {
        'movie': movie,
        'reviews': reviews
    }
    return render(request, template_path, context)
