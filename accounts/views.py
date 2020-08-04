from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from accounts.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout


# Create your views here.

@user_passes_test(lambda user: not user.username, login_url='/channels/', redirect_field_name=None)
def login(request):
	c = {}
	retry = request.GET.get('retry','')
	if retry:
		retry = True
	else:
		retry = False
	c.update(csrf(request))

	c.update({'retry':retry})
	return render_to_response('accounts/login.html',c)

def auth_view(request):
	username = request.POST.get('username','')
	password = request.POST.get('password','')	
	user = auth.authenticate(username=username,password=password)

	if user is not None:
		auth.login(request,user)
		return HttpResponseRedirect('/dashboard/')
	else:
		return HttpResponseRedirect('/login/?retry=1')

def _logout(request):
	c = {}
	logout(request)
	return HttpResponseRedirect('/login/?loggedout=1')

def invalid(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('accounts/invalid.html',c)

@user_passes_test(lambda user: not user.username, login_url='/channels/', redirect_field_name=None)
def register(request):
	c = {}
	c.update(csrf(request))	
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = auth.authenticate(username=username, password=raw_password)		
			auth.login(request, user)
			# return HttpResponseRedirect('/verify/')
			return HttpResponseRedirect('/channels/')
	else:
		form = RegisterForm()
	c.update({'form': form})
	return render_to_response('accounts/register.html',c)