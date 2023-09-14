from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from user.models import User
from django.urls import reverse

from user.tests.test_utils import BaseTestCase
from user.tests.test_utils import get_valid_account_details
from user.tests.test_utils import get_invalid_account_details


class CreateUserTestCase(BaseTestCase):

    def test_that_valid_user_creation_succeeds(self):
        valid_details = get_valid_account_details()
        response = self.client.post(reverse('register'), valid_details)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email=valid_details['email']).exists())
        self.assertTrue(User.objects.filter(email=valid_details['email']).count(), 1)

    def test_that_user_creation_fails_with_non_unique_username(self):
        valid_details_with_non_unique_username = get_valid_account_details()
        valid_details_with_non_unique_username['username'] = self.user.username
        response = self.client.post(reverse('register'), valid_details_with_non_unique_username)
        # In Django, unsuccessful updates cause the view to rerender the form which means no redirect thus a 200 code
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email=valid_details_with_non_unique_username['email']).exists())

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

    def test_that_user_creation_fails_with_invalid_input(self):
        invalid_details = get_invalid_account_details()
        response = self.client.post(reverse('register'), invalid_details)
        # In Django, unsuccessful updates cause the view to rerender the form which means no redirect thus a 200 code
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_details['username']).exists())
