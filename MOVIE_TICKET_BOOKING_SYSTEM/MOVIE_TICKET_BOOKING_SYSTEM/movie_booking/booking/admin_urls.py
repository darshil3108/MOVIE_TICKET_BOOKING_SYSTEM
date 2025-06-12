from django.urls import path
from . import admin_views

urlpatterns = [
    # Dashboard
    path('admin-panel/', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Movie Management
    path('admin-panel/movies/', admin_views.admin_movie_list, name='admin_movie_list'),
    path('admin-panel/movies/add/', admin_views.admin_movie_add, name='admin_movie_add'),
    path('admin-panel/movies/<int:movie_id>/edit/', admin_views.admin_movie_edit, name='admin_movie_edit'),
    path('admin-panel/movies/<int:movie_id>/delete/', admin_views.admin_movie_delete, name='admin_movie_delete'),
    
    # Theater Management
    path('admin-panel/theaters/', admin_views.admin_theater_list, name='admin_theater_list'),
    path('admin-panel/theaters/add/', admin_views.admin_theater_add, name='admin_theater_add'),
    path('admin-panel/theaters/<int:theater_id>/edit/', admin_views.admin_theater_edit, name='admin_theater_edit'),
    path('admin-panel/theaters/<int:theater_id>/delete/', admin_views.admin_theater_delete, name='admin_theater_delete'),
    
    # Show Management
    path('admin-panel/shows/', admin_views.admin_show_list, name='admin_show_list'),
    path('admin-panel/shows/add/', admin_views.admin_show_add, name='admin_show_add'),
    path('admin-panel/shows/<int:show_id>/edit/', admin_views.admin_show_edit, name='admin_show_edit'),
    path('admin-panel/shows/<int:show_id>/delete/', admin_views.admin_show_delete, name='admin_show_delete'),
    
    # Seat Management
    path('admin-panel/seats/', admin_views.admin_seat_list, name='admin_seat_list'),
    path('admin-panel/seats/add/', admin_views.admin_seat_add, name='admin_seat_add'),
    path('admin-panel/seats/bulk-add/', admin_views.admin_seat_bulk_add, name='admin_seat_bulk_add'),
    
    # Booking Management
    path('admin-panel/bookings/', admin_views.admin_booking_list, name='admin_booking_list'),
    path('admin-panel/bookings/<int:booking_id>/', admin_views.admin_booking_detail, name='admin_booking_detail'),
    path('admin-panel/bookings/<int:booking_id>/update-status/', admin_views.admin_booking_update_status, name='admin_booking_update_status'),
    
    # Genre Management
    path('admin-panel/genres/', admin_views.admin_genre_list, name='admin_genre_list'),
    path('admin-panel/genres/add/', admin_views.admin_genre_add, name='admin_genre_add'),
    
    # Seat Type Management
    path('admin-panel/seat-types/', admin_views.admin_seat_type_list, name='admin_seat_type_list'),
    path('admin-panel/seat-types/add/', admin_views.admin_seat_type_add, name='admin_seat_type_add'),
    
    # User Management
    path('admin-panel/users/', admin_views.admin_user_list, name='admin_user_list'),
    path('admin-panel/users/<int:user_id>/edit/', admin_views.admin_user_edit, name='admin_user_edit'),
    
    # API Endpoints
    path('admin-panel/api/theaters/<int:theater_id>/seats/', admin_views.admin_api_theater_seats, name='admin_api_theater_seats'),
    path('admin-panel/api/shows/<int:show_id>/bookings/', admin_views.admin_api_show_bookings, name='admin_api_show_bookings'),
]
