from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Movie
from django.views import generic


class MovieListView(generic.ListView):
    model = Movie
    template_name = 'movie/list.html'
    context_object_name = 'movies'
    paginate_by = 8


class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = 'movie/detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_reviews'] = self.object.review_set.all().exists()
        return context
