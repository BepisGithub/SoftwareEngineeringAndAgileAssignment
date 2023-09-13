from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from user.models import User
from django.urls import reverse


class CreateUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='test_user',
            email="JDoe@email.com",
            password='asdfasdf123123'
        )
        self.user.save()
        self.client.force_login(self.user)
        self.another_user = User.objects.create(
            username='test_user2',
            email="JDoe2@email.com",
            password='asdfasdf123123'
        )
        self.another_user.save()

    def test_that_valid_user_creation_succeeds(self):
        valid_details ={
            'username': 'unique',
            'email': 'unique@email.com',
            'first_name': 'unique',
            'last_name': 'unique',
            'password1': 'asdfasdf123',
            'password2': 'asdfasdf123',
        }

        response = self.client.post(reverse('register'), valid_details)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(User.objects.filter(email=valid_details['email']).exists())

        self.assertTrue(User.objects.filter(email=valid_details['email']).count(), 1)

    def test_that_user_creation_fails_with_non_unique_username(self):
        valid_details_with_invalid_username = {
            'username': self.user.username,
            'email': 'unique@email.com',
            'first_name': 'unique',
            'last_name': 'unique',
            'password1': 'asdfasdf123',
            'password2': 'asdfasdf123',
        }

        response = self.client.post(reverse('register'), valid_details_with_invalid_username)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email=valid_details_with_invalid_username['email']).exists())

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
        valid_details = {
            'username': '',
            'email': 'notanemail',
            'first_name': '1',
            'last_name': '1',
            'password1': 'samepassword',
            'password2': 'differentpassword',
        }

        response = self.client.post(reverse('register'), valid_details)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=valid_details['username']).exists())
