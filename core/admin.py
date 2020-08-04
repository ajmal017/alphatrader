from django.contrib import admin
from .models import Options,Historical1D,Instruments


admin.site.register(
    Options,
    list_display=["id", "option_name","option_value"],
    list_display_links=["id", "option_name"],
)

admin.site.register(
    Historical1D,
    list_display=["id", "name","time","open","high","low","close","volume"],
    list_display_links=["id", "name"],
)

admin.site.register(
    Instruments,
    list_display=["id", "name"],
    list_display_links=["id", "name"],
)