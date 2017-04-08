from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'age', 'weight', 'gender', 'gym',)


class GymAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RecordAdmin(admin.ModelAdmin):
    list_display = ('profile', 'WOD_type', 'metcon_rec', 'gymnastics_rec', 'weightlifting_rec', 'registered_time', 'modified_time', 'is_newest',)


class WODAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Gym, GymAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(WOD, WODAdmin)
