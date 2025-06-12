from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta
import json

from .models import Movie, Theater, Show, Seat, Booking, BookingSeat, SeatType, Genre
from .forms import UserRegistrationForm, BookingForm

def home(request):
    """Homepage with featured movies and upcoming shows."""
    # Get featured movies (latest releases)
    featured_movies = Movie.objects.order_by('-release_date')[:6]
    
    # Get upcoming shows for the next 7 days
    today = timezone.now().date()
    upcoming_shows = Show.objects.filter(
        date__gte=today,
        date__lte=today + timedelta(days=7),
        is_active=True
    ).select_related('movie', 'theater').order_by('date', 'time')[:10]
    
    context = {
        'featured_movies': featured_movies,
        'upcoming_shows': upcoming_shows,
    }
    return render(request, 'booking/home.html', context)

def movie_list(request):
    """List all movies with filtering options."""
    # Get filter parameters
    genre = request.GET.get('genre')
    search_query = request.GET.get('search')
    
    # Base queryset
    movies = Movie.objects.all().prefetch_related('genres')
    
    # Apply filters
    if genre:
        movies = movies.filter(genres__name=genre)
    
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(movies, 12)  # Show 12 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all genres for filter dropdown
    genres = Genre.objects.all()
    
    context = {
        'page_obj': page_obj,
        'genres': genres,
        'current_genre': genre,
        'search_query': search_query,
    }
    return render(request, 'booking/movie_list.html', context)

def movie_detail(request, movie_id):
    """Movie detail page with show schedule."""
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Get upcoming shows for this movie
    today = timezone.now().date()
    shows = Show.objects.filter(
        movie=movie,
        date__gte=today,
        is_active=True
    ).select_related('theater').order_by('date', 'time')
    
    # Group shows by date
    shows_by_date = {}
    for show in shows:
        if show.date not in shows_by_date:
            shows_by_date[show.date] = []
        shows_by_date[show.date].append(show)
    
    context = {
        'movie': movie,
        'shows_by_date': shows_by_date,
    }
    return render(request, 'booking/movie_detail.html', context)

def theater_list(request):
    """List all theaters."""
    city = request.GET.get('city')
    theaters = Theater.objects.all()
    
    if city:
        theaters = theaters.filter(city__icontains=city)
    
    # Get unique cities for filter
    cities = Theater.objects.values_list('city', flat=True).distinct()
    
    context = {
        'theaters': theaters,
        'cities': cities,
        'current_city': city,
    }
    return render(request, 'booking/theater_list.html', context)

def theater_detail(request, theater_id):
    """Theater detail page with show schedule."""
    theater = get_object_or_404(Theater, id=theater_id)
    
    # Get upcoming shows for this theater
    today = timezone.now().date()
    shows = Show.objects.filter(
        theater=theater,
        date__gte=today,
        is_active=True
    ).select_related('movie').order_by('date', 'time')
    
    # Group shows by date
    shows_by_date = {}
    for show in shows:
        if show.date not in shows_by_date:
            shows_by_date[show.date] = []
        shows_by_date[show.date].append(show)
    
    context = {
        'theater': theater,
        'shows_by_date': shows_by_date,
    }
    return render(request, 'booking/theater_detail.html', context)

@login_required
def seat_selection(request, show_id):
    """Seat selection page for a specific show."""
    show = get_object_or_404(Show, id=show_id)
    
    # Check if show is in the future
    today = timezone.now().date()
    if show.date < today:
        messages.error(request, "This show has already passed.")
        return redirect('movie_detail', movie_id=show.movie.id)
    
    # Get all seats for this theater
    seats = Seat.objects.filter(theater=show.theater).select_related('seat_type')
    
    # Get already booked seats for this show
    booked_seats = BookingSeat.objects.filter(
        booking__show=show,
        booking__status__in=['pending', 'confirmed']
    ).values_list('seat_id', flat=True)
    
    # Organize seats by row
    seat_map = {}
    for seat in seats:
        if seat.row not in seat_map:
            seat_map[seat.row] = []
        
        seat_map[seat.row].append({
            'id': seat.id,
            'number': seat.number,
            'type': seat.seat_type.name,
            'price': float(show.base_price) * float(seat.seat_type.price_multiplier),
            'is_booked': seat.id in booked_seats
        })
    
    # Sort rows alphabetically and seats by number
    for row in seat_map:
        seat_map[row].sort(key=lambda x: x['number'])
    sorted_seat_map = {k: seat_map[k] for k in sorted(seat_map.keys())}
    
    # Get seat types for legend
    seat_types = SeatType.objects.all()
    
    context = {
        'show': show,
        'seat_map': sorted_seat_map,
        'seat_types': seat_types,
        'form': BookingForm()
    }
    return render(request, 'booking/seat_selection.html', context)

