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

def calculate_max_co_order_size(stock_data,price,transaction_type,stoploss):
	margin_to_use = int(self.margin)/5

	logging.info("Stock data"+str(stock_data))
	logging.info("Margin to use"+str(margin_to_use))

	co_lower = stock_data[5]
	co_upper = stock_data[6]

	co_lower = co_lower/100

	co_upper = co_upper/100
	#logging.info("CO Lower"+str(co_lower))
	#logging.info("CO upper"+str(co_upper))

	if transaction_type == 'buy':
		trigger = price - (co_upper * price)

		if stoploss < trigger:
			stoploss = trigger
		else:
			trigger = stoploss
	else:
		trigger = price + (co_upper * price)

		if stoploss > trigger:
			stoploss = trigger
		else:
			trigger = stoploss

	quantity1 = 0

	if transaction_type == 'buy':
		quantity1= margin_to_use / (price - trigger) 
	else:
		quantity1 = margin_to_use / (trigger - price)

	quantity2 = margin_to_use / (co_lower * price)

	#logging.info("quantity1"+str(quantity1))
	#logging.info("quantity2"+str(quantity2))
	#Might not be right. Test and check
	if quantity1 < quantity2:
		quantity = round(quantity1)
	else:
		quantity = round(quantity2)

	quantity = quantity - (0.25 * quantity)
	return int(round(quantity))

def calculate_co_order_size(margin,stock_data,price,transaction_type,stoploss):
	max_multiplier = 18
	margin_to_use = int(margin)/5

	quantity = (margin_to_use * max_multiplier)/price
	logging.info("Stock data"+str(stock_data))
	logging.info("Margin to use"+str(margin_to_use))

	return int(round(quantity))

def calculate_margin_required(stock_token,price,quantity,transaction_type,stoploss):
	"""
		You get the trigger price by using the upper and lower bars for stoplosses
		Check if stoploss is less than trigger and change stoploss to trigger if
	"""
	# Equity:-

	stock_data = get_stock_data(stock_token)
	logging.info("Stock data"+str(stock_data))

	co_lower = stock_data[5]
	co_upper = stock_data[6]

	co_lower = co_lower/100

	co_upper = co_upper/100


	if transaction_type == 'buy':
		trigger = price - (co_upper * price)

		if stoploss < trigger:
			stoploss = trigger
		else:
			trigger = stoploss
	else:
		trigger = price + (co_upper * price)

		if stoploss > trigger:
			stoploss = trigger
		else:
			trigger = stoploss

	x = 0

	if transaction_type == 'buy':
		x = (price - trigger) * quantity
	else:
		x = (trigger - price) * quantity

	y = co_lower * price * quantity

	if x > y:
		margin = x
	else:
		margin = y

	margin = margin + (margin * 0.2)
	return margin