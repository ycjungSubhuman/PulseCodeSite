from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button, Div, Field, Submit
from posting.models import Track

class TrackUploadForm(forms.ModelForm):
	class Meta:
		model = Track
		fields = [
			'download',
			'title',
			'image',
			'description',
		]
		
	tag_string = forms.CharField(max_length=50,
		help_text='Split each tag with ,(comma), &>< is not allowed')

	def __init__(self, *args, **kwargs):
		super(TrackUploadForm, self).__init__(*args, **kwargs)

		#form helper
		self.helper = FormHelper()

		self.helper.form_id = 'track_upload_form'
		self.helper.attrs = {'role': 'form'}
		self.helper.layout = Layout(
			Div( #this div is for track upload form
				Field('download', id='upload_form'),
				Button('upload', "Upload", id='upload_button', css_class='btn btn-default'),
			),
			Div( # this div is for information form
				Field('image', id='image_form'),
				Field('title', id='title_form', css_class='form-control'),
				Field('description', id='description_form', css_class='form-control'),
				Field('tag_string', id='tag_form'),
				Submit('submit', "Save", id='submit'),
				css_class='hidden'
			),
		)
		self.fields['description'].widget = forms.Textarea()
		self.fields['tag_string'].label = 'Tags'

	def is_valid(self):
		valid = super(TrackUploadForm, self).is_valid()

		# - super() test
		if not valid:
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
