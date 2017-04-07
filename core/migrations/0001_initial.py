# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=10)),
                ('age', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('gender', models.BooleanField(default=False)),
                ('gym', models.ForeignKey(to='core.Gym')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('metcon_rec', models.IntegerField(default=0, null=True)),
                ('gymnastics_rec', models.IntegerField(default=0, null=True)),
                ('weightlifting_rec', models.IntegerField(default=0, null=True)),
                ('registered_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True, null=True)),
                ('is_newest', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='WOD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='record',
            name='WOD_type',
            field=models.ForeignKey(to='core.WOD'),
        ),
        migrations.AddField(
            model_name='record',
            name='profile',
            field=models.ForeignKey(to='core.Profile'),
        ),
    ]
