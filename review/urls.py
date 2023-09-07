from django.urls import path

from . import views

app_name = 'review'

urlpatterns = [
    path('', views.movie_reviews, name='movie_reviews')
]