from datetime import timedelta, datetime

from django.db import IntegrityError
from django.test import TestCase, Client


# Create your tests here.
from django.urls import reverse

from movie.models import Movie
from user.models import User

from review.models import Review


class ReviewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='test_user',
            email="JDoe@email.com",
            password='asdfasdf123123'
        )
        self.user.save()
        self.client.force_login(self.user)

        self.movie = Movie.objects.create(
            id=1,
            title='Test Movie',
            description='Test Description',
            duration=timedelta(hours=3),
            date_released=datetime.today(),
            average_rating_out_of_five=None
        )

        self.movie.save()

    # Create tests

    def test_that_an_authenticated_user_can_see_the_create_view_if_its_their_first_review_of_a_movie(self):
        response = self.client.get(reverse('review:create_movie_review', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/review_form.html')

    def test_that_an_authenticated_user_cannot_see_the_create_view_if_its_not_their_first_review_of_a_movie(self):
        valid_review = {
            'title': 'review title',
            'message': 'review message',
            'rating_out_of_five': 5,
        }
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie.id]), valid_review)

        response = self.client.get(reverse('review:create_movie_review', args=[self.user.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'review/review_form.html')

    # def test_that_an_authenticated_user_can_see_the_create_view_of_another_movie_even_if_they_have_a_review_for_a_different_movie(self):

    # def test_that_creating_a_review_causes_the_average_rating_of_a_movie_to_be_recalculated(self):

    # def test_that_a_review_cannot_have_an_empty_title(self):

    # def test_that_a_review_cannot_have_an_empty_message(self):

    # def test_that_a_review_cannot_have_a_rating_less_than_1(self):

    # def test_that_a_review_cannot_have_a_rating_greater_than_5(self):

    # def test_that_a_review_cannot_have_a_float_rating(self):

    # def test_that_a_review_cannot_have_an_alphabetical_rating(self):

    def test_that_valid_review_creation_succeeds(self):
        valid_review = {
            'title': 'review title',
            'message': 'review message',
            'rating_out_of_five': 5,
        }
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie.id]), valid_review)
        self.assertEqual(Review.objects.filter(movie=self.movie).get(title=valid_review['title']).user, self.user)

    def test_that_a_user_cannot_have_two_reviews_for_the_same_movie(self):
        # TODO: if i use this exact first_review object a lot, consider making it a class variable to reduce repetition
        first_review = {
            'title': 'review title',
            'message': 'review message',
            'rating_out_of_five': 5,
        }
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie.id]), first_review)
        second_review = {
            'title': 'second review title',
            'message': 'second review message',
            'rating_out_of_five': 5,
        }

        with self.assertRaises(IntegrityError):
            response = self.client.post(reverse('review:create_movie_review', args=[self.movie.id]), second_review)

    # Read tests

    def test_review_list_view(self):
        response = self.client.get(reverse('review:movie_reviews', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/movie_reviews.html')

    def test_review_display_view(self):
        valid_review = {
            'title': 'review title',
            'message': 'review message',
            'rating_out_of_five': 5,
        }
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie.id]), valid_review)

        review = Review.objects.filter(movie=self.movie).get(title=valid_review['title'])

        response = self.client.get(reverse('review:display', kwargs={'pk': self.movie.id, 'review_id': review.id }))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/display.html')
        self.assertEqual(valid_review['title'], review.title)
        self.assertEqual(valid_review['message'], review.message)
        self.assertEqual(valid_review['rating_out_of_five'], review.rating_out_of_five)

        self.assertEqual(review.movie.id, self.movie.id)
        self.assertEqual(review.user.id, self.user.id)
