from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from upload.forms import TrackUploadForm
from posting.models import Track

#--Template views
class TrackUploadFormView(FormView):
	template_name = 'upload/upload.html'
	form_class = TrackUploadForm

	def form_valid(self, form):
		# - fill in non-complete fields
		#	author, tag, audio, playtime, datetime(auto)

		#author
		return super(TrackUploadFormView, self).form_valid(form)

		#tag
	def post(self, request):



		#redirect to success page with super()
		return super(TrackUploadFormView, self).post(request)





