# Bracket and cover order Margins calculation:-
import multiprocessing

import threading
import time
from datetime import datetime
import os
import csv
import json
import logging
import pandas as pd
import MySQLdb
from trader.includes.tools.notifier import *
from trader.includes.tools.traderdb import TraderDB
from dateutil import tz

from trader.models import Historical1Minute
import pytz

#Each order needs to calculate margin to use based on available funds
#An order is initiated for the quantity based on margin available
#The order is then made. The order time is present in order_data
#The order is saved to trader_backtestorders (entry time as order_time in message)
#The historical_1minute tables holds the price. Get the row with same time and stock as in order. Use open price as entry price
#Get all data from the entry time to the end of that day i.e 3:20
#GO through each candle and see if high or low of the candle has reached target or stop loss respectively
#If yes, then exit the order
#Exit the order in intervals

"""

Items that need to be backtested
1. Recommendations - Just entry orders that needs to be tested out with minimal future data 
2. Strategies - Specific strategies (like SELL when RSI > 70) that needs to be tested out with much larger historical data

Modelling the data:
1. Have a type column to specify the type of strategy [
eg, recommendation from a strategist with exit point =1 , recommendation without exit = 2, technical strategy = 3, ai strategy = 4
]
2 Have the backtest be done based on the type of strategy
3 The strategy itself gets a new column, which will be json
4 The JSON data will contain specific key value pairs based on the strategy
 eg: {
	type : 3,
	rsi : {
		denom : "gt"
		val : 75
	}
}
5. Last tested date
6. Last tested profit
7. Timeframe - Intraday, positional
8. Stock type - EQ, FUT, OPTIONS, COMM, FX

"""

