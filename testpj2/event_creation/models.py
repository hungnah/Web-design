"""
Event Creation Models
This module contains models for creating language exchange events, lessons, and partner requests.
Handles Vietnamese phrases, cafe locations, language exchange posts, and lesson management.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

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

class ConnectionHistory(models.Model):
    """
    Model để lưu trữ lịch sử kết nối và đánh giá giữa người Nhật và người Việt
    """
    # Thông tin kết nối
    japanese_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='japanese_connections')
    vietnamese_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vietnamese_connections')
    
    # Liên kết với post gốc (nếu có)
    language_exchange_post = models.ForeignKey(LanguageExchangePost, on_delete=models.SET_NULL, null=True, blank=True)
    partner_request = models.ForeignKey(PartnerRequest, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Thông tin phiên học
    session_date = models.DateTimeField(help_text="Ngày diễn ra phiên học")
    session_duration = models.PositiveIntegerField(help_text="Thời lượng phiên học (phút)")
    session_type = models.CharField(max_length=20, choices=[
        ('online', 'Trực tuyến'),
        ('offline', 'Trực tiếp'),
    ], default='offline')
    
    # Đánh giá từ người Nhật
    japanese_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True, blank=True,
        help_text="Điểm đánh giá từ 1-10"
    )
    japanese_comment = models.TextField(null=True, blank=True, help_text="Nhận xét từ người Nhật")
    japanese_rating_date = models.DateTimeField(auto_now_add=True)
    
    # Đánh giá từ người Việt (tùy chọn)
    vietnamese_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True, blank=True,
        help_text="Điểm đánh giá từ 1-10"
    )
    vietnamese_comment = models.TextField(null=True, blank=True, help_text="Nhận xét từ người Việt")
    vietnamese_rating_date = models.DateTimeField(null=True, blank=True)
    
    # Trạng thái kết nối
    status = models.CharField(max_length=30, choices=[
        ('active', 'Đang hoạt động'),
        ('waiting_japanese_rating', 'Chờ đánh giá từ người Nhật'),
        ('waiting_vietnamese_rating', 'Chờ đánh giá từ người Việt'),
        ('fully_rated', 'Đã đánh giá đầy đủ'),
        ('cancelled', 'Đã hủy'),
        ('no_show', 'Không tham gia'),
    ], default='active')
    
    # Ghi chú bổ sung
    notes = models.TextField(null=True, blank=True, help_text="Ghi chú bổ sung về phiên học")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lịch sử kết nối'
        verbose_name_plural = 'Lịch sử kết nối'
        ordering = ['-session_date']
        unique_together = ['japanese_user', 'vietnamese_user', 'session_date']
    
    def __str__(self):
        return f"{self.japanese_user.username} - {self.vietnamese_user.username} - {self.session_date.strftime('%Y-%m-%d')}"
    
    def get_average_rating(self):
        """Tính điểm trung bình của cả hai người dùng"""
        ratings = []
        if self.japanese_rating:
            ratings.append(self.japanese_rating)
        if self.vietnamese_rating:
            ratings.append(self.vietnamese_rating)
        
        if ratings:
            return sum(ratings) / len(ratings)
        return None
    
    def is_fully_rated(self):
        """Kiểm tra xem cả hai người dùng đã đánh giá chưa"""
        return bool(self.japanese_rating and self.vietnamese_rating)
    
    def update_status(self):
        """Cập nhật trạng thái dựa trên đánh giá"""
        if self.japanese_rating and self.vietnamese_rating:
            self.status = 'fully_rated'
            # Tự động cập nhật trạng thái của LanguageExchangePost hoặc PartnerRequest
            if self.language_exchange_post:
                self.language_exchange_post.status = 'completed'
                self.language_exchange_post.save()
            if self.partner_request:
                self.partner_request.status = 'completed'
                self.partner_request.save()
            
            # Vô hiệu hóa chat room
            try:
                from chat_system.models import ChatRoom
                if self.language_exchange_post:
                    chat_room = ChatRoom.objects.get(post=self.language_exchange_post)
                elif self.partner_request:
                    chat_room = ChatRoom.objects.get(partner_request=self.partner_request)
                else:
                    return
                
                chat_room.deactivate_if_completed()
            except ChatRoom.DoesNotExist:
                pass
                
        elif self.japanese_rating and not self.vietnamese_rating:
            self.status = 'waiting_vietnamese_rating'
        elif not self.japanese_rating and self.vietnamese_rating:
            self.status = 'waiting_japanese_rating'
        else:
            self.status = 'active'
        self.save()
    
    def can_rate(self, user):
        """Kiểm tra xem người dùng có thể đánh giá không"""
        if user == self.japanese_user:
            return not self.japanese_rating
        elif user == self.vietnamese_user:
            return not self.vietnamese_rating
        return False
    
    def get_partner_rating(self, user):
        """Lấy điểm đánh giá từ đối phương"""
        if user == self.japanese_user:
            return self.vietnamese_rating
        elif user == self.vietnamese_user:
            return self.japanese_rating
        return None
    
    def get_partner_comment(self, user):
        """Lấy nhận xét từ đối phương"""
        if user == self.japanese_user:
            return self.vietnamese_comment
        elif user == self.vietnamese_user:
            return self.japanese_comment
        return None
    
    def get_rating_status_display(self):
        """Trả về trạng thái đánh giá hiển thị cho người dùng"""
        if self.status == 'fully_rated':
            return 'Đã đánh giá đầy đủ'
        elif self.status == 'waiting_japanese_rating':
            return 'Chờ đánh giá từ người Nhật'
        elif self.status == 'waiting_vietnamese_rating':
            return 'Chờ đánh giá từ người Việt'
        elif self.status == 'active':
            return 'Đang hoạt động'
        elif self.status == 'cancelled':
            return 'Đã hủy'
        elif self.status == 'no_show':
            return 'Không tham gia'
        else:
            return self.status
    
    def get_rating_status(self):
        """Trả về trạng thái đánh giá (tương thích ngược)"""
        return self.get_rating_status_display()