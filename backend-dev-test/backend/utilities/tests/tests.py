from django.test import TestCase
from django.http import HttpRequest, QueryDict
from django.template.loader import render_to_string
from unittest import mock

from utilities.views import WebsiteDemoView
from utilities.models import User

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
        request.method = 'POST'
        request.POST = self.build_post_website_demo_body()
        response = view.post(request=request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Aether Energy Utilities Demo</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))
    
    def test_website_can_save_a_POST_request(self) -> None:
        view = WebsiteDemoView()
        request = HttpRequest()
        request.method = 'POST'
        request.POST = self.build_post_website_demo_body()
        response = view.post(request=request)
        self.assertIn('user_form', response.content.decode())
        expected_html = render_to_string(
            'website_demo.html',
            {'new_user_address': 'Black Star #45',
             'new_user_consumption': '15',
             'new_user_percentage_scale': '10'
            },
            request=request
        )
        self.assertEqual(response.content.decode(), expected_html)
 
class UserModelTest(TestCase):
    def test_saving_and_retrieving_users(self) -> None:
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
        self.assertEqual(saved_users.count(), 1)
        first_saved_user = saved_users[-1]
        second_saved_user = saved_users[0]
        self.assertEqual(first_saved_user.firstname, 'Luke')
        self.assertEqual(second_saved_user.firstname, 'Han')