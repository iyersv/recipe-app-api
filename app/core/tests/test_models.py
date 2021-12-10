from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch


def sample_user(email='test@abc.com', password="testpass"):
    """ creates a sample user """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with email is a success

        """

        email = 'satish@abc.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized
        :return:
        """
        email = 'test@ABC.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """
        TEst creating new superuser
        :return:
        """
        user = get_user_model().objects.create_superuser(
            'test@abc.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ test the tag string representation """
        tag = models.Tag.objects.create(
            user=sample_user(), name='Vegan')

        # self.assertEqual(str(tag),tag.name)

    def test_ingredient_str(self):
        """ test ingredient string represtenation """

        ingredient = models.Ingredient.objects.create(
            user=sample_user(), name='Cucumber'
        )

        self.assertEqual(str(ingredient),ingredient.name)

    def test_recipe_str(self):
        """ test recipe string representation """

        recipe = models.Recipe.objects.create(
            user = sample_user(),
            title = 'Steak and mushroom sauce',
            time_in_minutes = 5,
            price=5.00
        )

        self.assertEqual(str(recipe),recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_filename_uuid(self,mock_uuid):
        """" test that the image is served in the correct location """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None,'my_image.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path,exp_path)
