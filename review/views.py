from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Avg
from datetime import datetime

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
        context['first_review'] = True
        if not self.request.user.is_authenticated:
            return context
        review_already_exists = Review.objects.filter(user=self.request.user, movie=context['movie']).exists()
        if review_already_exists:
            context['first_review'] = False
        return context


class ReviewDetailView(generic.DetailView):
    model = Review
    template_name = 'review/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, pk=self.kwargs['pk'])
        context['review_index'] = self.kwargs['review_id'] # TODO: refactor to have review_id and index consistent across URLs
        return context

    def get_object(self, queryset=None):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        review = movie.review_set.all()[self.kwargs['review_id'] - 1]
        return review


class ReviewCreateView(LoginRequiredMixin, generic.CreateView):
    model = Review
    fields = ['title', 'message', 'rating_out_of_five']

    def get(self, request, *args, **kwargs):
        movie = get_object_or_404(Movie, id=self.kwargs['pk'])
        review_already_exists = Review.objects.filter(user=self.request.user, movie=movie).exists()
        if review_already_exists:
            raise PermissionDenied('You have already written a review for this movie')
        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, pk=self.kwargs['pk'])
        context['action'] = 'Create'
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


# Whenever the rating is displayed, append "/5" to it so people know the rating is out of 5 not 10
class ReviewUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Review
    fields = ['title', 'message', 'rating_out_of_five']

    def get_success_url(self):
        return reverse_lazy('review:display', kwargs={'pk': self.kwargs['pk'], 'review_id': self.kwargs['review_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, pk=self.kwargs['pk'])
        context['action'] = 'Update'
        return context

    def get_object(self, queryset=None):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        review = movie.review_set.all()[self.kwargs['review_id'] - 1]
        if self.request.user != review.user:
            raise PermissionDenied('You cannot update this review because you did not write it!')
        return review

    def form_valid(self, form):
        form.instance.date_last_edited = datetime.now()
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


class ReviewDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Review

    def get_success_url(self):
        return reverse_lazy('review:movie_reviews', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        # TODO: Duplicate code fragment, consider extracting to a helper method
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        review = movie.review_set.all()[self.kwargs['review_id'] - 1]
        if self.request.user != review.user and not self.request.user.is_admin:
            raise PermissionDenied('You cannot delete this review since you neither wrote it nor are you an admin')
        return review

    def form_valid(self, form):

        response = super().form_valid(form)

        # TODO: make this a helper method since we will call this also for updating and deleting reviews
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        updated_average_rating = Review.objects.filter(movie=movie).aggregate(
            Avg('rating_out_of_five'))['rating_out_of_five__avg']
        movie.average_rating_out_of_five = updated_average_rating
        movie.save()
        return response


