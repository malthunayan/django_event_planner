from rest_framework import serializers
from events.models import Event, BookTicket
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class AttendeesSerializer(serializers.ModelSerializer):
	user = serializers.SlugRelatedField(
			slug_field = 'username',
			read_only= True,
	)
	class Meta:
		model = BookTicket
		exclude = ['id']


class MyEventsListSerializer(serializers.ModelSerializer):
	bookings = AttendeesSerializer(many=True)
	class Meta:
		model = Event
		fields = ['title', 'occurance', 'bookings', ]


class EventListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ['title', 'occurance']


class BookListSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookTicket
		exclude = ['user', 'id']


class BookEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookTicket
		fields = ['tickets', 'event']

	def create(self, validated_data):
		tickets = validated_data['tickets']
		event = validated_data['event']
		if tickets <= event.tickets_available:
			event.tickets_available -= tickets
			event.save()
		else:
			raise ValidationError('You have exceeded the maximum number of available tickets.')
		return validated_data


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username', 'password', 'first_name', 'last_name']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		first_name = validated_data['first_name']
		last_name = validated_data['last_name']
		new_user = User(username=username, first_name=first_name, last_name=last_name)
		new_user.set_password(password)
		new_user.save()
		return validated_data


class CreateEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		exclude = ['owner', 'created_on']

