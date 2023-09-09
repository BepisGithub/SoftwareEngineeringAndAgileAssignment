from django.urls import path

from . import views

app_name = 'review'

urlpatterns = [
    path('', views.ReviewListView.as_view(), name='movie_reviews'),
    path('create/', views.ReviewCreateView.as_view(), name='create_movie_review'),
    path('<int:review_id>/', views.ReviewDetailView.as_view(), name='display')
]