from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from user.models import User
from django.urls import reverse

class ReadUserTestCase(TestCase):
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

    def test_user_list_view(self):
        response = self.client.get(reverse('user:users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/users.html')

    def test_user_display_view(self):
        response = self.client.get(reverse('user:user', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user.html')