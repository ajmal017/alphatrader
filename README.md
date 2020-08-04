alpha3
Things to do:
**** Make the private chat end to end encrypted*****
-----> Can be sold as a solution to brokerage teams working in house at a high premium
Think 2000rs per user
1 In house team will have 200-300 users. And since we are end to end encrypted, this would mean a significant amount of revenue if we can convince brokerages to sign up their teams.
Estimated revenue per brokerage - 20 * 2000 per month = 40000 per month from one brokerage. This is for the lowest brokerage company in India. Scalable across the world

We can get newsfeed subscriptions as well from each user.
1 newsfeed could be charged 100rs per month



1. Create wireframe for - $5 per wireframe
	1. Channels + Graph page - 5
	2. Explore Channels page - 5
	3. Price alerts page - 5
	4. Technical alerts page - 5
	5. Multiple alerts page - 5
	6. Main Dashboard - 5
2. Send wireframes to UI designer - $25 per design
3. First use the minimum design and ask the telegram users to test it out. Get feedback and redo the design

Remaining tasks:
1. Channel page
2. Channel follow
3. Channel search
4. Channel chat - use django channels for now. It can be tested first. Scalability can be figured out later. - https://gearheart.io/blog/creating-a-chat-with-django-channels/
5. Channel telegram linking


Budget required for product
1. Facebook ad marketing - https://www.fiverr.com/sanjayy_86/manage-and-optimise-your-facebook-ad-campaign 
--> Cost $130 = Rs 8190/month + $50/week = $50*4*66 = 13200 ----Total = 21390/month. Need credit card worth 1L for this.

2. Server costs -> 10000/month
3. App UI design - $25 + App UI html - $94 ===> $119 per page. Only make one page as html. Use the same responsive template for all other pages. = 7854
4. Home page design - $50 ===> 3300
5. Rest of App UI design. = 8 * 25 = $200 = 13200
6. Landing page design - $50 = 3300
---------------------------------------
= Rs 67000. 

Do all app designs this month. And then have htmlsplice do the html for the page.
The Channel and messaging UI is done. So the remaining tasks are for the channel creation,channel follow,and channel settings.  
Channel creation can come later. Just do default channels for now. And keep adding users to it.
Default channels are : 1. All Indian Stocks, 2. Most followed telegram channels which are private.
Link telegram single - way channels with the channels here for interaction of users and auto trade recommendation abilities. Mark messages from telegram in a special way. Don't do ads from them.

UX
-----

[1] Calendar + Price/Technical/Time alerts
-------------------------------------
UI idea
1 tab with a calendar UI that shows trade alerts scheduled, on the specific date. 
Global alerts for all times have a special color to it
Auto trade based alerts will have special color to it
These types will be shown as numbers on each date block
Clicking on a date block will show a popup to create alerts or edit scheduled ones for that day

2nd tab will have all alerts shows as strips, which can be edited manually or deleted

1. Adding an alert.
2. All alerts in a row which can be edited.

3. Alpha alerter:
	1. The technical indicator + The value range / just greater than or less than ==> Optional
	2. The time ==> Optional
	3. The price + greater than/ less than ===> Optional
	4. Stock
	5. Sell/ Buy
	6. Order type
	7. Auto/Popup
	8. If auto, then add risk reward ratio for specific order.

4. Trade manager
	1. List all trades in list
	2. Add trade
	3. Modify trade.
	4. Auto publish trade data to channels.

[2] Explore Area
-------------------
1. Trending Channels
3. Trending News
4. Trending users
5. 1 Ad/Premium call to action for autotrader/alexa
6. Trending stocks
7. Trending recommendations
8. Latest orders
9. Featured Channel
10. Trade profit graph - linear bar graph


[3] Profile
------------------------
1. User photo
2. Bio
3. Subscribed channels
4. Subscribed stocks
5. Followers
6. Follow button

[Plan for Telegram channel messages realtime to channels]
----------------------------------------------------------
Use the update handler in telethon. 
Any updates telegram sends will be received by your client program. 
Also keep a getDifference check periodically to see that you havent lost messages in between.
Confirm that this works

