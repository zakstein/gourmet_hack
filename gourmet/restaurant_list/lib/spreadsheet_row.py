from exceptions import RequiredColumnNotFound
from restaurant_list.lib.yelp_api import Yelp_API
from restaurant_list.models import Restaurant, fetch_restaurant_from_database_or_api


class SpreadsheetRow(object):
    """
    This class represents a row in a spreadsheet
    """
    def __init__(self,
                 row,
                 list_element_model,
                 spreadsheet
    ):
        self.row = row
        self.list_element_model_instance = list_element_model()
        self.header_to_column_index_map = spreadsheet.header_to_column_index_map
        self.required_columns = spreadsheet.required_headers
        self.unclassified_info = {}

        self.list_element_model_instance.set_list(spreadsheet.list_model_instance)

    def parse_row(self):
        """
        Parses the raw spreadsheet row into the list_model class and unclassified info
        """
        list_element_fields, restaurant_fields, unclassified_fields = self._process_row_columns()

        if not restaurant_fields['city']:
            raise RequiredColumnNotFound('Address is a required field')

        api = Yelp_API()
        api_search_result = api.search(name=restaurant_fields['name'], location=self._get_address_including_city(restaurant_fields))

        restaurant = None

        if api_search_result.match_confidence:
            restaurant = fetch_restaurant_from_database_or_api(api_search_result.top_match)
        else:
            unclassified_fields = dict(restaurant_fields.items() + unclassified_fields.items())

        self.list_element_model_instance.set_all_fields_from_restaurant_and_element_info(
            list_element_fields,
            restaurant,
            unclassified_fields
        )

        if not self._check_required_columns_are_present():
            raise RequiredColumnNotFound('Required column not populated')

    def _get_address_including_city(self, info):
        address = info['city']
        if 'address' in info:
            address = '{}, {}'.format(info['address'].strip(), info['city'])

        return address


    def _process_row_columns(self):
        """
        Takes in a row and header information and returns three lists: the fields for a
        restaurant object, a restaurantListElement, and unclassified(neither)
        """
        unclassified_info = {}
        restaurant_fields = {}
        list_element_fields = {}
        model_field_names = self.list_element_model_instance._meta.get_all_field_names()
        restaurant_field_names = Restaurant._meta.get_all_field_names()
        for idx, cell in enumerate(self.row):
            cell_name = self.header_to_column_index_map[idx].lower()
            cell_value = cell.value
            if cell_name in model_field_names:
                if cell_name != 'restaurant':
                    list_element_fields[cell_name] = cell_value
                else:
                    restaurant_fields['name'] = cell_value
            elif cell_name in restaurant_field_names:
                restaurant_fields[cell_name] = cell_value
            else:
                unclassified_info[cell_name] = cell_value
        return [list_element_fields, restaurant_fields, unclassified_info]

    def _check_required_columns_are_present(self):
        """
        Checks if the required columns are present and returns true if they are
        """
        required_columns_count = dict(zip(
            self.required_columns,
            [0] * len(self.required_columns)
        ))
        for idx, cell in enumerate(self.row):
            self._update_required_column_count_with_header_name(
                self.header_to_column_index_map[idx].lower(),
                required_columns_count
            )
        for required_column, count in required_columns_count.items():
            if count != 1:
                return False

        return True


    def _update_required_column_count_with_header_name(self, header_name, required_columns_count):
        if header_name in self.required_columns:
            required_columns_count[header_name] += 1
