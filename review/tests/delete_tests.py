from django.urls import reverse

from review.models import Review
from review.tests.test_utils import BaseTestCase, create_valid_review_for_movie


class DeleteReviewTestCase(BaseTestCase):

    def test_that_an_authenticated_user_can_see_the_delete_confirmation_for_his_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        response = self.client.get(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/review_confirm_delete.html')

    def test_that_an_authenticated_user_can_delete_his_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        response = self.client.post(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=1).exists())

    def test_that_a_user_is_redirected_after_a_successful_review_deletion(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        response = self.client.post(reverse('review:delete', args=[self.movie1.id, 1]),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/movie_reviews.html')

    def test_that_an_authenticated_user_cannot_see_the_delete_confirmation_for_anothers_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.get(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'review/review_confirm_delete.html')

    def test_that_an_authenticated_user_cannot_delete_anothers_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.post(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'review/review_confirm_delete.html')
        self.assertTrue(Review.objects.filter(id=1).exists())

    def test_that_an_admin_user_can_see_the_delete_confirmation_for_anothers_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        self.user2.is_admin = True
        self.user2.save()
        self.client.force_login(self.user2)
        self.assertTrue(self.user2.is_admin)
        response = self.client.get(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/review_confirm_delete.html')

    def test_that_an_admin_user_can_delete_anothers_review(self):
        # TODO: extract this switching user code to a helper method, should work since we're modifying the instance vars
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        self.user2.is_admin = True
        self.user2.save()
        self.client.force_login(self.user2)
        self.assertTrue(self.user2.is_admin)
        response = self.client.post(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=1).exists())

    def test_that_an_unauthenticated_user_cannot_see_the_delete_confirmation_for_anothers_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        response = self.client.get(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertTemplateNotUsed(response, 'review/review_confirm_delete.html')

    def test_that_an_unauthenticated_user_cannot_delete_anothers_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        response = self.client.post(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'review/review_confirm_delete.html')
        self.assertTrue(Review.objects.filter(id=1).exists())

    def test_that_an_unauthenticated_user_is_redirected_after_attempting_to_delete_anothers_review(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.client.logout()
        response = self.client.post(reverse('review:delete', args=[self.movie1.id, 1]), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')