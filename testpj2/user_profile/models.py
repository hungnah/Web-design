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
    
    def get_average_rating(self):
        """
        Calculate average rating from received evaluations
        Returns average score out of 10, or 0 if no evaluations
        """
        from session.models import Evaluation
        evaluations = Evaluation.objects.filter(evaluatee=self)
        if evaluations.exists():
            total_score = sum(eval.score for eval in evaluations)
            return round(total_score / evaluations.count(), 1)
        return 0.0
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class DiscountVoucher(models.Model):
    """
    Discount Voucher model for exchanging ganbari points
    Users can exchange their points for various types of discount vouchers
    """
    VOUCHER_TYPE_CHOICES = [
        ('coffee', 'Coffee Shop Discount'),
        ('restaurant', 'Restaurant Discount'),
        ('shopping', 'Shopping Discount'),
        ('transport', 'Transport Discount'),
        ('entertainment', 'Entertainment Discount'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='discount_vouchers')
    voucher_type = models.CharField(max_length=20, choices=VOUCHER_TYPE_CHOICES)
    discount_percentage = models.IntegerField(help_text="Discount percentage (e.g., 10 for 10%)")
    points_required = models.IntegerField(help_text="Points required to exchange for this voucher")
    description = models.TextField(help_text="Description of the discount offer")
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(help_text="Expiry date of the voucher")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_voucher_type_display()} ({self.discount_percentage}% off)"
    
    def is_valid(self):
        """Check if voucher is still valid and not used"""
        now = timezone.now()
        return self.status == 'active' and now <= self.valid_until
    
    def use_voucher(self):
        """Mark voucher as used"""
        if self.is_valid():
            self.status = 'used'
            self.used_at = timezone.now()
            self.save()
            return True
        return False
    
    class Meta:
        verbose_name = 'Discount Voucher'
        verbose_name_plural = 'Discount Vouchers'
        ordering = ['-created_at']