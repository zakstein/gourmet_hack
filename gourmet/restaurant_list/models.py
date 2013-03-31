from django.db import models
from django.contrib.auth import models as auth_models
from django.core.exceptions import ObjectDoesNotExist

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=1023)
    location = models.CharField(max_length=512)

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
