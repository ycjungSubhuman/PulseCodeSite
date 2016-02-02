from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeView(TemplateView):
	template_name = 'home/home.html'

class AcademyView(TemplateView):
	template_name = 'home/academy.html'

class JournalView(TemplateView):
    template_name = 'home/journal.html'

class TuneView(TemplateView):
	template_name = 'home/tune.html'

class TutorialView(TemplateView):
    template_name = 'home/tutorial.html'
