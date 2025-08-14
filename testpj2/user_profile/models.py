"""
User Profile Models
This module contains the custom user model for the Vietnam-Japan language exchange platform.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import date

class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Supports both Vietnamese and Japanese users with additional profile information
    """
    # User type choices - Vietnamese or Japanese
    NATIONALITY_CHOICES = [
        ('vietnamese', 'Vietnamese'),
        ('japanese', 'Japanese'),
    ]
    
    # Gender options
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    # Available cities in Vietnam for language exchange
    CITY_CHOICES = [
        ('hanoi', 'Hà Nội'),
        ('hochiminh', 'Hồ Chí Minh'),
        ('haiphong', 'Hải Phòng'),
        ('danang', 'Đà Nẵng'),
        ('cantho', 'Cần Thơ'),
    ]
    
    # Basic user information
    full_name = models.CharField(max_length=100, blank=True, help_text="User's full name")
    date_of_birth = models.DateField(null=True, blank=True, help_text="Must be 18+ to register")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    nationality = models.CharField(max_length=20, choices=NATIONALITY_CHOICES, help_text="Vietnamese or Japanese")
    city = models.CharField(max_length=20, choices=CITY_CHOICES, help_text="City for language exchange meetups")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    # Additional profile information
    point = models.IntegerField(default=0, help_text="User's current point")
    bio = models.TextField(max_length=500, blank=True, help_text="Tell others about yourself")
    interests = models.TextField(max_length=300, blank=True, help_text="Your hobbies and interests")
    
    # Language and interface preferences
    preferred_language = models.CharField(max_length=10, default='en', help_text="Interface language preference")
    
    # Automatic timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    def get_age(self):
        """
        Calculate user's current age based on date of birth
        Returns None if date of birth is not set
        """
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    def is_adult(self):
        """
        Check if user is 18 years old or older
        Required for platform registration
        """
        age = self.get_age()
        return age is not None and age >= 18
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

