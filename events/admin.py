from django.contrib import admin
from .models import Event, BookTicket, UserProfile

admin.site.register(Event)
admin.site.register(BookTicket)
admin.site.register(UserProfile)
