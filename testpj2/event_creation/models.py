"""
Event Creation Models
This module contains models for creating language exchange events, lessons, and partner requests.
Handles Vietnamese phrases, cafe locations, language exchange posts, and lesson management.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

class VietnamesePhrase(models.Model):
    """
    Vietnamese language phrases with Japanese and English translations
    Used by Japanese users to create language exchange posts
    """
    # Categories for organizing phrases by topic
    CATEGORY_CHOICES = [
        ('greetings', 'Greetings'),
        ('family', 'Family'),
        ('health', 'Health'),
        ('time', 'Time'),
        ('weather', 'Weather'),
        ('directions', 'Directions'),
        ('self_intro', 'Self Introduction'),
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
    
    USER_TYPE_CHOICES = [
        ('vietnamese', 'Vietnamese User'),
        ('japanese', 'Japanese User'),
    ]
    
    # User who created the post
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='vietnamese', help_text="Type of user who created this post")
    
    # User fields - one will be filled based on user_type
    japanese_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='japanese_posts', null=True, blank=True)
    vietnamese_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vietnamese_posts', null=True, blank=True)
    
    # Partner who accepted the post (will be filled when matched)
    japanese_partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accepted_japanese_posts', null=True, blank=True)
    vietnamese_partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accepted_vietnamese_posts', null=True, blank=True)
    
    phrase = models.ForeignKey(VietnamesePhrase, on_delete=models.CASCADE, null=True, blank=True)
    cafe_location = models.ForeignKey(CafeLocation, on_delete=models.CASCADE)
    meeting_date = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def creator(self):
        """Get the user who created this post"""
        if self.user_type == 'vietnamese':
            return self.vietnamese_user
        else:
            return self.japanese_user
    
    @property
    def partner(self):
        """Get the partner who accepted this post"""
        if self.user_type == 'vietnamese':
            return self.japanese_partner
        else:
            return self.vietnamese_partner
    
    @property
    def chatroom(self):
        """Get the chat room for this post"""
        try:
            from chat_system.models import ChatRoom
            return ChatRoom.objects.get(post=self)
        except ChatRoom.DoesNotExist:
            return None
    
    def clean(self):
        """Validate that only one user field is filled based on user_type"""
        from django.core.exceptions import ValidationError
        
        # Skip validation if this is a new instance being created
        if not self.pk:
            return
        
        # Only validate if we have a user_type set
        if not self.user_type:
            return
            
        # Basic validation: ensure the creator user is set correctly
        if self.user_type == 'vietnamese':
            if not self.vietnamese_user:
                raise ValidationError('Vietnamese user must be set when user_type is vietnamese')
        elif self.user_type == 'japanese':
            if not self.japanese_user:
                raise ValidationError('Japanese user must be set when user_type is japanese')
        
        # Note: We allow both user fields to be set for partner matching purposes
        # This is more flexible and realistic for a language exchange platform
    
    def save(self, *args, **kwargs):
        # Only run validation on existing instances and when we have user_type
        if self.pk and self.user_type:
            try:
                self.clean()
            except ValidationError as e:
                # Log the validation error but don't stop the save
                print(f"Validation warning in LanguageExchangePost {self.id}: {e}")
                # Continue with save operation
        super().save(*args, **kwargs)
    
    def __str__(self):
        creator_name = self.creator.username if self.creator else "Unknown"
        phrase_text = self.phrase.vietnamese_text if self.phrase else "No phrase"
        return f"{creator_name} ({self.get_user_type_display()}) - {phrase_text}"

class Lesson(models.Model):
    """Model for Vietnamese language lessons"""
    CATEGORY_CHOICES = [
        ('greetings', 'Chào hỏi (挨拶)'),
        ('self_introduction', 'Giới thiệu bản thân (自己紹介)'),
        ('asking_directions', 'Hỏi đường (道を尋ねる)'),
        ('shopping', 'Mua sắm (買い物)'),
        ('restaurant', 'Nhà hàng / gọi món (レストラン)'),
        ('transportation', 'Giao thông / đi lại (交通)'),
        ('weather', 'Thời tiết (天気)'),
        ('family', 'Gia đình (家族)'),
        ('health_emergency', 'Sức khỏe / trường hợp khẩn cấp (健康・緊急)'),
        ('time_schedule', 'Thời gian / lịch trình (時間・予定)'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', '初級'),
        ('intermediate', '中級'),
        ('advanced', '上級'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES)
    image = models.ImageField(upload_to='lesson_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['difficulty', 'category', 'title']
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.title}"


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

class QuizQuestion(models.Model):
    """Model for quiz questions in Vietnamese lessons"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quiz_questions')
    question = models.TextField(help_text="Câu hỏi trắc nghiệm")
    option_a = models.CharField(max_length=100, help_text="Lựa chọn A")
    option_b = models.CharField(max_length=100, help_text="Lựa chọn B")
    option_c = models.CharField(max_length=100, help_text="Lựa chọn C")
    option_d = models.CharField(max_length=100, help_text="Lựa chọn D")
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ], help_text="Đáp án đúng")
    explanation = models.TextField(blank=True, help_text="Giải thích đáp án")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['lesson', 'order']
    
    def __str__(self):
        return f"{self.lesson.title} - Question {self.order}"

