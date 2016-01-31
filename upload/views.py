from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from upload.forms import TrackUploadForm, JournalForm
from posting.models import Track, Member, Tag, Journal
from django.core.exceptions import PermissionDenied

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

		# - author
		try: 
			journal.author = Member.objects.get(user=self.request.user)
		except Member.DoesNotExist: # user not defined in server
			raise PermissionDenied
			
		# - body
		journal.body = form.cleaned_data['body']

		# - bgimage
		journal.bgimage = self.request.FILES['bgimage']

		journal.save()

		tag_string = form.cleaned_data['tag_string']
		addFromRawTagstring(journal, tag_string)

		return super(JournalWriteView, self).form_valid(form)




