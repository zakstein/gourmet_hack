from django.db import models
from django.contrib.auth import models as auth_models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=1023)
    location = models.CharField(max_length=512)

class RestaurantList(models.Model):
    owner = models.ForeignKey(auth_models.User)

class RestaurantListElement(models.Model):
    restaurantList = models.ForeignKey('RestaurantList')
    restaurant = models.ForeignKey('Restaurant')
    rating = models.PositiveIntegerField()
    has_been = models.BooleanField()
