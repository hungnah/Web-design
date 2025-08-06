from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('O', 'Khác'),
    ]
    
    CITY_CHOICES = [
        ('hanoi', 'Hà Nội'),
        ('hcm', 'Hồ Chí Minh'),
        ('haiphong', 'Hải Phòng'),
        ('danang', 'Đà Nẵng'),
        ('cantho', 'Cần Thơ'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, verbose_name='Họ tên')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Giới tính')
    birth_date = models.DateField(verbose_name='Ngày sinh')
    city = models.CharField(max_length=20, choices=CITY_CHOICES, verbose_name='Thành phố')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Giới thiệu')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Ảnh đại diện')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.get_city_display()}"
    
    class Meta:
        verbose_name = 'Hồ sơ người dùng'
        verbose_name_plural = 'Hồ sơ người dùng'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, verbose_name='Tiêu đề')
    description = models.TextField(verbose_name='Mô tả')
    city = models.CharField(max_length=20, choices=UserProfile.CITY_CHOICES, verbose_name='Thành phố')
    location = models.CharField(max_length=200, verbose_name='Địa điểm cụ thể')
    date = models.DateField(verbose_name='Ngày')
    time = models.TimeField(verbose_name='Giờ')
    duration = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)], verbose_name='Thời lượng (giờ)')
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Chi phí dự kiến (VNĐ)')
    max_participants = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)], verbose_name='Số người tối đa')
    current_participants = models.IntegerField(default=1, verbose_name='Số người hiện tại')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_city_display()}"
    
    class Meta:
        verbose_name = 'Bài đăng'
        verbose_name_plural = 'Bài đăng'
        ordering = ['-created_at']

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối'),
    ]
    
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField(blank=True, verbose_name='Lời nhắn')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Trạng thái')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.applicant.profile.full_name} - {self.post.title}"
    
    class Meta:
        verbose_name = 'Đơn ứng tuyển'
        verbose_name_plural = 'Đơn ứng tuyển'
        unique_together = ['applicant', 'post']

class GroupChat(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='group_chat')
    participants = models.ManyToManyField(User, related_name='group_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chat - {self.post.title}"
    
    class Meta:
        verbose_name = 'Nhóm chat'
        verbose_name_plural = 'Nhóm chat'

class Message(models.Model):
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(verbose_name='Nội dung')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.profile.full_name}: {self.content[:50]}..."
    
    class Meta:
        verbose_name = 'Tin nhắn'
        verbose_name_plural = 'Tin nhắn'
        ordering = ['timestamp']
