# Send to single device.
from pyfcm import FCMNotification
from core.models import Options
import json



class FCMWrapper(object):

	API_KEY = "AAAAR98L-8U:APA91bFqUMe6xo-rbpM7oUW1FJwgu8nJOidPpBfP_ESNbOdXjhjlvDNxq2FkO-NNdXUZ2ZumA4nWa-ksCGRlUmW-FJEn_0GeQi1qAX9VNaUaBRi9AV_UW43d2QDhSaWxavzqq3CZbtXX"
	
	def __init__(self):
		self.push_service = FCMNotification(api_key=self.API_KEY)
		self.registration_ids = json.loads(Options.objects.get_option("gcmregistered"))



	def send_push(self,reg_ids):
		message_title = "Alpha Trader Update"
		message_body = "Your notification just happened!"		
		result = self.push_service.notify_multiple_devices(registration_ids=self.registration_ids, message_title=message_title, message_body=message_body)
		print(result)		

	def push_recommendation(self,reg_ids,broker,stock,order_type,exchange):
		message_title = broker
		message_body = {
			"stock" : stock,
			"exchange" : exchange,
			"order_type" : order_type
		}	
		msg = json.dumps(message_body)	
		result = self.push_service.notify_multiple_devices(registration_ids=reg_ids, message_title=message_title, message_body=msg)

	def push_alert(self,reg_ids,stock,**kwargs):
		message_title = broker
		message_body = {
			"stock" : stock,
		}	
		if kwargs is not None:
			for key, value in kwargs.iteritems():
				message_body.update(key=value)
		msg = json.dumps(message_body)	
		result = self.push_service.notify_multiple_devices(registration_ids=reg_ids, message_title=message_title, message_body=msg)

