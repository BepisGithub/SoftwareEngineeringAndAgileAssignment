from django.urls import path, include

from . import views

# A mapping of urls to views
urlpatterns = [
    path('', views.MovieListView.as_view(), name='list'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='detail'),
    path('<int:pk>/reviews/', include('review.urls'))
]