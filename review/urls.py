from django.urls import path

from . import views

app_name = 'review'

urlpatterns = [
    path('', views.ReviewListView.as_view(), name='movie_reviews')
]