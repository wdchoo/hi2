from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=10, null=False)
    age = models.IntegerField(null=False)
    weight = models.IntegerField(null=False)
    gender = models.BooleanField(default=False) # True: woman, False: man
    gym = models.ForeignKey('Gym', null=False)


class Gym(models.Model):
    name = models.CharField(max_length=20, null=False)


class Record(models.Model):
    profile = models.ForeignKey('core.Profile')
    WOD_type = models.ForeignKey('WOD')
    metcon_rec = models.IntegerField(null=True, default=0)  # input seconds
    gymnastics_rec = models.IntegerField(null=True, default=0)  # input number
    weightlifting_rec = models.IntegerField(null=True, default=0)  # input KG
    registered_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_newest = models.BooleanField(default=True)


class WOD(models.Model):
    name = models.CharField(max_length=20, null=False)