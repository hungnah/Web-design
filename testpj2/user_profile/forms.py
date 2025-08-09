"""
User Profile Forms
Handles user registration, authentication, and profile management forms:
- Custom user registration with age validation
- Profile update forms
- Integration with Django's built-in authentication forms
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from datetime import date
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Custom user registration form with additional fields
    Validates age requirement (18+) for platform safety
    """
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'full_name', 
                 'date_of_birth', 'gender', 'nationality', 'city')
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise ValidationError('You must be at least 18 years old to register.')
        return dob
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'date_of_birth', 'gender', 
                 'nationality', 'city', 'profile_picture', 'bio', 'interests')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'profile_picture', 'bio', 'interests', 'city')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'interests': forms.Textarea(attrs={'rows': 3}),
        }
