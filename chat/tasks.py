# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import pytz
from alerter.includes.processor import AlertProcessor
from dateutil import tz
from datetime import datetime
import celery
from alerter.includes.rediswrapper import RedisWrapper
import os
import csv
import logging
from chat.models import Message,AlphaChannel

@shared_task
def add_message(message,userid,channelid,msgtype,msgtime):

	# myData = [[time,token,ltp,volume]] 
	print("In message task")
	#Test latency between adding to queue and processing it
	tz = pytz.timezone('Asia/Calcutta')

	qtime = datetime.now(tz=tz)
	# diff = qtime - time
	print(qtime)
	# print(time)
	#------------------------------------------------------
	print(channelid)

	redis_server = RedisWrapper().redis_connect(server_key='main_server')
	redis_server.set("channels/"+str(channelid)+"/messages",message)

	#Append message to the channels last 10 datastructure
	#Add to database
	#TODO:: Find why this area fails
	channel = AlphaChannel.objects.get(name=channelid)
	Message.objects.create(text = message,user_id = userid,channel = channel,type = msgtype, posted_at = msgtime)