from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User 
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from login.forms import LoginForm, MemberForm
from django.http import JsonResponse
from posting.models import Member
from ipware.ip import get_ip
import logging
logger = logging.getLogger('login')

#---Template views




class LoginFormView(FormView):
	form_class = LoginForm
	template_name = 'login/login.html'

	#Ajax login
	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		is_remember = request.POST.get('remember_me', None)
		print is_remember

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
			logger.warning('a login fail - '+username+'/'+get_ip(request))
			return JsonResponse(response)

class UserSetupView(FormView):
	form_class = MemberForm
	template_name = 'login/setup.html'

	def form_valid(self, form):
		member = Member()
		member.name = form.cleaned_data['name']
		member.salutation = form.cleaned_data['salutation']
		member.picture = form.cleaned_data['picture']
		member.save()

		return HttpResponseRedirect(reverse('home:home'))



#---Function views
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('login:login'))

def check_username(request):
	username = request.POST['username']
	result = {'success': False, 'message': ''}

	# check for multiple value
	if User.objects.filter(username=username):
		result['message'] = 'You cannot use this username'
		return JsonResponse(result)
	elif not format_username(username):
		result['message'] = 'Username should be 4~30 characters. alphanumeric only.'
		return JsonResponse(result)
	else:
		result['success']=True
		result['message'] = ''
		return JsonResponse(result)

def format_username(username):
	if len(username) < 4:
		return False
	elif len(username) >= 30:
		return False
	elif not username.isalnum():
		return False
	else:
		return True

def signup(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		official = request.POST.get('official', False)
		povisid = request.POST['povisid']

		user = User.objects.create_user(username)
		user.set_password(password)
		if official:
			user.email = povisid +'@postech.ac.kr'

		user.save()
		authuser = authenticate(username=username, password=password)
		login(request, authuser)
		logger.info('A user signed up! --- '+username+'/'+get_ip(request))
	return HttpResponseRedirect(reverse('login:setup'))

