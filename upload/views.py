from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from upload.forms import TrackUploadForm, JournalForm
from posting.models import Track, Member, Tag, Journal
from upload.models import Image
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpResponseForbidden

def addFromRawTagstring(modelinst, tagstring):
	tags = tagstring.split(',')
	tags[:] = [word.strip().capitalize() for word in tags]
	for word in tags:
		try:
			tag = Tag.objects.get(name=word)
		except Tag.DoesNotExist:
			tag = Tag()
			tag.name = word
			tag.save()

		modelinst.tag.add(tag)


#--Template views
class TrackUploadFormView(FormView):
	template_name = 'upload/upload.html'
	form_class = TrackUploadForm
	success_url = '/home/'

	def form_valid(self, form):
		""" fill in the fields

			title, author, audio_file
			image, description, tag
		"""
		track = Track()

		# - title
		track.title = form.cleaned_data['title'] 

		# - author
		try: 
			track.author = Member.objects.get(user=self.request.user)
		except Member.DoesNotExist: # user not defined in server
			raise PermissionDenied

		# - audio_file
		track.audio_file = self.request.FILES['audio_file']

		# - image
		track.image = self.request.FILES['image']

		# - description
		track.description = form.cleaned_data['description']

		track.save()

		# - tag parsing and adding
		tag_string = form.cleaned_data['tag_string']
		addFromRawTagstring(track, tag_string)

		return super(TrackUploadFormView, self).form_valid(form)

class JournalWriteView(FormView):
	template_name = 'upload/write.html'
	form_class = JournalForm

	def form_valid(self, form):
		"""fill in the fields

			title, author, body, bgimage, tag
		"""
		journal = Journal()

		# - title
		journal.title = form.cleaned_data['title']

		try:
			# - author
			journal.author = Member.objects.get(user=self.request.user)
		except:
			return HttpResponseForbidden('<h1>GEEEEEEEEET<br />DUNKEDONNNNNNNNNNN(403)<br /></h1><p>forbidden. please login.')
			
		# - body
		journal.body = form.cleaned_data['body']
		print journal.body

		# - bgimage
		journal.bgimage = self.request.FILES['bgimage']

		journal.save()

		tag_string = form.cleaned_data['tag_string']
		addFromRawTagstring(journal, tag_string)

		return HttpResponseRedirect(reverse('home:home'));


class ImageUpload(View):
	def post(self, request):
		success = False
		try:
			image = request.FILES['image']
			upload = Image()
			upload.image = image
			upload.save()
			success = True
		except:
			success = False

		result = {'success': success, 'url': upload.image.url,}

		return JsonResponse(result)


