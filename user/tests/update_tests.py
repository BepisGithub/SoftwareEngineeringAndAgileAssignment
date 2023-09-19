from unittest.mock import patch

from django.test import TestCase, Client
from user.models import User
from django.urls import reverse

from user.tests.test_utils import BaseTestCase

from user.tests.test_utils import get_valid_account_details, get_invalid_account_details


class UpdateUserTestCase(BaseTestCase):

    def test_that_an_authenticated_user_can_see_the_update_view_for_himself(self):
        response = self.client.get(reverse('user:update', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/update_user_form.html')

    def test_that_an_authenticated_user_can_update_their_username(self):
        updated_details = get_valid_account_details()
        updated_details['username'] = 'new_username'
        self.assertNotEqual(self.user.username, updated_details['username'])
        response = self.client.post(reverse('user:update', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, updated_details['username'])

    def test_that_an_authenticated_user_cannot_set_their_username_to_empty(self):
        updated_details = get_valid_account_details()
        updated_details['username'] = ''
        response = self.client.post(reverse('user:update', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, updated_details['username'])

    def test_that_a_user_cannot_set_their_username_to_another_username_that_is_in_use(self):
        updated_details = get_valid_account_details()
        updated_details['username'] = self.another_user.username
        response = self.client.post(reverse('user:update', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, updated_details['username'])

    def test_that_an_authenticated_user_can_update_their_first_name_to_a_new_value(self):
        updated_details = get_valid_account_details()
        updated_details['first_name'] = 'newname'
        response = self.client.post(reverse('user:update', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, updated_details['first_name'])

    def test_that_an_authenticated_user_can_update_their_first_name_to_empty(self):
        updated_details = get_valid_account_details()
        updated_details['first_name'] = ''
        response = self.client.post(reverse('user:update', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, updated_details['first_name'])

    def test_that_an_authenticated_user_can_update_their_last_name_to_a_new_value(self):
        updated_details = get_valid_account_details()
        updated_details['last_name'] = 'newname'
        response = self.client.post(reverse('user:update', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, updated_details['last_name'])

    def test_that_an_authenticated_user_can_update_their_last_name_to_empty(self):
        updated_details = get_valid_account_details()
        updated_details['last_name'] = ''
        response = self.client.post(reverse('user:update', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, updated_details['last_name'])

    def test_that_an_authenticated_user_can_update_their_email(self):
        updated_details = get_valid_account_details()
        updated_details['email'] = 'new@email.com'
        response = self.client.post(reverse('user:update', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, updated_details['email'])

    def test_that_an_authenticated_user_cannot_update_their_email_to_empty(self):
        updated_details = get_valid_account_details()
        updated_details['email'] = ''
        response = self.client.post(reverse('user:update', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, updated_details['email'])

    def test_that_an_authenticated_user_is_redirected_back_to_the_update_form_on_unsuccessful_update(self):
        updated_details = get_invalid_account_details()
        response = self.client.post(reverse('user:update', args=[self.user.id]), updated_details)

        # In Django, unsuccessful updates cause the view to rerender the form which means no redirect thus a 200 code
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('user/update_user_form.html')
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())

    def test_that_an_authenticated_user_cannot_see_the_update_view_for_another_user(self):
        response = self.client.get(reverse('user:update', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden action
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_authenticated_user_cannot_update_another_user(self):
        response = self.client.post(reverse('user:update', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden action
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_unauthenticated_user_cannot_see_the_update_view_for_another_user(self):
        self.client.logout()
        response = self.client.get(reverse('user:update', args=[1]), follow=True)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_unauthenticated_user_cannot_update_another_user(self):
        self.client.logout()
        response = self.client.post(reverse('user:update', args=[1]), follow=True)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_unauthenticated_user_is_redirected_to_login_when_trying_to_update_a_user(self):
        self.client.logout()
        response = self.client.get(reverse('user:update', args=[1]), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

    @patch('user.views.logger')
    def test_that_logging_occurs_when_updating_a_user_with_invalid_input(self, mock_logger):
        updated_details = get_invalid_account_details()
        response = self.client.post(reverse('user:update', args=[self.user.id]), updated_details)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, updated_details['username'])
        self.assertTrue(mock_logger.warning.called)