from django.db import models
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Strategy(models.Model):
	name =  models.CharField(max_length=200)#Name of strategy
	inst_type = models.CharField(max_length=100,null=True, blank=True, default=None)	#EQ, FUT, OPTIONS, COMM, FX		
	timeframe = models.CharField(max_length=100,null=True, blank=True, default=None)#Intraday,Positional
	st_type =  models.IntegerField() #1,2,3,4 based on [recommendations,rec2, technical,ai]
	strategy =  JSONField()	#JSON
	last_tested_time =  models.DateTimeField(auto_now=False, auto_now_add=False) #Last time the strategy was backtested
	last_tested_profit =  models.FloatField(null=True, blank=True, default=None) #Last tested profit for the strategy
	remarks = models.TextField(null=True, blank=True, default=None)

class BacktestOrder(models.Model):
	token =  models.IntegerField()	
	strategy =  models.ForeignKey(Strategy, on_delete=models.CASCADE)
	order_no =  models.BigIntegerField()
	order_type =  models.TextField(null=True, blank=True, default=None)		
	status =  models.TextField(null=True, blank=True, default=None)
	order_time =  models.TextField()
	order_price =  models.FloatField()
	quantity =  models.IntegerField()
	order_value = models.FloatField()
	margin_used = models.FloatField(null=True, blank=True, default=None)	
	leverage =  models.TextField(null=True, blank=True, default=None)
	exit_price = models.FloatField(null=True, blank=True, default=None)
	exit_value = models.FloatField(null=True, blank=True, default=None)
	exit_time =  models.TextField(null=True, blank=True, default=None)
	exit_order_no = models.BigIntegerField(null=True, blank=True, default=None)
	profit = models.FloatField(null=True, blank=True, default=None)
	remarks = models.TextField(null=True, blank=True, default=None)


