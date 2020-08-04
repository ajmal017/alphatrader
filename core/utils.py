#Utility functions for core areas
from core.constants import KITE_INSTRUMENTS_URL,KITE_EQ_MARGIN_URL,KITE_API_KEY,NIFTY_FO_URL
from core.models import Instruments,Options
import os
import csv
import json
import logging
import urllib
from django.core.exceptions import ObjectDoesNotExist

def collect_instruments():
	instruments_url = KITE_INSTRUMENTS_URL+"?api_key="+KITE_API_KEY
	data = urllib.request.urlopen(instruments_url)
	instdir = os.path.join(os.getcwd(), 'instruments')
	if not os.path.exists(instdir):
		os.makedirs(instdir)	

	with open(os.path.join(instdir, 'instruments.csv'),'wb') as output:
		output.write(data.read())

def save_instruments():
	instdir = os.path.join(os.getcwd(), 'instruments')		
	with open(os.path.join(instdir, 'instruments.csv')) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		next(readCSV, None)  # skip the headers
		for row in readCSV:
			print(row)
			Instruments.objects.save_inst(row[2],row[0],row[10],row[11],row[7],row[5])
			logging.info("Updated row")

def collect_margins():
	data = urllib.request.urlopen(KITE_EQ_MARGIN_URL)
	instdir = os.path.join(os.getcwd(), 'instruments')
	if not os.path.exists(instdir):
		os.makedirs(instdir)	

	with open(os.path.join(instdir, 'margins.json'),'wb') as output:
		output.write(data.read())

def save_margins():
	instdir = os.path.join(os.getcwd(), 'instruments')		
	json_data=open(os.path.join(instdir, 'margins.json'))
	data = json.load(json_data)

	for d in data:
		logging.info("symbol is")
		logging.info(d['tradingsymbol'])
		Instruments.objects.update_margins(d['tradingsymbol'],d['mis_multiplier'],d['co_lower'],d['co_upper'])
		logging.info("margin added")

def update_futures_list():
	#nse = Nse()
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'en-US,en;q=0.8',
		'Connection': 'keep-alive'}
	req1 = urllib.request.Request(NIFTY_FO_URL, headers=hdr)

	data1 = urllib.request.urlopen(req1)
	ildir = os.path.join(os.getcwd(), 'futureslist')
	if not os.path.exists(ildir):
		os.makedirs(ildir)	

	with open(os.path.join(ildir, 'futuresuseful.csv'),'a') as output:
		output.write(data1.read().decode('utf-8'))

def save_useful_futures():
	instdir = os.path.join(os.getcwd(), 'futureslist')		
	with open(os.path.join(instdir, 'futuresuseful.csv')) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		next(readCSV, None)  # skip the headers
		useful = []
		for row in readCSV:
			#print(row)
			#logging.info(row[2])
			stocktoken = None
			try:					
				stocktoken = Instruments.objects.get(name=row[1],exchange="NSE")
			except ObjectDoesNotExist:
				try:					
					stocktoken = Instruments.objects.get(name=row[1],exchange="BSE")
				except ObjectDoesNotExist:
					pass
					
			if stocktoken:					
				logging.info(stocktoken.token)
				useful.append(stocktoken.token)
			#Instruments.objects.set_useful(row[2],1)
		Options.objects.save_option("futuresstocklist",json.dumps(useful))
		logging.info(useful)


