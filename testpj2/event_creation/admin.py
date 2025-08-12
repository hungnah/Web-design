"""
Event Creation Admin Configuration
Provides Django admin interface for managing language exchange content:
- Vietnamese phrases with translations
- Cafe locations for meetups
- Language exchange posts
- Partner requests
- Lessons and lesson phrases
"""

from django.contrib import admin
from .models import VietnamesePhrase, CafeLocation, LanguageExchangePost, PartnerRequest, Lesson, LessonPhrase, QuizQuestion, TheorySection, TheoryPhrase, ConversationExample, ConversationLine

@admin.register(VietnamesePhrase)
class VietnamesePhraseAdmin(admin.ModelAdmin):
    """Admin interface for managing Vietnamese phrases with translations"""
    list_display = ['category', 'difficulty', 'vietnamese_text', 'japanese_translation', 'created_at']
    list_filter = ['category', 'difficulty', 'created_at']
    search_fields = ['vietnamese_text', 'japanese_translation', 'english_translation']
    ordering = ['category', 'difficulty']

@admin.register(CafeLocation)
class CafeLocationAdmin(admin.ModelAdmin):
    """Admin interface for managing cafe and meeting locations"""
    list_display = ['name', 'city', 'address']
    list_filter = ['city']
    search_fields = ['name', 'address']

@admin.register(LanguageExchangePost)
class LanguageExchangePostAdmin(admin.ModelAdmin):
    """Admin interface for managing language exchange posts created by Japanese users"""
    list_display = ['japanese_user', 'vietnamese_user', 'phrase', 'cafe_location', 'meeting_date', 'status', 'created_at']
    list_filter = ['status', 'meeting_date', 'created_at', 'cafe_location__city']
    search_fields = ['japanese_user__username', 'vietnamese_user__username', 'notes']
    date_hierarchy = 'created_at'

@admin.register(PartnerRequest)
class PartnerRequestAdmin(admin.ModelAdmin):
    """Admin interface for managing partner requests for language exchange"""
    list_display = ['requester', 'request_type', 'title', 'preferred_city', 'meeting_preference', 'frequency', 'status', 'created_at']
    list_filter = ['request_type', 'preferred_city', 'meeting_preference', 'frequency', 'status', 'created_at']
    search_fields = ['requester__username', 'requester__full_name', 'title', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin interface for managing Vietnamese language lessons"""
    list_display = ['title', 'category', 'difficulty', 'created_at']
    list_filter = ['category', 'difficulty', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['difficulty', 'category', 'title']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(LessonPhrase)
class LessonPhraseAdmin(admin.ModelAdmin):
    """Admin interface for managing phrases within lessons"""
    list_display = ['lesson', 'vietnamese_text', 'japanese_translation', 'order']
    list_filter = ['lesson__category', 'lesson__difficulty', 'lesson']
    search_fields = ['vietnamese_text', 'japanese_translation', 'english_translation']
    ordering = ['lesson', 'order']
    list_select_related = ['lesson']  # Optimize database queries

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    """Admin interface for managing quiz questions"""
    list_display = ['lesson', 'question', 'correct_answer', 'order', 'created_at']
    list_filter = ['lesson__category', 'lesson__difficulty', 'lesson']
    search_fields = ['question', 'option_a', 'option_b', 'option_c', 'option_d']
    ordering = ['lesson', 'order']
    list_select_related = ['lesson']
    fieldsets = (
        ('Question Information', {
            'fields': ('lesson', 'question', 'order')
        }),
        ('Answer Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')
        }),
        ('Learning Support', {
            'fields': ('explanation',)
        }),
    )

@admin.register(TheorySection)
class TheorySectionAdmin(admin.ModelAdmin):
    """Admin interface for managing theory sections"""
    list_display = ['lesson', 'title', 'order', 'created_at']
    list_filter = ['lesson__category', 'lesson__difficulty', 'lesson']
    search_fields = ['title', 'description']
    ordering = ['lesson', 'order']
    list_select_related = ['lesson']
    fieldsets = (
        ('Basic Information', {
            'fields': ('lesson', 'title', 'description', 'order')
        }),
    )

@admin.register(TheoryPhrase)
class TheoryPhraseAdmin(admin.ModelAdmin):
    """Admin interface for managing theory phrases"""
    list_display = ['theory_section', 'vietnamese_text', 'is_essential', 'order', 'created_at']
    list_filter = ['theory_section__lesson__category', 'is_essential', 'theory_section']
    search_fields = ['vietnamese_text', 'japanese_translation', 'english_translation']
    ordering = ['theory_section', 'order']
    list_select_related = ['theory_section']
    fieldsets = (
        ('Phrase Information', {
            'fields': ('theory_section', 'vietnamese_text', 'japanese_translation', 'english_translation', 'order')
        }),
        ('Learning Support', {
            'fields': ('pronunciation_guide', 'usage_note', 'is_essential')
        }),
    )

@admin.register(ConversationExample)
class ConversationExampleAdmin(admin.ModelAdmin):
    """Admin interface for managing conversation examples"""
    list_display = ['theory_section', 'title', 'order', 'created_at']
    list_filter = ['theory_section__lesson__category', 'theory_section']
    search_fields = ['title', 'description']
    ordering = ['theory_section', 'order']
    list_select_related = ['theory_section']
    fieldsets = (
        ('Conversation Information', {
            'fields': ('theory_section', 'title', 'description', 'order')
        }),
    )

@admin.register(ConversationLine)
class ConversationLineAdmin(admin.ModelAdmin):
    """Admin interface for managing conversation lines"""
    list_display = ['conversation', 'speaker', 'vietnamese_text', 'order', 'created_at']
    list_filter = ['speaker', 'conversation__theory_section__lesson__category']
    search_fields = ['vietnamese_text', 'japanese_translation', 'english_translation']
    ordering = ['conversation', 'order']
    list_select_related = ['conversation']
    fieldsets = (
        ('Line Information', {
            'fields': ('conversation', 'speaker', 'vietnamese_text', 'japanese_translation', 'english_translation', 'order')
        }),
    )