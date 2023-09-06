from django.db import models
from django.contrib.auth.models import AbstractUser

# The abstract user class provides most of the base functionality needed for a user class, e.g. username, email, etc.
# See here: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser


class User(AbstractUser):

    # These inbuilt Django attributes are being removed because the only special behaviour I want from admins
    # is that they can delete any review, this will be easier to implement by disabling all other admin
    # tools (like the dashboard) and creating a custom field instead
    is_superuser = None
    is_staff = None

    # This custom field is being used instead of Django's built-in groups/permissions system because the scope of
    # this application is small and no other groups will be needed, unlike a real, production-level application that
    # may change and evolve
    is_admin = models.BooleanField(default=False)




