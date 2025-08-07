from django.db import models
from django.urls import reverse

class UserGoal(models.Model):
    """Mục tiêu của người dùng"""
    GOAL_CHOICES = [
        ('student', 'Du học sinh'),
        ('tourist', 'Khách tham quan'),
        ('resident', 'Định cư'),
    ]
    
    name = models.CharField(max_length=50, choices=GOAL_CHOICES)
    description = models.TextField()
    
    def __str__(self):
        return self.get_name_display()

class Topic(models.Model):
    """Chủ đề học tiếng Việt"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='topics/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('talk:topic_detail', args=[str(self.id)])

class Lesson(models.Model):
    """Bài học trong chủ đề"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField(help_text="Nội dung bài học với HTML")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.topic.name} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('talk:lesson_detail', args=[str(self.topic.id), str(self.id)])

class Sentence(models.Model):
    """Mẫu câu trong bài học"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='sentences')
    vietnamese = models.CharField(max_length=500)
    english = models.CharField(max_length=500)
    pronunciation = models.CharField(max_length=500, help_text="Phiên âm")
    usage_context = models.TextField(help_text="Tình huống sử dụng")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.vietnamese[:50]

class MiniGame(models.Model):
    """Mini game cho bài học"""
    GAME_TYPES = [
        ('matching', 'Ghép từ'),
        ('fill_blank', 'Điền từ'),
        ('multiple_choice', 'Trắc nghiệm'),
        ('speaking', 'Phát âm'),
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='minigames')
    title = models.CharField(max_length=200)
    game_type = models.CharField(max_length=20, choices=GAME_TYPES)
    content = models.JSONField(help_text="Nội dung game dạng JSON")
    instructions = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"
