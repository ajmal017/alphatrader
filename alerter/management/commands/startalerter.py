from django.core.management.base import BaseCommand, CommandError
from .models import Options
from alerter.collector import Collector
from alerter.util import get_access_token
import time
import logging
from kiteconnect import KiteConnect
import json
import traceback

class Command(BaseCommand):
	help = 'Starts the Alerter'


	def handle(self, *args, **options):		
	
		try:

			kite_api_key = "8sawti1bam50o624"
			user_id = "ZZ8276"
			kite_api_secret = "oum6c2bnqtnhz1os5qmz6saaz7yxxts1"

			stocklist = json.loads(Options.objects.get_option("futuresstocklist"))
			commoditylist = [53556743,53480199,53470983,53709575,53645831,53645319]

			kite = KiteConnect(api_key=kite_api_key)
			access_token = get_access_token(kite)
			kite.set_access_token(access_token)	

			Collector(user_id,kite_api_key,access_token,commoditylist)
			while True:
				pass


		except Exception as e:
			print(e)
			traceback.print_exc()
			data={}
			data['message'] = str(e)
			event = "Error"
			# send_push("Backtest","Failed")