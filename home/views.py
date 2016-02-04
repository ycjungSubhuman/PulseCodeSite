from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from posting.models import Post, Member

# Create your views here.
class HomeView(TemplateView):
	template_name = 'home/home.html'

	def post(self, request):
		isscroll = request.POST['isscroll']
		startfrom = request.POST['startfrom']
		linetype = request.POST['type']

		if isscroll:
			# load 4 more form database
			if linetype == 'new':
				objects = Post.objects
			elif linetype == 'liked':
				try:
					user = Member.get(user=request.user)
					model = user.liked_post
				except Member.DoesNotExist:
					model = None
			elif linetype == 'scraped':
				try:
					user = Member.get(user=request.user)
					model = user.scraped_post
				except Member.DoesNotExist:
					model = None


class AcademyView(TemplateView):
	template_name = 'home/academy.html'

class JournalView(TemplateView):
    template_name = 'home/journal.html'

class TuneView(TemplateView):
	template_name = 'home/tune.html'

class TutorialView(TemplateView):
    template_name = 'home/tutorial.html'
