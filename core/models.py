from django.db import models
import logging
from django.core.exceptions import ObjectDoesNotExist

class OptionManager(models.Manager):

	def get_option(self,name):
		try:
			field = self.get(option_name=name)
		except ObjectDoesNotExist:
			field = None

		if not field:
			return None
		else:
			return field.option_value

	def save_option(self,name,value):
		try:
			field = self.get(option_name=name)
		except ObjectDoesNotExist:
			field = None

		if not field:
			self.create(option_name=name,option_value=value)
		else:	
			self.filter(option_name=name).update(option_value=value)

	def clear_option(self,name):
		try:
			field = self.get(option_name=name)
		except ObjectDoesNotExist:
			field = None

		if not field:
			pass
		else:	
			self.filter(option_name=name).update(option_value="")

class Options(models.Model):
	option_name =  models.TextField()
	option_value =  models.TextField()
	objects = OptionManager()

class InstrumentManager(models.Manager):

	def get_inst(self,name):
		try:
			field = self.get(name=name)
		except ObjectDoesNotExist:
			field = None

		return field.name

	def save_inst(self,name,token,segment,exchange,tick_size,expiry,mis_multiplier=None,co_lower=None,co_upper=None):
		try:
			field = self.get(name=name)
		except ObjectDoesNotExist:
			field = None

		if expiry == "":
			expiry = None

		if not field:
			self.create(name=name,token=token,segment=segment,exchange=exchange,tick_size=tick_size,expiry=expiry)
		else:	
			self.filter(name=name).update(token=token,segment=segment,exchange=exchange,tick_size=tick_size,expiry=expiry)

	def update_margins(self,name,mis_multiplier=None,co_lower=None,co_upper=None):
		try:
			self.filter(name=name).update(mis_multiplier=mis_multiplier,co_lower=co_lower,co_upper=co_upper)
		except Exception as e:
			print(e)	

	def get_data(self,token):
		try:
			field = self.get(token=token)
		except ObjectDoesNotExist:
			field = None

		if not field:
			return None
		else:	
			return field

	def set_useful(self,name,use=0):
		try:
			logging.info(self.get(name=name).query)
			field = self.get(name=name)
		except ObjectDoesNotExist:
			field = None

		if not field:
			return None
		else:	
			self.filter(name=name).update(use=use)
			
class Instruments(models.Model):
	name =  models.TextField()
	token =  models.IntegerField()
	segment =  models.CharField(max_length=30)
	exchange =  models.CharField(max_length=30)
	mis_multiplier =  models.FloatField(null=True, blank=True, default=None)
	co_lower =  models.FloatField(null=True, blank=True, default=None)
	co_upper =  models.FloatField(null=True, blank=True, default=None)
	tick_size =  models.FloatField(null=True, blank=True, default=None)
	expiry =   models.DateTimeField(null=True, blank=True, default=None)
	use = models.IntegerField(default=0)
	objects = InstrumentManager()

class Historical1M(models.Model):
	name =  models.TextField()	
	token =  models.IntegerField(db_index=True)	
	time =  models.DateTimeField(db_index=True)
	open =  models.FloatField(null=True, blank=True, default=None)
	high =  models.FloatField(null=True, blank=True, default=None)
	low = models.FloatField(null=True, blank=True, default=None)
	close = models.FloatField(null=True, blank=True, default=None)	
	volume =  models.BigIntegerField(null=True, blank=True, default=None)

class Historical1D(models.Model):
	name =  models.TextField()	
	token =  models.IntegerField(db_index=True)	
	time =  models.DateTimeField(db_index=True)
	open =  models.FloatField(null=True, blank=True, default=None)
	high =  models.FloatField(null=True, blank=True, default=None)
	low = models.FloatField(null=True, blank=True, default=None)
	close = models.FloatField(null=True, blank=True, default=None)	
	volume =  models.BigIntegerField(null=True, blank=True, default=None)


class TicksManager(models.Manager):

	def create_tick(self,name,token,time,ltp,volume):
		self.create(name=name,token=token,time=time,ltp=ltp,volume=volume)
		
class Ticks(models.Model):
	name =  models.TextField()	
	token =  models.IntegerField(db_index=True)	
	time =  models.DateTimeField(db_index=True)
	ltp =  models.FloatField()	
	volume =  models.BigIntegerField()	
	objects = TicksManager()
