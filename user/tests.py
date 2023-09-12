from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from datetime import datetime

from django.urls import reverse

from .models import User

# TODO: add comments of all the test cases you're NOT covering because django covers them for you

class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email="JDoe@email.com",
            password='asdfasdf123123',
        )
        logged_in = self.client.login(username='test_user', passwords='asdfasdf123123')
        print(logged_in)

    def test_that_first_name_cannot_have_numbers(self):
        self.user.first_name = '1'

        with self.assertRaises(ValidationError):
            self.user.full_clean()

        self.user.first_name = '1a'

        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_that_last_name_cannot_have_numbers(self):
        self.user.last_name = '1'

        with self.assertRaises(ValidationError):
            self.user.full_clean()

        self.user.last_name = '1a'

        with self.assertRaises(ValidationError):
            self.user.full_clean()

    # def test_that_a_user_can_see_the_update_view_for_himself(self):
    #     response = self.client.get(reverse('user:update_user', kwargs={'pk': self.user.id}))
    #     self.assertEqual(response.status_code, 302) # due to the redirect defined by success_url
    #     self.assertEqual(response.url, reverse('user:user', kwargs={'pk': self.user.id}))
    #     self.assertTemplateUsed(response, 'user/update_user_form.html')
