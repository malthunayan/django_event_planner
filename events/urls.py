from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('detail/<int:event_id>/', views.detail, name='detail'),
    path('purchase/<int:event_id>/', views.book, name='purchase'),
    path('list/', views.list, name='list'),
    path('update/<int:event_id>/', views.update, name='update'),
    path('create/', views.create, name='create'),
]