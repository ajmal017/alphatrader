"""alpha3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from accounts import views as acc_views
from dashboard.views import ChannelView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="home.html")),
    url(r'^login/$', acc_views.login),
    url(r'^register/$', acc_views.register),    
    url(r'^logout/$', acc_views._logout),
    url(r'^accounts/auth/$', acc_views.auth_view),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^trade/', include('trader.urls')),

    url(r'^channels/$',ChannelView.as_view()),    
    url(r'^channels/(?P<chname>[\w-]+)/$',ChannelView.as_view()),

    url(r'^login/invalid/$', acc_views.invalid),
    url(r'^admin/', admin.site.urls),
]
