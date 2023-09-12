from django.contrib.auth import get_user_model, login
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from datetime import datetime

from django.urls import reverse

from .models import User

# TODO: add comments of all the test cases you're NOT covering because django covers them for you


class UserTestCase(TestCase):
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
        print(response.content)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, updated_details['username'])

    # def test_that_an_authenticated_user_cannot_set_his_username_to_empty(self):


    # def test_that_a_user_cannot_set_his_username_to_another_username_that_is_in_use(self):

    # def test_that_an_authenticated_user_can_update_his_first_name_to_a_new_value(self):
    #     updated_details = {
    #         'username':
    #     }
    #
    # def test_that_an_authenticated_user_can_update_his_first_name_to_empty(self):
    #     updated_details = {
    #         'username':
    #     }
    #
    #
    # def test_that_an_authenticated_user_can_update_his_last_name_to_a_new_value(self):
    #     updated_details = {
    #         'username':
    #     }
    #
    # def test_that_an_authenticated_user_can_update_his_first_name_to_empty(self):
    #     updated_details = {
    #         'username':
    #     }
    #
    # def test_that_an_authenticated_user_can_update_his_email(self):
    #     updated_details = {
    #         'username':
    #     }

    def test_that_an_authenticated_user_cannot_see_the_update_view_for_another_user(self):
        response = self.client.get(reverse('user:update_user', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_unauthenticated_user_cannot_see_the_update_view_for_another_user(self):
        self.client.logout()
        response = self.client.get(reverse('user:update_user', args=[1]), follow=True)
        self.assertTemplateNotUsed(response, 'user/update_user_form.html')

    def test_that_an_unauthenticated_user_is_redirected_to_login_when_trying_to_update_a_user(self):
        self.client.logout()
        response = self.client.get(reverse('user:update_user', args=[1]), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_that_an_authenticated_user_can_see_the_delete_confirmation_for_himself(self):
        response = self.client.get(reverse('user:delete_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_confirm_delete.html')

    def test_that_an_authenticated_user_can_delete_his_own_account(self):
        response = self.client.post(reverse('user:delete_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)

    def test_that_a_user_is_redirected_after_a_successful_account_deletion(self):
        response = self.client.post(reverse('user:delete_user', args=[self.user.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/users.html')

    def test_that_an_authenticated_user_cannot_see_the_delete_confirmation_for_another(self):
        response = self.client.get(reverse('user:delete_user', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, 'user/user_confirm_delete.html')

    def test_that_an_authenticated_user_cannot_delete_anothers_account(self):
        response = self.client.post(reverse('user:delete_user', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(User.objects.filter(id=self.another_user.id).exists())

    def test_that_an_unauthenticated_user_cannot_see_the_delete_confirmation_for_another(self):
        self.client.logout()
        response = self.client.get(reverse('user:delete_user', args=[self.another_user.id]))
        self.assertEqual(response.status_code, 302) # due to the redirect
        self.assertTemplateNotUsed(response, 'user/user_confirm_delete.html')

    def test_that_an_unauthenticated_user_cannot_delete_anothers_account(self):
        self.client.logout()
        response = self.client.post(reverse('user:delete_user', args=[self.another_user.id]), follow=True)
        self.assertTrue(User.objects.filter(id=self.another_user.id).exists())

    def test_that_an_unauthenticated_user_is_redirected_after_attempting_to_delete_another_user(self):
        self.client.logout()
        response = self.client.post(reverse('user:delete_user', args=[self.user.id]), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(response.status_code, 200)

