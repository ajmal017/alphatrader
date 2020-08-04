from telethon import TelegramClient
from telethon import utils
import json
import re
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon import sync
# import asyncio

class TelegramScraper():
	shared_state = {}
	API_ID = 198795
	API_HASH = '7bd2c69ddd992d15cc3bc0a11dfb2a0c'

	def __init__(self):
		self.__dict__ = self.shared_state

		self.initiate_telclient()
		#Get data from one main channel
		data = self.get_data("https://t.me/breakoutinshares")
		#Scrape all data in the channel and check if there are invite links to other channels
		#If yes, join the channel, save the channel name in db and go to next message 
			# Public channels:
			# 	[lonami = client.get_entity('t.me/lonami')]
			# 	self.telclient(JoinChannelRequest(channel))

			# Private Channels:
			# 	https://t.me/joinchat/AAAAAFFszQPyPEZ7wgxLtd
			# 	from telethon.tl.functions.messages import ImportChatInviteRequest
			# 	self.telclient(ImportChatInviteRequest('AAAAAFFszQPyPEZ7wgxLtd'))

		#If the name of the channel was already saved, move on to next message 
		self.parse_scraped_data(data)
		#After all messages are done, go to the next saved channel in the table after the first one.
		#Keep repeating this until all saved channels are done.
		# loop = asyncio.get_event_loop()
		# loop.run_until_complete(coro())


	def initiate_telclient(self):
		self.telclient = TelegramClient('trader', self.API_ID, self.API_HASH)
		self.telclient.start()
		self.last_read_message = 0

	def get_data(self,telid):
		entity = self.telclient.get_entity(telid)

		return self.telclient(GetHistoryRequest(
			entity,
			limit=10000,
			offset_date=None,
			offset_id=0,
			max_id=0,
			min_id=self.last_read_message,
			add_offset=0,
			hash=0,
		))	

	def parse_scraped_data(self,msg_history):
		i=0	
		for message in msg_history.messages:
			print(message)
			i = i + 1
		print(i)


	def join_channel(self,channel=None,telehash=None):
		if channel:
			self.telclient(JoinChannelRequest(channel))			
		else:
			self.telclient(ImportChatInviteRequest(telehash))


	def parse_and_save_channels(self,message):
		content = message.message
		# new =  re.sub(r'[^a-zA-Z& \n]','',message)
		# caps = re.findall('([A-Z&]+(?:(?!\s?[A-Z][a-z])\s?[A-Z])+)', new)

		# if "t.me" in new:
		print(content)