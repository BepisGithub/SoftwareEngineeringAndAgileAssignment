from django.urls import reverse

from review.models import Review
from review.tests.test_utils import BaseTestCase


class ReadReviewTestCase(BaseTestCase):

    def test_review_list_view(self):
        response = self.client.get(reverse('review:list', args=[self.movie1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/list.html')

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
