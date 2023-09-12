from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import generic

from .forms import UserRegistrationForm
from .models import User


class UserListView(generic.ListView):
    model = User
    template_name = 'user/users.html'
    context_object_name = 'users'

class UserDetailView(generic.DetailView):
    model = User
    template_name = 'user/user.html'
    context_object_name = 'displayed_user'



# TODO: add a forgot account/forgot details option

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})