[Plan for unread messages architecture]
-----------------------------------------
1. An unread message is a message that hasnt been seen before. So we need to identify instances when a user sees a message
	1. When a channel is opened direclty via a page load
	2. Channel opened via some link using the single page app
2. Bigger notifications require a manual intervention from the user. The message id that was last seen needs to be saved for each user
3. This can happen during each message room send. If the user is present in channel during a message sent time, then the message id for the channel needs to be updated. If different tabs are used to check different channels at the same time, then only if they click on the message area will it be updated.
4. A different table to note message read status might be required. It will need 
	1. Channel
	2. User 
	3. Last Message id [INT]
	4. Last message time.
Once the persistency is taken care of , then add the whole data inside a redis datastore as well
Redis Data Structure:
-------------------------
<userid>/<channel>/last_message --> last read message id
<userid>/sub_chnls_last_read --> json data of all last read statuses. Should be done only when the user logs out if at all. Not sure if needed

5. Subtract current message id with last read message to find out the number of unread messages
6. Subtract current message date from last read date to find out the date since unread

Tags:
1. Tagging a different username in a message will send a notification to the user on their notification icon and its panel
2. Direct messages will also do this
3. To implement this, whenever a message comes in , it needs to be parsed for usernames and a notification to be added in to the user
4. A new notification table needs to be present to add notification data in json 
5. The notification table will have
	1. Id
	2. User
	3. Notification
	4. Status
	5. Type - Normal,Tag

During a realtime communication phase, the notifications needs to be done on the frontend first. A server notification to be sent only if the user if offline.
If the user is not online, then add the notifications in to the db and keep this to the next session.
Mark as read will expire the notification.

[Plan for unique messages like trades, news , or alerts]
---------------------------------------------------------
1. The message content will be stored as json only for retrieval purposes inside the normal message table
2. Once the message is stored, the second part is to store it in a dedicated table for its type. [eg: trade, news etc]
3. The type will be designated in the message added in
4. For retrieval and showing purpose, the json data will be parsed and shown
5. All messages of a different type will need to first try and parse the json. If failed parse, alert db admin.

[Plan for message rating architecture]
------------------------------------------
1. New table to store message ratings
2. Model for table
	1. Id
	2. Message
	3. Upvote
	4. Downvote
	5. Reply
	6. Bookmark
	7. Reported
3. Query this table with message id to get the data for each message
4. Update column as users react
5. Sort using upvotes to identify trending trades/users


Channel/Recommendation alerts:
1. Adding a recommendation [ Considered in channel message UI]

TODO::
1. Make the html in bootstrap - 3 days
2. Make interactions in jquery - ;;
3. Make backend for chat - 14 days

4. Design alert pages for UI - 3 days
5. Make all endpoints as written in book - 5 days
6. Make alert pages - 9 days
7. Design explore page - 3 days
8. Make explore page - 3 days
9. Make telegram integrated channels 

Remaining things to do in chat:
1. Submit on enter - Done
2. Backend functionality to broadcast a message to a group - Done
3. Queue to save messages to db - Done
4. Image and user retrieval for a message 
5. Redis datastore for user data 
6. Redis datastore for last 10 messages in each channel
7. Redis datastore for all channels
8. Form for channel request. [Sort of like a contact form. Approved channels will have their admin functions]
9. Facebook sign up for user


Show telegram-messages linked channels using an icon on the right of the channel name

Recommendation Engine:

Collector collects tick data and saves it to appropriate csv files with name as the token in /ticks/

Ordermanager checks the Shared memory object for pending orders

Telegram group is polled every second.
1. KaranNidhy group message is parsed for latest recommendation
 	TODO:: Save the recommendation in a table with message id



--------------------------------------------------------
Datatypes:
-----------------
Prices - Float
User IDs - Int
Redis data - byte string

Redis Data Structure:
-------------------------
<userid>/device --> registration id
<token>/ltp --> last trade price
<token> --> get data of token i.e stocks data
<token>/gt --> alerts set for greater than price
<token>/lt  ---> alerts set for less than price
<token>/subscribers  ---> list of user ids subscribed to token
<token>/<price> --> list of users subscribed to the price

