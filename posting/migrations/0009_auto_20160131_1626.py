# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 07:26
from __future__ import unicode_literals

from django.db import migrations
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0008_auto_20160131_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journal',
            name='upload',
        ),
        migrations.AlterField(
            model_name='journal',
            name='body',
            field=django_markdown.models.MarkdownField(),
        ),
    ]