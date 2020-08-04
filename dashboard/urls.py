from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.DashboardView.as_view()),
	url(r'^profile/$', views.ProfileView.as_view()),
	url(r'^channels/$', views.ChannelView.as_view()),

]