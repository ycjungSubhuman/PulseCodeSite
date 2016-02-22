from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button, Div, Field, Fieldset, Submit
from posting.models import Member

class LoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'username',
			'password'
		]
	password = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()

		self.helper.form_id = 'login_form'
		self.helper.attrs = {'role': 'form'}
		self.helper.layout = Layout(
			Field('username', css_class="form-control", id="user_id"),
			Field('password', css_class="form-control", id="user_pass"),
			Submit('submit', "Login", id="submit"),
		)
		self.fields['username'].help_text=None

class MemberForm(forms.ModelForm):
	class Meta:
		model = Member
		fields = [
			'name',
			'salutation',
			'picture',
		]
	error_messages = {
		'image_exceed': 'Image Exceeds 2MiB.'
	}

	def clean_picture(self):
		try:
			size_image = self.cleaned_data['picture'].size
		except:
			return
		print 'wow passed'
		if size_image > 2*1024*1024: # 2MiB
			raise ValidationError(self.error_messages['image_exceed'])
		return self.cleaned_data['picture']

	def __init__(self, *args, **kwargs):
		super(MemberForm, self).__init__(*args, **kwargs)

		self.fields['salutation'].widget = forms.Textarea(attrs={'maxlength':300})