class BackTestOrder(object):

	def __init__(self,token,price,order_data):
		""" Constructor
		:type interval: int
		:param interval: Check interval, in seconds	"""
		logging.info("In Backorder init")
		print(order_data)
		self.tickfile = token
		self.token= int(token)
		self.price = price
		self.txn_type = order_data['order_type']
		self.order_time = datetime.strptime(order_data['order_time'],"%Y-%m-%d %H:%M:%S").replace(tzinfo=tz.tzlocal())
		self.leve_type = order_data['leve_type'] #CO,BO,NRML,MIS
		self.order_success = False
		self.order_failed = False

		self.margin_to_use = 2000

		start_time = self.order_time
		print(str(start_time))
		end_time = self.order_time.replace(minute=20, hour=15)#new2
		starttime_in_utc = start_time.astimezone(pytz.utc)
		endtime_in_utc = end_time.astimezone(pytz.utc)

		self.candles = self.get_onemin_candle_data(self.token,starttime_in_utc,endtime_in_utc)
		if self.candles:
			# print(self.candles)
			if not self.price:
				if self.txn_type == "sell":
					self.price = self.candles[0].low
				else:
					self.price = self.candles[0].high
			self.run()

		else:
			logging.info("No candles for token:"+str(token)+" at "+str(self.order_time))
			logging.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


	def run(self):
		""" Mthod that runs forever """
		# self.shared = shared
		logging.info("In backtest order run")

		order_placed = self.initiate_order()
		if order_placed:
			self.succeed_order()
			self.monitor_order()
		else:
			self.fail_order()				

		logging.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

	def save_order_db(self,token,order_no,status,order_time,price,quantity):
		#Server Connection to MySQL:
		conn = MySQLdb.connect(host= "alphalive.cvb8cqc2yslc.us-west-2.rds.amazonaws.com",user="alpha",passwd="alpha123",db="alphalive")
		x = conn.cursor()
		self.order_value = price * quantity
		logging.info(token)
		try:
			x.execute("""INSERT INTO trader_backtestorders (token, order_no, status, order_time, order_price,quantity,order_value,leverage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(token,order_no,status,order_time,price,quantity,self.order_value,self.leve_type))
			conn.commit()
		except:
			logging.info("Save to db failed")
			conn.rollback()

		insertid= x.lastrowid
		if insertid== 0:
			insertid = conn.insert_id()
		conn.close()
		logging.info("Order saved to db:"+str(insertid))

		return insertid

	def exit_order_db(self,orderid,exit_price,exit_value,exit_time,profit,remarks,order_type,exit_order_no):
		#Server Connection to MySQL:
		conn = MySQLdb.connect(host= "alphalive.cvb8cqc2yslc.us-west-2.rds.amazonaws.com",user="alpha",passwd="alpha123",db="alphalive")
		status = "complete"
		if not remarks:
			remarks = ""
		x = conn.cursor()
		try:
			x.execute("""UPDATE trader_backtestorders SET status= %s,exit_price = %s,exit_value = %s ,exit_time = %s,profit=%s,remarks=%s, order_type=%s,exit_order_no=%s WHERE id = %s""",(status,exit_price,exit_value,exit_time,profit,remarks,order_type,exit_order_no,orderid))
			conn.commit()
		except:
			conn.rollback()
		conn.close()

	def log_order(self):
		ordersdir = os.path.join(os.getcwd(), 'orders')
		if not os.path.exists(ordersdir):
			os.makedirs(ordersdir)	

		orderdata = [[str(datetime.now()),self.token,"15 Min RSI greater than 77"]]  

		orderfile = open(os.path.join(ordersdir, str(self.token)), 'a')  #Add +csv here after token is cleansed
		with orderfile:  
			writer = csv.writer(orderfile)
			writer.writerows(orderdata)

	def initiate_order(self):
		#margin = self.calculate_margin()
		logging.info("Order start:"+str(self.token))


		stock_data = TraderDB.get_stock_data(self.token)
		self.stockname = stock_data[1]
		self.tick_size = stock_data[9]
		exit_data = self.get_order_exit_data(self.tick_size,self.txn_type)

		logging.info("Order Price:"+str(self.price))
		logging.info("Stoploss:"+str(exit_data['stoploss']))
		logging.info("Target:"+str(exit_data['target']))
		logging.info("Leverage type"+str(self.leve_type))

		if self.leve_type == "CO":

			self.quantity = int(18 * self.margin_to_use/self.price)
			logging.info("Quantity:"+str(self.quantity))
			if (self.quantity > 0):
				# self.order_no = self.kitealpha.place_market_co_order(stock_data[1],stock_data[3],self.txn_type,self.quantity,exit_data['stoploss'])
				self.order_no = 100000000001
			else:
				self.order_no = False
				self.retry = False
				data={}
				data['message'] = "Order quantity is 0 for stock:"+self.stockname
				event = "Error inside Order"
				send_notification(event,data)
				send_push(event,data['message'])


		if self.order_no:
			return True
		else:
			return False
		#self.order_no = self.kitealpha.place_market_bo_order(stock_data[0],stock_data[3],self.txn_type,self.quantity,target,stoploss,trailing_stoploss)

		# self.order_no = self.get_order_details()
		#self.orderid = self.save_order_db(self.token,self.order_no,str(datetime.now().time()),self.price,self.quantity)
		#self.log_order()

	def get_order_exit_data(self,tick_size,txn_type):
		data = {}
		if txn_type == "sell":
			self.stoploss = data['stoploss']= self.round_to_tick(self.price + (0.0050 * self.price),base=tick_size)
			self.target = data['target']	= self.round_to_tick(self.price - (0.0030 * self.price),base=tick_size)
		else:
			self.stoploss = data['stoploss']= self.round_to_tick(self.price - (0.0050 * self.price),base=tick_size)
			self.target = data['target']	= self.round_to_tick(self.price + (0.0030 * self.price),base=tick_size)

		data['trailing_stoploss'] = 1	
		return data


	def round_to_tick(self,x, prec=2, base=.05):
		return round(base * round(float(x)/base),prec)


	def succeed_order(self):
		logging.info("Success.Adding order to db")

		status = "active"
		self.price = self.price
		self.orderid = self.save_order_db(self.token,self.order_no,status,self.order_time,self.price,self.quantity)	

		logging.info("Order Success..."+str(self.order_no))	

	def succeed_exit(self):
		status = "complete"
		# self.shared.remove_from_active_orders(self.co_stop_orderid)

		exit_price = self.exit_price
		self.exit_value = exit_price * self.quantity

		if self.txn_type == "sell":
			self.profit = round(self.order_value - self.exit_value,2)
		else:
			self.profit = round(self.exit_value - self.order_value,2)

		remarks = "{type:'recommended',broker:'nse2mcx',medium:'telegram'}"

		self.exit_order_db(self.orderid,exit_price,self.exit_value,self.exit_time,self.profit,remarks,self.txn_type,self.exit_order_no)

		logging.info("Exit Success...")


	def monitor_order(self):
		logging.info("Start Monitoring")
		monitoring_success_notif = False

		exited = False


		# print(self.candles)
		for candle in self.candles:
			low = candle.low
			high = candle.high
			time = candle.time
			tz = pytz.timezone('Asia/Kolkata')
			time = time.astimezone(tz)
			# print(time)
			if self.txn_type == "sell":
				if low <= self.target:


					self.exit_order_no = 100000000002
					self.exit_time = time
					self.exit_price = low		

					self.succeed_exit()	
					send_push("Successful exit: "+self.stockname,"exit with profit")
					break				
			else:
				if high >= self.target:

					self.exit_order_no = 100000000002
					self.exit_time = time	
					self.exit_price = high		
		
					self.succeed_exit()	
					
					send_push("Successful exit: "+self.stockname,"exit with profit")
					break

			if self.txn_type == "sell":
				if high >= self.stoploss:

					self.exit_order_no = 100000000002
					self.exit_time = time
					self.exit_price = high		

					self.succeed_exit()	
					send_push("Lossy exit: "+self.stockname,"exit with loss")	
					break			
			else:
				if low <= self.stoploss:

					self.exit_order_no = 100000000002
					self.exit_time = time	
					self.exit_price = low		
					self.succeed_exit()	
					
					send_push("Lossy exit: "+self.stockname,"exit with loss")	
					break

	def get_onemin_candle_data(self,token,start,end):
		candles = Historical1Minute.objects.filter(token=token,time__range=[start,end])	

		if candles:
			return candles
		else:
			return None

	def	update_exit_data(self):
		currentstoplosspercent = self.stoplosspercent
		currenttargetpercent = self.targetpercent
		cureentstoploss = self.stoploss

		if currenttargetpercent == 0.30:
			self.stoplosspercent = 0
			self.targetpercent = 0.50

		elif currenttargetpercent == 0.50:
			self.stoplosspercent = 0.50
			self.targetpercent = 1

		elif currenttargetpercent == 1:
			self.stoplosspercent = 0.75
			self.targetpercent = 1

		elif currenttargetpercent == 1.5:
			self.stoplosspercent = 1
			self.targetpercent = 2

		elif currenttargetpercent == 2:
			self.stoplosspercent = 1.5
			self.targetpercent = 2.5

		elif currenttargetpercent == 2.5:
			self.stoplosspercent = 2
			#TODO:: Initiate trend reversal signalling machine learned algorithm eithere here or inside monitor
			self.targetpercent = 25

		if self.txn_type == "sell":

			self.stoploss= self.round_to_tick(self.price + (self.stoplosspercent/100 * self.price),base=self.tick_size)
			self.target	= self.round_to_tick(self.price - (self.targetpercent/100 * self.price),base=self.tick_size)

		else:
			self.stoploss= self.round_to_tick(self.price - (self.stoplosspercent/100 * self.price),base=self.tick_size)
			self.target	= self.round_to_tick(self.price + (self.targetpercent/100 * self.price),base=self.tick_size)


