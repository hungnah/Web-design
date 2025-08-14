"""
Event Creation Admin Configuration
Provides Django admin interface for managing language exchange content:
- Vietnamese phrases with translations
- Cultural locations for meetups
- Language exchange posts
- Partner requests
- Cultural lessons and challenges
"""

from django.contrib import admin
from .models import VietnamesePhrase, CulturalLocation, LanguageExchangePost, PartnerRequest, CulturalLesson, CulturalChallenge

@admin.register(VietnamesePhrase)
class VietnamesePhraseAdmin(admin.ModelAdmin):
    """Admin interface for managing Vietnamese phrases with translations"""
    list_display = ['category', 'difficulty', 'vietnamese_text', 'japanese_translation', 'created_at']
    list_filter = ['category', 'difficulty', 'created_at']
    search_fields = ['vietnamese_text', 'japanese_translation', 'english_translation']
    ordering = ['category', 'difficulty']

@admin.register(CulturalLocation)
class CulturalLocationAdmin(admin.ModelAdmin):
    """Admin interface for managing cultural and tourist locations"""
    list_display = ['name', 'location_type', 'city', 'address', 'created_at']
    list_filter = ['location_type', 'city', 'created_at']
    search_fields = ['name', 'address', 'cultural_description']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'location_type', 'city', 'address')
        }),
        ('Cultural Details', {
            'fields': ('cultural_description', 'cultural_tips', 'best_time_to_visit', 'entrance_fee', 'opening_hours')
        }),
        ('Location Details', {
            'fields': ('description', 'latitude', 'longitude')
        }),
    )

@admin.register(CulturalLesson)
class CulturalLessonAdmin(admin.ModelAdmin):
    """Admin interface for managing cultural location-specific lessons"""
    list_display = ['title', 'location', 'difficulty', 'estimated_duration', 'order', 'created_at']
    list_filter = ['difficulty', 'location__city', 'location__location_type', 'created_at']
    search_fields = ['title', 'description', 'vocabulary_list', 'essential_phrases']
    ordering = ['location', 'order', 'difficulty']
    list_select_related = ['location']
    fieldsets = (
        ('Basic Information', {
            'fields': ('location', 'title', 'description', 'difficulty', 'order')
        }),
        ('Lesson Content', {
            'fields': ('vocabulary_list', 'essential_phrases', 'cultural_context')
        }),
        ('Lesson Structure', {
            'fields': ('estimated_duration',)
        }),
    )

@admin.register(CulturalChallenge)
class CulturalChallengeAdmin(admin.ModelAdmin):
    """Admin interface for managing cultural communication challenges"""
    list_display = ['title', 'location', 'challenge_type', 'difficulty', 'is_final_challenge', 'order', 'created_at']
    list_filter = ['challenge_type', 'difficulty', 'is_final_challenge', 'location__city', 'created_at']
    search_fields = ['title', 'description', 'objective', 'success_criteria']
    ordering = ['location', 'order', 'difficulty']
    list_select_related = ['location']
    fieldsets = (
        ('Basic Information', {
            'fields': ('location', 'title', 'description', 'challenge_type', 'difficulty', 'order')
        }),
        ('Challenge Requirements', {
            'fields': ('objective', 'success_criteria', 'time_limit', 'is_final_challenge')
        }),
        ('Supporting Materials', {
            'fields': ('helpful_phrases', 'cultural_tips')
        }),
    )

@admin.register(LanguageExchangePost)
class LanguageExchangePostAdmin(admin.ModelAdmin):
    """Admin interface for managing language exchange posts created by Japanese users"""
    list_display = ['japanese_user', 'vietnamese_user', 'phrase', 'accepted_phrase', 'cultural_location', 'meeting_date', 'status', 'created_at']
    list_filter = ['status', 'meeting_date', 'created_at', 'cultural_location__city']
    search_fields = ['japanese_user__username', 'vietnamese_user__username', 'notes']
    date_hierarchy = 'created_at'
    filter_horizontal = ['japanese_learning_phrases', 'vietnamese_learning_phrases']
    fieldsets = (
        ('User Information', {
            'fields': ('japanese_user', 'vietnamese_user', 'status')
        }),
        ('Learning Content', {
            'fields': ('phrase', 'accepted_phrase', 'japanese_learning_phrases', 'vietnamese_learning_phrases')
        }),
        ('Meeting Details', {
            'fields': ('cultural_location', 'meeting_date', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(PartnerRequest)
class PartnerRequestAdmin(admin.ModelAdmin):
    """Admin interface for managing partner requests for language exchange"""
    list_display = ['requester', 'request_type', 'title', 'preferred_city', 'meeting_preference', 'frequency', 'status', 'created_at']
    list_filter = ['request_type', 'preferred_city', 'meeting_preference', 'frequency', 'status', 'created_at']
    search_fields = ['requester__username', 'requester__full_name', 'title', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

