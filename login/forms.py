from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button, Div, Field, Fieldset, Submit

class LoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'username',
			'password'
		]
	password = forms.CharField(widget=forms.PasswordInput)
	remember_me = forms.BooleanField()

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()

		self.helper.form_id = 'login_form'
		self.helper.attrs = {'role': 'form'}
		self.helper.layout = Layout(
			Field('username', css_class="form-control", id="user_id"),
			Field('password', css_class="form-control", id="user_pass"),
			Field('remember_me', css_class="checkbox", id="rememberme"),
			Submit('submit', "Login", id="submit"),
		)
		self.fields['username'].help_text=None