class TheorySection(models.Model):
    """Model for theory sections with basic conversation phrases"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='theory_sections')
    title = models.CharField(max_length=200, help_text="Tiêu đề phần lý thuyết")
    description = models.TextField(help_text="Mô tả phần lý thuyết")
    order = models.PositiveIntegerField(default=0, help_text="Thứ tự hiển thị")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['lesson', 'order']
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"

class TheoryPhrase(models.Model):
    """Model for phrases in theory sections"""
    theory_section = models.ForeignKey(TheorySection, on_delete=models.CASCADE, related_name='phrases')
    vietnamese_text = models.CharField(max_length=200, help_text="Câu tiếng Việt")
    japanese_translation = models.CharField(max_length=200, help_text="Bản dịch tiếng Nhật")
    english_translation = models.CharField(max_length=200, help_text="Bản dịch tiếng Anh")
    pronunciation_guide = models.CharField(max_length=200, blank=True, help_text="Hướng dẫn phát âm")
    usage_note = models.TextField(blank=True, help_text="Ghi chú cách sử dụng")
    is_essential = models.BooleanField(default=False, help_text="Câu nói cần thiết")
    order = models.PositiveIntegerField(default=0, help_text="Thứ tự hiển thị")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['theory_section', 'order']
    
    def __str__(self):
        return f"{self.theory_section.title} - {self.vietnamese_text}"

class ConversationExample(models.Model):
    """Model for conversation examples in theory sections"""
    theory_section = models.ForeignKey(TheorySection, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=200, help_text="Tiêu đề đoạn hội thoại")
    description = models.TextField(help_text="Mô tả tình huống")
    order = models.PositiveIntegerField(default=0, help_text="Thứ tự hiển thị")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['theory_section', 'order']
    
    def __str__(self):
        return f"{self.theory_section.title} - {self.title}"

class ConversationLine(models.Model):
    """Model for individual lines in conversation examples"""
    conversation = models.ForeignKey(ConversationExample, on_delete=models.CASCADE, related_name='lines')
    speaker = models.CharField(max_length=50, choices=[
        ('tutor', 'TUTOR'),
        ('student', 'STUDENT'),
        ('person_a', 'PERSON A'),
        ('person_b', 'PERSON B'),
    ], help_text="Người nói")
    vietnamese_text = models.CharField(max_length=300, help_text="Nội dung tiếng Việt")
    japanese_translation = models.CharField(max_length=300, help_text="Bản dịch tiếng Nhật")
    english_translation = models.CharField(max_length=300, help_text="Bản dịch tiếng Anh")
    order = models.PositiveIntegerField(default=0, help_text="Thứ tự trong hội thoại")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['conversation', 'order']
    
    def __str__(self):
        return f"{self.conversation.title} - {self.speaker} - Line {self.order}"