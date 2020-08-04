from django.core.management.base import BaseCommand, CommandError
import time
import logging
import json
import traceback
import core.utils as utils
import core.includes.kite as _kite

#Purpose: To be used in a cron command, which will update this data at the beginning of each week.

class Command(BaseCommand):
	help = 'Updates instrument data and margins'


	def handle(self, *args, **options):		
	
		try:

			self.update_useful_futures()


		except Exception as e:
			print(e)
			traceback.print_exc()
			data={}
			data['message'] = str(e)
			event = "Error"
			# send_push("Backtest","Failed")

	def update_instruments(self):
		utils.collect_instruments()
		utils.save_instruments()

	def update_margins(self):
		utils.collect_margins()
		utils.save_margins()

	def update_useful_futures(self):
		utils.update_futures_list()
		utils.save_useful_futures()