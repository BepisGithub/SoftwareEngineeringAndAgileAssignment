from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Avg

from movie.models import Movie
from .models import Review
from django.views import generic


class ReviewListView(generic.ListView):
    model = Review
    # TODO: refactor all template names to have a consistent naming convention across apps
    template_name = 'review/movie_reviews.html'
    context_object_name = 'reviews'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, id=self.kwargs['pk'])
        context['reviews'] = context['reviews'].filter(movie_id=self.kwargs['pk'])
        return context


class ReviewDetailView(generic.DetailView):
    model = Review
    template_name = 'review/display.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, pk=self.kwargs['pk'])
        return context

    def get_object(self, queryset=None):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        review = movie.review_set.all()[self.kwargs['review_id'] - 1]
        return review


class ReviewCreateView(LoginRequiredMixin, generic.CreateView):
    model = Review
    fields = ['title', 'message', 'rating_out_of_five']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('review:movie_reviews', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie = get_object_or_404(Movie, id=self.kwargs['pk'])
        form.save()
        response = super().form_valid(form)

        # Updating the movie's average rating upon review creation
        # TODO: make this a helper method since we will call this also for updating and deleting reviews
        movie = form.instance.movie
        updated_average_rating = Review.objects.filter(movie=movie).aggregate(
            Avg('rating_out_of_five'))['rating_out_of_five__avg']
        movie.average_rating_out_of_five = updated_average_rating
        movie.save()
        return response


class ReviewUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Review
    fields = ['title', 'message', 'rating_out_of_five']

    def get_success_url(self):
        return reverse_lazy('review:movie_reviews', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, pk=self.kwargs['pk'])
        return context

    def get_object(self, queryset=None):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        review = movie.review_set.all()[self.kwargs['review_id'] - 1]
        return review

    def form_valid(self, form):

        form.save()
        response = super().form_valid(form)

        # Updating the movie's average rating upon review creation
        # TODO: make this a helper method since we will call this also for updating and deleting reviews
        movie = form.instance.movie
        updated_average_rating = Review.objects.filter(movie=movie).aggregate(
            Avg('rating_out_of_five'))['rating_out_of_five__avg']
        movie.average_rating_out_of_five = updated_average_rating
        movie.save()
        return response
