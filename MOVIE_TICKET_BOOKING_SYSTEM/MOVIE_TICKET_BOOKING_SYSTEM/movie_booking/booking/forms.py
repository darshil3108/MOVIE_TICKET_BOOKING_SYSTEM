from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Booking

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            user_profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'phone_number': self.cleaned_data.get('phone_number', '')}
            )
        
        return user

class BookingForm(forms.Form):
    selected_seats = forms.CharField(widget=forms.HiddenInput())
    
    def clean_selected_seats(self):
        seats = self.cleaned_data['selected_seats']
        if not seats:
            raise forms.ValidationError("Please select at least one seat.")
        return seats
