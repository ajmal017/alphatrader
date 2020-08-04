List 
[4451329, 2079745, 25601, 41729, 70401, 4268801, 108033, 81153, 85761, 160001, 1195009, 103425, 2714625, 3861249, 4267265, 149249, 320001, 737793, 1256193, 261889, 2952193, 302337, 345089, 60417, 7712001, 1346049, 2997505, 2661633, 4774913, 4879617, 2674433, 1076225, 884737, 4343041, 524545, 40193, 6054401, 1629185, 7455745, 356865, 681985, 462849, 636673, 878593, 1921537, 900609, 3637249, 3529217, 1723649, 486657, 1102337, 2933761]

Architecture of alerter:
1. Subscribed to webscocket for live data feed.
2. On each price that is received, it is checked with users who have subscribed to the data feed.
3. If there are users subscribed, then the price is checked with a list of subscribed price data.
4. If a condition is matched, then an alert is sent to all users subscribed to a specific price point.

Architecture of chat:
1. A websocket is connected with the channel name as id.
2. This is then consumed by the channel id

Architecture of api calls to kite:
1. One instance controls all API functions
2. Initialise the instance
	On initialising, it should check if the api user has been logged in
	One parameter needs to be passed in to init, if the algorithm has permission to use selenium to auto login, if not logged in
	Actions the instance can do:
		1. Log the user in
		2. Keep track of logged in user states
		3. Get historical data from kite api and return outside to the caller
		4. Send a trade/order to the terminal
		5. Probably needs to be a singleton

Architecture of telegram data analytics
	1.



Setup of project, apps and models :

1. Core parts of the platform are placed in the core app
	It includes:
		1. All the stock instruments
		2. Historical timeseries data
		3. Collection of data from api
		4. Core system options
		5. 

2. Alerting system to alert users about prices are placed in the alerter app

3. Backtesting strategies (by parsing a constant strategy file/input) is done by the backtest app

4. Autotrading using live feed data is done by the trader app. If it simple, hardcoded strategies, it would be readed in from a constant syntax file which will be parsed for the strategy. words in the file will correlate to items/table names in the db.

5. If its a machine learned strategy, then it should be connected with the analyst app [which will be the machine learning brain]

6. Chatting wil be completely handled by the chat application. This inlcudes:
	1. Two way chat between users
	2. Groups and channel chat
	3. Parsed live data coming in from telegram or a different social network
	4. Upvotin downvoting quoting features etc which are part of chat.

7. Dashboard app will contain all other areas, including and not limited to calendar,tasks and other features

8. Miner app will get data from different real sources and add to the db. This includes and is not limited to 
	1. Telegram live data from channels
	2. Whatsapp live data
	3. Broker data from sites
	4. News from sites [live apis and other normal news websites]
	5. Conversations and rumours on the net