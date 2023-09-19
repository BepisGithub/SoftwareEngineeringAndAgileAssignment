from django.urls import reverse

from review.models import Review
from review.tests.test_utils import BaseTestCase, create_review_for_movie

from review.tests.test_utils import set_user_to_admin

from movie.models import Movie


class DeleteReviewTestCase(BaseTestCase):

    def test_that_an_authenticated_user_can_see_the_delete_confirmation_for_their_review(self):
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie1.id)
        response = self.client.get(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/review_confirm_delete.html')

    def test_that_an_authenticated_user_can_delete_their_review(self):
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie1.id)
        response = self.client.post(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=1).exists())

    def test_that_deleting_a_review_causes_the_average_rating_of_a_movie_to_be_recalculated(self):
        movie = Movie.objects.filter(id=self.movie1.id).get()
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie1.id)
        movie.refresh_from_db()
        self.assertNotEqual(movie.average_rating_out_of_five, None)
        response = self.client.post(reverse('review:delete', args=[self.movie1.id, 1]))
        movie.refresh_from_db()
        self.assertEqual(movie.average_rating_out_of_five, None)

    def test_that_a_user_is_redirected_to_the_movie_detail_page_after_deleting_the_only_review(self):
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie1.id)
        response = self.client.post(reverse('review:delete', args=[self.movie1.id, 1]),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'review/list.html')
        self.assertTemplateUsed(response, 'movie/detail.html')

    def test_that_an_authenticated_user_cannot_see_the_delete_confirmation_for_anothers_review(self):
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie1.id)
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.get(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'review/review_confirm_delete.html')

    def test_that_an_authenticated_user_cannot_delete_anothers_review(self):
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie1.id)
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.post(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'review/review_confirm_delete.html')
        self.assertTrue(Review.objects.filter(id=1).exists())

    def test_that_an_admin_user_can_see_the_delete_confirmation_for_anothers_review(self):
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie1.id)
        self.client.logout()
        set_user_to_admin(self.user2)
        self.client.force_login(self.user2)
        self.assertTrue(self.user2.is_admin)
        response = self.client.get(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/review_confirm_delete.html')

    def test_that_an_admin_user_can_delete_anothers_review(self):
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie1.id)
        self.client.logout()
        set_user_to_admin(self.user2)
        self.client.force_login(self.user2)
        self.assertTrue(self.user2.is_admin)
        response = self.client.post(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=1).exists())

    def test_that_an_unauthenticated_user_cannot_see_the_delete_confirmation_for_anothers_review(self):
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie1.id)
        self.client.logout()
        response = self.client.get(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertTemplateNotUsed(response, 'review/review_confirm_delete.html')

    def test_that_an_unauthenticated_user_cannot_delete_anothers_review(self):
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie1.id)
        self.client.logout()
        response = self.client.post(reverse('review:delete', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'review/review_confirm_delete.html')
        self.assertTrue(Review.objects.filter(id=1).exists())

    def test_that_an_unauthenticated_user_is_redirected_after_attempting_to_delete_anothers_review(self):
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie1.id)
        self.client.logout()
        response = self.client.post(reverse('review:delete', args=[self.movie1.id, 1]), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_that_deleting_a_user_also_deletes_their_reviews(self):
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie1.id)
        self.assertTrue(Review.objects.filter(id=1).exists())
        response = self.client.post(reverse('user:delete', args=[self.user1.id]))
        self.assertFalse(Review.objects.filter(id=1).exists())
