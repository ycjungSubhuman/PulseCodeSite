from __future__ import unicode_literals

from django.db import models

# Create your models here.
class JournalUpload(models.Model):
	data = models.FileField(upload_to='uploads/journalupload/%Y/%m/%d/')
