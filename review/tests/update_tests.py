from datetime import timedelta, datetime

from django.db import IntegrityError
from django.test import TestCase, Client


from django.urls import reverse

from movie.models import Movie
from user.models import User

from review.models import Review

from review.tests.test_utils import BaseTestCase


class UpdateReviewTestCase(BaseTestCase):

    def create_valid_review_for_movie(self, movie_id):
        response = self.client.post(reverse('review:create_movie_review', args=[movie_id]), self.valid_review)
        return response

    def test_that_an_authenticated_user_can_see_the_update_view_for_his_review(self):
        self.create_valid_review_for_movie(self.movie1.id)
        response = self.client.get(reverse('review:update', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/review_form.html')

    def test_that_an_authenticated_user_can_update_his_reviews_title(self):
        self.create_valid_review_for_movie(self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = {
            'title': 'new title',
            'message': review.message,
            'rating_out_of_five': review.rating_out_of_five
        }

        self.assertNotEqual(review.title, updated_details['title'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertEqual(review.title, updated_details['title'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_title_to_empty(self):
        self.create_valid_review_for_movie(self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = {
            'title': '',
            'message': review.message,
            'rating_out_of_five': review.rating_out_of_five
        }

        self.assertNotEqual(review.title, updated_details['title'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.title, updated_details['title'])

    def test_that_an_authenticated_user_can_update_his_reviews_message(self):
        self.create_valid_review_for_movie(self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = {
            'title': review.title,
            'message': 'new message',
            'rating_out_of_five': review.rating_out_of_five
        }

        self.assertNotEqual(review.message, updated_details['message'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertEqual(review.message, updated_details['message'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_message_to_empty(self):
        self.create_valid_review_for_movie(self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = {
            'title': review.title,
            'message': '',
            'rating_out_of_five': review.rating_out_of_five
        }

        self.assertNotEqual(review.message, updated_details['message'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.message, updated_details['message'])

    def test_that_an_authenticated_user_can_update_his_reviews_rating(self):
        self.create_valid_review_for_movie(self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = {
            'title': review.title,
            'message': review.message,
            'rating_out_of_five': review.rating_out_of_five - 1
        }

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_empty(self):
        self.create_valid_review_for_movie(self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = {
            'title': review.title,
            'message': review.message,
            'rating_out_of_five': ''
        }

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_less_than_one(self):
        self.create_valid_review_for_movie(self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = {
            'title': review.title,
            'message': review.message,
            'rating_out_of_five': 0
        }

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_greater_than_five(self):
        self.create_valid_review_for_movie(self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = {
            'title': review.title,
            'message': review.message,
            'rating_out_of_five': 6
        }

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_a_float(self):
        self.create_valid_review_for_movie(self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = {
            'title': review.title,
            'message': review.message,
            'rating_out_of_five': 4.4
        }

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_an_alphabetical_value(self):
        self.create_valid_review_for_movie(self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = {
            'title': review.title,
            'message': review.message,
            'rating_out_of_five': 'five'
        }

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_is_redirected_back_to_the_update_form_on_unsuccessful_update(self):
        self.create_valid_review_for_movie(self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = {
            'title': '',
            'message': '',
            'rating_out_of_five': 0
        }

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        self.assertEqual(response.status_code, 200) # TODO: comment that unsuccessfull updates cause the view to rerender the form which means no redirect thus a 200 code
        self.assertTemplateUsed('review/review_form.html')
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())


    def test_that_an_authenticated_user_cannot_see_the_update_view_for_another_users_review(self):
        self.create_valid_review_for_movie(self.movie1.id)
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.get(reverse('review:update', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_admin_user_cannot_see_the_update_view_for_another_users_review(self):
        self.create_valid_review_for_movie(self.movie1.id)
        self.client.logout()
        self.user2.is_admin = True
        self.user2.save()
        self.client.force_login(self.user2)
        self.assertTrue(self.user2.is_admin)
        response = self.client.get(reverse('review:update', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_authenticated_user_cannot_update_another_users_review(self):
        self.create_valid_review_for_movie(self.movie1.id)
        self.client.logout()
        self.client.force_login(self.user2)

        updated_details = {
            'title': 'new title',
            'message': 'new message',
            'rating_out_of_five': 1
        }
        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        self.assertNotEqual(review.title, updated_details['title'])
        self.assertNotEqual(review.message, updated_details['message'])
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, 1]), updated_details)

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(review.title, updated_details['title'])
        self.assertNotEqual(review.message, updated_details['message'])
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_admin_user_cannot_update_another_users_review(self):
        self.create_valid_review_for_movie(self.movie1.id)
        self.client.logout()
        self.user2.is_admin = True
        self.user2.save()
        self.client.force_login(self.user2)
        self.assertTrue(self.user2.is_admin)

        updated_details = {
            'title': 'new title',
            'message': 'new message',
            'rating_out_of_five': 1
        }
        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        # Only need to check one since the update either succeeded entirely or failed entirely
        self.assertNotEqual(review.title, updated_details['title'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, 1]), updated_details)

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(review.title, updated_details['title'])

    def test_that_an_unauthenticated_user_cannot_see_the_update_view_for_another_users_review(self):
        self.create_valid_review_for_movie(self.movie1.id)
        self.client.logout()
        response = self.client.get(reverse('review:update', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_unauthenticated_user_cannot_update_another_users_review(self):
        self.create_valid_review_for_movie(self.movie1.id)
        self.client.logout()

        updated_details = {
            'title': 'new title',
            'message': 'new message',
            'rating_out_of_five': 1
        }
        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        self.assertNotEqual(review.title, updated_details['title'])
        self.assertNotEqual(review.message, updated_details['message'])
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, 1]), updated_details)

        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(review.title, updated_details['title'])
        self.assertNotEqual(review.message, updated_details['message'])
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_unauthenticated_user_is_redirected_to_login_when_trying_to_update_a_user(self):
        self.create_valid_review_for_movie(self.movie1.id)
        self.client.logout()
        updated_details = {
            'title': 'new title',
            'message': 'new message',
            'rating_out_of_five': 1
        }
        response = self.client.post(reverse('review:update', args=[self.movie1.id, 1]), updated_details, follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')
