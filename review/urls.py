from django.urls import path

from . import views

urlpatterns = [
    path('', views.movie_reviews, name='movie_reviews')
]