# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from pulsecode import settings
from django.utils.html import format_html
import os


class Tag(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name

class Creator(models.Model):
	name = models.CharField(max_length=12)
	salutation = models.CharField(max_length=140, blank=True)
	picture = models.ImageField(upload_to='uploads/userimage', default='default/user_default.png')
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
		help_text=u'트랙은 10MiB 미만으로 올려주세요.')

	image = models.ImageField(upload_to='uploads/images/%Y/%m/%d', 
		help_text=u'배경으로 쓰일 이미지입니다. 2MiB 미만의 이미지만 올려주세요.',
		default='default/background_default.png')

	description = models.CharField(max_length=140, 
		help_text='트랙에 대한 간단한 설명을 써주세요.')
	datetime = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.title

class Journal(Post):
	body = models.TextField()
	bgimage = models.ImageField(upload_to='uploads/bgimage/%Y/%m/%d/',
		default='default/background_default.png')

	def __unicode__(self):
		return self.title
class Comment(models.Model):
	author = models.ForeignKey(Member)
	post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
	text = models.CharField(max_length=140)

	def __unicode__(self):
		return self.text

@receiver(models.signals.post_delete, sender=Track)
def delete_file_on_model_delete(sender, instance, **kwargs):
	if instance.audio_file:
		if os.path.isfile(instance.audio_file.path):
			os.remove(instance.audio_file.path)

