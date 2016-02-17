from django.shortcuts import render, get_object_or_404
from posting.models import Post, Member, Comment
from django.http import HttpResponseForbidden, JsonResponse

# Create your views here.
def like(request):
	if request.method == 'POST':
		result = {'error': None}
		post_pk = request.POST['post_pk']
		try:
			post = Post.objects.get(pk=post_pk)
		except Post.DoesNotExist:
			result['error']='PostNotFound'
			return JsonResponse(result)

		try:
			member = Member.objects.get(user=request.user)
		except Member.DoesNotExist:
			result['error']='UserNotFound'
			return JsonResponse(result)

		# - add likes if user doesn't exist in the list. Otherwise, remove the member
		if post.liked_member.filter(user=member.user):
			post.liked_member.remove(member)
			result['on'] = False
		else:
			post.liked_member.add(member)
			result['on'] = True

		post.save()
		result['like_num'] = len(post.liked_member.all())
		return JsonResponse(result)

def scrap(request):
	if request.method == 'POST':
		result = {'error': None}
		post_pk = request.POST['post_pk']
		try:
			post = Post.objects.get(pk=post_pk)
		except Post.DoesNotExist:
			result['error']='PostNotFound'
			return JsonResponse(result)

		try:
			member = Member.objects.get(user=request.user)
		except Member.DoesNotExist:
			result['error']='UserNotFound'
			return JsonResponse(result)

		if post.scraped_member.filter(user=member.user):
			post.scraped_member.remove(member)
			result['on'] = False
		else:
			post.scraped_member.add(member)
			result['on'] = True
	
		post.save()
		result['scrap_num'] = len(post.scraped_member.all())
		return JsonResponse(result)

def comment(request, pk):
	if request.method == 'POST':
		result = {'error': None}
		post_pk = pk
		body = request.POST['body']

		if len(body)==0:
			result['error']='BodyEmpty'
			return JsonResponse(result)

		try:
			post = Post.objects.get(pk=post_pk)
		except Post.DoesNotExist:
			result['error']='PostNotFound'
			return JsonResponse(result)

		try:
			member = Member.objects.get(user=request.user)
		except Member.DoesNotExist:
			result['error']='UserNotFound'
			return JsonResponse(result)

		comment = Comment()
		comment.author = member
		comment.post = post
		comment.text = body
		comment.save()

		return JsonResponse(result)

	if request.method == 'GET':
		result = {'error': None, 'comment': []}
		post_pk = pk

		try:
			post = Post.objects.get(pk=post_pk)
		except Post.DoesNotExist:
			result['error']='PostNotFound'
			return JsonResponse(result)

		for comment in post.comment.all()[::-1]:
			ele = {'author': comment.author.name, 'text': comment.text, 'image': comment.author.picture.url}
			result['comment'].append(ele)

		return JsonResponse(result)
