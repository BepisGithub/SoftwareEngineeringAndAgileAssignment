from django.db import IntegrityError
from django.urls import reverse

from review.models import Review
from review.tests.test_utils import BaseTestCase

from review.tests.test_utils import create_valid_review_for_movie


class CreateReviewTestCase(BaseTestCase):
    # TODO: refactor these to use the test utils helper method for creating a review
    def test_that_an_authenticated_user_can_see_the_create_view_if_its_their_first_review_of_a_movie(self):
        response = self.client.get(reverse('review:create', args=[self.user1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/review_form.html')

    def test_that_an_authenticated_user_can_create_a_review_if_its_their_first_review_of_a_movie(self):
        response = create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.assertEqual(Review.objects.filter(movie=self.movie1).get(title=self.valid_review['title']).user,
                         self.user1)

    def test_that_an_authenticated_user_cannot_see_the_create_view_if_its_not_their_first_review_of_a_movie(self):
        create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        response = self.client.get(reverse('review:create', args=[self.user1.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'review/review_form.html')

    def test_that_an_authenticated_user_cannot_create_a_review_if_its_not_their_first_review_of_a_movie(self):
        response = create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)

        with self.assertRaises(IntegrityError):
            response = self.client.post(reverse('review:create', args=[self.movie1.id]), self.second_review)

    def test_that_an_unauthenticated_user_cannot_see_the_create_view(self):
        self.client.logout()
        response = self.client.get(reverse('review:create', args=[self.movie1.id]), self.valid_review)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'review/review_form.html')

    def test_that_an_unauthenticated_user_cannot_create_a_review(self):
        self.client.logout()
        response = create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    def test_that_an_unauthenticated_user_is_redirected_to_login_when_trying_to_see_the_create_view(self):
        self.client.logout()
        response = self.client.get(reverse('review:create', args=[self.movie1.id]), self.valid_review, follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_that_an_unauthenticated_user_is_redirected_to_login_when_trying_to_create_a_review(self):
        self.client.logout()
        response = self.client.post(reverse('review:create', args=[self.movie1.id]), self.valid_review, follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    # TODO: refactor all test method names to be shorter
    def test_that_an_authenticated_user_can_see_the_create_view_of_another_movie_even_if_they_have_a_review_for_a_different_movie(self):
        first_response = create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        second_response = self.client.get(reverse('review:create', args=[self.movie2.id]), self.valid_review)
        self.assertEqual(second_response.status_code, 200)
        self.assertTemplateUsed(second_response, 'review/review_form.html')

    def test_that_an_authenticated_user_can_create_a_review_for_another_movie_even_if_they_have_a_review_for_a_different_movie(self):
        first_response = create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        second_response = create_valid_review_for_movie(self.client, self.valid_review, self.movie2.id)
        self.assertTrue(Review.objects.filter(movie=self.movie2).exists())

    def test_that_creating_a_review_causes_the_average_rating_of_a_movie_to_be_recalculated(self):
        self.assertNotEqual(self.movie1.average_rating_out_of_five, self.valid_review['rating_out_of_five'])
        response = create_valid_review_for_movie(self.client, self.valid_review, self.movie1.id)
        self.movie1.refresh_from_db()
        self.assertEqual(self.movie1.average_rating_out_of_five, self.valid_review['rating_out_of_five'])

    def test_that_a_review_cannot_have_an_empty_title(self):
        invalid_review = self.valid_review
        invalid_review['title'] = ''
        response = create_valid_review_for_movie(self.client, invalid_review, self.movie1.id)
        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    def test_that_a_review_cannot_have_an_empty_message(self):
        invalid_review = self.valid_review
        invalid_review['message'] = ''
        response = create_valid_review_for_movie(self.client, invalid_review, self.movie1.id)
        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    def test_that_a_review_cannot_have_a_rating_less_than_1(self):
        invalid_review = self.valid_review
        invalid_review['rating_out_of_five'] = 0
        response = create_valid_review_for_movie(self.client, invalid_review, self.movie1.id)
        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    def test_that_a_review_cannot_have_a_rating_greater_than_5(self):
        invalid_review = self.valid_review
        invalid_review['rating_out_of_five'] = 6
        response = create_valid_review_for_movie(self.client, invalid_review, self.movie1.id)
        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    def test_that_a_review_cannot_have_a_float_rating(self):
        invalid_review = self.valid_review
        invalid_review['rating_out_of_five'] = 3.3
        response = create_valid_review_for_movie(self.client, invalid_review, self.movie1.id)
        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())

    def test_that_a_review_cannot_have_an_alphabetical_rating(self):
        invalid_review = self.valid_review
        invalid_review['rating_out_of_five'] = 'a'
        response = create_valid_review_for_movie(self.client, invalid_review, self.movie1.id)
        self.assertFalse(Review.objects.filter(movie=self.movie1).exists())