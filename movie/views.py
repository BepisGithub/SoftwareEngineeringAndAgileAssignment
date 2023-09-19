from .models import Movie
from django.views import generic


# This lists all the movies in the database
class MovieListView(generic.ListView):
    model = Movie
    # Renders the result to the list.html file
    template_name = 'movie/list.html'
    context_object_name = 'movies'
    # Displays 8 movies per page
    paginate_by = 8


# Displays an individual movie with more information
class MovieDetailView(generic.DetailView):
    model = Movie
    # Renders the result to the detail.html file
    template_name = 'movie/detail.html'
    context_object_name = 'movie'

    # This method is used to get additional data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We create a variable to see if the movie has any reviews, and if it does then we  create a hyperlink to
        # view them
        context['has_reviews'] = self.object.review_set.all().exists()
        return context
