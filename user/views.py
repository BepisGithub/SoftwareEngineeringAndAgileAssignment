import logging

from django.contrib.auth import login, user_login_failed

# This mixin means only authenticated users can access the views that take it in their constructor
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import UserRegistrationForm
from .models import User

# Get logger to log form errors
logger = logging.getLogger('logger')


# This lists all the users
class UserListView(generic.ListView):
    model = User
    # Renders the result to the list.html file
    template_name = 'user/list.html'
    context_object_name = 'users'
    # Displays 8 users per page
    paginate_by = 8


# Displays an individual user with more information
class UserDetailView(generic.DetailView):
    model = User
    # Renders the result to the detail.html file
    template_name = 'user/detail.html'
    context_object_name = 'displayed_user'


# Handles the editing/updating of existing users
class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    # Updatable fields
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'user/update_user_form.html'
    context_object_name = 'displayed_user'

    # Enforces the constraint that a user can only edit their own profile, not anyone elses
    def get_object(self):
        displayed_user = User.objects.get(id=self.kwargs['pk'])
        if self.request.user != displayed_user:
            raise PermissionDenied('You cannot update someone else\'s user profile!')
        return self.request.user

    # Additional checks to enforce the presence of the email
    def form_valid(self, form):
        self.request.user = User.objects.get(id=self.kwargs['pk'])
        if not form.instance.email:
            form.add_error('email', "email must be present")
            logger.warning('User profile update by user ' + self.request.user.username + ' failed. Form errors: '
                           + str(form.errors))
            return super().form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):

        # The clean() method in the user model throws an error called __all__ when it failes, so we rename it here
        # to make it clearer to the user
        if '__all__' in form.errors:
            form.errors['first and last names'] = form.errors['__all__']
            del form.errors['__all__']

        # Additional checks to enforce the presence of the email
        if not form.instance.email:
            form.add_error('email', "email must be present")

        # This is to fix a bug where when trying to change a username to one that is taken, the updated username shows
        # in the navbar, like "Hello, (taken username)" which is extremely confusing for the user since the username
        # change did not take place. Hence, this fix
        self.request.user = User.objects.get(id=self.kwargs['pk'])

        # If the form is invalid, we log the form errors
        logger.warning('User profile update by user ' + self.request.user.username + ' failed. Form errors: '
                       + str(form.errors))
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('user:detail', kwargs={'pk': self.kwargs['pk']})


# Handles the deleting of existing users
class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('user:list')
    context_object_name = 'displayed_user'

    # Enforces the constraint that a user can only delete their own profile, not anyone elses
    def get_object(self):
        displayed_user = User.objects.get(id=self.kwargs['pk'])
        if self.request.user != displayed_user:
            raise PermissionDenied('You cannot delete someone else\'s user profile!')
        return self.request.user


# Extending Django's built in password change view so we can log if there is an error
class CustomPasswordChangeView(PasswordChangeView):
    def form_invalid(self, form):
        logger.warning('Password change failed for username: ' + form.user.username)
        return super().form_invalid(form)


# This method handles the creation of new users
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        # We check if the names have digits. The reason we do this manually instead of relying on the error raised by
        # the clean() method on the user model is that I want this error to be specific to which name is in violation
        # of the rule
        first_name = form.data.get('first_name', "")
        last_name = form.data.get('last_name', "")

        if first_name and not first_name.isalpha():
            form.add_error('first_name', "Names cannot have digits")

        if last_name and not last_name.isalpha():
            form.add_error('last_name', "Names cannot have digits")

        if form.is_valid():
            # Create the user account and then log them in and redirect them to the home page
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

            # If the form is invalid, we log the form errors
            logger.warning('User creation failed. Form errors: ' + str(form.errors))

    else:
        # Display the registration form
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})


# This listens for when a login fails and then logs the incident
@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    logger.warning('User login failed for username: ' + str(credentials['username']))
