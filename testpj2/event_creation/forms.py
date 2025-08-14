"""
Event Creation Forms
Handles forms for creating language exchange content:
- Language exchange post creation with date/time validation
- Partner request forms with user-specific defaults
- Meeting scheduling and location selection
"""

from django import forms
from .models import LanguageExchangePost, CulturalLocation, PartnerRequest, VietnamesePhrase
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class LanguageExchangePostForm(forms.ModelForm):
    """
    Form for creating language exchange posts
    Validates meeting dates and provides datetime picker interface
    """
    meeting_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = LanguageExchangePost
        fields = ['cultural_location', 'meeting_date', 'japanese_learning_phrases', 'vietnamese_learning_phrases', 'notes']
        widgets = {
            'cultural_location': forms.Select(attrs={'class': 'form-control', 'id': 'id_cultural_location'}),
            'japanese_learning_phrases': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '4'}),
            'vietnamese_learning_phrases': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '4'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add any additional notes about your meeting...'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Store user for use in validation methods
        self.user = user
        # Ensure cultural_location field has proper choices
        if 'cultural_location' in self.fields:
            self.fields['cultural_location'].queryset = CulturalLocation.objects.all().order_by('name')
            self.fields['cultural_location'].required = True  # Changed to True for better validation
            # Add choices for better form rendering
            locations = CulturalLocation.objects.all().order_by('name')
            self.fields['cultural_location'].choices = [('', 'Chọn địa điểm văn hóa...')] + [(loc.id, f"{loc.name} - {loc.city}") for loc in locations]
            self.fields['cultural_location'].help_text = "Chọn địa điểm văn hóa nơi bạn muốn gặp mặt và học tiếng"
            self.fields['cultural_location'].label = "Địa điểm văn hóa"
            # Set initial value to empty string to show placeholder
            self.fields['cultural_location'].initial = ''
            # Add custom error messages
            self.fields['cultural_location'].error_messages = {
                'invalid_choice': 'Vui lòng chọn một địa điểm văn hóa hợp lệ.',
                'required': 'Vui lòng chọn địa điểm văn hóa.'
            }
        
        # Ensure meeting_date field is properly configured
        if 'meeting_date' in self.fields:
            self.fields['meeting_date'].required = True
            self.fields['meeting_date'].help_text = "Chọn ngày và giờ gặp mặt"
            self.fields['meeting_date'].label = "Ngày và giờ gặp mặt"
            self.fields['meeting_date'].error_messages = {
                'required': 'Vui lòng chọn ngày và giờ gặp mặt.'
            }
        
        # Configure learning phrases fields based on user nationality
        if user:
            if user.nationality == 'vietnamese':
                # Vietnamese users learn Japanese, so show japanese_learning_phrases
                if 'japanese_learning_phrases' in self.fields:
                    self.fields['japanese_learning_phrases'].required = False
                    self.fields['japanese_learning_phrases'].queryset = VietnamesePhrase.objects.all().order_by('category', 'difficulty', 'vietnamese_text')
                    self.fields['japanese_learning_phrases'].help_text = "Chọn các câu nói tiếng Việt mà bạn muốn học (tùy chọn)"
                    self.fields['japanese_learning_phrases'].label = "Japanese Learning"
                    # Add choices for better form rendering
                    phrases = VietnamesePhrase.objects.all().order_by('category', 'difficulty', 'vietnamese_text')
                    self.fields['japanese_learning_phrases'].choices = [(phrase.id, f"{phrase.category} - {phrase.vietnamese_text} ({phrase.difficulty})") for phrase in phrases]
                
                # Hide vietnamese_learning_phrases for Vietnamese users
                if 'vietnamese_learning_phrases' in self.fields:
                    self.fields['vietnamese_learning_phrases'].widget = forms.HiddenInput()
                    self.fields['vietnamese_learning_phrases'].required = False
                    # Set empty choices to avoid validation issues
                    self.fields['vietnamese_learning_phrases'].choices = []
                    
            elif user.nationality == 'japanese':
                # Japanese users learn Vietnamese, so show vietnamese_learning_phrases
                if 'vietnamese_learning_phrases' in self.fields:
                    self.fields['vietnamese_learning_phrases'].required = False
                    self.fields['vietnamese_learning_phrases'].queryset = VietnamesePhrase.objects.all().order_by('category', 'difficulty', 'vietnamese_text')
                    self.fields['vietnamese_learning_phrases'].help_text = "Chọn các câu nói tiếng Việt mà bạn muốn học (tùy chọn)"
                    self.fields['vietnamese_learning_phrases'].label = "Vietnamese Learning"
                    # Add choices for better form rendering
                    phrases = VietnamesePhrase.objects.all().order_by('category', 'difficulty', 'vietnamese_text')
                    self.fields['vietnamese_learning_phrases'].choices = [(phrase.id, f"{phrase.category} - {phrase.vietnamese_text} ({phrase.difficulty})") for phrase in phrases]
                
                # Hide japanese_learning_phrases for Japanese users
                if 'japanese_learning_phrases' in self.fields:
                    self.fields['japanese_learning_phrases'].widget = forms.HiddenInput()
                    self.fields['japanese_learning_phrases'].required = False
                    # Set empty choices to avoid validation issues
                    self.fields['japanese_learning_phrases'].choices = []
        else:
            # Fallback if no user is provided - show both fields
            if 'japanese_learning_phrases' in self.fields:
                self.fields['japanese_learning_phrases'].required = False
                self.fields['japanese_learning_phrases'].queryset = VietnamesePhrase.objects.all().order_by('category', 'difficulty', 'vietnamese_text')
                self.fields['japanese_learning_phrases'].help_text = "Chọn các câu nói tiếng Việt mà bạn muốn học (tùy chọn)"
                self.fields['japanese_learning_phrases'].label = "Japanese Learning"
                phrases = VietnamesePhrase.objects.all().order_by('category', 'difficulty', 'vietnamese_text')
                self.fields['japanese_learning_phrases'].choices = [(phrase.id, f"{phrase.category} - {phrase.vietnamese_text} ({phrase.difficulty})") for phrase in phrases]
            
            if 'vietnamese_learning_phrases' in self.fields:
                self.fields['vietnamese_learning_phrases'].required = False
                self.fields['vietnamese_learning_phrases'].queryset = VietnamesePhrase.objects.all().order_by('category', 'difficulty', 'vietnamese_text')
                self.fields['vietnamese_learning_phrases'].help_text = "Chọn các câu nói tiếng Nhật mà bạn muốn học (tùy chọn)"
                self.fields['vietnamese_learning_phrases'].label = "Vietnamese Learning"
                phrases = VietnamesePhrase.objects.all().order_by('category', 'difficulty', 'vietnamese_text')
                self.fields['vietnamese_learning_phrases'].choices = [(phrase.id, f"{phrase.category} - {phrase.vietnamese_text} ({phrase.difficulty})") for phrase in phrases]
    
    def clean_cultural_location(self):
        """Validate cultural location field"""
        cultural_location = self.cleaned_data.get('cultural_location')
        if not cultural_location:
            raise forms.ValidationError('Vui lòng chọn địa điểm văn hóa.')
        
        # Check if location exists
        try:
            CulturalLocation.objects.get(id=cultural_location.id)
        except CulturalLocation.DoesNotExist:
            raise forms.ValidationError('Địa điểm văn hóa không tồn tại.')
        
        return cultural_location
    
    def clean_meeting_date(self):
        meeting_date = self.cleaned_data.get('meeting_date')
        if not meeting_date:
            raise forms.ValidationError('Vui lòng chọn ngày và giờ gặp mặt.')
        
        if meeting_date:
            # Ensure meeting is in the future
            if meeting_date <= timezone.now():
                raise forms.ValidationError('Ngày gặp mặt phải trong tương lai.')
            
            # Ensure meeting is not too far in the future (within 30 days)
            max_date = timezone.now() + timedelta(days=30)
            if meeting_date > max_date:
                raise forms.ValidationError('Ngày gặp mặt không được quá 30 ngày trong tương lai.')
        
        return meeting_date
    
    def clean(self):
        """Clean all form data"""
        cleaned_data = super().clean()
        
        # Get user from form instance if available
        user = getattr(self, 'user', None)
        
        if user:
            if user.nationality == 'vietnamese':
                # Vietnamese users must provide japanese_learning_phrases
                japanese_learning_phrases = cleaned_data.get('japanese_learning_phrases', [])
                if not japanese_learning_phrases:
                    raise forms.ValidationError('Vui lòng chọn ít nhất một câu nói tiếng Việt mà bạn muốn học.')
                
                # Set empty value for hidden field to avoid validation issues
                cleaned_data['vietnamese_learning_phrases'] = []
                
            elif user.nationality == 'japanese':
                # Japanese users must provide vietnamese_learning_phrases
                vietnamese_learning_phrases = cleaned_data.get('vietnamese_learning_phrases', [])
                if not vietnamese_learning_phrases:
                    raise forms.ValidationError('Vui lòng chọn ít nhất một câu nói tiếng Việt mà bạn muốn học.')
                
                # Set empty value for hidden field to avoid validation issues
                cleaned_data['japanese_learning_phrases'] = []
        else:
            # Fallback validation if no user is provided
            japanese_learning_phrases = cleaned_data.get('japanese_learning_phrases', [])
            vietnamese_learning_phrases = cleaned_data.get('vietnamese_learning_phrases', [])
            
            if not japanese_learning_phrases and not vietnamese_learning_phrases:
                raise forms.ValidationError('Vui lòng chọn ít nhất một câu nói muốn học từ một trong hai trường: Japanese Learning hoặc Vietnamese Learning.')
        
        # Ensure cultural_location is selected
        cultural_location = cleaned_data.get('cultural_location')
        if not cultural_location:
            raise forms.ValidationError('Vui lòng chọn địa điểm văn hóa.')
        
        # Ensure meeting_date is provided and valid
        meeting_date = cleaned_data.get('meeting_date')
        if not meeting_date:
            raise forms.ValidationError('Vui lòng chọn ngày và giờ gặp mặt.')
        
        return cleaned_data
    
    def save(self, commit=True):
        """Save the form with proper handling of cultural location"""
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    
    def is_valid(self):
        """Check if form is valid"""
        return super().is_valid()
    
    def has_error(self, field):
        """Check if field has error"""
        return field in self.errors
    
    def get_field(self, field_name):
        """Get field by name"""
        return self.fields.get(field_name)
    
    def get_field_errors(self, field_name):
        """Get field errors by name"""
        return self.errors.get(field_name, [])
    
    def get_field_help_text(self, field_name):
        """Get field help text by name"""
        field = self.fields.get(field_name)
        return field.help_text if field else ''
    
    def get_field_label(self, field_name):
        """Get field label by name"""
        field = self.fields.get(field_name)
        return field.label if field else ''
    
    def get_field_choices(self, field_name):
        """Get field choices by name"""
        field = self.fields.get(field_name)
        return field.choices if field else []
    
    def get_field_widget(self, field_name):
        """Get field widget by name"""
        field = self.fields.get(field_name)
        return field.widget if field else None
    
    def get_field_attrs(self, field_name):
        """Get field widget attributes by name"""
        field = self.fields.get(field_name)
        return field.widget.attrs if field and field.widget else {}
    
    def get_field_required(self, field_name):
        """Get field required status by name"""
        field = self.fields.get(field_name)
        return field.required if field else False
    
    def get_field_readonly(self, field_name):
        """Get field readonly status by name"""
        field = self.fields.get(field_name)
        return getattr(field, 'readonly', False) if field else False
    
    def get_field_initial(self, field_name):
        """Get field initial value by name"""
        field = self.fields.get(field_name)
        return field.initial if field else None
    
    def get_field_value(self, field_name):
        """Get field value by name"""
        return self.cleaned_data.get(field_name)


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
