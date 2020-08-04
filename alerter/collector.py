import threading
import time
from kiteconnect import KiteTicker
from nsetools import Nse
from datetime import datetime
import pytz
import os
import csv
import json
import logging
import urllib
from trader.models import Instruments
from core.models import Options
from django.core.exceptions import ObjectDoesNotExist
from alerter.tasks import add_tick
import redis

""" 

Documentation 

On connect method is where the stocks are subscribed to
The subscribed tokens are got from the saved list of useful stocks

On tick method is call back from the websocket
The ticks are collected and stored as csv files in ticks/ directory
The files are named as the token.csv

"""


class Collector(object):

	def __init__(self,user_id,api_key,access_token,stocklist,interval=1):

		logging.basicConfig(filename='alphapython.log',level=logging.DEBUG)
		self.interval = interval
		self.api_key = api_key
		self.access_token = access_token
		self.user_id = user_id
		self.stocklist = stocklist
		self.postback = False
		self.redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True                            # Daemonize thread
		thread.start()                                  # Start the execution

	def run(self):
		""" Mthod that runs forever """
		self.start_collecting()


	def start_collecting(self):
		# Assign the callbacks.

		ticksdir = os.path.join(os.getcwd(), 'ticks')
		if not os.path.exists(ticksdir):
			os.makedirs(ticksdir)

		kwsone = KiteTicker(self.api_key, self.access_token)

		kwsone.on_ticks = self.on_tick()

		kwsone.on_connect = self.on_connect(self.stocklist)

		if self.postback:	
			kwsone.on_order_update = self.on_order_update() 
		kwsone.connect(threaded=True)


	def split_list(self,a_list):
		return a_list[::2], a_list[1::2]

	# Callback for successful connection.
	def on_connect(self,stocklist):
		# Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
		def connect(ws,response):
			ws.subscribe(stocklist)
			ws.set_mode(ws.MODE_FULL,stocklist)

		return connect

	def write_tick_to_csv(self,name,time,tick,volume):
		myData = [[time,name,tick,volume]]  
		ticksdir = os.path.join(os.getcwd(), 'ticks')

		myFile = open(os.path.join(ticksdir, str(name)+'.csv'), 'a')  
		with myFile:  
			writer = csv.writer(myFile)
			writer.writerows(myData)

	# Callback for tick reception.
	def on_tick(self):

		def tick(ws,ticks):
			for tick in ticks:
				token=tick['instrument_token']
				lastPrice=tick['last_price']
				volume = tick['volume']
				tz = pytz.timezone('Asia/Calcutta')
				time = datetime.now(tz=tz)
				add_tick.apply_async((token,time,lastPrice,volume,), queue='ticks')
				# add_tick.delay()				
		return tick
