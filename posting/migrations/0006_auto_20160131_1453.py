# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 05:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0005_remove_track_download'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='liked_member',
            field=models.ManyToManyField(blank=True, related_name='liked_post', to='posting.Member'),
        ),
        migrations.AlterField(
            model_name='post',
            name='scraped_member',
            field=models.ManyToManyField(blank=True, related_name='scraped_post', to='posting.Member'),
        ),
    ]
