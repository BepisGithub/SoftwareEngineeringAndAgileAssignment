import logging

# This mixin means only authenticated users can access the views that take it in their constructor
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Avg
from datetime import datetime

from movie.models import Movie
from .models import Review
from django.views import generic

# Get logger to log form errors
logger = logging.getLogger('logger')


# This lists all the reviews for a given movie in the database
class ReviewListView(generic.ListView):
    model = Review
    # Renders the result to the list.html file
    template_name = 'review/list.html'
    context_object_name = 'reviews'
    # Displays 5 reviews per page
    paginate_by = 5

    # This method is used to get additional data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Here we check if a user has written a review for the movie or not
        context['movie'] = get_object_or_404(Movie, id=self.kwargs['pk'])
        context['first_review'] = True
        if not self.request.user.is_authenticated:
            return context
        pre_existing_review = Review.objects.filter(user=self.request.user, movie=context['movie'])
        # If they have, then we pass their review into the template so that we can add a hyperlink to it.
        # This is because if a user has written a review, they are not shown the form to create a review, but a user
        # may have forgotten that they wrote a review, so they could be confused. This is to remind and show them theirs
        if pre_existing_review.exists():
            context['first_review'] = False
            context['pre_existing_review'] = pre_existing_review.get()
        return context

    # Filter the reviews for the specific movie (as opposed to getting all reviews that exist in the database)
    def get_queryset(self):
        return Review.objects.filter(movie_id=self.kwargs['pk'])


# Displays an individual review with more information
class ReviewDetailView(generic.DetailView):
    model = Review
    # Renders the result to the detail.html file
    template_name = 'review/detail.html'

    # This method is used to get additional data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We pass in the movie so that we can show both the review and the movie the review was written for
        context['movie'] = get_object_or_404(Movie, pk=self.kwargs['pk'])
        return context

    # Get the specific review
    def get_object(self, queryset=None):
        review = Review.objects.filter(id=self.kwargs['review_id']).get()
        return review


# Handles the creation of new reviews
class ReviewCreateView(LoginRequiredMixin, generic.CreateView):
    model = Review
    # These are the required form fields when creating a review
    fields = ['title', 'message', 'rating_out_of_five']

    # This checks whether a user has already written a review, and, if so, prevents them from writing another
    def get(self, request, *args, **kwargs):
        movie = get_object_or_404(Movie, id=self.kwargs['pk'])
        review_already_exists = Review.objects.filter(user=self.request.user, movie=movie).exists()
        if review_already_exists:
            raise PermissionDenied('You have already written a review for this movie')
        return super().get(request, *args, **kwargs)

    # This method is used to get additional data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, pk=self.kwargs['pk'])
        context['action'] = 'Create'
        return context

    # If the review is successfully created, this defines which view to go to
    def get_success_url(self):
        return reverse_lazy('review:list', kwargs={'pk': self.kwargs['pk']})

    # If the form is declared valid, we then set the movie and the user as the foreign key for the review before saving
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie = get_object_or_404(Movie, id=self.kwargs['pk'])
        form.save()
        response = super().form_valid(form)
        # Updating the movie's average rating upon review creation
        update_average_rating_for_movie(form.instance.movie)
        return response

    # If the form is invalid, we log the form errors
    def form_invalid(self, form):
        logger.warning('Review creation by user ' + self.request.user.username + ' failed. Form errors: '
                       + str(form.errors))
        return super().form_invalid(form)


# Handles the editing/updating of existing reviews
# It is handled in a very similar way to the creation of reviews
class ReviewUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Review
    fields = ['title', 'message', 'rating_out_of_five']

    def get_success_url(self):
        return reverse_lazy('review:detail', kwargs={'pk': self.kwargs['pk'], 'review_id': self.kwargs['review_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, pk=self.kwargs['pk'])

        # Since the same form is used for creating and updating, this action defines what to display in the HTML
        context['action'] = 'Update'
        return context

    def get_object(self, queryset=None):
        review = Review.objects.filter(id=self.kwargs['review_id']).get()
        # Enforce the restriction that only an author can edit a review
        if self.request.user != review.user:
            raise PermissionDenied('You cannot update this review because you did not write it!')
        return review

    def form_valid(self, form):
        # If the form is valid, we update the date_last_edited to when the request is processed
        form.instance.date_last_edited = datetime.now()
        form.save()
        response = super().form_valid(form)
        # Updating the movie's average rating upon review creation
        update_average_rating_for_movie(form.instance.movie)
        return response

    # If the form is invalid, we log the form errors
    def form_invalid(self, form):
        logger.warning('Review update by user ' + self.request.user.username + 'for review id ' +
                       str(self.kwargs['review_id']) + 'failed. Form errors: ' + str(form.errors))
        return super().form_invalid(form)


# Handles the deleting of existing reviews
class ReviewDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Review

    # If the movie has any reviews left after the user deletes theirs, then we show the user the rest of the reviews
    # But if it has no reviews left (i.e. the user deleted the last review for the movie), then we should the movie
    # detail page (we cannot show them the reviews since there are none)
    def get_success_url(self):
        movie_id = self.object.movie.id
        movie_has_reviews = Review.objects.filter(movie_id=movie_id).exclude(id=self.object.id).exists()
        if movie_has_reviews:
            return reverse_lazy('review:list', kwargs={'pk': self.kwargs['pk']})
        else:
            return reverse_lazy('detail', kwargs={'pk': self.kwargs['pk']})

    # Here we enforce the restriction that only authors and admins can delete a review
    def get_object(self, queryset=None):
        review = Review.objects.filter(id=self.kwargs['review_id']).get()
        if self.request.user != review.user and not self.request.user.is_admin:
            raise PermissionDenied('You cannot delete this review since you neither wrote it nor are you an admin')
        return review

    # Updating the movie's average rating upon review deletion
    def form_valid(self, form):
        response = super().form_valid(form)
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        update_average_rating_for_movie(movie)
        return response


# Helper method to reduce repetition
def update_average_rating_for_movie(movie):
    updated_average_rating = Review.objects.filter(movie=movie).aggregate(
        Avg('rating_out_of_five'))['rating_out_of_five__avg']
    movie.average_rating_out_of_five = updated_average_rating
    movie.save()
