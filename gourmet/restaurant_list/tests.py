"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from models import RestaurantList, restaurant_list_for_user
from mock import MagicMock, patch


class RestaurantListTest(TestCase):
    @patch.object(RestaurantList, 'save')
    def test_restaurant_list_for_user_creates_new_restaurant_list(self, mock_method):
        user = User(username='zakstein', password='test1234')
        restaurant_list_for_user(user)
        mock_method.assert_called_with()