@login_required
def booking_confirmation(request, show_id):
    """Process booking confirmation."""
    if request.method != 'POST':
        return redirect('seat_selection', show_id=show_id)
    
    show = get_object_or_404(Show, id=show_id)
    form = BookingForm(request.POST)
    
    if form.is_valid():
        try:
            selected_seats = json.loads(form.cleaned_data['selected_seats'])
        except json.JSONDecodeError:
            messages.error(request, "Invalid seat selection data.")
            return redirect('seat_selection', show_id=show_id)
        
        if not selected_seats:
            messages.error(request, "Please select at least one seat.")
            return redirect('seat_selection', show_id=show_id)
        
        # Get seat objects
        seats = Seat.objects.filter(id__in=selected_seats)
        
        if len(seats) != len(selected_seats):
            messages.error(request, "Some selected seats are invalid.")
            return redirect('seat_selection', show_id=show_id)
        
        # Check if seats are still available
        booked_seats = BookingSeat.objects.filter(
            booking__show=show,
            booking__status__in=['pending', 'confirmed'],
            seat_id__in=selected_seats
        )
        
        if booked_seats.exists():
            messages.error(request, "Some of the selected seats are no longer available. Please try again.")
            return redirect('seat_selection', show_id=show_id)
        
        # Calculate total amount
        total_amount = sum(
            float(show.base_price) * float(seat.seat_type.price_multiplier)
            for seat in seats
        )
        
        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            show=show,
            total_amount=total_amount,
            status='confirmed'  # In production, this would be 'pending' until payment
        )
        
        # Add seats to booking
        for seat in seats:
            price = float(show.base_price) * float(seat.seat_type.price_multiplier)
            BookingSeat.objects.create(
                booking=booking,
                seat=seat,
                price=price
            )
        
        messages.success(request, "Booking confirmed successfully!")
        return redirect('booking_detail', booking_id=booking.id)
    
    messages.error(request, "There was an error with your booking. Please try again.")
    return redirect('seat_selection', show_id=show_id)

@login_required
def booking_detail(request, booking_id):
    """Booking detail page."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking_seats = BookingSeat.objects.filter(booking=booking).select_related('seat', 'seat__seat_type')
    
    context = {
        'booking': booking,
        'booking_seats': booking_seats,
    }
    return render(request, 'booking/booking_detail.html', context)

@login_required
def booking_history(request):
    """User's booking history."""
    bookings = Booking.objects.filter(user=request.user).select_related(
        'show', 'show__movie', 'show__theater'
    ).order_by('-booking_date')
    
    # Pagination
    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'booking/booking_history.html', context)

def register(request):
    """User registration."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome!")
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'booking/register.html', context)

# API endpoints for AJAX requests
@login_required
def get_seat_price(request):
    """API endpoint to get seat price."""
    if request.method == 'GET':
        seat_id = request.GET.get('seat_id')
        show_id = request.GET.get('show_id')
        
        try:
            seat = Seat.objects.get(id=seat_id)
            show = Show.objects.get(id=show_id)
            price = float(show.base_price) * float(seat.seat_type.price_multiplier)
            
            return JsonResponse({
                'success': True,
                'price': price,
                'seat_type': seat.seat_type.name,
                'seat_label': f"{seat.row}{seat.number}"
            })
        except (Seat.DoesNotExist, Show.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Invalid seat or show'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
