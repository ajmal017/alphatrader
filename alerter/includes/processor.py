import threading
import time
from nsetools import Nse
from datetime import datetime
import pytz
import os
import csv
import json
import logging
from django.core.exceptions import ObjectDoesNotExist
import celery
import redis
from alerter.includes.rediswrapper import RedisWrapper
import numpy as np
# from alerter.tasks import send_alert

""" 

Documentation 

On connect method is where the stocks are subscribed to
The subscribed tokens are got from the saved list of useful stocks

On tick method is call back from the websocket
The ticks are collected and stored as csv files in ticks/ directory
The files are named as the token.csv

"""


class AlertProcessor(object):

	def __init__(self,token,ltp):

		self.token = token
		self.price = ltp
		
		# thread = threading.Thread(target=self.run, args=())
		# thread.daemon = True                            # Daemonize thread
		# thread.start()   
		self.run()

	def run(self):
		""" Mthod that runs forever """
		# Pseudocode
		# 1. select all users who have subscribed to this token from redis_db
		# 2. if a new user subscribes, immediately update the database and redis via queues
		# 3. If there are no users subscribed, end
		# 4. If there are users subscribed , then check if the current price is greater or less the
		# 	gt or lt list
		# 5. If it is, then add a task to send notification to all users with that price. 
		# 6. This happens by selecting all users with that price for that particular stock in redis_db,
		# 	and queueing notifications for each of them, or all at once if possible
		logging.info("Inside AlertProcessor")
		subs_key = str(self.token)+"/subscribers"


		redis_server = RedisWrapper().redis_connect(server_key='main_server')

		subscribers = redis_server.lrange(subs_key, 0, -1 )
		if subscribers:
			gt_key = str(self.token)+"/gt"
			lt_key = str(self.token)+"/lt"

			if not gt_key:
				redis_server.lpush(gt_key,900.10)

			gt_list = redis_server.lrange(gt_key, 0, -1 )
			lt_list = redis_server.lrange(lt_key, 0, -1 )

			logging.info("Inside Subscribers")
			# print(gt_list)
			# print(self.price)
			#TODO: Change string conversion here:
			# It comes up as ["b'889'"]

			gt = [float(x) for x in gt_list if self.price > float(x)] 
			lt = [float(x) for x in lt_list if self.price < float(x)] 
			# print(gt)
			# print(lt)
			# gt = [*filter(lambda x: float(x) >= self.price, gt_list)] 
			# lt = [*filter(lambda x: float(x) <= self.price, lt_list)] 
			gt_true = len(gt) > 0
			lt_true = len(lt) > 0

			if gt_true:
				logging.info("Alert Task Sent")

				# send_alert.delay(1,gt)
				# send_alert.apply_async((1,gt), queue='celery')
				celery.current_app.send_task('alerter.tasks.send_alert', args=[self.token,1,gt])
				logging.info("Alert Task Sent")

			if lt_true:
				# send_alert.apply_async((-1,lt), queue='celery')
				# send_alert.delay(-1,lt)
				celery.current_app.send_task('alerter.tasks.send_alert', args=[self.token,-1,lt])
				logging.info("Alert Task Sent")

		logging.info("Alert Processing Done")
