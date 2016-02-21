from django.conf.urls import url
from login import views

urlpatterns = [
	url(r'^$', views.LoginFormView.as_view(), name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^username/$', views.check_username, name='username_validation'),
	url(r'^setup/$', views.UserSetupView.as_view(), name='setup'),
	url(r'^signup/$', views.signup, name='signup'),
]

