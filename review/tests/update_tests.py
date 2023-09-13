from django.urls import reverse

from review.models import Review
from review.tests.test_utils import BaseTestCase, get_updated_details, create_valid_review_for_movie


class UpdateReviewTestCase(BaseTestCase):

    def test_that_an_authenticated_user_can_see_the_update_view_for_his_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        response = self.client.get(reverse('review:update', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/review_form.html')

    def test_that_an_authenticated_user_can_update_his_reviews_title(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = get_updated_details(self.valid_review, 'new title', None, None)

        self.assertNotEqual(review.title, updated_details['title'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertEqual(review.title, updated_details['title'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_title_to_empty(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = get_updated_details(self.valid_review, '', None, None)

        self.assertNotEqual(review.title, updated_details['title'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.title, updated_details['title'])

    def test_that_an_authenticated_user_can_update_his_reviews_message(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = get_updated_details(self.valid_review, None, 'new message', None)

        self.assertNotEqual(review.message, updated_details['message'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertEqual(review.message, updated_details['message'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_message_to_empty(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = get_updated_details(self.valid_review, None, '', None)

        self.assertNotEqual(review.message, updated_details['message'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.message, updated_details['message'])

    def test_that_an_authenticated_user_can_update_his_reviews_rating(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = get_updated_details(self.valid_review, None, None, self.valid_review['rating_out_of_five'] - 1)

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_empty(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = get_updated_details(self.valid_review, None, None, '')

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_less_than_one(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = get_updated_details(self.valid_review, None, None, 0)

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_greater_than_five(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = get_updated_details(self.valid_review, None, None, 6)

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_a_float(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = get_updated_details(self.valid_review, None, None, 4.4)

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_cannot_update_his_reviews_rating_to_an_alphabetical_value(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = get_updated_details(self.valid_review, None, None, 'five')

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        review.refresh_from_db()

        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_authenticated_user_is_redirected_back_to_the_update_form_on_unsuccessful_update(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        updated_details = get_updated_details(self.valid_review, '', '', 0)

        response = self.client.post(reverse('review:update', args=[self.movie1.id, review.id]), updated_details)
        self.assertEqual(response.status_code, 200) # TODO: comment that unsuccessfull updates cause the view to rerender the form which means no redirect thus a 200 code
        self.assertTemplateUsed('review/review_form.html')
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())

    def test_that_an_authenticated_user_cannot_see_the_update_view_for_another_users_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.get(reverse('review:update', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_admin_user_cannot_see_the_update_view_for_another_users_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        self.user2.is_admin = True
        self.user2.save()
        self.client.force_login(self.user2)
        self.assertTrue(self.user2.is_admin)
        response = self.client.get(reverse('review:update', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_authenticated_user_cannot_update_another_users_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        self.client.force_login(self.user2)

        updated_details = get_updated_details(self.valid_review, 'new title', 'new message', 1)

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
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        self.user2.is_admin = True
        self.user2.save()
        self.client.force_login(self.user2)
        self.assertTrue(self.user2.is_admin)

        updated_details = get_updated_details(self.valid_review, 'new title', 'new message', 1)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        # Only need to check one since the update either succeeded entirely or failed entirely
        self.assertNotEqual(review.title, updated_details['title'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, 1]), updated_details)

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(review.title, updated_details['title'])

    def test_that_an_unauthenticated_user_cannot_see_the_update_view_for_another_users_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        response = self.client.get(reverse('review:update', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_unauthenticated_user_cannot_update_another_users_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()

        updated_details = get_updated_details(self.valid_review, 'new title', 'new message', 1)

        review = Review.objects.filter(movie_id=self.movie1.id).get(id=1)

        self.assertNotEqual(review.title, updated_details['title'])
        self.assertNotEqual(review.message, updated_details['message'])
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

        response = self.client.post(reverse('review:update', args=[self.movie1.id, 1]), updated_details)

        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(review.title, updated_details['title'])
        self.assertNotEqual(review.message, updated_details['message'])
        self.assertNotEqual(review.rating_out_of_five, updated_details['rating_out_of_five'])

    def test_that_an_unauthenticated_user_is_redirected_to_login_when_trying_to_update_another_users_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        updated_details = get_updated_details(self.valid_review, 'new title', 'new message', 1)

        response = self.client.post(reverse('review:update', args=[self.movie1.id, 1]), updated_details, follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')
