from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.utils import timezone
from django.db.models import Q
from .forms import (UserSignup, UserLogin, EventUpdateForm, BookingForm,
	CreateEventForm, EditProfileForm, EditUserForm)
from .models import Event, BookTicket, UserProfile

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
			return redirect("events:home")
		messages.warning(request, form.errors)
		return redirect("events:signup")


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
				return redirect('events:dashboard')
			messages.warning(request, "Wrong email/password combination. Please try again.")
			return redirect("events:login")
		messages.warning(request, form.errors)
		return redirect("events:login")


class Logout(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		messages.success(request, "You have successfully logged out.")
		return redirect("events:login")

def dashboard(request):
	if request.user.is_anonymous:
		return redirect('events:login')

	user = request.user
	my_upcoming_bookings = user.attended.filter(event__occurance__gte=timezone.now())
	my_past_bookings = user.attended.filter(event__occurance__lt=timezone.now())
	my_events = user.events.all()
	context = {
		'my_upcoming_bookings': my_upcoming_bookings,
		'my_past_bookings': my_past_bookings,
		'my_events': my_events,
	}
	return render(request, 'dashboard.html', context)

def detail(request, event_id):
	if request.user.is_anonymous:
		return redirect('events:login')
	event = Event.objects.get(id=event_id)
	context = {
		'event': event,
		'bookings': event.bookings.all(),
	}
	return render(request, 'detail.html', context)

def update(request, event_id):
	event = Event.objects.get(id=event_id)
	form = EventUpdateForm(instance=event)
	if request.method == 'POST':
		form = EventUpdateForm(request.POST, instance=event)
		if form.is_valid():
			form.save()
			messages.success(request, "You have successfully updated the event.")
			return redirect(event)
	context = {
		'event': event,
		'form': form,
	}
	return render(request, 'update.html', context)

def profile(request):
	if request.user.is_anonymous:
		return redirect('events:login')
	context = {
		'user': request.user.userprofile
	}
	return render(request, 'profile.html', context)

def book(request, event_id):
	event = Event.objects.get(id=event_id)
	form = BookingForm()
	if request.method == "POST":
		form = BookingForm(request.POST)
		if form.is_valid():
			book=form.save(commit=False)
			if event.full():
				messages.warning(request, "You have exceeded the maximum number of tickets available.")
				return redirect("events:list")
			book.user = request.user
			book.event = event
			book.save()
			return redirect(book.event)
	context = {
		'event': event,
		'form': form,
	}
	return render(request, 'book.html', context)

def list(request):
	events = Event.objects.filter(occurance__gte=timezone.now())
	query = request.GET.get("q")
	if query:
		events = events.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(owner__username__icontains=query)
			).distinct()
	context = {
		'events': events,
	}
	return render(request, 'list.html', context)

def create(request):
	if request.user.is_anonymous:
		return redirect("events:login")
	form = CreateEventForm()
	if request.method == "POST":
		form = CreateEventForm(request.POST, request.FILES)
		if form.is_valid():
			event = form.save(commit=False)
			event.owner = request.user
			event.save()
			return redirect("events:list")
	context = {
		"form": form,
	}
	return render(request, "create.html", context)

def edit_profile(request):
	if request.user.is_anonymous:
		return redirect('events:login')
	user = request.user
	profile_form = EditProfileForm(instance=user.userprofile)
	user_form = EditUserForm(instance=user)
	if request.method == 'POST':
		profile_form = EditProfileForm(request.POST, request.FILES, instance=user.userprofile)
		user_form = EditUserForm(request.POST, instance=user)
		if profile_form.is_valid() and user_form.is_valid():
			profile_form.save()
			user_form.save()
			messages.success(request, "You have successfully updated your profile.")
			return redirect('events:edit-profile')
	context = {
		'profile_form': profile_form,
		'user_form': user_form,
		'user': user,
	}
	return render(request, 'edit_profile.html')

def cancel_booking(request, booking_id):
	BookTicket.objects.filter(event__occurance__gte=timezone.now()).get(id=booking_id).delete()
	return redirect("events:dashboard")