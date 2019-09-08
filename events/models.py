from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Event(models.Model):
	title = models.CharField(max_length=105)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	tickets_available = models.PositiveIntegerField(default=1)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('detail', kwargs={'event_id':self.id})

class BookTicket(models.Model):
	tickets = models.PositiveIntegerField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return reverse('purchase', kwargs={'event_id':self.event.id})