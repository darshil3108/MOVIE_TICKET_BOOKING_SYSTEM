from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import json

from .decorators import admin_required, superuser_required
from .models import Movie, Theater, Show, Genre, SeatType, Seat, Booking, BookingSeat
from .admin_forms import (
    MovieForm, TheaterForm, ShowForm, GenreForm, SeatTypeForm, 
    SeatForm, BulkSeatForm, UserForm
)

@admin_required
def admin_dashboard(request):
    """Admin dashboard with statistics."""
    # Get statistics
    total_movies = Movie.objects.count()
    total_theaters = Theater.objects.count()
    total_bookings = Booking.objects.count()
    total_revenue = Booking.objects.filter(status='confirmed').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    # Recent bookings
    recent_bookings = Booking.objects.select_related(
        'user', 'show__movie', 'show__theater'
    ).order_by('-booking_date')[:10]
    
    # Popular movies (by booking count)
    popular_movies = Movie.objects.annotate(
        booking_count=Count('shows__bookings')
    ).order_by('-booking_count')[:5]
    
    # Upcoming shows today
    today = timezone.now().date()
    today_shows = Show.objects.filter(
        date=today, is_active=True
    ).select_related('movie', 'theater').order_by('time')[:10]
    
    context = {
        'total_movies': total_movies,
        'total_theaters': total_theaters,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'popular_movies': popular_movies,
        'today_shows': today_shows,
    }
    return render(request, 'booking/admin/dashboard.html', context)

# Movie Management Views
@admin_required
def admin_movie_list(request):
    """List all movies with search and filter."""
    search_query = request.GET.get('search', '')
    genre_filter = request.GET.get('genre', '')
    
    movies = Movie.objects.all().prefetch_related('genres')
    
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if genre_filter:
        movies = movies.filter(genres__name=genre_filter)
    
    # Pagination
    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    genres = Genre.objects.all()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'genre_filter': genre_filter,
        'genres': genres,
    }
    return render(request, 'booking/admin/movie_list.html', context)

@admin_required
def admin_movie_add(request):
    """Add new movie."""
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            messages.success(request, f'Movie "{movie.title}" added successfully!')
            return redirect('admin_movie_list')
    else:
        form = MovieForm()
    
    context = {'form': form, 'title': 'Add Movie'}
    return render(request, 'booking/admin/movie_form.html', context)

@admin_required
def admin_movie_edit(request, movie_id):
    """Edit existing movie."""
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save()
            messages.success(request, f'Movie "{movie.title}" updated successfully!')
            return redirect('admin_movie_list')
    else:
        form = MovieForm(instance=movie)
    
    context = {'form': form, 'title': 'Edit Movie', 'movie': movie}
    return render(request, 'booking/admin/movie_form.html', context)

@admin_required
def admin_movie_delete(request, movie_id):
    """Delete movie."""
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'POST':
        movie_title = movie.title
        movie.delete()
        messages.success(request, f'Movie "{movie_title}" deleted successfully!')
        return redirect('admin_movie_list')
    
    context = {'movie': movie}
    return render(request, 'booking/admin/movie_delete.html', context)

