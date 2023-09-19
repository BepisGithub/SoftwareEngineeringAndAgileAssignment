from unittest.mock import patch

from django.urls import reverse

from review.models import Review
from review.tests.test_utils import BaseTestCase, get_updated_details, create_review_for_movie

from review.tests.test_utils import set_user_to_admin

from movie.models import Movie


class UpdateReviewTestCase(BaseTestCase):

    def test_that_an_authenticated_user_can_see_the_update_view_for_their_review(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        response = self.client.get(reverse('review:update', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/review_form.html')

    def test_that_an_authenticated_user_can_update_their_reviews_title(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        review = Review.objects.filter(id=1).get()
        updated_details = get_updated_details(self.valid_review, 'new title', None, None)
        self.assertNotEqual(review.title, updated_details['title'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()
        self.assertEqual(review.title, updated_details['title'])

    def test_that_an_authenticated_user_cannot_update_their_reviews_title_to_empty(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        review = Review.objects.filter(id=1).get()
        updated_details = get_updated_details(self.valid_review, '', None, None)
        self.assertNotEqual(review.title, updated_details['title'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()
        self.assertNotEqual(review.title, updated_details['title'])

    def test_that_an_authenticated_user_can_update_their_reviews_message(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        review = Review.objects.filter(id=1).get()
        updated_details = get_updated_details(self.valid_review, None, 'new message', None)
        self.assertNotEqual(review.message, updated_details['message'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()
        self.assertEqual(review.message, updated_details['message'])

    def test_that_an_authenticated_user_cannot_update_their_reviews_message_to_empty(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        review = Review.objects.filter(id=1).get()
        updated_details = get_updated_details(self.valid_review, None, '', None)
        self.assertNotEqual(review.message, updated_details['message'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()
        self.assertNotEqual(review.message, updated_details['message'])

    def test_that_an_authenticated_user_can_update_their_reviews_rating(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        review = Review.objects.filter(id=1).get()
        updated_details = get_updated_details(self.valid_review, None, None, self.valid_review['rating_out_of_five'] - 1)
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()
        self.assertEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_updating_a_review_causes_the_average_rating_of_a_movie_to_be_recalculated(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        movie = Movie.objects.filter(id=self.movie1.id).get()
        review = Review.objects.filter(id=1).get()
        updated_details = get_updated_details(self.valid_review, None, None,
                                              self.valid_review['rating_out_of_five'] - 1)
        self.assertNotEqual(movie.average_rating_out_of_five, updated_details['rating_out_of_five'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        movie.refresh_from_db()
        self.assertEqual(movie.average_rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_their_reviews_rating_to_empty(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        review = Review.objects.filter(id=1).get()
        updated_details = get_updated_details(self.valid_review, None, None, '')
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_their_reviews_rating_to_less_than_one(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        review = Review.objects.filter(id=1).get()
        updated_details = get_updated_details(self.valid_review, None, None, 0)
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_their_reviews_rating_to_greater_than_five(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        review = Review.objects.filter(id=1).get()
        updated_details = get_updated_details(self.valid_review, None, None, 6)
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_their_reviews_rating_to_a_float(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        review = Review.objects.filter(id=1).get()
        updated_details = get_updated_details(self.valid_review, None, None, 4.4)
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_their_reviews_rating_to_an_alphabetical_value(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        review = Review.objects.filter(id=1).get()
        updated_details = get_updated_details(self.valid_review, None, None, 'five')
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_is_redirected_back_to_the_update_form_on_unsuccessful_update(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        review = Review.objects.filter(id=1).get()
        updated_details = get_updated_details(self.valid_review, '', '', 0)
        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        # In Django, unsuccessful updates cause the view to rerender the form which means no redirect thus a 200 code
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('review/review_form.html')
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())

    def test_that_an_authenticated_user_cannot_see_the_update_view_for_another_users_review(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.get(reverse('review:update', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_admin_user_cannot_see_the_update_view_for_another_users_review(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        set_user_to_admin(self.user2)
        self.client.force_login(self.user2)
        self.assertTrue(self.user2.is_admin)
        response = self.client.get(reverse('review:update', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_authenticated_user_cannot_update_another_users_review(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        self.client.force_login(self.user2)
        updated_details = get_updated_details(self.valid_review, 'new title', 'new message', 1)
        review = Review.objects.filter(id=1).get()
        self.assertNotEqual(review.title, updated_details['title'])
        self.assertNotEqual(review.message, updated_details['message'])
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, 1]), updated_details)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(review.title, updated_details['title'])
        self.assertNotEqual(review.message, updated_details['message'])
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_admin_user_cannot_update_another_users_review(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        set_user_to_admin(self.user2)
        self.client.force_login(self.user2)
        self.assertTrue(self.user2.is_admin)
        updated_details = get_updated_details(self.valid_review, 'new title', 'new message', 1)
        review = Review.objects.filter(id=1).get()
        # Only need to check one since the update either succeeded entirely or failed entirely
        self.assertNotEqual(review.title, updated_details['title'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, 1]), updated_details)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(review.title, updated_details['title'])

    def test_that_an_unauthenticated_user_cannot_see_the_update_view_for_another_users_review(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        response = self.client.get(reverse('review:update', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_unauthenticated_user_cannot_update_another_users_review(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        updated_details = get_updated_details(self.valid_review, 'new title', 'new message', 1)
        review = Review.objects.filter(id=1).get()
        self.assertNotEqual(review.title, updated_details['title'])
        self.assertNotEqual(review.message, updated_details['message'])
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])
        response = self.client.post(reverse('review:update', args=[self.movie1.id, 1]), updated_details)
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(review.title, updated_details['title'])
        self.assertNotEqual(review.message, updated_details['message'])
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_unauthenticated_user_is_redirected_to_login_when_trying_to_update_another_users_review(self):
        create_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        updated_details = get_updated_details(self.valid_review, 'new title', 'new message', 1)
        response = self.client.post(reverse('review:update', args=[self.movie1.id, 1]), updated_details, follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

    @patch('review.views.logger')
    def test_that_logging_occurs_when_updating_a_review_with_invalid_input(self, mock_logger):
        updated_details = get_updated_details(self.valid_review, None, None, 6)
        response = create_review_for_movie(self.client, updated_details, self.movie1.id)
        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())
        self.assertTrue(mock_logger.warning.called)
