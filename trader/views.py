from django.shortcuts import render
from django.views.generic import TemplateView
from core.models import Options
import datetime
import json
import time
from kiteconnect import KiteConnect
from core.constants import KITE_API_KEY,KITE_API_SECRET


# Create your views here.
class TraderLoginView(TemplateView):
	
	def get(self, request, **kwargs):
		status = self.request.GET.get('status',None)
		force_refresh = self.request.GET.get('force_refresh',None)

		user_id = "ZZ8276"

		if status == "success":

			self.request_token = self.request.GET.get('request_token',None)
			Options.objects.save_option("request_token",self.request_token)
			current_time = datetime.datetime.now().time()
			access_refresh_time = datetime.time(13, 00)

			if force_refresh:
				self.remove_access_token()

			if current_time < access_refresh_time :
				self.remove_access_token()

			self.kite = KiteConnect(api_key=KITE_API_KEY)
			self.get_new_access_token()

			# collector = Collector(kite_api_key,request_token,user_id,commoditylist)
			# analyst = Analyst(commoditylist,0)# 0 for commodity, 1 for stocks
			# kitelalpha = KiteAlpha(kite_api_key,request_token,kite_api_secret)
			# collector = Collector(kite_api_key,request_token,user_id,stocklist)
			# analyst = Analyst(stocklist,1,kitelalpha)# 0 for commodity, 1 for stocks

			return render(request, 'login_success.html', {'token': self.request_token})

		else:

			loginlink = "https://kite.trade/connect/login?v=3&api_key={api_key}".format(api_key=KITE_API_KEY)
			return render(request, 'login.html', {'loginlink': loginlink,'api_key':KITE_API_KEY})

	def get_request_token(self):
		token = Options.objects.get_option("request_token")
		if not token:
			return None
		else:
			return token

	def get_new_access_token(self):
		data = self.kite.generate_session(self.request_token,KITE_API_SECRET)
		access_token = data["access_token"]
		Options.objects.save_option("access_token",access_token)
		Options.objects.save_option("access_token_last_updated",int(datetime.datetime.now().strftime('%s')))
		self.kite.set_access_token(access_token)

	def remove_access_token(self):
		Options.objects.clear_option("access_token")
		Options.objects.clear_option("access_token_last_updated")