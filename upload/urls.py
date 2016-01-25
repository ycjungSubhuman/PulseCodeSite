from django.conf.urls import url
from upload import views

urlpatterns = [
	url(r'^$', views.UploadFormView.as_view(), name='upload'),
	url(r'^submit/$', views.submit_track, name='submit'),
]
