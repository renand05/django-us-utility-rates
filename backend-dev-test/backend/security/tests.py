from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from pydantic import BaseModel
from rest_framework import test, status
from unittest.mock import Mock, patch


class RefreshMock(BaseModel):
    access_token: str = 'sometoken'

class RegistrationApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

    @override_settings(
        REST_FRAMEWORK={
            'DEFAULT_AUTHENTICATION_CLASSES': [
                'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            ],
        }
    )

    @patch('security.views.RefreshToken.for_user', return_value=RefreshMock())
    @patch('security.views.SignUpForm.save', return_value=None)
    @patch('security.views.SignUpForm.is_valid', return_value=True)
    def test_should_register_user(self, is_valid: Mock, save: Mock, for_user: Mock) -> None:
        client = test.APIClient()
        response = client.post(
            '/register',
            {'username': 'testuser', 'password': 'testpassword'},
            format='json'
        )
        is_valid.assert_called_once()
        save.assert_called_once()
        for_user.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
 