Alerter system:

1. Queue to add tick data to redis[elasticache], as well as tick file
2. Use signals from celery to catch a task added event. When its a tick being added in, pass the data over to the processor object which uses a pool to process all the info.
3. The processor first checks if the stock is in a subscribed list, then checks if the price is in the list of ls or gt. If it is, then a new task to send the alert is queued.
4. The messages in queue gets consumed by available workers. Once consumed, the message is removed from the message broker.

TODO::
1. Use a many to many intermediary model as described here : 
https://docs.djangoproject.com/en/2.0/topics/db/models/#intermediary-manytomany
 for the relationship between a user and a channel
2. Create a separate table for adding alerts from users

3. Make a database model for all the relationships involved here.
4. Create alert area for users to add alerts to. The alert should be posted to an endpoint in the alerter app.
5. A submit request with json data to that endpoint from a registered user will:
	1. Use a queue to add the user to the subscriber list for the stock in db and redis, and add the alert to the database and redis(as a set)
	2. Create and manage the template part of these areas in the dashboard app

---------------------------------------------------------
Legality 
---------
An investment advisor is someone/ some company who provides investment advise for a compensation
Here all advise is free.
We charge only for the autotrading extension feature
Later in the future, registered sebi advisors can join and charge for their services through private channels


Business goal:
-----------------------------------------------------------
1. Approach zerodha management / other brokerage companies for a partnership after getting to 200 paid customers = 599 * 200 = 11980
2. Make it a mission to sell the company/product
3. 20 * 599 = 11980 * 12 = 143000
4. Set up a video call with telegram group founders to have them join the platform
5. Explain to them our affiliate program that gets them 100rs for each paid user 	they bring in for all time.
6. Do not be afraid to get in front of people and face rejection! It makes you grow As well as learn new things!
7. Make a list of avenues and events where you can target customers directly face to face
8. Speak and go to trading events as much as you can
9. Register the company
10. Look for advertising partnerships with financial news portal/ websites / brokerages/ advisors
11. As a trading education app. Look for tie ups with trade education sites.

Launch idea:
-------------
1. Create a crowdfunding campaign on indiegogo for selling 1 year subscriptions to the product
2. Use this fiverr guy to do the prospecting and sales: https://www.fiverr.com/giovannibe/drive-backers-to-your-kickstarter-campaign
3. Use producthunt for launch as well

PR idea:
-----------
https://yourstory.com/2015/03/pr-agencies/

Marketing ideas:
-----------------
We are the slack for traders
-------------------------------
1. Keep an invite only landing page to collect joinee emails
	And have a lucky contest like deal to collect emails
	 - Ask users to see if they qualify for a special pass and collect their email
	 - Invited members get full price and technical alerts for a year.
	 - Keep this check option fixed on the page

2. Run facebook ads continuously for 3 months using fiver seller: https://www.fiverr.com/gopros/set-up-your-facebook-ads
	Read this and write it here:
		https://blog.wishpond.com/post/66197931282/the-psychology-behind-a-successful-facebook-ad-part-1



3. Make a webinar for 1 hour explaining what the product does and how you can be a better trader.
	Webinar members get invite code to access the platform
	Possible contents - Talk slowly , be calm and create and urgency to sign up. 
		1. Introduction to the platform
		<-----Community and chat ------------->
		2. Community of traders
		3. Telegram integration
		4. Public and Free Trade Recommendations
		5. Sponsor good traders/channels on profitable trades
		6. Show complete trade profit/loss ratio on channel
		7. Add trade feature
		8. Add news feature
		9. Filter news/trades/messages
		10. Users upgraded to moderators get the ability to ban other users for spam
		11. Warning issue on first offence and ban on second
		12. Add message to telegram feature -> Converts trade and news to normal text, and sends normal messages directly [only for channels]
		13. Voice trading using pretrades on chat
		14. Upvote for profitable and downvote for lossy trade. Rep increase for correct upvotes.Rep decrease for incorrect downvotes
		15. Shortcuts from the chat screen
		16. Realtime datafeed and tv while you chat
		<-----Calendar Section ------------->
		17. Calendar short view to show number of alerts,trades. And a color to indicate the type of day - neutral , profitable, lossy
		18. Calendar popup on date to show analytics of the day, the number of trades done and their profit percent, the alerts expired
		19. 

