from django.contrib import admin
from .models import UserMeta


admin.site.register(
    UserMeta,
    list_display=["id", "user","meta_key", "meta_value"],
    list_display_links=["id", "user"],
)