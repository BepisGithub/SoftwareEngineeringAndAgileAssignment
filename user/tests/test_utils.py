from django.test import TestCase, Client
from user.models import User


class BaseTestCase(TestCase):
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


def get_valid_account_details():
    valid_details = {
        'username': 'unique',
        'email': 'unique@email.com',
        'first_name': 'unique',
        'last_name': 'unique',
        'password1': 'asdfasdf123',
        'password2': 'asdfasdf123',
    }
    return valid_details


def get_invalid_account_details():
    invalid_details = {
        'username': '',
        'email': 'notanemail',
        'first_name': '1',
        'last_name': '1',
        'password1': 'samepassword',
        'password2': 'differentpassword',
    }
    return invalid_details
