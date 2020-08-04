from django.db import models
import logging
from django.core.exceptions import ObjectDoesNotExist


class Orders(models.Model):
	token =  models.IntegerField()	
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


class OrderMeta(models.Model):
	order_id =  models.AutoField(primary_key=True)	
	order_meta_key =  models.TextField()	
	order_meta_value =  models.TextField()