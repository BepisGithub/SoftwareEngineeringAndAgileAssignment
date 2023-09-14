from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Avg
from datetime import datetime

from movie.models import Movie
from .models import Review
from django.views import generic


class ReviewListView(generic.ListView):
    model = Review
    template_name = 'review/list.html'
    context_object_name = 'reviews'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, id=self.kwargs['pk'])
        context['first_review'] = True
        if not self.request.user.is_authenticated:
            return context
        review_already_exists = Review.objects.filter(user=self.request.user, movie=context['movie']).exists()
        if review_already_exists:
            context['first_review'] = False
        return context

    def get_queryset(self):
        return Review.objects.filter(movie_id=self.kwargs['pk'])


class ReviewDetailView(generic.DetailView):
    model = Review
    template_name = 'review/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, pk=self.kwargs['pk'])
        return context

    def get_object(self, queryset=None):
        review = Review.objects.filter(id=self.kwargs['review_id']).get()
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
        return reverse_lazy('review:list', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie = get_object_or_404(Movie, id=self.kwargs['pk'])
        form.save()
        response = super().form_valid(form)
        # Updating the movie's average rating upon review creation
        update_average_rating_for_movie(form.instance.movie)
        return response


class ReviewUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Review
    fields = ['title', 'message', 'rating_out_of_five']

    def get_success_url(self):
        return reverse_lazy('review:detail', kwargs={'pk': self.kwargs['pk'], 'review_id': self.kwargs['review_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, pk=self.kwargs['pk'])
        context['action'] = 'Update'
        return context

    def get_object(self, queryset=None):
        review = Review.objects.filter(id=self.kwargs['review_id']).get()
        if self.request.user != review.user:
            raise PermissionDenied('You cannot update this review because you did not write it!')
        return review

    def form_valid(self, form):
        form.instance.date_last_edited = datetime.now()
        form.save()
        response = super().form_valid(form)
        # Updating the movie's average rating upon review creation
        update_average_rating_for_movie(form.instance.movie)
        return response


class ReviewDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Review

    def get_success_url(self):
        movie_id = self.object.movie.id
        movie_has_reviews = Review.objects.filter(movie_id=movie_id).exclude(id=self.object.id).exists()
        if movie_has_reviews:
            return reverse_lazy('review:list', kwargs={'pk': self.kwargs['pk']})
        else:
            return reverse_lazy('detail', kwargs={'pk': self.kwargs['pk']})


    def get_object(self, queryset=None):
        review = Review.objects.filter(id=self.kwargs['review_id']).get()
        if self.request.user != review.user and not self.request.user.is_admin:
            raise PermissionDenied('You cannot delete this review since you neither wrote it nor are you an admin')
        return review

    def form_valid(self, form):
        response = super().form_valid(form)
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        update_average_rating_for_movie(movie)
        return response


def update_average_rating_for_movie(movie):
    updated_average_rating = Review.objects.filter(movie=movie).aggregate(
        Avg('rating_out_of_five'))['rating_out_of_five__avg']
    movie.average_rating_out_of_five = updated_average_rating
    movie.save()