Landing page:
--------------
Idea:
Green gradient full page background with an orange CTA
Image of one Indian business person


Convert to leads using three different versions of a landing page:
 1. With an invite code won - click to see if you've won an invite code
 2. Just a pre sign up form
 3. Without invite code - sign up for daily raffle of winners with timer
 4. Collect phone number on all pages with otp
A/B Test these three variants of landing pages for 3 months. And then run the best one after.

Keep an offer to make the user return when exiting by a limited time offer
	Use a red button as CTA here to convey the urgency of the offer

Keep directional cues to tell people what to read [Arrows and lines]

Use an image of a person in your landing page -> But A/B test variation where the user points to and doesnt point to the cta
	 A line drawing is more powerful than a photograph. He writes that this is because the ‘idea’ of a person is more appealing than the truth of it

Ensure color contrast between CTA and the rest of the page 
Use and orange CTA button
1. Use the points here:
	https://www.hatchbuck.com/blog/science-behind-high-converting-landing-page/

Monetisations plans:
------------------------
1. A per user subscription fee for pro features - [Autotrade data feed, Analytics of trades]
2. Advertising from luxury brands
3. Sponsoring analysts by users [we take out 5% from each sponsored amount] - These are not paid recommendations. Users choose to sponsor an anlayst
Paid recommendations can be possible after getting sebi approval.

4. Private channels for brokerages and their teams. They should be charged 2k per user. Look at slacks pricing to understand more.
Number of brokerages in india - 250 , average number of employee analysts = 10, cost per sign up = 2000. Total revenue = 250*10*2000 = 50L per month [Target for 5th year]

Algo ideas:
---------------
Backtested samples from streak:
1. True range
Interval : 1H
Sell when TR greater than 0.1 
Stoploss :0.45%
Target: 1.5%
Basket of stocks:

2. DI
Interval : 1H
Sell when -DI(14) greater than 20
Exit when +DI(14) greater than 20
Stoploss :1%
Target: 2.5%
Basket of stocks: PSU banks
Seems to work wonderfully

Patentable tech of new improved AI brain.
------------------------------------------
Key : In Email

Inbound marketing
------------------
This is all about creating new and good content every day.
Hubspot does this still using 50 good articles every week. They invented the concept.

Prospecting
----------------
Use Linkedin Sales Navigator which cost 5k per month and reach out to the prospects there.
People who follow up are potential sales leads.

Getting new investor leads
---------------------------
1. Make a list of indian investors and angels who have seedfunded before.
2. Get their emails and cold email them for a call.
3. Once you get the call appointment, follow a call script.
4. The call script needs to evolve as you go to more sales/investors.

Cold emailing:
----------------
Calculate open rates
Different strategies at each point of the customer journey
A/B test for future informations
1. Monday emails get more response rates
2. Saturday emails get more open rates
Response rates are more important.
[At the end of a cold email campaign, one company received 73 responses from a 523 prospect list]


Pitching new investors
---------------------------
https://www.youtube.com/watch?v=IPNtZdNOUnY
Watch this video as much as you can to understand how to pitch and communicate the best way possible. 
Claire did an amazing job at their pitch.
They took it slow, made everyone watching fall into this calm mood to actually listen to the pitch.
The images were also really good.

Best Shark tank pitch ever:
https://www.youtube.com/watch?v=tWlfK_qfvS8
The 17 year old kid was calm, collected and just explained how he came to the valuation.
[Projected revenue with a 5X multiple, which seemed fair to the sharks.]

Go to investors when you do not need the money. They are just like banks. They will only go for people who are calm and they believe will get them returns

