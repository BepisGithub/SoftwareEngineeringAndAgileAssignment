from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.MovieListView.as_view(), name='index'),
    path('movies/<int:pk>', views.MovieDetailView.as_view(), name='display'),
    path('<int:pk>/reviews', include('review.urls'))
]