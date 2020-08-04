# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import pytz
from alerter.includes.processor import AlertProcessor
from dateutil import tz
from datetime import datetime
import celery
from alerter.includes.rediswrapper import RedisWrapper
from alerter.includes.fcmwrapper import FCMWrapper
import os
import csv
import logging

@shared_task
def alert_process(token,time,ltp,volume):
	AlertProcessor(token,ltp)	

@shared_task
def send_alert(token,type,price_list):
	redis_server = RedisWrapper().redis_connect(server_key='main_server')	
	stock_data = redis_server.get(token)
	for price in price_list:
		logging.info("In Price:"+str(price))
		#Get all users subscribed to the price of a token
		keyname = str(token)+"/"+str(price)
		print(keyname)
		user_list = redis_server.lrange(keyname,0,-1)
		logging.info("In Users:"+str(user_list))

		for user in user_list:

			# send_push.apply_async((user,token,price), queue='celery')
			logging.info("Sending Alert to " + str(float(user)) + "for price "+str(price))

@shared_task
def send_push(user,stock,price):
	#Get registered id
	#Keep broker as alerter
	reg_id = redis_server.get(user+"/device")
	FCMWrapper().push_alert(reg_id,stock,price=price)