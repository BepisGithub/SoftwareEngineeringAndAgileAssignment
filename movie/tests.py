from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, timedelta

from .models import Movie

# Relatively few tests are required for this since there is no way for any user (apart from the site owner) to create,
# update or delete any

class MovieTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.movie = Movie.objects.create(
            id=1,
            title='Test Movie',
            description='Test Description',
            duration=timedelta(hours=3),
            date_released=datetime.today(),
            average_rating_out_of_five=None
        )

    def test_movie_list_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movie/index.html')

    def test_movie_display_view(self):
        response = self.client.get(reverse('display', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movie/display.html')

    def test_that_movie_title_cannot_exceed_100_chars(self):
        self.movie.title = 'A'*101

        with self.assertRaises(ValidationError):
            self.movie.full_clean()

    def test_that_movie_title_cannot_be_empty(self):
        self.movie.title = ''

        with self.assertRaises(ValidationError):
            self.movie.full_clean()

    def test_that_movie_description_cannot_be_empty(self):
        self.movie.description = ''

        with self.assertRaises(ValidationError):
            self.movie.full_clean()

    def test_that_movie_duration_cannot_be_empty(self):
        self.movie.duration = None

        with self.assertRaises(ValidationError):
            self.movie.full_clean()

    def test_that_movie_date_released_cannot_be_empty(self):
        self.movie.date_released = None

        with self.assertRaises(ValidationError):
            self.movie.full_clean()

    def test_that_movie_rating_can_be_empty(self):
        self.movie.average_rating_out_of_five = None

        self.movie.full_clean()
