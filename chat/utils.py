from functools import wraps

from .exceptions import ClientError
from .models import AlphaChannel


def catch_client_error(func):
	"""
	Decorator to catch the ClientError exception and translate it into a reply.
	"""
	@wraps(func)
	def inner(message, args, **kwargs):
		try:
			return func(message, args, **kwargs)
		except ClientError as e:
			# If we catch a client error, tell it to send an error string
			# back to the client on their reply channel
			e.send_to(message.reply_channel)
	return inner


def get_channel_or_error(channel_id, user):
	"""
	Tries to fetch a channel for the user, checking permissions along the way.
	"""
	# Check if the user is logged in
	if not user.is_authenticated():
		raise ClientError("USER_HAS_TO_LOGIN")
	# Find the room they requested (by ID)
	try:
		apchannel = AlphaChannel.objects.get(pk=channel_id)
	except AlphaChannel.DoesNotExist:
		raise ClientError("CHANNEL_INVALID")
	# Check permissions
	if apchannel.admin_only and not user.is_admin:
		raise ClientError("CHANNEL_ACCESS_DENIED")
	return apchannel