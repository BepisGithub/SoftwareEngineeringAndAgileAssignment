from django.urls import path

from . import views

# Declare app name to reference these views from other apps
app_name = 'review'

# A mapping of urls to views
urlpatterns = [
    path('', views.ReviewListView.as_view(), name='list'),
    path('create/', views.ReviewCreateView.as_view(), name='create'),
    path('<int:review_id>/', views.ReviewDetailView.as_view(), name='detail'),
    path('<int:review_id>/update/', views.ReviewUpdateView.as_view(), name='update'),
    path('<int:review_id>/delete/', views.ReviewDeleteView.as_view(), name='delete')

]