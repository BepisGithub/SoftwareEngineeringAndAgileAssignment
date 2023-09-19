import logging

from django.contrib.auth import login, user_login_failed
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import UserRegistrationForm
from .models import User

logger = logging.getLogger('logger')


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

    def form_valid(self, form):
        self.request.user = User.objects.get(id=self.kwargs['pk'])
        if not form.instance.email:
            form.add_error('email', "email must be present")
            logger.warning('User profile update by user ' + self.request.user.username + ' failed. Form errors: '
                           + str(form.errors))
            return super().form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        # This is to fix a bug where when trying to change a username to one that is taken, the updated username shows
        # in the navbar, like "Hello, (taken username)" which is extremely confusing for the user since the username
        # change did not take place. Hence, this fix
        if '__all__' in form.errors:
            form.errors['first and last names'] = form.errors['__all__']
            del form.errors['__all__']

        if not form.instance.email:
            form.add_error('email', "email must be present")

        self.request.user = User.objects.get(id=self.kwargs['pk'])

        logger.warning('User profile update by user ' + self.request.user.username + ' failed. Form errors: '
                       + str(form.errors))
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


class CustomPasswordChangeView(PasswordChangeView):
    def form_invalid(self, form):
        logger.warning('Password change failed for username: ' + form.user.username)
        return super().form_invalid(form)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        first_name = form.data.get('first_name', "")
        last_name = form.data.get('last_name', "")

        if first_name and not first_name.isalpha():
            form.add_error('first_name', "Names cannot have digits")

        if last_name and not last_name.isalpha():
            form.add_error('last_name', "Names cannot have digits")

        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('/')
        else:
            # This is the error from the user model that is raised when the names have numbers, we do not need this
            # Since we are doing another check here to get which names specifically have numbers
            if '__all__' in form.errors:
                del form.errors['__all__']

            # Removing the underscore in the key name
            if 'first_name' in form.errors:
                form.errors['first name'] = form.errors['first_name']
                del form.errors['first_name']
            if 'last_name' in form.errors:
                form.errors['last name'] = form.errors['last_name']
                del form.errors['last_name']

            # Renaming the password errors
            if 'password2' in form.errors:
                form.errors['password'] = form.errors['password2']
                del form.errors['password2']

            logger.warning('User creation failed. Form errors: ' + str(form.errors))

    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    logger.warning('User login failed for username: ' + str(credentials['username']))
