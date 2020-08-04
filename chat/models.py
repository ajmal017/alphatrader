from django.db import models
from django.utils.six import python_2_unicode_compatible
# from channels import Group
from .settings import MSG_TYPE_MESSAGE
from django.contrib.auth import get_user_model

User = get_user_model()

@python_2_unicode_compatible
class AlphaChannel(models.Model):
	"""
	A channel for people to chat in.
	"""
	# Channel title
	name = models.CharField(max_length=255)
	type = models.IntegerField(default=0)
	owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	# private channel
	private = models.BooleanField(default=False)
	admin_only = models.BooleanField(default=False)

	def str(self):
		return self.name

	@property
	def websocket_group(self):
		"""
		Returns the Channels Group that sockets should subscribe to to get sent
		messages as they are generated.
		"""
		# return Group("channel-%s" % self.id)

	def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
		"""
		Called to send a message to the room on behalf of a user.
		"""
		final_msg = {'channel': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}

		# Send out the message to everyone in the room
		self.websocket_group.send(
			{"text": json.dumps(final_msg)}
		)

class MessageManager(models.Manager):

	# def create(self,message,user,channel,mtype,remarks=None):
	# 	self.create(message=message,user=user,channel=channel,type=mtype,remarks=remarks)

	def get_last_message(self,broker):
		try:
			row = self.filter(broker=broker).order_by("-id")[0]
			return int(row.message_id)
		except Exception as e:
			return None

class Message(models.Model):
	text =  models.TextField(null=False)  
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	channel =  models.ForeignKey(AlphaChannel, on_delete=models.SET_NULL, null=True)
	type =  models.IntegerField(default=0)
	posted_at =  models.DateTimeField(db_index=True)
	remarks = models.TextField(null=True, blank=True, default=None)
	objects = MessageManager()
