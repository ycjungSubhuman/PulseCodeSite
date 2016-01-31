"""pulsecode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from login.views import user_logout
from upload.views import JournalWriteView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^login/', include('login.urls', namespace='login')),
	url(r'^upload/', include('upload.urls', namespace='upload')),
    url(r'^logout/', user_logout, name='logout'),
    url(r'^write/', JournalWriteView.as_view(), name='write'),
    url(r'^markdown/', include('django_markdown.urls')),
#url(r'^register/', include('register.urls', namespace='register')),
]

