import xlrd

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from models import RestaurantList, RestaurantListElement, restaurant_list_for_user, Restaurant
import django.http
from lib.spreadsheet import Spreadsheet
from lib.spreadsheet_row import SpreadsheetRow
from lib.yelp_api import Yelp_API
from mock import patch, Mock
from lib.authorization_check import Authorization_Check, DELETE_ACTION
from decorators import authorization_required
from lib.api_search_results import Api_Search_Results


class YelpAPITest(TestCase):
    def setUp(self):
        self.apimatch = Yelp_API()
        self.mock_response = {"businesses": [
            {"categories": [["Local Flavor", "localflavor"], ["Mass Media", "massmedia"]],
             "display_phone": "+1-415-908-3801", "id": "yelp-san-francisco", "is_claimed": "true", "is_closed": "false",
             "image_url": "http://s3-media2.ak.yelpcdn.com/bphoto/7DIHu8a0AHhw-BffrDIxPA/ms.jpg",
             "location": {"address": ["706 Mission St"], "city": "San Francisco",
                          "coordinate": {"latitude": 37.786138600000001, "longitude": -122.40262130000001},
                          "country_code": "US", "cross_streets": "3rd St & Opera Aly",
                          "display_address": ["706 Mission St", "(b/t 3rd St & Opera Aly)", "SOMA",
                                              "San Francisco, CA 94103"], "geo_accuracy": 8, "neighborhoods": ["SOMA"],
                          "postal_code": "94103", "state_code": "CA"},
             "mobile_url": "http://m.yelp.com/biz/4kMBvIEWPxWkWKFN__8SxQ", "name": "Yelp", "phone": "4159083801",
             "rating_img_url": "http://media1.ak.yelpcdn.com/static/201012161694360749/img/ico/stars/stars_3.png",
             "rating_img_url_large": "http://media3.ak.yelpcdn.com/static/201012161053250406/img/ico/stars/stars_large_3.png",
             "rating_img_url_small": "http://media1.ak.yelpcdn.com/static/201012162337205794/img/ico/stars/stars_small_3.png",
             "review_count": 3347,
             "snippet_image_url": "http://s3-media2.ak.yelpcdn.com/photo/LjzacUeK_71tm2zPALcj1Q/ms.jpg",
             "snippet_text": "Sometimes we ask questions without reading an email thoroughly as many of us did for the last event. In honor of Yelp, the many questions they kindly...",
             "url": "http://www.yelp.com/biz/yelp-san-francisco"}],
                              "region": {"center": {"latitude": 37.786138600000001, "longitude": -122.40262130000001},
                                         "span": {"latitude_delta": 0.0, "longitude_delta": 0.0}}, "total": 10651}

    def test_that_parse_response_handles_the_api_response_properly(self):
        result = Api_Search_Results(self.apimatch._parse_search_response(self.mock_response), 1, 'yelp')
        parsed_keys = result.top_match.keys()
        parsed_keys.sort()
        self.assertEqual(parsed_keys, ['address', 'api_id', 'name', 'url'])


class RestaurantListTest(TestCase):
    def setUp(self):
        self.user = User(username='zakstein', password='test1234')
        self.user.save()

    @patch.object(RestaurantList, 'save')
    def test_restaurant_list_for_user_creates_new_restaurant_list(self, mock_method):
        restaurant_list_for_user(self.user)
        mock_method.assert_called_with()

    def test_restaurant_list_for_user_does_not_create_second_restaurant_list(self):
        restaurant_list = RestaurantList(owner=self.user)
        restaurant_list.save()
        same_restaurant_list = restaurant_list_for_user(self.user)
        self.assertEqual(restaurant_list, same_restaurant_list)

    def test_update_restaurant_list_with_file_data_works(self):
        restaurant_list = RestaurantList(owner=self.user)
        restaurant_list.save()
        rows = restaurant_list.update_restaurant_list_with_file_data(xlrd.open_workbook('restaurant_list/sophia_test_data.xlsx', encoding_override='utf-8'))
        self.assertEqual(155, len(rows))


class SpreadsheetTest(TestCase):
    def setUp(self):
        self.book = xlrd.open_workbook('restaurant_list/sophia_test_data.xlsx')
        self.sheet = Spreadsheet(RestaurantListElement, self.book, ['restaurant'])

    def test_get_headers_returns_correctly(self):
        headers = self.sheet._get_headers_from_sheet(self.book.sheet_by_index(0))
        self.assertEqual(10, len(headers))
        self.assertEqual(u'Restaurant', headers[0].value)

    def test_check_headers_returns_true_when_headers_are_present(self):
        headers = self.sheet._get_headers_from_sheet(self.book.sheet_by_index(0))

        self.assertTrue(self.sheet._check_headers_have_required_headers(headers))

    def test_check_headers_returns_false_when_headers_are_not_present(self):
        headers = [self.CellMock(ctype=1, value=u'notrestaurant')]

        self.assertFalse(self.sheet._check_headers_have_required_headers(headers))

    def test_map_header_name_to_column_index_correctly_maps_headers(self):
        headers = self.sheet._get_headers_from_sheet(self.book.sheet_by_index(0))

        self.sheet._map_header_name_to_column_index(headers)

        self.assertEqual('Restaurant', self.sheet.header_to_column_index_map[0])
        self.assertEqual('Rating', self.sheet.header_to_column_index_map[4])
        self.assertEqual('Notes', self.sheet.header_to_column_index_map[6])

    class CellMock(object):
        def __init__(self, ctype, value):
            self.ctype = ctype
            self.value = value


