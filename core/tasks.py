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
from core.models import Instruments,Historical1D,Historical1M

@shared_task
def add_tick(token,time,ltp,volume):

	# myData = [[time,token,ltp,volume]] 
	print("In tick task")
	#Test latency between adding to queue and processing it
	tz = pytz.timezone('Asia/Calcutta')

	qtime = datetime.now(tz=tz)
	# diff = qtime - time
	print(qtime)
	print(time)
	#------------------------------------------------------

	redis_server = RedisWrapper().redis_connect(server_key='main_server')

	redis_server.set(str(token)+"/ltp",ltp)


@shared_task
def write_tick_to_file(token,time,ltp,volume):
	myData = [[time,token,ltp,volume]] 
	ticksdir = os.path.join(os.getcwd(), 'ticks')
	file = open(os.path.join(ticksdir, str(token)+'.csv'), 'a')

	with file:  
		writer = csv.writer(file)
		writer.writerows(myData)

@shared_task
def add_1M_data(token,minute_data):
	stockname = Instruments.objects.get_data(token).name
	records = []
	for minute in minute_data:
		time_ = minute['date']
		records.append(Historical1M(name=stockname,token=token,time=time_,open=minute['open'],high=minute['high'],low=minute['low'],close=minute['close'],volume=minute['volume']))
	
	Historical1M.objects.bulk_create(records,batch_size=1000)

@shared_task
def add_1D_data(token,daily_data):
	stockname = Instruments.objects.get_data(token).name
	print(stockname)
	records = []
	for day in daily_data:
		time_ = day['date']
		records.append(Historical1D(name=stockname,token=token,time=time_,open=day['open'],high=day['high'],low=day['low'],close=day['close'],volume=day['volume']))
	
	Historical1D.objects.bulk_create(records,batch_size=1000)