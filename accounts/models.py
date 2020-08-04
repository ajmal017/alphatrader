from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class UserMeta(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	meta_key = models.CharField(max_length=255)
	meta_value = models.TextField(null=True, blank=True, default=None)