class RestaurantListElementTest(TestCase):
    def test_set_all_fields_from_spreadsheet_row_and_save(self):
        user = User(username='zakstein', password='test1234')
        user.save()

        list_element = RestaurantListElement()
        restaurant_list = RestaurantList(owner=user)
        restaurant_list.save()

        list_element_fields = {'rating': '90', 'has_been': True, 'notes': 'good test'}
        restaurant = Restaurant(
            name='test restaurant',
            full_address='1234 test ave, testopolis testifornia',
            address='1234 test ave',
            city='testopolis',
            state='testifornia',
            country='testopia',
            zip_code='12345',
            url='http://www.example.com',
        )

        unclassified_info = {'did_zak_go': True, 'reservation_size': 20}

        list_element.restaurantList = restaurant_list
        list_element.set_all_fields_from_restaurant_and_element_info(
            list_element_fields, restaurant, unclassified_info
        )

        self.assertEqual(list_element_fields['rating'], list_element.rating)
        self.assertEqual(restaurant, list_element.restaurant)


class SpreadsheetRowTest(TestCase):
    """
    Tests the SpreadsheetRow class
    """

    def setUp(self):
        self.required_column_count = {'restaurant': 0}
        self.book = xlrd.open_workbook('restaurant_list/sophia_test_data.xlsx')
        self.first_sheet = self.book.sheet_by_index(0)
        self.spreadsheet = Spreadsheet(
            list_model_instance=RestaurantList(),
            data=self.book,
            required_headers=['restaurant']
        )
        self.row = SpreadsheetRow(
            row=None,
            list_element_model=RestaurantListElement,
            spreadsheet=self.spreadsheet
        )

    @patch.object(RestaurantListElement, 'set_all_fields_from_restaurant_and_element_info')
    def test_parse_row_correctly_parses_row(self, mock_method):
        self.spreadsheet._map_header_name_to_column_index(
            self.spreadsheet._get_headers_from_sheet(self.first_sheet)
        )
        self.row.row = self.first_sheet.row(1)
        self.row.header_to_column_index_map = self.spreadsheet.header_to_column_index_map

        self.row.parse_row()

        self.assertFalse(self.row.list_element_model_instance.has_been)
        self.assertTrue(mock_method.called)

    def test_update_required_column_count_with_header_name_correctly_updates(self):
        self.row._update_required_column_count_with_header_name('restaurant', self.required_column_count)

        self.assertEqual(1, self.required_column_count['restaurant'])

    def test_update_required_column_count_does_not_update_with_no_required(self):
        self.row._update_required_column_count_with_header_name('not_restaurant', self.required_column_count)

        self.assertEqual(0, self.required_column_count['restaurant'])

    def test_get_address_including_city_and_self(self):
        info = {'address': '108 Mission ', 'city': 'San Francisco'}
        spreadsheet_row = SpreadsheetRow(self.spreadsheet.data.sheet_by_index(0).row(0), RestaurantListElement, self.spreadsheet)
        self.assertEqual('108 Mission, San Francisco', spreadsheet_row._get_address_including_city(info))



class AuthorizationRequiredTest(TestCase):
    """
    Tests the authorization_required decorator
    """

    def setUp(self):
        self.request = Mock()
        self.request.user = 'user_1'

    def test_decorator_calls_func_if_authorized(self):
        function = Mock()
        authorization_check = authorization_required(DELETE_ACTION)

        decorated_function = authorization_check(function)

        decorated_function(self.request, user='user_1')
        self.assertTrue(function.called)

    def test_decorator_does_not_call_func_if_not_authorized(self):
        function = Mock()
        authorization_check = authorization_required(DELETE_ACTION)

        decorated_function = authorization_check(function)

        decorated_function(self.request, user='user_2')

        self.assertFalse(function.called)

class EndToEndTests(TestCase):
    """
    Tests various key end to end features
    """
    def setUp(self):
        self.user = User.objects.create_user('zakstein', 'zakstein@test.com', 'test1234')
        self.user.save()
        self.client = Client()
        self.client.login(username=self.user.username, password='test1234')

    def test_add_restaurant(self):
        # {u'rating': [u'85'], u'restaurant_id': [u'marlowe-san-francisco-2'], u'location': [u'San Francisco'], u'restaurant_name': [u'Marlowe'], u'has_been': [u'on'], u'csrfmiddlewaretoken': [u'944f8e66176a6b072c5cd93d03d9138d'], u'notes': [u'notes1']}
        post_data = django.http.QueryDict('rating=85&restaurant_id=marlowe-san-francisco-2&location=San%20Francisco&restaurant_name=Marlowe&has_been=on&notes=notes1')
        response = self.client.post('/add/', post_data)
        print response

    def test_upload_sheet(self):
        with open('restaurant_list/sophia_test_data.xlsx') as fp:
            import pdb; pdb.set_trace()
            response = self.client.post('/upload/', {'input_spreadsheet': fp})

