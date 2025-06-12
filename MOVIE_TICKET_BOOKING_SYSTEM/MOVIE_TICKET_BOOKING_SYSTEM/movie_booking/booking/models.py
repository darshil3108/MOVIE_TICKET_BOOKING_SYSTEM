from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True)
    trailer_url = models.URLField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    genres = models.ManyToManyField(Genre, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-release_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('movie_detail', args=[self.pk])

class Theater(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    total_capacity = models.IntegerField()
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['city', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.city}"

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='shows')
    date = models.DateField()
    time = models.TimeField()
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('theater', 'date', 'time')
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.movie.title} at {self.theater.name} - {self.date} {self.time}"

class SeatType(models.Model):
    name = models.CharField(max_length=50)  # Regular, Premium, Recliner
    price_multiplier = models.DecimalField(max_digits=3, decimal_places=2)
    
    def __str__(self):
        return self.name

class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=1)  # A-K
    number = models.IntegerField()  # 1-10
    seat_type = models.ForeignKey(SeatType, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('theater', 'row', 'number')
        ordering = ['row', 'number']
    
    def __str__(self):
        return f"{self.theater.name} - {self.row}{self.number} ({self.seat_type.name})"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    seats = models.ManyToManyField(Seat, through='BookingSeat')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} - {self.show}"
    
    def get_absolute_url(self):
        return reverse('booking_detail', args=[self.pk])

class BookingSeat(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('booking', 'seat')
    
    def __str__(self):
        return f"{self.booking.id} - {self.seat}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
