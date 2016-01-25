from __future__ import unicode_literals

from django.db import models
from upload.models import JournalUpload
from django.contrib.auth.models import User

class Tag(models.Model):
	name = models.CharField(max_length=20)

class Creator(models.Model):
	name = models.CharField(max_length=12)
	salutation = models.CharField(max_length=140)
	picture = models.ImageField(upload_to='uploads/userimage')
	post_num = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

class Member(Creator):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

class Team(Creator):
	member = models.ManyToManyField(Member)
	
class Post(models.Model):
	title = models.CharField(max_length=40)
	author = models.OneToOneField(Creator)
	tag = models.ManyToManyField(Tag)
	liked_member = models.ManyToManyField(Member, related_name='liked_post')
	scraped_member = models.ManyToManyField(Member, related_name='scraped_post')

class Track(Post):
	#data
	audio = models.FileField(upload_to='uploads/tracks/converted/%Y/%m/%d/')
	download = models.FileField(upload_to='uploads/tracks/raw/%Y/%m/%d/', 
		help_text='A track should be smaller than 10MiB')

	image = models.ImageField(upload_to='uploads/images/%Y/%m/%d', 
		help_text='Image should be smaller than 2MiB')

	description = models.CharField(max_length=140)
	playtime = models.IntegerField() #in seconds
	datetime = models.DateTimeField(auto_now=True)

class Journal(Post):
	body = models.TextField()
	bgimage = models.ImageField(upload_to='uploads/bgimage/%Y/%m/%d/')
	upload = models.ManyToManyField(JournalUpload)

