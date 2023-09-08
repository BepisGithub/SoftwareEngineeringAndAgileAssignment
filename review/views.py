from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from movie.models import Movie
from .models import Review
from django.views import generic


class ReviewListView(generic.ListView):
    model = Review
    template_name = 'review/movie_reviews.html'
    context_object_name = 'reviews'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, id=self.kwargs['pk'])
        context['reviews'] = context['reviews'].filter(id=self.kwargs['pk'])
        return context
