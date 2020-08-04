from django.db import models
import logging
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class RecommendationsManager(models.Manager):

	def create_recommendation(self,name,token,order_type,order_time,message_id,broker,remarks=None):
		self.create(name=name,token=token,order_type=order_type,order_time=order_time,message_id = message_id,broker = broker,remarks=remarks)

	def get_last_message(self,broker):
		try:
			row = self.filter(broker=broker).order_by("-id")[0]
			return int(row.message_id)
		except Exception as e:
			return None

class Recommendations(models.Model):
	name =  models.TextField()	
	token =  models.IntegerField()	
	order_time =  models.TextField()
	order_type =  models.TextField()
	order_price =  models.FloatField(null=True, blank=True, default=None)
	quantity =  models.IntegerField(null=True, blank=True, default=None)
	order_value = models.FloatField(null=True, blank=True, default=None)
	margin_used = models.FloatField(null=True, blank=True, default=None)	
	leverage =  models.TextField(null=True, blank=True, default=None)
	exit_price = models.FloatField(null=True, blank=True, default=None)
	exit_value = models.FloatField(null=True, blank=True, default=None)
	exit_time =  models.TextField(null=True, blank=True, default=None)
	profit = models.FloatField(null=True, blank=True, default=None)
	status =  models.TextField(null=True, blank=True, default=None)
	message_id =  models.IntegerField()
	broker = models.TextField()
	remarks = models.TextField(null=True, blank=True, default=None)
	objects = RecommendationsManager()