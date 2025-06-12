from django import forms
from django.contrib.auth.models import User
from .models import Movie, Theater, Show, Genre, SeatType, Seat, Booking

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'duration', 'release_date', 'poster', 'trailer_url', 'rating', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),
            'trailer_url': forms.URLInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '1', 'max': '10'}),
            'genres': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

class TheaterForm(forms.ModelForm):
    class Meta:
        model = Theater
        fields = ['name', 'address', 'city', 'total_capacity', 'contact_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'total_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['movie', 'theater', 'date', 'time', 'base_price', 'is_active']
        widgets = {
            'movie': forms.Select(attrs={'class': 'form-select'}),
            'theater': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SeatTypeForm(forms.ModelForm):
    class Meta:
        model = SeatType
        fields = ['name', 'price_multiplier']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price_multiplier': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ['theater', 'row', 'number', 'seat_type']
        widgets = {
            'theater': forms.Select(attrs={'class': 'form-select'}),
            'row': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '1'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'seat_type': forms.Select(attrs={'class': 'form-select'}),
        }

class BulkSeatForm(forms.Form):
    theater = forms.ModelChoiceField(
        queryset=Theater.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    rows = forms.CharField(
        max_length=50,
        help_text="Enter rows separated by commas (e.g., A,B,C,D,E)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    seats_per_row = forms.IntegerField(
        min_value=1,
        max_value=50,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    seat_type = forms.ModelChoiceField(
        queryset=SeatType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
