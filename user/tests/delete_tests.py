from django.test import TestCase, Client
from user.models import User
from django.urls import reverse

from user.tests.test_utils import BaseTestCase


class DeleteUserTestCase(BaseTestCase):

    def test_that_an_authenticated_user_can_see_the_delete_confirmation_for_himself(self):
        response = self.client.get(reverse('user:delete_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_confirm_delete.html')

    def test_that_an_authenticated_user_can_delete_his_own_account(self):
        response = self.client.post(reverse('user:delete_user', args=[self.user.id]))
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_that_a_user_is_redirected_after_a_successful_account_deletion(self):
        response = self.client.post(reverse('user:delete_user', args=[self.user.id]), follow=True)
        self.assertEqual(response.status_code, 200)  # The all users page is rendered successfully
        self.assertTemplateUsed(response, 'user/list.html')

    def test_that_an_authenticated_user_cannot_see_the_delete_confirmation_for_another(self):
        response = self.client.get(reverse('user:delete_user', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden action
        self.assertTemplateNotUsed(response, 'user/user_confirm_delete.html')

    def test_that_an_authenticated_user_cannot_delete_anothers_account(self):
        response = self.client.post(reverse('user:delete_user', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden action
        self.assertTrue(User.objects.filter(id=self.another_user.id).exists())

    def test_that_an_unauthenticated_user_cannot_see_the_delete_confirmation_for_another(self):
        self.client.logout()
        response = self.client.get(reverse('user:delete_user', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 302)  # Redirected away
        self.assertTemplateNotUsed(response, 'user/user_confirm_delete.html')

    def test_that_an_unauthenticated_user_cannot_delete_anothers_account(self):
        self.client.logout()
        response = self.client.post(reverse('user:delete_user', args=[self.another_user.id]), follow=True)
        self.assertTrue(User.objects.filter(id=self.another_user.id).exists())

    def test_that_an_unauthenticated_user_is_redirected_after_attempting_to_delete_another_user(self):
        self.client.logout()
        response = self.client.post(reverse('user:delete_user', args=[self.user.id]), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(response.status_code, 200) # The login page is rendered successfully
