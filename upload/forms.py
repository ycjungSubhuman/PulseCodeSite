# -*- coding: utf-8 -*-

from django import forms
from django.forms.utils import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button, Div, Field, Submit
from posting.models import Track, Journal

class TrackUploadForm(forms.ModelForm):
	class Meta:
		model = Track
		fields = [
			'audio_file',
			'title',
			'image',
			'description',
		]
	audio_file = forms.FileField()
	tag_string = forms.CharField(max_length=50,
		help_text='Split each tag with ,(comma), only Alphabets allowed')

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

	def is_valid(self):
		valid = super(TrackUploadForm, self).is_valid()

		# - super() test
		if not valid:
			self._errors['super_fail'] = 'super validation false'
			return False

		# - the size of track is checked in ajax POST handler
		# 	Pass

		# - check the size of Image
		size_image = self.cleaned_data['image'].size
		if size_image > 2*1024*1024: # 2MiB
			self._errors['image_exceed'] = 'Image size exceeds 2MiB'
			return False

		# - tag format test --- all should be alphabet
		tags = self.cleaned_data['tag_string'].split(',')
		tags[:] = [tag.strip() for tag in tags]
		for tag in tags:
			if not tag.isalpha():
				return False

		# - test all-passed
		return True

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



		