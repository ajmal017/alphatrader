import MySQLdb
import logging

class TraderDB(object):

	@staticmethod
	def get_stock_data(token):
		#Server Connection to MySQL:
		conn = MySQLdb.connect(host= "alphalive.cvb8cqc2yslc.us-west-2.rds.amazonaws.com",user="alpha",passwd="alpha123",db="alphalive")
		x = conn.cursor()
		data= None
		try:
			x.execute("""SELECT * from trader_instruments WHERE token = %s""", (token,))
			data=x.fetchone()

		except:
			logging.info("Retrieve stock failed")
		

		conn.close()
		logging.info("Instrument retrieved from db:"+str(data))

		return data

	@staticmethod
	def get_all_stock_names(exchange):
		#Server Connection to MySQL:
		conn = MySQLdb.connect(host= "alphalive.cvb8cqc2yslc.us-west-2.rds.amazonaws.com",user="alpha",passwd="alpha123",db="alphalive")
		x = conn.cursor()
		data= None
		try:
			x.execute("""SELECT name from trader_instruments WHERE exchange = %s""", (exchange))
			data=x.fetchall()

		except:
			logging.info("Retrieve all stocks failed")
		
		conn.close()
		# logging.info("Instrument retrieved from db:"+str(data))

		return data

	@staticmethod
	def get_all_stockdata(exchange):
		#Server Connection to MySQL:
		conn = MySQLdb.connect(host= "alphalive.cvb8cqc2yslc.us-west-2.rds.amazonaws.com",user="alpha",passwd="alpha123",db="alphalive")
		x = conn.cursor()
		data= None
		try:
			x.execute("""SELECT * from trader_instruments WHERE exchange = %s""", (exchange))
			data=x.fetchone()

		except:
			logging.info("Retrieve all stocks failed")
		
		conn.close()
		# logging.info("Instrument retrieved from db:"+str(data))

		return data

	@staticmethod
	def get_stock_data_from_name(stockname,exchange):
		#Server Connection to MySQL:
		conn = MySQLdb.connect(host= "alphalive.cvb8cqc2yslc.us-west-2.rds.amazonaws.com",user="alpha",passwd="alpha123",db="alphalive")
		x = conn.cursor()
		data= None
		try:
			x.execute("""SELECT * from trader_instruments WHERE name = %s AND exchange=%s""", (stockname,exchange))
			data=x.fetchone()
		except:
			logging.info("Retrieve stock failed")
		

		conn.close()
		logging.info("Instrument retrieved from db:"+str(data))

		return data