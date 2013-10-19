import json

from django.db import models
import lib.spreadsheet
from django.contrib.auth import models as auth_models
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from denorm import denormalized

SORT_BY_NAME = 'restaurant_name'
SORT_BY_RATING = 'rating'
SORT_DIRECTION_ASC = 'ASC'
SORT_DIRECTION_DESC = 'DESC'

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
    sort_by = models.CharField(max_length=256, default='rating')
    sort_direction = models.CharField(max_length=256, default='DESC')

    def update_restaurant_list_with_file_data(self, file_book):
        """
        Takes in a xlrd work_book and populates the database
        """
        required_headers = ['restaurant', 'city']
        spreadsheet = lib.spreadsheet.Spreadsheet(self, file_book, required_headers)
        return spreadsheet.parse(RestaurantListElement)


def sort_by_options_for_restaurant_list():
    return [SORT_BY_NAME, SORT_BY_RATING]


def sort_direction_options_for_restaurant_list():
    return [SORT_DIRECTION_ASC, SORT_DIRECTION_DESC]

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


def fetch_restaurant_from_database_or_api(restaurant_info):
    """
    Attempts to fetch a restaurant from the DB. If that fails, create one
    """
    try:
        restaurant = Restaurant.objects.get(
            name=restaurant_info['name'],
            address=restaurant_info['address']['address'][0],
            city=restaurant_info['address']['city']
        )
    except ObjectDoesNotExist:
        full_address = "%s, %s, %s %s" % (
            restaurant_info['address']['address'][0],
            restaurant_info['address']['city'],
            restaurant_info['address']['state_code'],
            restaurant_info['address']['postal_code']
        )
        restaurant = Restaurant(
            name=restaurant_info['name'],
            full_address=full_address,
            address=restaurant_info['address']['address'][0],
            city=restaurant_info['address']['city'],
            state=restaurant_info['address']['state_code'],
            country=restaurant_info['address']['country_code'],
            zip_code=restaurant_info['address']['postal_code'],
            geo_coordinate=json.dumps(restaurant_info['address']['coordinate']),
            url=restaurant_info['url'],
        )

        if 'neighborhoods' in restaurant_info['address']:
            setattr(restaurant, 'neighborhood', restaurant_info['address']['neighborhoods'][0])

        restaurant.save()

    return restaurant


class RestaurantListElement(models.Model):
    restaurantList = models.ForeignKey('RestaurantList')
    restaurant = models.ForeignKey('Restaurant', null=True)
    rating = models.IntegerField(default=-1)
    has_been = models.BooleanField()
    notes = models.TextField(default='')
    # This field contains all info that is uploaded for later use
    raw_upload_info = models.TextField(default='')

    @denormalized(models.CharField, max_length=256)
    def restaurant_name(self):
        return self.restaurant.name

    def set_all_fields_from_restaurant_and_element_info(self, list_element_fields, restaurant, unclassified_info):
        """
        Takes info from three arrays about the restaurant and list element and creates objects in DB
        """
        self.set_fields(list_element_fields)

        if restaurant is not None:
            self.restaurant = restaurant

        setattr(self, 'raw_upload_info', json.dumps(unclassified_info))

        try:
            self.save()
        except Exception, error:
            print error.read()

        return unclassified_info

    def set_fields(self, fields):
        for name, value in fields.items():
            if value:
                setattr(self, name, value)

    def set_list(self, list_model_instance):
        self.restaurantList = list_model_instance
