# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-22 10:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0019_auto_20160222_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='datetime',
        ),
        migrations.AddField(
            model_name='comment',
            name='datetime',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 2, 22, 10, 44, 30, 166402, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='datetime',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 2, 22, 10, 44, 39, 588757, tzinfo=utc)),
            preserve_default=False,
        ),
    ]