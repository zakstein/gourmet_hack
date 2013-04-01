import xlrd

from django.test import TestCase
from django.contrib.auth.models import User
from models import RestaurantList, RestaurantListElement, restaurant_list_for_user
from lib.spreadsheet import Spreadsheet
from lib.spreadsheet_row import SpreadsheetRow
from lib.api import MatchAPI
from mock import MagicMock, patch
from django.forms.models import model_to_dict


class MatchAPITest(TestCase):
        def setUp(self):
                self.apimatch = MatchAPI("yelp","san francisco")
                self.mock_response = { "businesses": [ { "categories": [ [ "Local Flavor", "localflavor" ], [ "Mass Media", "massmedia" ] ], "display_phone": "+1-415-908-3801", "id": "yelp-san-francisco", "is_claimed": "true", "is_closed": "false", "image_url": "http://s3-media2.ak.yelpcdn.com/bphoto/7DIHu8a0AHhw-BffrDIxPA/ms.jpg", "location": { "address": [ "706 Mission St" ], "city": "San Francisco", "coordinate": { "latitude": 37.786138600000001, "longitude": -122.40262130000001 }, "country_code": "US", "cross_streets": "3rd St & Opera Aly", "display_address": [ "706 Mission St", "(b/t 3rd St & Opera Aly)", "SOMA", "San Francisco, CA 94103" ], "geo_accuracy": 8, "neighborhoods": [ "SOMA" ], "postal_code": "94103", "state_code": "CA" }, "mobile_url": "http://m.yelp.com/biz/4kMBvIEWPxWkWKFN__8SxQ", "name": "Yelp", "phone": "4159083801", "rating_img_url": "http://media1.ak.yelpcdn.com/static/201012161694360749/img/ico/stars/stars_3.png", "rating_img_url_large": "http://media3.ak.yelpcdn.com/static/201012161053250406/img/ico/stars/stars_large_3.png", "rating_img_url_small": "http://media1.ak.yelpcdn.com/static/201012162337205794/img/ico/stars/stars_small_3.png", "review_count": 3347, "snippet_image_url": "http://s3-media2.ak.yelpcdn.com/photo/LjzacUeK_71tm2zPALcj1Q/ms.jpg", "snippet_text": "Sometimes we ask questions without reading an email thoroughly as many of us did for the last event. In honor of Yelp, the many questions they kindly...", "url": "http://www.yelp.com/biz/yelp-san-francisco" } ], "region": { "center": { "latitude": 37.786138600000001, "longitude": -122.40262130000001 }, "span": { "latitude_delta": 0.0, "longitude_delta": 0.0 } }, "total": 10651 }

        def test_that_parse_response_handles_the_api_response_properly(self):
                self.apimatch.parse_response(self.mock_response)
                parsed_keys = self.apimatch.top_match.keys()
                parsed_keys.sort()
                self.assertEqual(parsed_keys,['address','name','url'])


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

class SpreadsheetRowTest(TestCase):
    """
    Tests the SpreadsheetRow class
    """
    def setUp(self):
        self.required_column_count = {'restaurant': 0}
        self.row = SpreadsheetRow(
            row=None,
            list_element_model=RestaurantListElement,
            header_column_map=None,
            required_columns=['restaurant']
        )

    def test_parse_row_correctly_parses_row(self):
        book = xlrd.open_workbook('restaurant_list/sophia_test_data.xlsx')
        first_sheet = book.sheet_by_index(0)
        spreadsheet = Spreadsheet(
            RestaurantListElement,
            book,
            ['Restaurant']
        )

        spreadsheet._map_header_name_to_column_index(
            spreadsheet._get_headers_from_sheet(first_sheet)
        )
        self.row.row = first_sheet.row(1)
        self.row.header_column_map =  spreadsheet.header_to_column_index

        self.row.parse_row()

        print self.row.list_model_element_instance
        print self.row.unclassified_info
        print model_to_dict(self.row.list_model_element_instance)

    def test_update_required_column_count_with_header_name_correctly_updates(self):
        self.row._update_required_column_count_with_header_name('restaurant', self.required_column_count)

        self.assertEqual(1, self.required_column_count['restaurant'])

    def test_update_required_column_count_does_not_update_with_no_required(self):
        self.row._update_required_column_count_with_header_name('not_restaurant', self.required_column_count)

        self.assertEqual(0, self.required_column_count['restaurant'])

    def test_required_columns_are_present_returns_true_when_columns_are_present(self):
        required_columns = {'restaurant': 1, 'notes': 1}
        self.assertTrue(self.row._check_required_columns_are_present(required_columns))

    def test_required_columns_are_present_returns_false_when_columns_are_not_present(self):
        required_columns = {'restaurant': 1, 'notes': 0}
        self.assertFalse(self.row._check_required_columns_are_present(required_columns))

