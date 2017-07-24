from __future__ import unicode_literals

from django.db import models
import re
import datetime

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Name must be at least 2 characters long."
        if len(postData['username']) <3:
            errors['username'] = "Username must be at least 2 characters long."
        if len(postData['pw']) < 8:
            errors['pw'] = "Password must be at least 8 characters long."
        if postData['pw'] != postData['pwconfirm']:
            errors['pw'] = "Password and confirmation must match."
        return errors

class User(models.Model):
    name = models.CharField(max_length=254)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData['plan']) ==0:
            errors['plan'] = "Please include a plan."
        if len(postData['destination']) == 0:
            errors['destination'] = "Please include a destination."
        if len(postData['start_date']) == 0:
            errors['start_date'] = "Please include a start date."
        if len(postData['end_date']) == 0:
            errors['end_date'] = "Please include an end date."
        if str(postData['start_date']) < str(datetime.date.today()):
            errors['start_date'] = "Start date must be in the future!"
        if str(postData['end_date']) < str(datetime.date.today()):
            errors['end_date'] = "End date must be in the future!"
        if str(postData['end_date']) < str(postData['start_date']):
            errors['end_date'] = "End date must be after start date!"
        return errors

class Trip(models.Model):
    plan = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name = "trips")
    joined = models.ManyToManyField(User, related_name = "joining")
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()
