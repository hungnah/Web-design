"""
Event Creation Models
This module contains models for creating language exchange events and partner requests.
Handles Vietnamese phrases, cultural locations, language exchange posts, and cultural content management.
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
        ('culture', 'Culture & Customs'),
        ('tourism', 'Tourism & Sightseeing'),
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

class CulturalLocation(models.Model):
    """
    Cultural and tourist locations for language exchange sessions
    Places where users can experience Vietnamese culture while learning
    """
    # Location types
    LOCATION_TYPE_CHOICES = [
        ('historical', 'Historical Site'),
        ('museum', 'Museum'),
        ('temple', 'Temple/Pagoda'),
        ('market', 'Traditional Market'),
        ('park', 'Park/Garden'),
        ('landmark', 'Landmark'),
        ('cultural_center', 'Cultural Center'),
        ('workshop', 'Cultural Workshop'),
        ('performance', 'Performance Venue'),
        ('heritage', 'Heritage Site'),
    ]
    
    # Basic location information
    name = models.CharField(max_length=100, help_text="Location name")
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES, help_text="Type of cultural location")
    address = models.TextField(help_text="Full address")
    city = models.CharField(max_length=20, choices=[
        ('hanoi', 'Hà Nội'),
        ('hochiminh', 'Hồ Chí Minh'),
        ('haiphong', 'Hải Phòng'),
        ('danang', 'Đà Nẵng'),
        ('cantho', 'Cần Thơ'),
        ('hue', 'Huế'),
        ('hoian', 'Hội An'),
        ('sapa', 'Sa Pa'),
        ('nhatrang', 'Nha Trang'),
        ('dalat', 'Đà Lạt'),
    ], help_text="City for filtering locations")
    
    # Cultural information
    cultural_description = models.TextField(help_text="Description of cultural significance")
    best_time_to_visit = models.CharField(max_length=100, blank=True, help_text="Best time to visit")
    entrance_fee = models.CharField(max_length=50, blank=True, help_text="Entrance fee information")
    opening_hours = models.CharField(max_length=100, blank=True, help_text="Opening hours")
    
    # GPS coordinates for mapping (optional)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="GPS latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="GPS longitude")
    
    # Additional details
    description = models.TextField(blank=True, help_text="Additional details about the location")
    cultural_tips = models.TextField(blank=True, help_text="Cultural etiquette and tips for visitors")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['city', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.get_location_type_display()} - {self.city}"

class CulturalLesson(models.Model):
    """
    Language lessons specific to cultural locations
    Teaches vocabulary and phrases needed for each location
    """
    location = models.ForeignKey(CulturalLocation, on_delete=models.CASCADE, related_name='cultural_lessons')
    title = models.CharField(max_length=200, help_text="Lesson title")
    description = models.TextField(help_text="Lesson description")
    
    # Lesson content
    vocabulary_list = models.TextField(help_text="Key vocabulary for this location")
    essential_phrases = models.TextField(help_text="Essential phrases to know")
    cultural_context = models.TextField(help_text="Cultural background and context")
    
    # Difficulty and category
    difficulty = models.CharField(max_length=15, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ])
    
    # Lesson structure
    estimated_duration = models.PositiveIntegerField(help_text="Estimated duration in minutes")
    order = models.PositiveIntegerField(default=0, help_text="Order in the lesson sequence")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['location', 'order', 'difficulty']
    
    def __str__(self):
        return f"{self.location.name} - {self.title}"

class CulturalChallenge(models.Model):
    """
    Final communication challenge for Japanese users
    Requires them to interact with local Vietnamese people
    """
    CHALLENGE_TYPE_CHOICES = [
        ('conversation', 'Conversation Challenge'),
        ('question_asking', 'Question Asking'),
        ('cultural_exchange', 'Cultural Exchange'),
        ('local_interaction', 'Local Interaction'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    location = models.ForeignKey(CulturalLocation, on_delete=models.CASCADE, related_name='cultural_challenges')
    title = models.CharField(max_length=200, help_text="Challenge title")
    description = models.TextField(help_text="Challenge description")
    
    # Challenge details
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPE_CHOICES)
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES)
    
    # Challenge requirements
    objective = models.TextField(help_text="What the user needs to accomplish")
    success_criteria = models.TextField(help_text="How success is measured")
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes", null=True, blank=True)
    
    # Supporting materials
    helpful_phrases = models.TextField(blank=True, help_text="Phrases that might help with the challenge")
    cultural_tips = models.TextField(blank=True, help_text="Cultural tips for the challenge")
    
    # Challenge sequence
    order = models.PositiveIntegerField(default=0, help_text="Order in the challenge sequence")
    is_final_challenge = models.BooleanField(default=False, help_text="Is this the final challenge of the session")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['location', 'order', 'difficulty']
    
    def __str__(self):
        return f"{self.location.name} - {self.title}"

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
    vietnamese_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vietnamese_posts', null=True, blank=True)
    phrase = models.ForeignKey(VietnamesePhrase, on_delete=models.CASCADE, null=True, blank=True)
    japanese_learning_phrases = models.ManyToManyField(VietnamesePhrase, related_name='japanese_learning_posts', blank=True, help_text="Vietnamese phrases that Japanese users want to learn")
    vietnamese_learning_phrases = models.ManyToManyField(VietnamesePhrase, related_name='vietnamese_learning_posts', blank=True, help_text="Japanese phrases that Vietnamese users want to learn")
    
    # New field to store the phrase chosen by the person who accepted the post
    accepted_phrase = models.ForeignKey(VietnamesePhrase, on_delete=models.CASCADE, null=True, blank=True, related_name='accepted_posts', help_text="Phrase chosen by the person who accepted this post")
    
    cultural_location = models.ForeignKey(CulturalLocation, on_delete=models.CASCADE, null=True, blank=True)
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
        phrase_text = None
        if self.phrase:
            phrase_text = self.phrase.vietnamese_text
        elif self.japanese_learning_phrases.exists():
            first_phrase = self.japanese_learning_phrases.first()
            phrase_text = first_phrase.vietnamese_text if first_phrase else "Learning phrases"
        elif self.vietnamese_learning_phrases.exists():
            first_phrase = self.vietnamese_learning_phrases.first()
            phrase_text = first_phrase.vietnamese_text if first_phrase else "Learning phrases"
        else:
            phrase_text = "No content"
        owner = self.japanese_user.username if self.japanese_user else (self.vietnamese_user.username if self.vietnamese_user else 'unknown')
        return f"{owner} - {phrase_text}"














