from django.conf.urls import include, url
from home import views


urlpatterns = [
	url(r'^$', views.HomeView.as_view(), name='home'),
	url(r'^academy/$', views.AcademyView.as_view(), name='academy'),
	url(r'^tune/$', views.TuneView.as_view(), name='tune'),
	url(r'^journal/$', views.JournalView.as_view(), name='journal'),
]
