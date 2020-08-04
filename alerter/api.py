# from includes.collector import Collector
# from includes.analyst import Analyst
# from includes.brokers import Brokers

# from includes.kitealpha import KiteAlpha
# from includes.ordermanager import OrderManager

# from includes.postback import Postback
# from includes.chartist import Chartist
from django.shortcuts import render
# from multiprocessing import Process, Manager
# from multiprocessing.managers import BaseManager
# from trader.includes.tools.shared import SharedData
from django.views.generic import TemplateView
from trader.models import Options
import threading
import time
from telethon import TelegramClient
from telethon import utils

import logging
from core.includes.mixins.mixins import JSONResponseMixin,AllowCORSMixin

class GCMHandler(JSONResponseMixin,AllowCORSMixin,TemplateView):

	def render_to_response(self, context):
		response = JSONResponseMixin.render_to_response(self, context)
		return self.add_access_control_headers(response)

	def post(self, request, *args, **kwargs):
		data = request.POST
		regid = data.get('regid',"noid")
		self.register_device(regid)
		   
		return self.render_to_response({'success':'1','remarks':'register_device_done'})			

	def register_device(self,regid):
		json_ids = Options.objects.get_option("gcmregistered")
		if json_ids:
			registeredids = json.loads(json_ids)
		else:
			registeredids = []
		registeredids.append(regid)
		Options.objects.save_option("gcmregistered",json.dumps(registeredids))
