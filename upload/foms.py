from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button, Div, Field, FieldSet, Submit

class UploadForm(forms.ModelForm):
	class Meta:
		model = 