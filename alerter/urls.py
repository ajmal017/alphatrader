from django.conf.urls import url
from . import api

urlpatterns = [
	url(r'^gcm/register/$', api.GCMHandler.as_view()),	
]