Investor Questions
---------------------
How are you unique in your market and who are your competitors?

	Tradingview is probably our direct competitor.
	Our long term goal is to become the single place for a trader to communicate,analyse,get recommendations, and trade as easy as possible.

	But our uniqueness lies in 2 factors.
	1. the fact that, our proprietary trading platform is meant for analysts.
	We track every analyst trade and channel, and verify their monthly to yearly returns for their recommendations.

	2. The other unique feature we have is our automator.
	We automate all trades with our automation extension. Unlike trading view which integrates with trading platforms using their APIs,
	what we do is to use our automator flows to link data pushed on to servers with our macro system to completely automate every thing done in the browser.
	We have automations available for the leading brokerages available. And then we have automations available from the community that we vet and approve.

	Our plan is to differentiate the automator extension into its own separate product for companies to push data and send alerts and automations to users everywhere. This has a wide variety of use cases.

	So we become the data feed provider for all analysts from the world. As well as media platforms.


What data can the investor get to make a potential decision on investing

	We have grown our traffic to [X] amount per day. Our user base has expanded from 0 to 2000 in just 6 months from launch. We have 200 paid subscribers to our data feed and news feed combined, and we have deals across the pipeline for ads as well as strategic partnerships.
	We have 4 enterprise trading companies signed up on our product, with 500 users signed up. We charge anywhere from 500 per user to 2000 based on the companys plan package. We also intend to charge analysts for verifications.

What all problems can you address.
	
	When I started out trading, the first thing I felt lacking was the direct advise and exposure a trader got to experienced analysts.
	Sure, we had brokerages, and other advisors. But most of their advice was untrackable, and their results unmeasured. 
	By starting this company, this was the core problem that I wanted to address. Helping a novice trader and an experienced trader at the same time.
	We provide community wide help to all our traders, trade recommendations that users can track and verify themselves with our testing solution that is in the works, as well as a completely new way for traders and even enterprise brokerages to communicate.
	Our private channels provide the full security and all the same features for enterprise brokerages to send out trades to execute with a tap to their list of associates.

	And then there is our voice trading system, which is the first anywhere.
	Imagine that you are sitting in front of your television, and a news breaks affecting your stocks value tremendously. You do not have the time to even think at those times. So what can you do to get it done in the fastest time possible.
	Tell your voice assistant to do a pretrade for you that you have set before.
	Just call up your voice assistant, and say "Hey, do pretrade mona on SBI "
	The pretrade gets compiled, and you see an alert on your phone to initiate the trade. Just like that, you saved 50% of your time and a whole lot of money.


Valuation
----------

[Projected revenue with a 5X multiple, which seemed fair to the sharks for a product based company]

Revenue per year required for a valuation of 30000000 = 3cr
Revenue per month = 5 Lakhs

If in 6 months we make 20L, it means 3.2 lakhs per month in revenue for a projected revenue of 60Lakhs for the year.

You need to take this slow though. Unless brand presence can be established, you cant get the sales that you want from brokerages.

Giving this a PE multiple of 5, this makes the valuation of the company at 3cr.
We can raise seed funding at this stage for 10% equity stake in the company, which amounts to 30 Lakhs

Release Plan
--------------

First iteration MVP:
1. Home page
2. Chat area
	1. Realtime chatting
	2. Chat history
	3. Different message types:
		1. Normal message
		2. Trade message
		3. News message
		4. Telegram message
	4. Two way Telegram feed integration
	5. Filtering based on the message type
	6. Reputation for a user/channel
	7. Profit percent for the month for transparency
	8. Shortcuts from the chat bar for trading, setting alerts, using a pretrade etc
	9. Replying to a message by quoted messages

3. Explore area
	1. Find trending stocks
	2. Find trending channels.
	3. Find trending news

4. Search page.
5. Calendar
	1. Add trade
	2. Add alert
	3. See trades
	4. See alerts
	5. Click and see profitability of a month
6. Pretrades


7. Extension without a UI - maybe even barebones. Just need them to connect the data coming in from the subscribed feed to the brokers trade process
Look into how loadimpact does it with their chrome extension
The best idea would be to have them record a dummy transaction with {{name}} type fields into input fields. 
Here however they will have to create multiple automations depending on the data coming in. But this is still feasible.

Second Version:
1. Voice based trading
2. Sponsored Ads on 
	1. Live video feed
	2. Live news feed
	3. Messaging

Third version
1. Custom graphing and licensing model

Fourth version
1. Improve recording tasks and UI of extension
2. Build a marketplace for automation feeds to subscribe to

