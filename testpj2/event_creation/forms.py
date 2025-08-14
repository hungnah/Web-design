"""
Event Creation Forms
Handles forms for creating language exchange content:
- Language exchange post creation with date/time validation
- Partner request forms with user-specific defaults
- Meeting scheduling and location selection
"""

from django import forms
from .models import LanguageExchangePost, CafeLocation, PartnerRequest
from datetime import datetime, timedelta
from django.utils import timezone

class LanguageExchangePostForm(forms.ModelForm):
    """
    Form for creating language exchange posts
    Validates meeting dates and provides datetime picker interface
    Supports both Vietnamese and Japanese users
    """
    user_type = forms.ChoiceField(
        choices=[
            ('vietnamese', 'Vietnamese User'),
            ('japanese', 'Japanese User'),
        ],
        widget=forms.HiddenInput(),
        required=True
    )
    
    meeting_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = LanguageExchangePost
        fields = ['cafe_location', 'meeting_date', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add any additional notes about your meeting...'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Set user_type based on user nationality
            if user.nationality == 'vietnamese':
                self.fields['user_type'].initial = 'vietnamese'
            elif user.nationality == 'japanese':
                self.fields['user_type'].initial = 'japanese'
    
    def clean(self):
        """Custom validation to ensure user_type is set"""
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        
        if not user_type:
            raise forms.ValidationError('User type is required.')
        
        return cleaned_data
    
    def clean_meeting_date(self):
        meeting_date = self.cleaned_data.get('meeting_date')
        if meeting_date:
            # Ensure meeting is in the future
            if meeting_date <= timezone.now():
                raise forms.ValidationError('Meeting date must be in the future.')
            
            # Ensure meeting is not too far in the future (within 30 days)
            max_date = timezone.now() + timedelta(days=30)
            if meeting_date > max_date:
                raise forms.ValidationError('Meeting date cannot be more than 30 days in the future.')
        
        return meeting_date

class PartnerRequestForm(forms.ModelForm):
    class Meta:
        model = PartnerRequest
        fields = ['request_type', 'title', 'description', 'preferred_city', 'meeting_preference', 'frequency']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Looking for Vietnamese conversation partner'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell potential partners about your language goals, interests, and what you\'re looking for...'
            }),
            'request_type': forms.Select(attrs={'class': 'form-control'}),
            'preferred_city': forms.Select(attrs={'class': 'form-control'}),
            'meeting_preference': forms.Select(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Set default request type based on user nationality
            if user.nationality == 'japanese':
                self.fields['request_type'].initial = 'japanese_to_vietnamese'
            else:
                self.fields['request_type'].initial = 'vietnamese_to_japanese'
            
            # Set default city to user's city
            if user.city:
                self.fields['preferred_city'].initial = user.city
