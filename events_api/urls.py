from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

app_name='events_api'

urlpatterns = [
	path('list/', views.List.as_view(), name='list'),
	path('list/my_events/', views.MyEvents.as_view(), name='my-events'),
	path('list/my_bookings/', views.MyBookings.as_view(), name='my-bookings'),
	path('login/', TokenObtainPairView.as_view(), name='login'),
	path('register/', views.Register.as_view(), name='register'),
	path('create/', views.CreateEvent.as_view(), name='create'),
	path('update/<int:event_id>/', views.UpdateEvent.as_view(), name='update'),
	path('book/event/', views.BookEvent.as_view(), name='book'),
]