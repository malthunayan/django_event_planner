from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save


class Event(models.Model):
	title = models.CharField(max_length=105)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
	content = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	tickets_available = models.PositiveIntegerField()
	occurance = models.DateTimeField()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('events:detail', kwargs={'event_id':self.id})

	def tickets_booked(self):
		num_tickets = self.bookings.all()
		total = 0
		for num in num_tickets:
			total+=1
		return total

	def tickets_left(self):
		return self.tickets_available - self.tickets_booked()

	def full(self):
		return self.tickets_left() == 0


class BookTicket(models.Model):
	tickets = models.PositiveIntegerField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attended')
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
	purchase_date = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return reverse('purchase', kwargs={'event_id':self.event.id})

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(blank=True, null=True)
	bio = models.CharField(max_length=270, default='', null=True, blank=True)

	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse('events:profile')

def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = UserProfile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)

