from django.db import models
from django.contrib.auth import models as auth_models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=1023)
    location = models.CharField(max_length=512)

class RestaurantList(models.Model):
    owner = models.OneToOneField(auth_models.User)

    def update_restaurant_list_with_file_data(self, file_data):
        """
        Takes in a xlrd work_book and instantiates the
        """

def restaurant_list_for_user(user):
    """
    Returns restaurant list associated with a given user
    It will create one if none exist
    """
    if not user.restaurantlist:
        restaurant_list = RestaurantList(owner=user)
        restaurant_list.save()
    else:
        restaurant_list = user.restaurantlist

    return restaurant_list

class RestaurantListElement(models.Model):
    restaurantList = models.ForeignKey('RestaurantList')
    restaurant = models.ForeignKey('Restaurant')
    rating = models.PositiveIntegerField()
    has_been = models.BooleanField()
