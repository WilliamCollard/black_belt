from __future__ import unicode_literals
from django.db import models
from datetime import datetime


print("PRINTING TIME: ", datetime.now())
# Create your models here.

now = str(datetime.now())


class UserManager(models.Manager):
    def basic_validator(self, postData):

        print("POSTDATA is", postData)

        errors = {}
        # Name Validation
        if len(postData['name']) < 3:
            errors['name']= 'Name must be at least 3 characters!'
        #Username Validation
        if len(postData["username"]) < 3:
            errors["username"] = "Username must be at least 3 characters!"
        elif User.objects.filter(username = postData["username"]):
            errors["username"] = "Great one, but it's already taken!"

        #Password Validation
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if postData['confirm_password'] != postData['password']:
            errors['password'] = "Passwords don't match!"
        return errors

    def login_validator(self, postData):

        print("POSTDATA is", postData)

        errors = {}
        #Username Validation
        if len(postData["username"]) < 1:
            errors["username"] = "Username is required!"
        elif not User.objects.filter(username = postData["username"]):
            errors["username"] = "Username was not found, please register!"

        #Password Validation
        if len(postData['password']) < 1:
            errors['password'] = "Password is required!"
        return errors

class TripManager(models.Manager):

    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors['destination'] = "Destination must be filled out!"
        if len(postData['plan']) < 1:
            errors['plan'] = "Description must be filled out!"
        if len(postData['start_date']) <1:
            errors['start_date'] = "Travel date from must be filled out!"
        elif postData['start_date'] < now:
            errors['start_date'] = "Travel date from must be in the future!"
        elif postData['start_date'] > postData['end_date']:
            errors['start_date'] = "Travel date from must be before the trip's end date!"
        if len(postData['end_date']) <1:
            errors['start_date'] = "Travel date to must be filled out!"
        elif postData['end_date'] < now:
            errors['end_date'] = "Travel date to must be in the future!"
        return errors


class User(models.Model):
    name= models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    #represent method
    def __repr__(self):
        return f"User: {self.id} {self.username}"


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date= models.DateTimeField()
    plan= models.TextField()

    #ONE TO MANY RELATIONSHIP
    added_by = models.ForeignKey(User, related_name="trips", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = TripManager()

#MANY TO MANY RELATIONSHIP
class Join(models.Model):
    user = models.ForeignKey(User, related_name="user_joined", on_delete = models.CASCADE)
    trip = models.ForeignKey(Trip, related_name="trip_joined", on_delete = models.CASCADE)
