from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):

    # These are the foreign keys for the users who write the reviews and the movies that the reviews are about

    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE  # This means that if the user is deleted, the reviews are too. This will make data
                                  # compliance laws easier to follow (if the user deletes their account, they probably
                                  # want all their data deleted too)
    )

    movie_id = models.ForeignKey(
        'movie.Movie',
        on_delete=models.CASCADE  # this means that if the movie is deleted, the reviews for it will be too.
    )

    # MySQL allows for over 60,000 characters in the varchar type, which is what the charfield is stored as, making it
    # big enough for all types of text in the review model.

    # 100 characters is more than enough to have a concise review title
    title = models.CharField(max_length=100)

    # 25,000 characters is ~3500-6250 words, which should be sufficient for all reviews
    message = models.CharField(max_length=25_000)

    rating_out_of_five = models.IntegerField(
        validators=[  # Enforcing the 1-5 start limit
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )

    date_posted = models.DateTimeField()

    # This should be blank until the review has been edited at least once
    date_last_edited = models.DateTimeField(null=True, blank=True)



