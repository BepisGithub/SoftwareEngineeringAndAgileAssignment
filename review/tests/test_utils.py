from django.test import TestCase, Client
from django.urls import reverse
from user.models import User
from movie.models import Movie
from datetime import timedelta, datetime


# Common class shared between all the review test files
class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create two users
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

        # Create 2 movies
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

        # Constants

        self.VALID_REVIEW = {
            'title': 'review title',
            'message': 'review message',
            'rating_out_of_five': 5,
        }

        self.SECOND_REVIEW = {
            'title': 'second review title',
            'message': 'second review message',
            'rating_out_of_five': 5,
        }


# This method is passed a review and then there are optional parameters to modify each of the review fields
def get_updated_details(review_dict, title=None, message=None, rating_out_of_five=None):

    # the is not None check in the conditional is necessary because an empty string will evaluate to false
    # , but we may want to set the value to an empty string for certain tests
    if title is not None:
        review_dict['title'] = title
    if message is not None:
        review_dict['message'] = message
    if rating_out_of_five is not None:
        review_dict['rating_out_of_five'] = rating_out_of_five
    return review_dict


def create_review_for_movie(client, review, movie_id):
    response = client.post(reverse('review:create', args=[movie_id]), review)
    return response


def set_user_to_admin(user):
    user.is_admin = True
    user.save()