from django.db import models
from django.contrib.auth.models import AbstractUser

# The abstract user class provides most of the base functionality needed for a user class, e.g. username, email, etc.
# See here: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser


class User(AbstractUser):

    # The user should not be an admin by default
    is_admin = models.BooleanField(default=False)



