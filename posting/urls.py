from django.conf.urls import url
from posting.views import like, scrap, comment

urlpatterns = [
	url(r'^like/$', like, name='like'),
	url(r'^scrap/$', scrap, name='scrap'),
	url(r'^comment/(?P<pk>[0-9]+)/$', comment, name='comment'),
]
