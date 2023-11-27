from django.test import TestCase
from django.http import HttpRequest, QueryDict
from django.template.loader import render_to_string
from unittest.mock import patch
from unittest import mock

from utilities.views import WebsiteDemoView
from utilities.models import User
from utilities.services import UtilityRatesService, FakeUtilityRatesService

from pydantic import BaseModel

class WebsiteDemoRequest(BaseModel):
    user_address: str
    user_consumption: str
    user_percentage_scale: str

@mock.patch('django.template.context_processors.get_token', mock.Mock(return_value='predicabletoken'))
class WebsiteDemoTest(TestCase):
    def build_post_website_demo_body(self) -> QueryDict:
        test_string = 'user_address=Black Star #45&user_consumption=15&user_percentage_scale=10'
        demo_body_dict = QueryDict(test_string)
        return demo_body_dict

    def test_website_has_correct_html_title(self) -> None:
        view = WebsiteDemoView()
        request = HttpRequest()
        fake_service = FakeUtilityRatesService()
        request.method = 'POST'
        request.POST = self.build_post_website_demo_body()
        response = view.post(request=request, service=fake_service)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Aether Energy Utilities Demo</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))
    
    def test_should_execute_a_POST_request(self) -> None:
        view = WebsiteDemoView()
        request = HttpRequest()
        fake_service = FakeUtilityRatesService()
        request.method = 'POST'
        request.POST = self.build_post_website_demo_body()
        response = view.post(request=request, service=fake_service)
        self.assertIn('user_form', response.content.decode())
        expected_html = render_to_string(
            'website_demo.html',
            {'new_user_address': 'Black Star #45',
             'new_user_consumption': '15',
             'new_user_percentage_scale': '10'},
            request=request
        )
        self.assertEqual(response.content.decode(), expected_html)
 
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
    def should_compute_average_consumptino_rate() -> None:
        pass

    def should_retrieve_utility_tariff_details() -> None:
        pass

    def should_retrieve_utilities() -> None:
        pass

    def should_compute_year_proyection_cost() -> None:
        pass