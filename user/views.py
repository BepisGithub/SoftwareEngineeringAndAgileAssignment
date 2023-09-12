from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
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


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'user/update_user_form.html'
    context_object_name = 'displayed_user'

    def get_object(self):
        displayed_user = User.objects.get(id=self.kwargs['pk'])
        if self.request.user != displayed_user:
            raise PermissionDenied('You cannot update someone else\'s user profile!')
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('user:user', kwargs={'pk': self.kwargs['pk']})


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('user:users')
    context_object_name = 'displayed_user'

    def get_object(self):
        displayed_user = User.objects.get(id=self.kwargs['pk'])
        if self.request.user != displayed_user:
            raise PermissionDenied('You cannot delete someone else\'s user profile!')
        return self.request.user



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