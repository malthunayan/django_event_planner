from django import forms
from django.contrib.auth.models import User
from .models import Event, BookTicket

class UserSignup(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email' ,'password']

		widgets={
		'password': forms.PasswordInput(),
		}


class UserLogin(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())

class EventUpdateForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['created_on', 'tickets']

		def clean(self):
			tickets = self.cleaned_data.get('tickets')
			if tickets and tickets.count() > maximum_number_of_tickets:
				raise ValidationError('Must be less than %s'%(maximum_number_of_tickets-tickets))
			return self.cleaned_data

class BookingForm(forms.ModelForm):
	class Meta:
		model = BookTicket
		fields = ['tickets']