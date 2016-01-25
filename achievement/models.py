from __future__ import unicode_literals

from django.db import models
from posting.models import Creator, Member

class Achievement(models.Model):
	image = models.ImageField(upload_to='uploads/achievement/')
	title = models.CharField(max_length=40)
	description = models.CharField(max_length=140)

class MemberAchievement(models.Model):
	member = models.ForeignKey(Member, on_delete=models.CASCADE)
	achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
	progress = models.IntegerField(default=0)
