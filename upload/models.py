from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Image(models.Model):
	data = models.ImageField(upload_to='uploads/image/%Y/%m/%d/')
