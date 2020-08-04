from core.models import Options
from alerter.collector import Collector
from alerter.kiteutil import get_access_token

import time
import logging
import json

def init():
	kite_api_key = "8sawti1bam50o624"
	user_id = "ZZ8276"
	kite_api_secret = "oum6c2bnqtnhz1os5qmz6saaz7yxxts1"

	request_token = Options.objects.get_option("request_token")
	stocklist = json.loads(Options.objects.get_option("futuresstocklist"))

	kite = KiteConnect(api_key=kite_api_key)
	access_token = get_access_token(kite)

	Collector(user_id,kite_api_key,access_token,stocklist)

