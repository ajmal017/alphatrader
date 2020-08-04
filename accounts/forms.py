from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'UserName'
        }
    ),max_length=30, required=False, help_text='Letters,numbers and @#_-')	
	first_name = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'First Name'
        }
    ),max_length=30, required=False,)
	last_name = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Last Name'
        }
    ),max_length=30, required=False,)
	email = forms.EmailField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Email'
        }
    ),max_length=254, help_text='Required. Inform a valid email address.')
    
	password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class':'form-control',
        'placeholder':'Password'
        }
	),max_length=30, required=True,)

	password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class':'form-control',
        'placeholder':'Confirm Password'
        }
	),max_length=30, required=True,)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )