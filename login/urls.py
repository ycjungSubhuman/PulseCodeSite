from django.conf.urls import url
from login import views

urlpatterns = [
	url(r'^$', views.LoginFormView.as_view(), name='login'),
	url(r'^$', views.user_logout, name='logout'),
]

