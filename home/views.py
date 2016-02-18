from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from posting.models import Post, Member

# Create your views here.
class HomeView(TemplateView):
	template_name = 'home/home.html'

	def post(self, request):
		isscroll = request.POST['isscroll']
		
		if isscroll:
			startfrom = int(request.POST['startfrom'])
			linetype = request.POST['type']
			entitynum = 8
			# load 4 more form database
			if linetype == 'new':
				objects = Post.objects
			elif linetype == 'liked':
				try:
					user = Member.objects.get(user=request.user)
					objects = user.liked_post
				except Member.DoesNotExist:
					objects = None
			elif linetype == 'scraped':
				try:
					user = Member.objects.get(user=request.user)
					objects = user.scraped_post
				except Member.DoesNotExist:
					objects = None

			# get 8 more from objects
			if objects:
				new8 = objects.all()[::-1][startfrom:startfrom+entitynum] # newest 8
			else:
				new8 = None
				
			# make json
			result = {
				'entitynum': len(new8),
				'loaded': True,
				'entity':[],
			}
			if new8:
				for idx, obj in enumerate(new8):
					objtype = 'track' if hasattr(obj, 'track') else 'journal'
					taglist = []
					liked_user = []
					scraped_user = []
					for tag in obj.tag.all()[:3]:
						taglist.append(tag.name)

					for liked in obj.liked_member.all():
						liked_user.append(liked.user)

					liked_on = request.user in liked_user

					for scraped in obj.scraped_member.all():
						scraped_user.append(scraped.user)

					scraped_on = request.user in scraped_user

					# common factors
					result['entity'].append({})

					result['entity'][idx] = {
						'objtype': objtype,
						'title': obj.title,
						'author': obj.author.name,
						'tag': taglist,
						'liked_num': len(liked_user),
						'liked_on': liked_on,
						'scraped_num': len(scraped_user),
						'scraped_on': scraped_on,
						'comment_num': len(obj.comment.all()),
						'bgimage_url': obj.track.image.url if objtype=='track' else obj.journal.bgimage.url,
						'pk': obj.pk,
					}
					# track specific
					if objtype is 'track':
						entity = result['entity'][idx]
						entity['track'] = {}
						entity = entity['track']
						track = obj.track

						entity['audio_url'] = track.audio_file.url
						entity['bgimage_url'] = track.image.url
						entity['description'] = track.description
						datetime = track.datetime
						entity['datetime'] = {
							'year': datetime.year,
							'month': datetime.month,
							'day': datetime.day,
							'hour': datetime.hour,
							'minute': datetime.minute,
							'second': datetime.second,
						}
					#journal specific
					else :
						entity = result['entity'][idx]
						entity['journal'] = {}
						entity = entity['journal']
						journal = obj.journal


			else: # the new list is empty
				result['loaded'] = False

		else: # not a scroll request, other requests like sidebar
			pass


		return JsonResponse(result)


class AcademyView(TemplateView):
	template_name = 'home/academy.html'

class JournalView(TemplateView):
    template_name = 'home/journal.html'

class TuneView(TemplateView):
	template_name = 'home/tune.html'

class TutorialView(TemplateView):
    template_name = 'home/tutorial.html'
