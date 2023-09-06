from django.db import models
from django.contrib.auth.models import AbstractUser

# The abstract user class provides most of the base functionality needed for a user class, e.g. username, email, etc.
# See here: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser


class User(AbstractUser):

    # This implementation has been chosen over the is_staff built in functionality because I plan to disable all the
    # admin dashboards and special features. The only special thing the admin should be able to do is delete other
    # users' reviews. This will be easier to implement with a custom field (as opposed to preventing a staff user from
    # using the other built in tools

    is_admin = models.BooleanField(default=False)

    is_superuser = None
    is_staff = None



