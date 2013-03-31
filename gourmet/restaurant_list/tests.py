import xlrd

from django.test import TestCase
from django.contrib.auth.models import User
from models import RestaurantList, RestaurantListElement, restaurant_list_for_user
from lib.spreadsheet import Spreadsheet
from mock import MagicMock, patch


class RestaurantListTest(TestCase):
    @patch.object(RestaurantList, 'save')
    def test_restaurant_list_for_user_creates_new_restaurant_list(self, mock_method):
        user = User(username='zakstein', password='test1234')
        user.save()
        restaurant_list_for_user(user)
        mock_method.assert_called_with()

    def test_restaurant_list_for_user_does_not_create_second_restaurant_list(self):
        user = User(username='zakstein', password='test1234')
        user.save()
        restaurant_list = RestaurantList(owner=user)
        restaurant_list.save()
        same_restaurant_list = restaurant_list_for_user(user)
        self.assertEqual(restaurant_list, same_restaurant_list)

class SpreadsheetTest(TestCase):
    def setUp(self):
        self.book = xlrd.open_workbook('restaurant_list/sophia_test_data.xlsx')
        self.sheet = Spreadsheet(RestaurantListElement, self.book, ['Restaurant'])

    def test_get_headers_returns_correctly(self):
        headers = self.sheet._get_headers_from_sheet(self.book.sheet_by_index(0))
        self.assertEqual(9, len(headers))
        self.assertEqual(u'Restaurant', headers[0].value)

    def test_check_headers_returns_true_when_headers_are_present(self):
        headers = self.sheet._get_headers_from_sheet(self.book.sheet_by_index(0))

        self.assertTrue(self.sheet._check_headers_have_required_headers(headers))

    def test_check_headers_returns_false_when_headers_are_not_present(self):
        headers = [ self.CellMock(ctype=1, value=u'notrestaurant')]

        self.assertFalse(self.sheet._check_headers_have_required_headers(headers))

    def test_map_header_name_to_column_index_correctly_maps_headers(self):
        headers = self.sheet._get_headers_from_sheet(self.book.sheet_by_index(0))

        self.sheet._map_header_name_to_column_index(headers)

        self.assertEqual('Restaurant', self.sheet.header_to_column_index[0])
        self.assertEqual('Rating', self.sheet.header_to_column_index[3])
        self.assertEqual('Notes', self.sheet.header_to_column_index[5])

    class CellMock(object):

        def __init__(self, ctype, value):
            self.ctype = ctype
            self.value = value

