from __future__ import unicode_literals

from django.db import models
from upload.models import JournalUpload
from django.contrib.auth.models import User
from django.dispatch import receiver
from pulsecode import settings
from django.utils.html import format_html
from django_markdown.models import MarkdownField
import os


class Tag(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name

class Creator(models.Model):
	name = models.CharField(max_length=12)
	salutation = models.CharField(max_length=140)
	picture = models.ImageField(upload_to='uploads/userimage')
	post_num = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

class Member(Creator):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __unicode__(self):
		return self.user.username

class Team(Creator):
	member = models.ManyToManyField(Member)
	
class Post(models.Model):
	title = models.CharField(max_length=40)
	author = models.ForeignKey(Creator)
	tag = models.ManyToManyField(Tag)
	liked_member = models.ManyToManyField(Member, related_name='liked_post', blank=True)
	scraped_member = models.ManyToManyField(Member, related_name='scraped_post', blank=True)

	def __unicode__(self):
		return self.title

class Track(Post):
	#data
	allow_tags = True
	audio_file = models.FileField(upload_to='uploads/tracks/converted/%Y/%m/%d/',
		help_text='A track should be smaller than 10MiB')

	image = models.ImageField(upload_to='uploads/images/%Y/%m/%d', 
		help_text='Image should be smaller than 2MiB')

	description = models.CharField(max_length=140)
	datetime = models.DateTimeField(auto_now=True)

	def audio_file_player(self):
	    """audio player tag for admin"""
	    self.allow_tags
	    if self.audio_file:
	        file_url = settings.MEDIA_URL + str(self.audio_file)
	        player_string = '<ul class="playlist"><li style="width:250px;">\
	        <a href="%s">%s</a></li></ul>' % (file_url, os.path.basename(self.audio_file.name))
	        return format_html(player_string)
	def __unicode__(self):
		return self.title

class Journal(Post):
	body = MarkdownField()
	bgimage = models.ImageField(upload_to='uploads/bgimage/%Y/%m/%d/')

	def __unicode__(self):
		return self.title
class Comment(models.Model):
	author = models.ForeignKey(Member)
	post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
	text = models.CharField(max_length=140)


@receiver(models.signals.post_delete, sender=Track)
def delete_file_on_model_delete(sender, instance, **kwargs):
	if instance.audio_file:
		if os.path.isfile(instance.audio_file.path):
			os.remove(instance.audio_file.path)

