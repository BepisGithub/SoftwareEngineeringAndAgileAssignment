from django.core.validators import DecimalValidator
from django.db import models


class Movie(models.Model):
    # Most movie titles are extremely short, so a 100 character length should be sufficient for any movie
    title = models.CharField(max_length=100)

    # A TextField is used here because a CharField in Django only guarantees 255 characters, which is not enough
    # for a lengthy review
    description = models.TextField()

    # The source will be taken from IMDB
    image_url = models.URLField(max_length=500, blank=True, null=True)

    # Stores the duration as a timedelta python object and stores the value as a bigint in the database
    # See: https://docs.djangoproject.com/en/4.2/ref/models/fields/#durationfield
    duration = models.DurationField()

    # The time that a movie was released is unnecessary to store, hence only the date is stored
    date_released = models.DateField()

    # This will be calculated according to the ratings from the review table, so we will set the initial value to null
    average_rating_out_of_five = models.DecimalField(
        null=True,
        blank=True,
        # We will have one decimal place to balance between accuracy and readability
        decimal_places=1,
        max_digits=2,
        validators=[DecimalValidator(max_digits=2, decimal_places=1)]
    )
