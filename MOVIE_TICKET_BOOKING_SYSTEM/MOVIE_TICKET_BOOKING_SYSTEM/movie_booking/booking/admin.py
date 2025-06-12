from django.contrib import admin
from .models import (
    Genre, Movie, Theater, Show, SeatType, 
    Seat, Booking, BookingSeat, UserProfile
)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'release_date', 'rating')
    list_filter = ('genres', 'release_date')
    search_fields = ('title', 'description')
    filter_horizontal = ('genres',)
    date_hierarchy = 'release_date'

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'total_capacity', 'contact_number')
    list_filter = ('city',)
    search_fields = ('name', 'address', 'city')

@admin.register(SeatType)
class SeatTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_multiplier')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('theater', 'row', 'number', 'seat_type')
    list_filter = ('theater', 'seat_type', 'row')
    search_fields = ('theater__name', 'row', 'number')

class BookingSeatInline(admin.TabularInline):
    model = BookingSeat
    extra = 0
    readonly_fields = ('price',)

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater', 'date', 'time', 'base_price', 'is_active')
    list_filter = ('date', 'is_active', 'theater', 'movie')
    search_fields = ('movie__title', 'theater__name')
    date_hierarchy = 'date'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'show', 'booking_date', 'status', 'total_amount')
    list_filter = ('status', 'booking_date', 'show__movie', 'show__theater')
    search_fields = ('user__username', 'show__movie__title')
    inlines = [BookingSeatInline]
    date_hierarchy = 'booking_date'
    readonly_fields = ('booking_date', 'total_amount')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'date_of_birth')
    search_fields = ('user__username', 'user__email', 'phone_number')
