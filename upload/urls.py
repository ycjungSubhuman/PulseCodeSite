from django.conf.urls import url
from upload import views

urlpatterns = [
	url(r'^$', views.TrackUploadFormView.as_view(), name='upload'),
]
