from django.core.management.base import BaseCommand, CommandError
import time
import logging
from datetime import datetime,timedelta
import json
import traceback
import core.utils as utils
from core.includes.kite import _Kite_
from core.models import Options
from core.tasks import add_1D_data

#Purpose: To be used in a cron command, which will update this data at the beginning of each week.

class Command(BaseCommand):
	help = 'Updates instrument data and margins'


	def handle(self, *args, **options):		
	
		try:
			self._kite_ = _Kite_()
			self.save_1D_futures_data()


		except Exception as e:
			print(e)
			traceback.print_exc()
			data={}
			data['message'] = str(e)
			event = "Error"
			# send_push("Backtest","Failed")

	def save_1D_futures_data(self):

		all_futures = json.loads(Options.objects.get_option("futuresstocklist"))

		current_date = datetime.now()

		from_date = datetime.strptime("2017-01-01 09:00:00","%Y-%m-%d %H:%M:%S")

		# to_date = from_date + timedelta(days=10)
		# to_date = datetime.strptime("2018-03-02 09:00:00","%Y-%m-%d %H:%M:%S")
		to_date = current_date

		# to_date = "2018-01-15 15:30:00"
		# from_date = "2018-02-02 09:30:00"
		#Run this loop until the to_date becomes the current date
		# while to_date <= current_date:
		print("From"+str(from_date))
		print("To"+str(to_date))

		for stock in all_futures:
			kite_success = False
			while not kite_success:
				try:
					daily_data = self._kite_.kite.historical_data(stock, from_date, to_date, 'day')
					kite_success = True
				except Exception as e:
					time.sleep(50)
					kite_success = False
					logging.info("Retry after failed")

			print(stock)
			add_1D_data.delay(stock,daily_data)
			logging.info("Task added")
			time.sleep(1)

			# #Change dates for next loop
			# from_date = from_date + timedelta(days=30)
			# to_date = to_date + timedelta(days=30)
			# if from_date < current_date:
			# 	if to_date >= current_date:
			# 		to_date = current_date
		logging.info("Task completed!")
