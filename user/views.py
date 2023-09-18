from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import UserRegistrationForm
from .models import User


class UserListView(generic.ListView):
    model = User
    template_name = 'user/list.html'
    context_object_name = 'users'
    paginate_by = 8


class UserDetailView(generic.DetailView):
    model = User
    template_name = 'user/detail.html'
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

    def form_invalid(self, form):
        # This is to fix a bug where when trying to change a username to one that is taken, the updated username shows
        # in the navbar, like "Hello, (taken username)" which is extremely confusing for the user since the username
        # change did not take place. Hence, this fix
        self.request.user = User.objects.get(id=self.kwargs['pk'])
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('user:detail', kwargs={'pk': self.kwargs['pk']})


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('user:list')
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
        first_name = form.data.get('first_name', "")
        last_name = form.data.get('last_name', "")

        if (first_name and not first_name.isalpha()) or (last_name and not last_name.isalpha()):
            form.add_error('first_name', "Names cannot have digits")
            form.add_error('last_name', "Names cannot have digits")
            messages.error(request, "Names cannot have digits")
            return render(request, 'user/register.html', {'form': form})

        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})