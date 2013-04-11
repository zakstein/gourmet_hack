import json
from django.db import models
from lib.api import MatchAPI
from lib.exceptions import RequiredColumnNotFound
from django.contrib.auth import models as auth_models
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

class Restaurant(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    url = models.CharField(max_length=1023, db_index=True)
    full_address = models.CharField(max_length=1023)
    address = models.CharField(max_length=256, db_index=True)
    city = models.CharField(max_length=128, db_index=True)
    state = models.CharField(max_length=64)
    zip_code = models.IntegerField()
    neighborhood = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    # Note: this version of django does not yet support PointField, so we just use a char field
    geo_coordinate = models.CharField(max_length=1024)

    def set_uniq_id_hash(self):
        self.uniq_id_hash = hash(self.name, self.city, self.address)

class RestaurantList(models.Model):
    owner = models.OneToOneField(auth_models.User)

    def update_restaurant_list_with_file_data(self, file_data):
        """
        Takes in a xlrd work_book and populates the database
        """
        pass

def restaurant_list_for_user(user):
    """
    Returns restaurant list associated with a given user
    It will create one if none exist
    """
    try:
        restaurant_list = user.restaurantlist
    except ObjectDoesNotExist:
        restaurant_list = RestaurantList(owner=user)
        restaurant_list.save()

    return restaurant_list

class RestaurantListElement(models.Model):
    restaurantList = models.ForeignKey('RestaurantList')
    restaurant = models.ForeignKey('Restaurant')
    rating = models.PositiveIntegerField()
    has_been = models.BooleanField()
    notes = models.TextField()

    def set_all_fields_from_spreadsheet_row_and_save(self, row, header_column_map):
        """
        Takes cells from a spreadsheet and sets the corresponding fields in the restaurant list element
        """
        unclassified_info, restaurant_info, self_fields = self._process_row_columns(
            row,
            header_column_map
        )

        self.set_fields(self_fields)

        if not restaurant_info['address']:
            raise RequiredColumnNotFound('Address is a required field')

        api = MatchAPI(name=restaurant_info['name'], location=self._get_address_including_city(restaurant_info))
        api.execute()
        if api.match_confidence:
            self.restaurant = self._fetch_restaurant_from_database_or_api(api, restaurant_info)
        else:
            unclassified_info += restaurant_info

        return unclassified_info

    def _process_row_columns(self, row, header_column_map):
        """
        Takes in a row and header information and returns three lists: the fields for a
        restaurant object, a restaurantListElement, and unclassified(neither)
        """
        unclassified_info = {}
        restaurant_info = {}
        self_fields = {}
        model_field_names = self._meta.get_all_field_names()
        restaurant_field_names = Restaurant._meta.get_all_field_names()
        for idx, cell in enumerate(row):
            cell_name = header_column_map[idx].lower()
            cell_value = cell.value
            if cell_name in model_field_names:
                if cell_name != 'restaurant':
                    self_fields[cell_name] = cell_value
                else:
                    restaurant_info['name'] = cell_value
            elif cell_name in restaurant_field_names:
                restaurant_info[cell_name] = cell_value
            else:
                unclassified_info[cell_name] = cell_value
        return [unclassified_info, restaurant_info, self_fields]

    def _fetch_restaurant_from_database_or_api(self, api, restaurant_info):
        """
        Attempts to fetch a restaurant from the DB. If that fails, create one
        """
        try:
            restaurant = Restaurant.objects.get(
                name=api.top_match['name'],
                address=api.top_match['address']['address'][0],
                city=api.top_match['address']['city']
            )
        except ObjectDoesNotExist:
            restaurant = Restaurant(
                name=api.top_match['name'],
                address=api.top_match['address']['address'][0],
                city=api.top_match['address']['city'],
                state=api.top_match['address']['state_code'],
                country=api.top_match['address']['country_code'],
                zip_code=api.top_match['address']['postal_code'],
                neighborhood=api.top_match['address']['neighborhoods'][0],
                geo_coordinate=json.dumps(api.top_match['address']['coordinate']),
            )

            restaurant.save()

            return restaurant

    def set_fields(self, fields):
        for name, value in fields.items():
            setattr(self, name, value)

    def _get_address_including_city(self, info):
        if 'city' in info:
            return '{} {}'.format(info['address'], info['city'])

        return info['address']

    def set_list(self, list_model_instance):
        self.restaurantList = list_model_instance
