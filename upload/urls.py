from django.conf.urls import url
from upload import views

urlpatterns = [
	url(r'^track/$', views.TrackUploadFormView.as_view(), name='track'),
	url(r'^journal/$', views.JournalWriteView.as_view(), name='journal'),
	url(r'^tutorial/$', views.JournalWriteView.as_view(), name='tutorial'),
]
