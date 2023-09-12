from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, timedelta

from .models import Movie


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