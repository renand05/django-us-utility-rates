from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from unittest import mock

from utilities.views import home_page
from utilities.models import User

@mock.patch('django.template.context_processors.get_token', mock.Mock(return_value='predicabletoken'))
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    
    def test_home_page_has_correct_html_title(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))
    
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)
        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'},
            request=request
        )
        self.assertEqual(response.content.decode(), expected_html)
 
class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_user = User()
        first_user.firstname = 'Luke'
        first_user.lastname = 'Skywalker'
        first_user.save()
        second_user = User()
        second_user.firstname = 'Han'
        second_user.lastname = 'Solo'
        second_user.save()
        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(), 2)
        first_saved_user = saved_users[0]
        second_saved_user = saved_users[1]
        self.assertEqual(first_saved_user.firstname, 'Luke')
        self.assertEqual(second_saved_user.firstname, 'Han')