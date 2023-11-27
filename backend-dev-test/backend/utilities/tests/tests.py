from django.test import TestCase, override_settings
from unittest.mock import patch
from unittest import mock
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from utilities.models import User
from utilities.services import UtilityRatesService, FakeUtilityRatesService

from pydantic import BaseModel

class WebsiteDemoRequest(BaseModel):
    user_address: str
    user_consumption: str
    user_percentage_scale: str

class WebsiteDemoTest(TestCase):
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

    def test_jwt_authenticated_endpoint(self):
        client = APIClient()
        response = client.post(
            reverse('token_obtain_pair'),
            {'username': 'testuser', 'password': 'testpassword'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = client.get(reverse('rates_demo'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
class ModelsTest(TestCase):
    def test_should_save_and_retrieve_users(self) -> None:
        first_user = User()
        first_user.firstname = 'Luke'
        first_user.lastname = 'Skywalker'
        first_user.address = 'Death Star #44'
        first_user.email = 'luke@star.com'
        first_user.national_id = '122star'
        first_user.national_id_type = 'PS'
        first_user.country = 'Tatoo'
        first_user.save()
        second_user = User()
        second_user.firstname = 'Han'
        second_user.lastname = 'Solo'
        second_user.address = 'Falcon #44'
        second_user.email = 'han@star.com'
        second_user.national_id = '320star'
        second_user.national_id_type = 'SS'
        second_user.country = 'Tatoo'
        second_user.save()
        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(), 2)
        first_saved_user = saved_users[1]
        second_saved_user = saved_users[0]
        self.assertEqual(first_saved_user.firstname, 'Han')
        self.assertEqual(second_saved_user.firstname, 'Luke')

class ServicesTest(TestCase):
    @patch('utilities.services.UtilityRatesDirector.process_request', return_value='test')
    @patch('utilities.services.UtilityRatesDirector.openei_request', return_value='test')
    def test_should_call_http_and_processor_once(self, request_method_mock: mock.Mock, process_method_mock: mock.Mock) -> None:
        service = UtilityRatesService()
        service.get_openei_results()
        request_method_mock.assert_called_once()
        process_method_mock.assert_called_once()

class ProcessorTest(TestCase):
    def should_compute_average_consumption_rate() -> None:
        pass

    def should_retrieve_utility_tariff_details() -> None:
        pass

    def should_retrieve_utilities() -> None:
        pass

    def should_compute_year_proyection_cost() -> None:
        pass