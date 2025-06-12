from django.urls import path, include
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('theaters/', views.theater_list, name='theater_list'),
    path('theaters/<int:theater_id>/', views.theater_detail, name='theater_detail'),
    
    # Booking flow
    path('shows/<int:show_id>/seats/', views.seat_selection, name='seat_selection'),
    path('shows/<int:show_id>/book/', views.booking_confirmation, name='booking_confirmation'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/history/', views.booking_history, name='booking_history'),
    
    # Authentication
    path('register/', views.register, name='register'),
    
    # API endpoints
    path('api/get-seat-price/', views.get_seat_price, name='get_seat_price'),
    
    # Admin URLs
    path('', include('booking.admin_urls')),
]
