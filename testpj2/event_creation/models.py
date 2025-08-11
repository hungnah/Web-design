"""
Event Creation Models
This module contains models for creating language exchange events, lessons, and partner requests.
Handles Vietnamese phrases, cafe locations, language exchange posts, and lesson management.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone

class VietnamesePhrase(models.Model):
    """
    Vietnamese language phrases with Japanese and English translations
    Used by Japanese users to create language exchange posts
    """
    # Categories for organizing phrases by topic
    CATEGORY_CHOICES = [
        ('greetings', 'Greetings'),
        ('food', 'Food & Dining'),
        ('shopping', 'Shopping'),
        ('transport', 'Transportation'),
        ('emergency', 'Emergency'),
        ('daily', 'Daily Life'),
        ('business', 'Business'),
        ('travel', 'Travel'),
    ]
    
    # Difficulty levels for language learners
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    # Phrase classification and content
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, help_text="Topic category")
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES, help_text="Learning difficulty level")
    vietnamese_text = models.CharField(max_length=200, help_text="Original Vietnamese phrase")
    japanese_translation = models.CharField(max_length=200, help_text="Japanese translation")
    english_translation = models.CharField(max_length=200, help_text="English translation for reference")
    audio_file = models.FileField(upload_to='phrase_audio/', null=True, blank=True, help_text="Pronunciation audio")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.category} - {self.vietnamese_text}"

class CafeLocation(models.Model):
    """
    Physical meeting locations for language exchange sessions
    Cafes and public spaces where users can meet safely
    """
    # Basic location information
    name = models.CharField(max_length=100, help_text="Cafe or location name")
    address = models.TextField(help_text="Full address")
    city = models.CharField(max_length=20, choices=[
        ('hanoi', 'Hà Nội'),
        ('hochiminh', 'Hồ Chí Minh'),
        ('haiphong', 'Hải Phòng'),
        ('danang', 'Đà Nẵng'),
        ('cantho', 'Cần Thơ'),
    ], help_text="City for filtering locations")
    
    # GPS coordinates for mapping (optional)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="GPS latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="GPS longitude")
    description = models.TextField(blank=True, help_text="Additional details about the location")
    
    def __str__(self):
        return f"{self.name} - {self.city}"

class PartnerRequest(models.Model):
    """Model for users to find language exchange partners"""
    REQUEST_TYPE_CHOICES = [
        ('japanese_to_vietnamese', 'Japanese learning Vietnamese'),
        ('vietnamese_to_japanese', 'Vietnamese learning Japanese'),
        ('both', 'Both languages'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('matched', 'Matched'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partner_requests')
    accepted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accepted_partner_requests', null=True, blank=True)
    request_type = models.CharField(max_length=25, choices=REQUEST_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    preferred_city = models.CharField(max_length=20, choices=[
        ('hanoi', 'Hà Nội'),
        ('hochiminh', 'Hồ Chí Minh'),
        ('haiphong', 'Hải Phòng'),
        ('danang', 'Đà Nẵng'),
        ('cantho', 'Cần Thơ'),
        ('any', 'Any city'),
    ])
    meeting_preference = models.CharField(max_length=20, choices=[
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('both', 'Both'),
    ])
    frequency = models.CharField(max_length=20, choices=[
        ('once', 'Once'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('flexible', 'Flexible'),
    ])
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.requester.username} - {self.title}"

class LanguageExchangePost(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('matched', 'Matched'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    japanese_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='japanese_posts', null=True, blank=True)
    vietnamese_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vietnamese_posts', null=False, blank=True)
    phrase = models.ForeignKey(VietnamesePhrase, on_delete=models.CASCADE, null=True, blank=True)
    cafe_location = models.ForeignKey(CafeLocation, on_delete=models.CASCADE)
    meeting_date = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def chatroom(self):
        """Get the chat room for this post"""
        try:
            from chat_system.models import ChatRoom
            return ChatRoom.objects.get(post=self)
        except ChatRoom.DoesNotExist:
            return None
    
def __str__(self):
    phrase_text = self.phrase.vietnamese_text if self.phrase else "No phrase"
    return f"{self.japanese_user.username} - {phrase_text}"

class Lesson(models.Model):
    """Model for Vietnamese language lessons"""
    CATEGORY_CHOICES = [
        ('greetings', '挨拶'),
        ('food', '料理'),
        ('shopping', '買い物'),
        ('transport', '交通'),
        ('daily', '日常生活'),
        ('business', '仕事'),
        ('travel', '旅行'),
        ('emergency', '緊急'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', '初級'),
        ('intermediate', '中級'),
        ('advanced', '上級'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES)
    image = models.ImageField(upload_to='lesson_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['difficulty', 'category', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"


class LessonPhrase(models.Model):
    """Model for phrases within a lesson"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='phrases')
    vietnamese_text = models.CharField(max_length=200)
    japanese_translation = models.CharField(max_length=200)
    english_translation = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='lesson_audio/', null=True, blank=True)
    pronunciation_guide = models.CharField(max_length=200, blank=True)
    usage_note = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['lesson', 'order']
    
    def __str__(self):
        return f"{self.lesson.title} - {self.vietnamese_text}"