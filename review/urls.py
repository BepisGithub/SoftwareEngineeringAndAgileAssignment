from django.urls import path

from . import views

app_name = 'review'

# TODO: improve the front end by using some CSS
urlpatterns = [
    path('', views.ReviewListView.as_view(), name='list'),
    path('create/', views.ReviewCreateView.as_view(), name='create'),
    path('<int:nth_review>/', views.ReviewDetailView.as_view(), name='detail'),
    path('<int:nth_review>/update/', views.ReviewUpdateView.as_view(), name='update'),
    path('<int:nth_review>/delete/', views.ReviewDeleteView.as_view(), name='delete')

]