from django.core.management.base import BaseCommand, CommandError
import time
import logging
import json
import traceback
import core.utils as utils
from core.models import Historical1D

#Purpose: To clear data completely from historical data tables

class Command(BaseCommand):
	help = 'Use CAUTIOUSLY --> Clears data from a whole table --> Use CAUTIOUSLY'


	def handle(self, *args, **options):		
	
		try:

			Historical1D.objects.all().delete()

		except Exception as e:
			print(e)
			traceback.print_exc()
			data={}
			data['message'] = str(e)
			event = "Error"