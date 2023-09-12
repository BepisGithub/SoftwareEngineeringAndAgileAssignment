from django.urls import path

from . import views

app_name = 'user'

# TODO: improve the front end by using some CSS
urlpatterns = [
    path('', views.UserListView.as_view(), name='users'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user')
]