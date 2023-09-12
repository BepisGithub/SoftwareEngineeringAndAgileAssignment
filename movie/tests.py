from django.test import TestCase, Client
from django.urls import reverse

from .models import Movie


class MovieTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_movie_list_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movie/index.html')