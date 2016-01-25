from django.shortcuts import render
from django.views.generic.base import TemplateView

#--Template views
class UploadFormView(TemplateView):
	template_name = 'upload/upload.html'

	def get_context_data(self, **kwargs):
		context = super(UploadFormView, self).get_context_data(**kwargs)


#--function views
def submit_track(request):
	file = request.POST['']


