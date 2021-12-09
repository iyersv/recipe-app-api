from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Test the users API (public)
    """

    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test creating user with valid payload is successful
        :return:
        """
        payload = {
            'email': 'test@abc.com',
            'password': 'dfsfsd',
            'name': 'Test'

        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
        test creating existing user already exists fails
        :return:
        """

        payload = {
            'email': 'test@abc.com',
            'password': 'dfsfsd',
            'name': 'Test'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            'email': 'test1@abc.com',
            'password': 'pw',
            'name': 'Test'
        }
        # create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
        Test tat the token is created for user
        :return:
        """
        payload = {
            'email': 'test1@abc.com',
            'password': 'testpass',
            'name': 'Test'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """
        Token is not created when invalid credentials are passed
        :return:
        """
        create_user(email='test@abc.com', password='testpass')
        payload = {
            'email': 'test@abc.com',
            'password': 'wrongpassword',
            'name': 'Test'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ test no token if user does not exists"""
        payload = {
            'email': 'test1@abc.com',
            'password': 'testpass',
            'name': 'Test'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ test that email and password required"""
        res = self.client.post(TOKEN_URL, {'email': 'test@abc.com', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
