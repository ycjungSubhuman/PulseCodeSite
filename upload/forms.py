# -*- coding: utf-8 -*-

from django import forms
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.forms.utils import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button, Div, Field, Submit
from posting.models import Track, Journal
import audiotools
import os
import time
import random
import string

class TrackUploadForm(forms.ModelForm):
	class Meta:
		model = Track
		fields = [
			'audio_file',
			'title',
			'image',
			'description',
		]
	tag_string = forms.CharField(max_length=50,
		help_text=u'태그: 최소 1개, 영문자만가능, 쉼표로 구분')

	def __init__(self, *args, **kwargs):
		super(TrackUploadForm, self).__init__(*args, **kwargs)

		#form helper
		self.helper = FormHelper()

		self.helper.form_id = 'track_upload_form'
		self.helper.attrs = {'role': 'form', 'enctype': 'multipart/form-data'}
		self.helper.layout = Layout(
			Div( #this div is for track upload form
				Field('audio_file', id='audio_form'),
			),
			Div( # this div is for information form
				Field('image', id='image_form'),
				Field('title', id='title_form', css_class='form-control'),
				Field('description', id='description_form', css_class='form-control'),
				Field('tag_string', id='tag_form', css_class='form-control'),
				Submit('submit', "Save", id='submit'),
			),
		)
		self.fields['description'].widget = forms.Textarea()
		self.fields['tag_string'].label = 'Tags'

	error_messages = {
		'tag_invalid': u'태그가 형식에 맞지 않습니다.',
		'image_exceed': u'이미지가 2MiB를 넘어갑니다. 더 작은 이미지를 선택해주세요.',
		'audio_exceed': u'트랙의 크기가 너무 틉니다.',
		'audio_invalid': u'지원하지 않는 오디오 형식입니다. mp3나 ogg를 올려주세요.',
		'audio_corrupted': u'올바르지 않거나 손상된 오디오 파일입니다.',
	}
	def clean_audio_file(self):
		audio = self.cleaned_data['audio_file']
		if audio.size > 10*1024*1024:
			raise ValidationError(self.error_messages['audio_exceed'])

		allowed_type = ['audio/mpeg', 'audio/ogg', 'audio/mp3']
		if not (audio.content_type in allowed_type):
			raise ValidationError(self.error_messages['audio_invalid'])

		randomfilename = str(time.time())+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
		path = default_storage.save('tmp/'+randomfilename, ContentFile(audio.read()))
		try:
			audiotools.open(os.path.join(settings.MEDIA_ROOT, path))
			default_storage.delete('tmp/'+randomfilename)
		except audiotools.UnsupportedFile:
			default_storage.delete('tmp/'+randomfilename)
			raise ValidationError(self.error_messages['audio_corrupted'])

		return audio





	def clean_tag_string(self):
		tags = self.cleaned_data['tag_string'].split(',')
		tags[:] = [tag.strip() for tag in tags]
		for tag in tags:
			if not tag.isalpha():
				print 'tag'
				raise ValidationError(self.error_messages['tag_invalid'])
			try:
				tag.decode()
			except UnicodeEncodeError:
				raise ValidationError(self.error_messages['tag_invalid'])
		return self.cleaned_data['tag_string']

	def clean_image(self):
		size_image = self.cleaned_data['image'].size
		if size_image > 2*1024*1024: # 2MiB
			raise ValidationError(self.error_messages['image_exceed'])
		return self.cleaned_data['image']


class JournalForm(forms.ModelForm):
	class Meta:
		model = Journal
		fields = [
			'title',
			'body',
			'bgimage',
		]
	tag_string = forms.CharField(max_length=50)
	error_messages = {
		'tag_invalid': u'태그가 형식에 맞지 않습니다.',
		'image_exceed': u'이미지가 2MiB를 넘어갑니다. 더 작은 이미지를 선택해주세요.'
	}
	def clean_bgimage(self):
		size_image = self.cleaned_data['bgimage'].size
		if size_image > 2*1024*1024: # 2MiB
			raise ValidationError(self.error_messages['image_exceed'])
		return self.cleaned_data['bgimage']

	def clean_tag_string(self):
		tags = self.cleaned_data['tag_string'].split(',')
		tags[:] = [tag.strip() for tag in tags]
		for tag in tags:
			if not tag.isalpha():
				print 'tag'
				raise ValidationError(self.error_messages['tag_invalid'])
			try:
				tag.decode()
			except UnicodeEncodeError:
				raise ValidationError(self.error_messages['tag_invalid'])
		return self.cleaned_data['tag_string']



		