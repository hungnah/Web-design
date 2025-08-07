from django.contrib import admin
from .models import UserGoal, Topic, Lesson, Sentence, MiniGame

@admin.register(UserGoal)
class UserGoalAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'lesson_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    ordering = ['order']
    
    def lesson_count(self, obj):
        return obj.lessons.count()
    lesson_count.short_description = 'Số bài học'

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'order', 'is_active', 'sentence_count']
    list_filter = ['topic', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['topic', 'order']
    
    def sentence_count(self, obj):
        return obj.sentences.count()
    sentence_count.short_description = 'Số mẫu câu'

@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    list_display = ['vietnamese', 'english', 'lesson', 'order']
    list_filter = ['lesson__topic']
    search_fields = ['vietnamese', 'english']
    ordering = ['lesson', 'order']

@admin.register(MiniGame)
class MiniGameAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'game_type', 'order']
    list_filter = ['game_type', 'lesson__topic']
    search_fields = ['title', 'instructions']
    ordering = ['lesson', 'order']
