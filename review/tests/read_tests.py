from django.urls import reverse

from review.models import Review
from review.tests.test_utils import BaseTestCase

from review.tests.test_utils import create_review_for_movie


class ReadReviewTestCase(BaseTestCase):

    def test_review_list_view(self):
        response = self.client.get(reverse('review:list', args=[self.movie1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/list.html')

    def test_that_review_list_only_contains_reviews_for_that_movie(self):
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie1.id)
        create_review_for_movie(self.client, self.VALID_REVIEW, self.movie2.id)
        response = self.client.get(reverse('review:list', args=[self.movie1.id]))
        self.assertEqual(response.context['reviews'].count(), 1)

    def test_review_display_view(self):
        response = self.client.post(reverse('review:create', args=[self.movie1.id]), self.VALID_REVIEW)
        review = Review.objects.filter(movie=self.movie1).get(title=self.VALID_REVIEW['title'])
        response = self.client.get(reverse('review:detail', args=[self.movie1.id, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/detail.html')
        self.assertEqual(self.VALID_REVIEW['title'], review.title)
        self.assertEqual(self.VALID_REVIEW['message'], review.message)
        self.assertEqual(self.VALID_REVIEW['rating_out_of_five'], review.rating_out_of_five)
        self.assertEqual(review.movie.id, self.movie1.id)
        self.assertEqual(review.user.id, self.user1.id)
