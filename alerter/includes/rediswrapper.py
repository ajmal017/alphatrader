import redis
from django.conf import settings

class RedisWrapper(object):
	shared_state = {}

	def __init__(self):
		self.__dict__ = self.shared_state

	def redis_connect(self, server_key):
		redis_server_conf = settings.REDIS_SERVER_CONF['servers'][server_key]
		connection_pool = redis.ConnectionPool(
			host=redis_server_conf['HOST'],
			port=redis_server_conf['PORT'],
			db=redis_server_conf['DATABASE']
		)
		return redis.StrictRedis(connection_pool=connection_pool)