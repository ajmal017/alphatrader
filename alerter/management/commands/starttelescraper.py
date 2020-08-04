from django.core.management.base import BaseCommand, CommandError
import time
import logging
from alerter.includes.scrapers.telegram import TelegramScraper
import json
import traceback

class Command(BaseCommand):
	help = 'Starts the Scraper'


	def handle(self, *args, **options):		
	
		try:
			scraper = TelegramScraper()

			while True:
				pass


		except Exception as e:
			print(e)
			traceback.print_exc()
			data={}
			data['message'] = str(e)
			event = "Error"
			# send_push("Backtest","Failed")