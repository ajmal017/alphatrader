from core.models import Options
import logging
from datetime import datetime,timedelta
from difflib import SequenceMatcher

def get_access_token(kiteconnect):
	access_token = Options.objects.get_option("access_token")
	access_token_last = Options.objects.get_option("access_token_last_updated")

	now = datetime.now()

	if not access_token_last:
		access_token_last = now	
	else:
		access_token_last = datetime.fromtimestamp(int(access_token_last))	

	logging.info("Access token last updated on:"+ str(access_token_last))

	if not access_token:
		logging.info("No Access token... Getting new one")
		access_token = new_access_token(kiteconnect)		
	else:
		access_token_expired =	access_token_last <= now-timedelta(days=1) 
		if access_token_expired:
			logging.info("Access token expired... Getting new one")
			access_token = new_access_token(kiteconnect)	
		else:
			logging.info("Using saved access token")
	return access_token

def new_access_token(kiteconnect):
	request_token = Options.objects.get_option("request_token")
	api_secret = "oum6c2bnqtnhz1os5qmz6saaz7yxxts1"
	# api_secret = Options.objects.get_option("kite_api_secret")
	data = kiteconnect.generate_session(request_token,api_secret)
	access_token = data["access_token"]
	Options.objects.save_option("access_token",access_token)
	Options.objects.save_option("access_token_last_updated",int(datetime.now().strftime('%s')))

def set_subscribers():
	redis_server = RedisWrapper().redis_connect(server_key='main_server')	
	subscribers = redis_server.lrange(subs_key, 0, -1 )
	if not subscribers:
		saved_subs = Options.objects.get_option("access_token_last_updated")

def get_most_similar_stock(stockname):
	redis_server = RedisWrapper().redis_connect(server_key='main_server')	
	allstocks = redis_server.lrange("allstocks", 0, -1 )

	allstockslist = [item[0] for item in allstocks]		
	high = {'stock':None,'ratio':0}
	for stock in allstockslist:
		last_three = stock[-3:]
		if last_three == "-BE" or last_three == "-BL":
			continue;

		# print(stock)

		similarity = float(similar(stock,stockname))
		if similarity > high['ratio']:
			high = {'stock':stock,'ratio':similarity}
			print(high)
	return high['stock']

def similar(a, b):
	return SequenceMatcher(None, a, b).ratio()