# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 05:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0003_auto_20160127_1746'),
    ]

    operations = [
        migrations.RenameField(
            model_name='track',
            old_name='audio',
            new_name='audio_file',
        ),
    ]
