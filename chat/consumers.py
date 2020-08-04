# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import re
import datetime
import time 
from chat.tasks import add_message
from .settings import MSG_TYPE_MESSAGE

class AsyncChatConsumer(AsyncWebsocketConsumer):

	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name
		self.user = self.scope["user"]
		if self.user:
			# Join room group
			await self.channel_layer.group_add(
				self.room_group_name,
				self.channel_name
			)

			await self.accept()
		

	async def disconnect(self, close_code):
		# Leave room group
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		channel = text_data_json['channel']

		time.ctime()
		current_time = datetime.datetime.now()
		message_time = time.strftime('%I:%M %p')

		urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', message)
		for url in urls:
			message = message.replace(url, "<a href="+url+">"+url+"</a>")
		
		add_message.apply_async((message,self.user.id,channel,MSG_TYPE_MESSAGE,current_time), queue='celery')

		# username = text_data_json['username']
		if message:		
			# Send message to room group
			await self.channel_layer.group_send(
				self.room_group_name,
				{
					'type': 'chat_message',
					'message': message,
					'channel': channel,
					'time':message_time,
					'username': self.user.username,
				}
			)

	# Receive message from room group
	async def chat_message(self, event):
		message = event['message']
		channel = event['channel']
		message_time = event['time']
		username = event['username']
		# Send message to WebSocket
		await self.send(text_data=json.dumps({
			'message': message,
			'msg_type':1,
			'channel_id': channel,
			'username': username,
			'posted_at':message_time,
			'icon_link':'http://www.alphatrader.in/static/dashboard/images/avatar1.png'
		}))