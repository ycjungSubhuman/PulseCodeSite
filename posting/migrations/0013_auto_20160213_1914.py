# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-13 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0012_auto_20160212_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='body',
            field=models.TextField(),
        ),
    ]
