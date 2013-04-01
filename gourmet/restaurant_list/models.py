from django.db import models
from lib.api import MatchAPI
from lib.exceptions import RequiredColumnNotFound
from django.contrib.auth import models as auth_models
from django.core.exceptions import ObjectDoesNotExist

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=1023)
    full_address = models.CharField(max_length=1023)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=64)
    zip_code = models.IntegerField()
    neighborhood = models.CharField(max_length=128)
    # Note: this version of django does not yet support PointField, so we just use a char field
    geo_coordinate = models.CharField(max_length=1024)

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

    def set_fields_from_spreadsheet_row(self, row, header_column_map):
        unclassified_info = {}
        for idx, cell in enumerate(row):
            cell_name = header_column_map[idx].lower()
            cell_value = cell.value
            model_field_names = self._meta.get_all_field_names()
            if cell_name in model_field_names:
                if cell_name != 'restaurant':
                    setattr(self, cell_name, cell_value)
                else:
                    restaurant_name = cell_value
            else:
                unclassified_info[cell_name] = cell_value

        if not unclassified_info['address']:
            raise RequiredColumnNotFound('Address is a required field')

        api = MatchAPI(restaurant_name, unclassified_info['address'])
        api.execute()



    def set_list(self, list_model_instance):
        self.restaurantList = list_model_instance
