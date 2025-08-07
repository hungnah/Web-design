from django.db import models
from django.urls import reverse

class TraditionalFood(models.Model):
    """Món ăn truyền thống Việt Nam"""
    name = models.CharField(max_length=200)
    vietnamese_name = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200)
    description = models.TextField()
    history_story = models.TextField(help_text="Câu chuyện lịch sử hoặc phong tục")
    image = models.ImageField(upload_to='foods/', blank=True, null=True)
    region = models.CharField(max_length=100, help_text="Vùng miền")
    difficulty_level = models.IntegerField(choices=[
        (1, 'Dễ'),
        (2, 'Trung bình'),
        (3, 'Khó')
    ], default=1)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('food_culture:food_detail', args=[str(self.id)])

class Ingredient(models.Model):
    """Nguyên liệu của món ăn"""
    food = models.ForeignKey(TraditionalFood, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=100)
    vietnamese_name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100)
    is_allergen = models.BooleanField(default=False, help_text="Có thể gây dị ứng")
    allergen_warning = models.TextField(blank=True, help_text="Cảnh báo dị ứng")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='ingredient_images/', blank=True, null=True, help_text="Hình ảnh minh họa cho nguyên liệu")
    
    def __str__(self):
        return f"{self.food.name} - {self.name}"

class OrderingPhrase(models.Model):
    """Cách gọi món bằng tiếng Việt"""
    food = models.ForeignKey(TraditionalFood, on_delete=models.CASCADE, related_name='ordering_phrases')
    vietnamese = models.CharField(max_length=200)
    english = models.CharField(max_length=200)
    pronunciation = models.CharField(max_length=200)
    context = models.TextField(help_text="Tình huống sử dụng")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.vietnamese

class CulturalTip(models.Model):
    """Mẹo văn hóa khi ăn"""
    TIP_CATEGORIES = [
        ('table_manners', 'Phép tắc bàn ăn'),
        ('chopsticks', 'Cách dùng đũa'),
        ('festival', 'Phong tục lễ Tết'),
        ('general', 'Văn hóa chung'),
    ]
    
    food = models.ForeignKey(TraditionalFood, on_delete=models.CASCADE, related_name='cultural_tips')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=TIP_CATEGORIES)
    content = models.TextField()
    image = models.ImageField(upload_to='cultural_tips/', blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.food.name} - {self.title}"

class FoodLink(models.Model):
    """Liên kết giữa từ khóa trong bài học và món ăn"""
    keyword = models.CharField(max_length=100, help_text="Từ khóa trong bài học")
    food = models.ForeignKey(TraditionalFood, on_delete=models.CASCADE)
    lesson = models.ForeignKey('talk.Lesson', on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"{self.keyword} -> {self.food.name}"
