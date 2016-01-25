from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from login.forms import LoginForm 
from django.http import JsonResponse

#---Template views




class LoginFormView(FormView):
	form_class = LoginForm
	template_name = 'login/login.html'

	#Ajax login
	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		is_remember = request.POST.get('remember_me', None)

		#json response
		response = {
			'success': False,
			'message': '',
		}

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				response['success'] = True

				#if not remember me
				if not is_remember:
					request.session.set_expiry(0)

				#redirect to home
				return JsonResponse(response)
			else:
			#login fail- - expired user
				response['message']='Your account was expired'
				return JsonResponse(response)
		else:
		#login fail - not matched
			response['message']='Username or Password is not matched'
			return JsonResponse(response)

#---Function views
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('login:login'));


