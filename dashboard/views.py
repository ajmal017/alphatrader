from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import redirect
from chat.models import Message,AlphaChannel
from accounts.models import UserMeta
import json
# Create your views here.
class DashboardView(TemplateView):
	template_name = "dashboard/index.html"
	
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('/login/?source=dashboard')
		return super(DashboardView, self).dispatch(request, *args, **kwargs)

class ProfileView(TemplateView):
	template_name = "dashboard/profile.html"
	
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('/login/?source=dashboard')
		return super(ProfileView, self).dispatch(request, *args, **kwargs)

class ChannelView(TemplateView):
	template_name = "dashboard/channels.html"

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		username = request.user.username
		context['username'] = username
		context['subscribed'] = False	

		try:
			chname = self.kwargs['chname']
		except:
			chname = None

		#Check if on root /channels/ page and redirect to default channel
		if chname:
			chnl = self.get_channel(chname)
			context['chname'] = chname

			#Check if logged in and show specific template
			if username:
				try:
					usermeta = UserMeta.objects.get(user__username=request.user.username,meta_key="alpha_subsc_chnls")
				except UserMeta.DoesNotExist:
					usermeta = None		

				if usermeta:
					context['subsc_chnls'] = json.loads(usermeta.meta_value)

					if any(d['name'] == chname for d in context['subsc_chnls']):
						context['subscribed'] = True
			
			#Check if channel exists and show specific template							
			if chnl:
				context['chnl'] = True

				context['latest_msgs'] = Message.objects.filter(channel__name=chname).order_by('-id')[:10][::-1]
				return self.render_to_response(context)
			else:
				#Show create channel CTA
				context['chnl'] = False

				return self.render_to_response(context)
				
		else:
			try:
				usermeta = UserMeta.objects.get(user__username=request.user.username,meta_key="alpha_subsc_chnls")
			except UserMeta.DoesNotExist:
				usermeta = None		

			if usermeta:
				sub_chnls = json.loads(usermeta.meta_value)
				return redirect('/channels/'+sub_chnls[0]['name'])
			else:				
				return self.render_to_response(context)


	
	def get_channel(self,name):
		try:
			channel = AlphaChannel.objects.get(name=name)
		except AlphaChannel.DoesNotExist:
			channel = None	

		return channel	

	# def dispatch(self, request, *args, **kwargs):
	# 	if not request.user.is_authenticated:
	# 		return redirect('/login/?source=dashboard')
	# 	return super(ChannelView, self).dispatch(request, *args, **kwargs)