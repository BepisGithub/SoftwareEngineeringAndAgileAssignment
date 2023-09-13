from django.test import TestCase, Client
from user.models import User
from django.urls import reverse

from user.tests.test_utils import BaseTestCase


class UpdateUserTestCase(BaseTestCase):

    def test_that_an_authenticated_user_can_see_the_update_view_for_himself(self):
        response = self.client.get(reverse('user:update_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/update_user_form.html')

    def test_that_an_authenticated_user_can_update_his_username(self):
        updated_details = {
            'username': 'new_username',
        }
        self.assertNotEqual(self.user.username, updated_details['username'])

        response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, updated_details['username'])

    def test_that_an_authenticated_user_cannot_set_his_username_to_empty(self):
        updated_details = {
            'username': '',
        }
        response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, updated_details['username'])

    def test_that_a_user_cannot_set_his_username_to_another_username_that_is_in_use(self):
        updated_details = {
            'username': self.another_user.username,
        }
        response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, updated_details['username'])

    def test_that_an_authenticated_user_can_update_his_first_name_to_a_new_value(self):
        updated_details = {
            'first_name': 'newname'
        }
        response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, updated_details['first_name'])

    def test_that_an_authenticated_user_can_update_his_first_name_to_empty(self):
        updated_details = {
            'first_name': ''
        }
        response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, updated_details['first_name'])

    def test_that_an_authenticated_user_can_update_his_last_name_to_a_new_value(self):
        updated_details = {
            'last_name': 'newname'
        }
        response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, updated_details['last_name'])

    def test_that_an_authenticated_user_can_update_his_last_name_to_empty(self):
        updated_details = {
            'last_name': ''
        }
        response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, updated_details['last_name'])

    def test_that_an_authenticated_user_can_update_his_email(self):
        updated_details = {
            'email': 'new@email.com'
        }
        response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, updated_details['email'])

    def test_that_an_authenticated_user_cannot_update_his_email_to_empty(self):
        updated_details = {
            'email': ''
        }
        response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, updated_details['email'])

    def test_that_an_authenticated_user_is_redirected_back_to_the_update_form_on_unsuccessful_update(self):
        updated_details = {
            'first_name': '1',
        }
        response = self.client.post(reverse('user:update_user', args=[self.user.id]), updated_details)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('user/update_user_form.html')
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())

    def test_that_an_authenticated_user_cannot_see_the_update_view_for_another_user(self):
        response = self.client.get(reverse('user:update_user', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_authenticated_user_cannot_update_another_user(self):
        response = self.client.post(reverse('user:update_user', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_unauthenticated_user_cannot_see_the_update_view_for_another_user(self):
        self.client.logout()
        response = self.client.get(reverse('user:update_user', args=[1]), follow=True)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_unauthenticated_user_cannot_update_another_user(self):
        self.client.logout()
        response = self.client.post(reverse('user:update_user', args=[1]), follow=True)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_unauthenticated_user_is_redirected_to_login_when_trying_to_update_a_user(self):
        self.client.logout()
        response = self.client.get(reverse('user:update_user', args=[1]), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')