Fifth version - Requires SEBI approval, and company incorporation
1. Sponsoring an analyst- We take 5% from the sponsorship, and ask the user to pay this amount
2. Analysts can sponsor their trades on public channels

Milestones
-----------
Year one: Monthly recurring revenue of 41.6k on average an year. Which means, 5L in one year from the product subscription sales 

Month 1: 0 , -25000 fb marketing, -5000 Linkedin Prospecting, -7000 server costs 
Month 2: 0 , -26000 fb marketing,  -5000 Linkedin Prospecting, -10000 server costs
Month 3: 0, -30000 fb marketing,  -5000 Linkedin Prospecting, -20000 server costs
Month 4: 10000, -25000 fb marketing,  -5000 Linkedin Prospecting, - 30000 server costs []
Month 5: 20000, -25000 fb marketing,  -5000 Linkedin Prospecting, - 30000 server costs []
Month 6: 30000, -25000 fb marketing,  -5000 Linkedin Prospecting, - 30000 server costs []
Month 7: 40000, -25000 fb marketing,  -5000 Linkedin Prospecting, - 30000 server costs []
Month 8: 60000, -25000 fb marketing,  -5000 Linkedin Prospecting, - 35000 server costs []
Month 9: 70000, -25000 fb marketing,  -5000 Linkedin Prospecting, - 35000 server costs []
Month 10: 80000, -25000 fb marketing,  -5000 Linkedin Prospecting, - 35000 server costs []
Month 11: 90000, -25000 fb marketing,  -5000 Linkedin Prospecting, - 35000 server costs []
Month 12: 100000, -25000 fb marketing,  -5000 Linkedin Prospecting, - 35000 server costs []
---------------------------------------------------------------------------------------------
7 Lakh rupees [+ Registering costs = 20000 + Monthly office costs = 12000 * 12] 

Personal experiences of building a SaaS company:
--------------------------------------------------
https://blog.kissmetrics.com/built-and-launched-a-saas-company/

Ideas for making the browser extension work
--------------------------------------------

For embedded systems like Java applets, flash , iframes etc, use click event based recording like this:
https://wiki.imacros.net/DirectScreen_Technology

For normal html based systems, just do a complete script compilation, that can be edited and used by other users as well.
[Just like the iMacros extension]

Idea for UI --
1. Transparent recording panel that doesnt take click event and can be moved around and collapsed
2. On each event that the user does, the panel will show a separate event being logged as text
3. On waittime, the logger will show the time lapsed as a comman - WAIT 10s
4. The record button can be on the collapisble bar that hovers.
5. A list of all automated macros is available on the settings page of the app.
6. Connected macros can be implemented with merge tags on input fields,which will be replaced with the assigned data when the macro is run 
7. A macro can be created just by coding it in as well.


Traffic and revenue modelling based on adsense
----------------------------------------------
With a click through rate 1% [1 in 100 viewers click on the ad for 25cents of revenue.
], you need

40,000 views per day -> $100 revenue per day

100 views on 400 channels.

Insert ad into a channel.
1 ad per hour is inserted and shown on each channel message randomly.
10 hours = 10 ads in a day on one channel from one user.
2000 users = 20000 ad views per day. = $50 per day.
So the priority should be to increase user count in the community which will inturn increase ad revenue.

Keep a public blogging option as well from the chat area. Bigger posts can be leveraged for more ad traffic from social media and google rankings

Market research
----------------
https://www.jonathanstark.com/market-research-cold-email-template

Data scraping telegram for prospective leads
----------------------------------------
Have a list of channels 
1. Scrape all data in the current channel
2. If a link of a channel is described in the message history of currently scraping channel, save the link and channel if it hasnt been saved before
3. Find all phone numbers [i.e numbers greater than 8] and retrieve those messages only into db.
4. Start looping through all saved channel links and join each one by one.
5. Repeat

After this whole loop is complete, all the telegram messages that has a phone number attached to it, or the words [contact,whatsapp,message] attached to it will be saved in db for manual checks. 
All these saved messages will then need to be checked individually to see if they include a prospects contacts in it.