# Theater Management Views
@admin_required
def admin_theater_list(request):
    """List all theaters."""
    search_query = request.GET.get('search', '')
    city_filter = request.GET.get('city', '')
    
    theaters = Theater.objects.all()
    
    if search_query:
        theaters = theaters.filter(
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    if city_filter:
        theaters = theaters.filter(city__icontains=city_filter)
    
    # Pagination
    paginator = Paginator(theaters, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    cities = Theater.objects.values_list('city', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'city_filter': city_filter,
        'cities': cities,
    }
    return render(request, 'booking/admin/theater_list.html', context)

@admin_required
def admin_theater_add(request):
    """Add new theater."""
    if request.method == 'POST':
        form = TheaterForm(request.POST)
        if form.is_valid():
            theater = form.save()
            messages.success(request, f'Theater "{theater.name}" added successfully!')
            return redirect('admin_theater_list')
    else:
        form = TheaterForm()
    
    context = {'form': form, 'title': 'Add Theater'}
    return render(request, 'booking/admin/theater_form.html', context)

@admin_required
def admin_theater_edit(request, theater_id):
    """Edit existing theater."""
    theater = get_object_or_404(Theater, id=theater_id)
    
    if request.method == 'POST':
        form = TheaterForm(request.POST, instance=theater)
        if form.is_valid():
            theater = form.save()
            messages.success(request, f'Theater "{theater.name}" updated successfully!')
            return redirect('admin_theater_list')
    else:
        form = TheaterForm(instance=theater)
    
    context = {'form': form, 'title': 'Edit Theater', 'theater': theater}
    return render(request, 'booking/admin/theater_form.html', context)

@admin_required
def admin_theater_delete(request, theater_id):
    """Delete theater."""
    theater = get_object_or_404(Theater, id=theater_id)
    
    if request.method == 'POST':
        theater_name = theater.name
        theater.delete()
        messages.success(request, f'Theater "{theater_name}" deleted successfully!')
        return redirect('admin_theater_list')
    
    context = {'theater': theater}
    return render(request, 'booking/admin/theater_delete.html', context)

# Show Management Views
@admin_required
def admin_show_list(request):
    """List all shows."""
    date_filter = request.GET.get('date', '')
    theater_filter = request.GET.get('theater', '')
    movie_filter = request.GET.get('movie', '')
    
    shows = Show.objects.select_related('movie', 'theater').all()
    
    if date_filter:
        shows = shows.filter(date=date_filter)
    
    if theater_filter:
        shows = shows.filter(theater_id=theater_filter)
    
    if movie_filter:
        shows = shows.filter(movie_id=movie_filter)
    
    # Pagination
    paginator = Paginator(shows, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    theaters = Theater.objects.all()
    movies = Movie.objects.all()
    
    context = {
        'page_obj': page_obj,
        'date_filter': date_filter,
        'theater_filter': theater_filter,
        'movie_filter': movie_filter,
        'theaters': theaters,
        'movies': movies,
    }
    return render(request, 'booking/admin/show_list.html', context)

@admin_required
def admin_show_add(request):
    """Add new show."""
    if request.method == 'POST':
        form = ShowForm(request.POST)
        if form.is_valid():
            show = form.save()
            messages.success(request, f'Show for "{show.movie.title}" added successfully!')
            return redirect('admin_show_list')
    else:
        form = ShowForm()
    
    context = {'form': form, 'title': 'Add Show'}
    return render(request, 'booking/admin/show_form.html', context)

@admin_required
def admin_show_edit(request, show_id):
    """Edit existing show."""
    show = get_object_or_404(Show, id=show_id)
    
    if request.method == 'POST':
        form = ShowForm(request.POST, instance=show)
        if form.is_valid():
            show = form.save()
            messages.success(request, f'Show for "{show.movie.title}" updated successfully!')
            return redirect('admin_show_list')
    else:
        form = ShowForm(instance=show)
    
    context = {'form': form, 'title': 'Edit Show', 'show': show}
    return render(request, 'booking/admin/show_form.html', context)

@admin_required
def admin_show_delete(request, show_id):
    """Delete show."""
    show = get_object_or_404(Show, id=show_id)
    
    if request.method == 'POST':
        show_info = f"{show.movie.title} at {show.theater.name}"
        show.delete()
        messages.success(request, f'Show "{show_info}" deleted successfully!')
        return redirect('admin_show_list')
    
    context = {'show': show}
    return render(request, 'booking/admin/show_delete.html', context)

# Seat Management Views
@admin_required
def admin_seat_list(request):
    """List all seats."""
    theater_filter = request.GET.get('theater', '')
    seat_type_filter = request.GET.get('seat_type', '')
    
    seats = Seat.objects.select_related('theater', 'seat_type').all()
    
    if theater_filter:
        seats = seats.filter(theater_id=theater_filter)
    
    if seat_type_filter:
        seats = seats.filter(seat_type_id=seat_type_filter)
    
    # Pagination
    paginator = Paginator(seats, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    theaters = Theater.objects.all()
    seat_types = SeatType.objects.all()
    
    context = {
        'page_obj': page_obj,
        'theater_filter': theater_filter,
        'seat_type_filter': seat_type_filter,
        'theaters': theaters,
        'seat_types': seat_types,
    }
    return render(request, 'booking/admin/seat_list.html', context)

@admin_required
def admin_seat_add(request):
    """Add new seat."""
    if request.method == 'POST':
        form = SeatForm(request.POST)
        if form.is_valid():
            seat = form.save()
            messages.success(request, f'Seat {seat.row}{seat.number} added successfully!')
            return redirect('admin_seat_list')
    else:
        form = SeatForm()
    
    context = {'form': form, 'title': 'Add Seat'}
    return render(request, 'booking/admin/seat_form.html', context)

@admin_required
def admin_seat_bulk_add(request):
    """Bulk add seats for a theater."""
    if request.method == 'POST':
        form = BulkSeatForm(request.POST)
        if form.is_valid():
            theater = form.cleaned_data['theater']
            rows = [row.strip().upper() for row in form.cleaned_data['rows'].split(',')]
            seats_per_row = form.cleaned_data['seats_per_row']
            seat_type = form.cleaned_data['seat_type']
            
            created_count = 0
            for row in rows:
                for seat_num in range(1, seats_per_row + 1):
                    seat, created = Seat.objects.get_or_create(
                        theater=theater,
                        row=row,
                        number=seat_num,
                        defaults={'seat_type': seat_type}
                    )
                    if created:
                        created_count += 1
            
            messages.success(request, f'{created_count} seats created successfully!')
            return redirect('admin_seat_list')
    else:
        form = BulkSeatForm()
    
    context = {'form': form, 'title': 'Bulk Add Seats'}
    return render(request, 'booking/admin/seat_bulk_form.html', context)

# Booking Management Views
@admin_required
def admin_booking_list(request):
    """List all bookings."""
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')
    user_filter = request.GET.get('user', '')
    
    bookings = Booking.objects.select_related(
        'user', 'show__movie', 'show__theater'
    ).all()
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    if date_filter:
        bookings = bookings.filter(booking_date__date=date_filter)
    
    if user_filter:
        bookings = bookings.filter(
            Q(user__username__icontains=user_filter) |
            Q(user__first_name__icontains=user_filter) |
            Q(user__last_name__icontains=user_filter)
        )
    
    # Pagination
    paginator = Paginator(bookings, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'user_filter': user_filter,
        'status_choices': Booking.STATUS_CHOICES,
    }
    return render(request, 'booking/admin/booking_list.html', context)

@admin_required
def admin_booking_detail(request, booking_id):
    """View booking details."""
    booking = get_object_or_404(Booking, id=booking_id)
    booking_seats = BookingSeat.objects.filter(booking=booking).select_related('seat')
    
    context = {
        'booking': booking,
        'booking_seats': booking_seats,
    }
    return render(request, 'booking/admin/booking_detail.html', context)

@admin_required
def admin_booking_update_status(request, booking_id):
    """Update booking status."""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()
            messages.success(request, f'Booking status updated to {new_status}!')
        else:
            messages.error(request, 'Invalid status!')
    
    return redirect('admin_booking_detail', booking_id=booking_id)

# Genre and Seat Type Management
@admin_required
def admin_genre_list(request):
    """List all genres."""
    genres = Genre.objects.all()
    
    context = {'genres': genres}
    return render(request, 'booking/admin/genre_list.html', context)

@admin_required
def admin_genre_add(request):
    """Add new genre."""
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.save()
            messages.success(request, f'Genre "{genre.name}" added successfully!')
            return redirect('admin_genre_list')
    else:
        form = GenreForm()
    
    context = {'form': form, 'title': 'Add Genre'}
    return render(request, 'booking/admin/genre_form.html', context)

@admin_required
def admin_seat_type_list(request):
    """List all seat types."""
    seat_types = SeatType.objects.all()
    
    context = {'seat_types': seat_types}
    return render(request, 'booking/admin/seat_type_list.html', context)

@admin_required
def admin_seat_type_add(request):
    """Add new seat type."""
    if request.method == 'POST':
        form = SeatTypeForm(request.POST)
        if form.is_valid():
            seat_type = form.save()
            messages.success(request, f'Seat type "{seat_type.name}" added successfully!')
            return redirect('admin_seat_type_list')
    else:
        form = SeatTypeForm()
    
    context = {'form': form, 'title': 'Add Seat Type'}
    return render(request, 'booking/admin/seat_type_form.html', context)

# User Management Views
@superuser_required
def admin_user_list(request):
    """List all users."""
    search_query = request.GET.get('search', '')
    is_staff_filter = request.GET.get('is_staff', '')
    
    users = User.objects.all()
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if is_staff_filter:
        users = users.filter(is_staff=is_staff_filter == 'true')
    
    # Pagination
    paginator = Paginator(users, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'is_staff_filter': is_staff_filter,
    }
    return render(request, 'booking/admin/user_list.html', context)

@superuser_required
def admin_user_edit(request, user_id):
    """Edit user."""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User "{user.username}" updated successfully!')
            return redirect('admin_user_list')
    else:
        form = UserForm(instance=user)
    
    context = {'form': form, 'title': 'Edit User', 'user_obj': user}
    return render(request, 'booking/admin/user_form.html', context)

# API Views for AJAX
@admin_required
def admin_api_theater_seats(request, theater_id):
    """Get seats for a theater (AJAX)."""
    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theater).select_related('seat_type')
    
    seat_data = []
    for seat in seats:
        seat_data.append({
            'id': seat.id,
            'row': seat.row,
            'number': seat.number,
            'seat_type': seat.seat_type.name,
        })
    
    return JsonResponse({'seats': seat_data})

@admin_required
def admin_api_show_bookings(request, show_id):
    """Get bookings for a show (AJAX)."""
    show = get_object_or_404(Show, id=show_id)
    bookings = Booking.objects.filter(show=show).select_related('user')
    
    booking_data = []
    for booking in bookings:
        booking_data.append({
            'id': booking.id,
            'user': booking.user.username,
            'status': booking.status,
            'total_amount': str(booking.total_amount),
            'seat_count': booking.seats.count(),
        })
    
    return JsonResponse({'bookings': booking_data})
