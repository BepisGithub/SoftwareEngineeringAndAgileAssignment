from datetime import timedelta, datetime

from django.db import IntegrityError
from django.test import TestCase, Client


from django.urls import reverse

from movie.models import Movie
from user.models import User

from review.models import Review


class ReviewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(
            username='test_user',
            email="JDoe@email.com",
            password='asdfasdf123123'
        )
        self.user1.save()
        self.client.force_login(self.user1)

        self.user2 = User.objects.create(
            username='second_test_user',
            email="DJoe@email.com",
            password='asdfasdf123123'
        )
        self.user2.save()

        self.movie1 = Movie.objects.create(
            id=1,
            title='Test Movie',
            description='Test Description',
            duration=timedelta(hours=3),
            date_released=datetime.today(),
            average_rating_out_of_five=None
        )

        self.movie1.save()

        self.movie2 = Movie.objects.create(
            id=2,
            title='Second Test Movie',
            description='Second Test Description',
            duration=timedelta(hours=3),
            date_released=datetime.today(),
            average_rating_out_of_five=None
        )

        self.movie2.save()

        self.valid_review = {
            'title': 'review title',
            'message': 'review message',
            'rating_out_of_five': 5,
        }

    # Create tests



    # Read tests

    # Update tests


    # Delete tests



