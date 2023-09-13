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

    def test_that_an_authenticated_user_can_see_the_create_view_if_its_their_first_review_of_a_movie(self):
        response = self.client.get(reverse('review:create_movie_review', args=[self.user1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/review_form.html')

    def test_that_an_authenticated_user_can_create_a_review_if_its_their_first_review_of_a_movie(self):
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), self.valid_review)
        self.assertEqual(Review.objects.filter(movie=self.movie1).get(title=self.valid_review['title']).user,
                         self.user1)

    def test_that_an_authenticated_user_cannot_see_the_create_view_if_its_not_their_first_review_of_a_movie(self):
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), self.valid_review)

        response = self.client.get(reverse('review:create_movie_review', args=[self.user1.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'review/review_form.html')

    def test_that_an_authenticated_user_cannot_create_a_review_if_its_not_their_first_review_of_a_movie(self):
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), self.valid_review)
        second_review = {
            'title': 'second review title',
            'message': 'second review message',
            'rating_out_of_five': 5,
        }

        with self.assertRaises(IntegrityError):
            response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), second_review)

    def test_that_an_unauthenticated_user_cannot_see_the_create_view(self):
        self.client.logout()
        response = self.client.get(reverse('review:create_movie_review', args=[self.movie1.id]), self.valid_review)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'review/review_form.html')

    def test_that_an_unauthenticated_user_cannot_create_a_review(self):
        self.client.logout()
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), self.valid_review)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    def test_that_an_unauthenticated_user_is_redirected_to_login_when_trying_to_see_the_create_view(self):
        self.client.logout()
        response = self.client.get(reverse('review:create_movie_review', args=[self.movie1.id]), self.valid_review, follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_that_an_unauthenticated_user_is_redirected_to_login_when_trying_to_create_a_review(self):
        self.client.logout()
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), self.valid_review, follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    def test_that_an_authenticated_user_can_see_the_create_view_of_another_movie_even_if_they_have_a_review_for_a_different_movie(self):
        first_response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), self.valid_review)
        second_response = self.client.get(reverse('review:create_movie_review', args=[self.movie2.id]), self.valid_review)
        self.assertEqual(second_response.status_code, 200)
        self.assertTemplateUsed(second_response, 'review/review_form.html')

    def test_that_an_authenticated_user_can_create_a_review_for_another_movie_even_if_they_have_a_review_for_a_different_movie(self):
        first_response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), self.valid_review)
        second_response = self.client.post(reverse('review:create_movie_review', args=[self.movie2.id]), self.valid_review)
        self.assertTrue(Review.objects.filter(movie=self.movie2).exists())

    def test_that_creating_a_review_causes_the_average_rating_of_a_movie_to_be_recalculated(self):
        self.assertNotEqual(self.movie1.average_rating_out_of_five, self.valid_review['rating_out_of_five'])
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), self.valid_review)
        self.movie1.refresh_from_db()
        self.assertEqual(self.movie1.average_rating_out_of_five, self.valid_review['rating_out_of_five'])

    def test_that_a_review_cannot_have_an_empty_title(self):
        invalid_review = self.valid_review
        invalid_review['title'] = ''
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), invalid_review)
        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    def test_that_a_review_cannot_have_an_empty_message(self):
        invalid_review = self.valid_review
        invalid_review['message'] = ''
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), invalid_review)
        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    def test_that_a_review_cannot_have_a_rating_less_than_1(self):
        invalid_review = self.valid_review
        invalid_review['rating_out_of_five'] = 0
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), invalid_review)

        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    def test_that_a_review_cannot_have_a_rating_greater_than_5(self):
        invalid_review = self.valid_review
        invalid_review['rating_out_of_five'] = 6
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), invalid_review)

        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    def test_that_a_review_cannot_have_a_float_rating(self):
        invalid_review = self.valid_review
        invalid_review['rating_out_of_five'] = 3.3
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), invalid_review)

        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    def test_that_a_review_cannot_have_an_alphabetical_rating(self):
        invalid_review = self.valid_review
        invalid_review['rating_out_of_five'] = 'a'
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), invalid_review)

        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    # Read tests

    def test_review_list_view(self):
        response = self.client.get(reverse('review:movie_reviews', args=[self.movie1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/movie_reviews.html')

    def test_review_display_view(self):
        response = self.client.post(reverse('review:create_movie_review', args=[self.movie1.id]), self.valid_review)

        review = Review.objects.filter(movie=self.movie1).get(title=self.valid_review['title'])

        response = self.client.get(reverse('review:display', kwargs={'pk': self.movie1.id, 'review_id': review.id }))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/display.html')
        self.assertEqual(self.valid_review['title'], review.title)
        self.assertEqual(self.valid_review['message'], review.message)
        self.assertEqual(self.valid_review['rating_out_of_five'], review.rating_out_of_five)

        self.assertEqual(review.movie.id, self.movie1.id)
        self.assertEqual(review.user.id, self.user1.id)

    # Update tests

    def create_valid_review_for_movie(self, movie_id):
        response = self.client.post(reverse('review:create_movie_review', args=[movie_id]), self.valid_review)
        return response

    def test_that_an_authenticated_user_can_see_the_update_view_for_his_review(self):
        self.create_valid_review_for_movie(self.movie1.id)
        response = self.client.get(reverse('review:update', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/review_form.html')

    # def test_that_an_authenticated_user_can_update_his_reviews_title(self):
    #     updated_details = {
    #         'username': 'new_username',
    #     }
    #     self.assertNotEqual(self.user.username, updated_details['username'])
    #
    #     response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
    #     self.assertEqual(response.status_code, 302)
    #     self.user.refresh_from_db()
    #     self.assertEqual(self.user.username, updated_details['username'])
    #
    # def test_that_an_authenticated_user_cannot_update_his_reviews_title_to_empty(self):
    #     updated_details = {
    #         'username': '',
    #     }
    #     response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
    #     self.user.refresh_from_db()
    #     self.assertNotEqual(self.user.username, updated_details['username'])
    #
    #
    # def test_that_an_authenticated_user_can_update_his_reviews_message(self):
    #     updated_details = {
    #         'first_name': 'newname'
    #     }
    #     response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
    #     self.user.refresh_from_db()
    #     self.assertNotEqual(self.user.username, updated_details['first_name'])
    #
    # def test_that_an_authenticated_user_cannot_update_his_reviews_message_to_empty(self):
    #     updated_details = {
    #         'username': '',
    #     }
    #     response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
    #     self.user.refresh_from_db()
    #     self.assertNotEqual(self.user.username, updated_details['username'])

    # def test_that_an_authenticated_user_can_update_his_reviews_rating(self):
    #     updated_details = {
    #         'first_name': 'newname'
    #     }
    #     response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
    #     self.user.refresh_from_db()
    #     self.assertNotEqual(self.user.username, updated_details['first_name'])
    #
    # def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_empty(self):
    #     updated_details = {
    #         'username': '',
    #     }
    #     response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
    #     self.user.refresh_from_db()
    #     self.assertNotEqual(self.user.username, updated_details['username'])
    # def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_less_than_one(self):
    #     updated_details = {
    #         'username': '',
    #     }
    #     response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
    #     self.user.refresh_from_db()
    #     self.assertNotEqual(self.user.username, updated_details['username'])
    # def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_greater_than_five(self):
    #     updated_details = {
    #         'username': '',
    #     }
    #     response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
    #     self.user.refresh_from_db()
    #     self.assertNotEqual(self.user.username, updated_details['username'])
    # def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_a_decimal(self):
    #     updated_details = {
    #         'username': '',
    #     }
    #     response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
    #     self.user.refresh_from_db()
    #     self.assertNotEqual(self.user.username, updated_details['username'])
    # def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_an_alphabetical_value(self):
    #     updated_details = {
    #         'username': '',
    #     }
    #     response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
    #     self.user.refresh_from_db()
    #     self.assertNotEqual(self.user.username, updated_details['username'])
    #
    #
    # def test_that_an_authenticated_user_is_redirected_back_to_the_update_form_on_unsuccessful_update(self):
    #     updated_details = {
    #         'first_name': '1',
    #     }
    #     response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed('user/update_user_form.html')
    #     self.assertIn('form', response.context)
    #     self.assertFalse(response.context['form'].is_valid())
    #
    # def test_that_an_authenticated_user_cannot_see_the_update_view_for_another_users_review(self):
    #     response = self.client.get(reverse('user:update_user', args=[self.another_user.id]))
    #     self.assertEqual(response.status_code, 403)
    #     self.assertTemplateNotUsed(response, 'user/update_user_form.html')
    #
    # def test_that_an_authenticated_user_cannot_update_another_users_review(self):
    #
    # def test_that_an_unauthenticated_user_cannot_see_the_update_view_for_another_user(self):
    #     self.client.logout()
    #     response = self.client.get(reverse('user:update_user', args=[1]), follow=True)
    #     self.assertTemplateNotUsed(response, 'user/update_user_form.html')
    #
    # def test_that_an_unauthenticated_user_is_redirected_to_login_when_trying_to_update_a_user(self):
    #     self.client.logout()
    #     response = self.client.post(reverse('user:update_user', args=[1]), follow=True)
    #     self.assertTemplateUsed(response, 'registration/login.html')

    # we need to make sure only the author can both see the update form and update (take reference from user/tests.py
    # and then we need to validate the fields of the new review, and test for success and failure and where they both
    # redirect (again, take reference from the user tests)

    # Delete tests

    # Should be the same as the user tests with the one exception being that an admin should also be able to both
    # view the form and delete the review
