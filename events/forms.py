from django import forms
from django.contrib.auth.models import User
from .models import Event, BookTicket, UserProfile
from django.contrib.admin.widgets import AdminDateWidget

class UserSignup(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email' ,'password']

		widgets = {
			'password': forms.PasswordInput(),
		}


class UserLogin(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())

class EventUpdateForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['created_on',]


class BookingForm(forms.ModelForm):
	class Meta:
		model = BookTicket
		fields = ['tickets']


class CreateEventForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['owner',]


class EditProfileForm(forms.ModelForm):
	# bio = forms.CharField(required=False)
	class Meta:
		model = UserProfile
		exclude = ['user',]


class EditUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = fields = ['username', 'first_name', 'last_name', 'email']

