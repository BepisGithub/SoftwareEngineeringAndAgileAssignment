from django.db import models


class Movie(models.Model):

    # Most movie titles are extremely short, so a 100 character length should be sufficient for any movie
    title = models.CharField(max_length=100)

    # A TextField is used here because a CharField in Django only guarantees 255 characters, which is not enough
    # for a lengthy review
    description = models.TextField()

    # Stores the duration as a timedelta python object and stores the value as a bigint in the database
    # See: https://docs.djangoproject.com/en/4.2/ref/models/fields/#durationfield
    duration = models.DurationField()

    # The time that a movie was released is unnecessary to store, hence only the date is stored
    date_released = models.DateField()

    # This will be calculated according to the ratings from the review table, so we will set the initial value to null
    average_rating_out_of_five = models.FloatField(null=True, blank=True)

    # Django by default appends the app name before the class name for the table title, this statement
    # renames the table for a cleaner naming convention (so the table is called Movie instead of movie_movie)
    class Meta:
        db_table = 'Movie'
