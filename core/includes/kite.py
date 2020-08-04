# Bracket and cover order Margins calculation:-
import multiprocessing
import time
from datetime import datetime,timedelta
import os
import csv
import json
import logging
import pandas as pd
from kiteconnect import KiteConnect
from core.models import Options
from core.models import Instruments
from core.includes.patterns.singleton import Singleton
from core.constants import KITE_INSTRUMENTS_URL,KITE_EQ_MARGIN_URL,KITE_API_KEY,KITE_API_SECRET

""" Handles all authentication, access tokens and requests to kite"""
class _Kite_(object,metaclass=Singleton):

	def __init__(self,autologin=False):
		#Get request token
		#If no token, and autologin is true, do the login flow on selenium to receive the token
		#If token already present just initialise normally and get access token
		#Flush request token at the end of the trading day which should be 11:59 pm everyday

		request_token = Options.objects.get_option("request_token")
		self.request_token = request_token
		self.kite = KiteConnect(api_key=KITE_API_KEY)


		access_token = Options.objects.get_option("access_token")
		access_token_last = Options.objects.get_option("access_token_last_updated")

		now = datetime.now()


		if not access_token_last:
			access_token_last = now	
		else:
			access_token_last = datetime.fromtimestamp(int(access_token_last))	

		logging.info("Access token last updated on:"+ str(access_token_last))

		access_token_expired =	access_token_last <= now-timedelta(days=1) #If access token updated time is greater than yesterday
		if not access_token:
			logging.info("No Access token... Getting new one")
			self.get_new_access_token()		
		else:
			if access_token_expired:
				logging.info("Access token expired... Getting new one")

				self.get_new_access_token()
			else:
				logging.info("Using saved access token")

				self.kite.set_access_token(access_token)	
				self.access_token = access_token

					
		margin_data = self.kite.margins("equity")
		self.margin = margin_data["net"]

		#margin_data = json.loads(self.margin)
		logging.info("Margin eq is :"+str(self.margin))

	def get_new_access_token(self):
		data = self.kite.generate_session(self.request_token,KITE_API_SECRET)
		access_token = data["access_token"]
		Options.objects.save_option("access_token",access_token)
		Options.objects.save_option("access_token_last_updated",int(datetime.now().strftime('%s')))
		self.kite.set_access_token(access_token)
		self.access_token = access_token

	def logout(self):
		self.kite.invalidate_access_token(self.access_token)

	def remove_access_token(self):
		Options.objects.clear_option("access_token")
		Options.objects.clear_option("access_token_last_updated")

	def place_market_nrml_order(self,symbol,exchange,txn_type,quantity):
		""" Mthod that runs forever """

		# Place an order
		try:
			order_id = self.kite.place_order(
							variety = "regular",
							exchange=exchange,
							tradingsymbol = symbol,
							transaction_type=self.kite.TRANSACTION_TYPE_BUY,
							quantity=int(quantity),
							order_type=self.kite.ORDER_TYPE_MARKET,
							product=self.kite.PRODUCT_MIS)
			logging.info("Order placed. ID is"+str(order_id))
			return order_id

		except Exception as e:
			logging.info("Order placement failed"+str(e))
			return None

	def place_market_bo_order(self,symbol,exchange,txn_type,quantity,target,stoploss,trailing_stoploss):
		""" Mthod that runs forever """

		# Place an order
		try:
			order_id = self.kite.place_order(
							tradingsymbol=symbol,
							exchange=exchange,
							transaction_type=txn_type,
							quantity=quantity,
							order_type='MARKET',
							trigger_price=None,
							squareoff_value=target,
							stoploss_value=stoploss,
							trailing_stoploss=trailing_stoploss,							
							product=self.kite.PRODUCT_MIS,
							variety=self.kite.VARIETY_BO)

			logging.info("Order placed. ID is"+str(order_id))
			return order_id

		except Exception as e:
			logging.info("Order placement failed"+str(e))
			return None

	def place_market_co_order(self,symbol,exchange,txn_type,quantity,stoploss):
		""" Mthod that runs forever """
		if txn_type == "buy":
			t = self.kite.TRANSACTION_TYPE_BUY
		else:
			t = self.kite.TRANSACTION_TYPE_SELL
		# Place an order
		try:
			order_id = self.kite.place_order(
							tradingsymbol=symbol,
							exchange=exchange,
							transaction_type=t,
							quantity=quantity,
							order_type=self.kite.ORDER_TYPE_MARKET,
							stoploss=stoploss,
							trigger_price=stoploss,
							product=self.kite.PRODUCT_MIS,
							variety=self.kite.VARIETY_CO,
							tag="SYSTEMCO")

			logging.info("Order placed. ID is"+str(order_id))
			return order_id

		except Exception as e:
			logging.info("Order placement failed"+str(e))
			return None

	def exit_co_order(self,order_no,parent_order_id=None):
		""" Mthod that runs forever """

		try:
			order_id = self.kite.exit_order(self.kite.VARIETY_CO, order_no)


			logging.info("Order exited. ID is"+str(order_id))
			return order_id

		except Exception as e:
			logging.info("Order exiting failed"+str(e))
			return None

	def modify_order(self,order_no,data):
		""" Mthod that runs forever """

		try:
			order_id = self.kite.exit_order(self.kite.VARIETY_CO, order_no)


			logging.info("Order modified. ID is"+str(order_id))
			return order_id

		except Exception as e:
			logging.info("Order modified"+str(e))
			return None

	def place_limit_bo_order(self,symbol,exchange,txn_type,quantity,order_type,product):
		""" Mthod that runs forever """

		# Place an order
		try:
			order_id = self.kite.place_order(
							tradingsymbol=symbol,
							exchange=exchange,
							transaction_type=txn_type,
							quantity=quantity,
							order_type=order_type,
							product=product)
			logging.info("Order placed. ID is"+str(order_id))
			return order_id

		except Exception as e:
			logging.info("Order placement failed"+str(e))
			return None