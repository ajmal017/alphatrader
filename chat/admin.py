from django.contrib import admin
from .models import AlphaChannel,Message


admin.site.register(
    AlphaChannel,
    list_display=["id", "name","owner", "private"],
    list_display_links=["id", "name"],
)

admin.site.register(
    Message,
    list_display=["id", "text","user", "channel","type","posted_at"],
    list_display_links=["id", "text","user","channel"],
)