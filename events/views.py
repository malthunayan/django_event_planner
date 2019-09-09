from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.utils import timezone
from .forms import UserSignup, UserLogin, EventUpdateForm, BookingForm
from .models import Event, BookTicket

def home(request):
	return render(request, 'home.html')

class Signup(View):
	form_class = UserSignup
	template_name = 'signup.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()
			messages.success(request, "You have successfully signed up.")
			login(request, user)
			return redirect("home")
		messages.warning(request, form.errors)
		return redirect("signup")


class Login(View):
	form_class = UserLogin
	template_name = 'login.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				messages.success(request, "Welcome Back!")
				return redirect('dashboard')
			messages.warning(request, "Wrong email/password combination. Please try again.")
			return redirect("login")
		messages.warning(request, form.errors)
		return redirect("login")


class Logout(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		messages.success(request, "You have successfully logged out.")
		return redirect("login")

def dashboard(request):
	if request.user.is_anonymous:
		return redirect('login')
	my_upcoming_bookings = BookTicket.objects.filter(user=request.user)
	my_past_bookings = BookTicket.objects.filter(user=request.user)
	my_events = Event.objects.filter(owner=request.user)
	context = {
		'my_upcoming_bookings': my_upcoming_bookings,
		'my_past_bookings': my_past_bookings,
		'my_events': my_events,
	}
	return render(request, 'dashboard.html', context)

def detail(request, event_id):
	event = Event.objects.get(id=event_id)
	form = EventUpdateForm(instance=event)
	if request.user.is_anonymous:
		return redirect('login')
	elif not (request.user.is_staff or request.user == event.owner):
		return render(request, 'detail.html', {'event': event})
	else:
		if request.method == 'POST':
			form = EventUpdateForm(request.POST, instance=event)
			if form.is_valid():
				form.save()
				messages.success(request, "You have successfully updated the event.")
				return redirect('detail')
	context = {
		'event': event,
		'form': form,
		'start_date': event.occurance.strftime("%b. %d, %Y"),
		'start_time': event.occurance.strftime("%I:%M %p"),
	}
	return render(request, 'detail.html', context)

def book(request, event_id):
	event = Event.objects.get(id=event_id)
	form = BookingForm()
	if request.method == "POST":
		form = BookingForm(request.POST)
		if form.is_valid():
			book=form.save(commit=False)
			book.user = request.user
			book.event = event
			if book.tickets <= event.tickets_available:
				event.tickets_available = event.tickets_available - book.tickets
				event.save()
				book.save()
			else:
				messages.warning(request, "You have exceeded the number of tickets available.")
				return redirect(book)
			return redirect(book.event)
	context = {
		'event': event,
		'form': form,
	}
	return render(request, 'book.html', context)

def list(request):
	context = {
		'events': Event.objects.all(),
	}
	return render(request, 'list.html', context)