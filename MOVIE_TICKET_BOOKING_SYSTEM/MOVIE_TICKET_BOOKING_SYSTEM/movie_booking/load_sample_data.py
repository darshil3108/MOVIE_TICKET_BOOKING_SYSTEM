# Sample data loading script
import os
import django
from datetime import date, time, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_booking.settings')
django.setup()

from booking.models import Genre, Movie, Theater, Show, SeatType, Seat
from django.contrib.auth.models import User

def load_sample_data():
    print("Loading sample data...")
    
    # Create genres
    genres_data = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller']
    genres = {}
    for genre_name in genres_data:
        genre, created = Genre.objects.get_or_create(name=genre_name)
        genres[genre_name] = genre
        if created:
            print(f"Created genre: {genre_name}")
    
    # Create movies
    movies_data = [
        {
            'title': 'Avengers: Endgame',
            'description': 'The Avengers assemble once more to reverse the damage caused by Thanos.',
            'duration': 181,
            'release_date': date(2024, 12, 1),
            'rating': 8.4,
            'genres': ['Action', 'Sci-Fi']
        },
        {
            'title': 'The Dark Knight',
            'description': 'Batman faces the Joker in this epic superhero thriller.',
            'duration': 152,
            'release_date': date(2024, 11, 15),
            'rating': 9.0,
            'genres': ['Action', 'Thriller']
        },
        {
            'title': 'Inception',
            'description': 'A mind-bending thriller about dreams within dreams.',
            'duration': 148,
            'release_date': date(2024, 10, 20),
            'rating': 8.8,
            'genres': ['Sci-Fi', 'Thriller']
        },
        {
            'title': 'The Hangover',
            'description': 'Four friends wake up from a bachelor party in Las Vegas.',
            'duration': 100,
            'release_date': date(2024, 9, 10),
            'rating': 7.7,
            'genres': ['Comedy']
        },
        {
            'title': 'Titanic',
            'description': 'A love story aboard the ill-fated RMS Titanic.',
            'duration': 194,
            'release_date': date(2024, 8, 5),
            'rating': 7.8,
            'genres': ['Romance', 'Drama']
        }
    ]
    
    movies = {}
    for movie_data in movies_data:
        movie, created = Movie.objects.get_or_create(
            title=movie_data['title'],
            defaults={
                'description': movie_data['description'],
                'duration': movie_data['duration'],
                'release_date': movie_data['release_date'],
                'rating': movie_data['rating']
            }
        )
        # Add genres
        for genre_name in movie_data['genres']:
            movie.genres.add(genres[genre_name])
        
        movies[movie_data['title']] = movie
        if created:
            print(f"Created movie: {movie_data['title']}")
    
    # Create seat types
    seat_types_data = [
        {'name': 'Regular', 'price_multiplier': Decimal('1.00')},
        {'name': 'Premium', 'price_multiplier': Decimal('1.50')},
        {'name': 'Recliner', 'price_multiplier': Decimal('2.00')}
    ]
    
    seat_types = {}
    for seat_type_data in seat_types_data:
        seat_type, created = SeatType.objects.get_or_create(
            name=seat_type_data['name'],
            defaults={'price_multiplier': seat_type_data['price_multiplier']}
        )
        seat_types[seat_type_data['name']] = seat_type
        if created:
            print(f"Created seat type: {seat_type_data['name']}")
    
    # Create theaters
    theaters_data = [
        {
            'name': 'Cineplex Downtown',
            'address': '123 Main Street',
            'city': 'New York',
            'total_capacity': 200,
            'contact_number': '+1-555-0101'
        },
        {
            'name': 'AMC Times Square',
            'address': '456 Broadway',
            'city': 'New York',
            'total_capacity': 300,
            'contact_number': '+1-555-0102'
        },
        {
            'name': 'Regal Cinema Mall',
            'address': '789 Shopping Center',
            'city': 'Los Angeles',
            'total_capacity': 250,
            'contact_number': '+1-555-0103'
        }
    ]
    
    theaters = {}
    for theater_data in theaters_data:
        theater, created = Theater.objects.get_or_create(
            name=theater_data['name'],
            defaults=theater_data
        )
        theaters[theater_data['name']] = theater
        if created:
            print(f"Created theater: {theater_data['name']}")
            
            # Create seats for this theater
            rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
            seats_per_row = 10
            
            for row in rows:
                for seat_num in range(1, seats_per_row + 1):
                    # Assign seat types based on row
                    if row in ['A', 'B']:  # Front rows - Regular
                        seat_type = seat_types['Regular']
                    elif row in ['H', 'I', 'J']:  # Back rows - Premium
                        seat_type = seat_types['Premium']
                    elif row in ['E', 'F']:  # Middle rows - Recliner
                        seat_type = seat_types['Recliner']
                    else:  # Other rows - Regular
                        seat_type = seat_types['Regular']
                    
                    Seat.objects.get_or_create(
                        theater=theater,
                        row=row,
                        number=seat_num,
                        defaults={'seat_type': seat_type}
                    )
    
    # Create shows
    today = date.today()
    times = [time(14, 0), time(17, 0), time(20, 0), time(22, 30)]
    
    movie_list = list(movies.values())
    theater_list = list(theaters.values())
    
    show_count = 0
    for days_ahead in range(7):  # Create shows for next 7 days
        show_date = today + timedelta(days=days_ahead)
        
        for theater in theater_list:
            for show_time in times:
                # Randomly assign movies to shows
                movie = movie_list[show_count % len(movie_list)]
                
                show, created = Show.objects.get_or_create(
                    movie=movie,
                    theater=theater,
                    date=show_date,
                    time=show_time,
                    defaults={
                        'base_price': Decimal('15.00'),
                        'is_active': True
                    }
                )
                
                if created:
                    show_count += 1
    
    print(f"Created {show_count} shows")
    print("Sample data loaded successfully!")

if __name__ == "__main__":
    load_sample_data()
