from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from events.models import Event, BookTicket
from .serializers import (EventListSerializer, BookListSerializer, RegisterSerializer, 
	CreateEventSerializer, MyEventsListSerializer, BookEventSerializer
	)
from .permissions import IsEventOwner

# Create your views here.
class List(ListAPIView):
	queryset = Event.objects.filter(occurance__gte=timezone.now())
	serializer_class = EventListSerializer

class MyEvents(ListAPIView):
	serializer_class = MyEventsListSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Event.objects.filter(owner=self.request.user, occurance__gte=timezone.now())

class MyBookings(ListAPIView):
	serializer_class = BookListSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return BookTicket.objects.filter(user=self.request.user)

class Register(CreateAPIView):
	serializer_class = RegisterSerializer

	# def perform_create(self, serializer):
	# 	queryset = SignupRequest.objects.filter(user=self.request.user)
	# 	if queryset.exist():
	# 		raise ValidationError('You have already signed up')
	# 	serializer.save(user=self.request.user)

class CreateEvent(CreateAPIView):
	serializer_class = CreateEventSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)

class UpdateEvent(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = CreateEventSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [IsAuthenticated, IsEventOwner]

class BookEvent(CreateAPIView):
	serializer_class = BookEventSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)