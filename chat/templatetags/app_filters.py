from django import template
import datetime

register = template.Library()

@register.filter
def parse_time(time):
	t = time
	t = t.strftime('%I:%M %p')
	return t