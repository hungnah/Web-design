from django.contrib import admin
from .models import UserProfile, Post, Application, GroupChat, Message

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'gender', 'city', 'created_at']
    list_filter = ['gender', 'city', 'created_at']
    search_fields = ['user__username', 'full_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'city', 'date', 'time', 'max_participants', 'current_participants', 'is_active']
    list_filter = ['city', 'date', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'post', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['applicant__username', 'post__title']
    readonly_fields = ['applied_at', 'updated_at']

@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = ['post', 'created_at']
    filter_horizontal = ['participants']
    readonly_fields = ['created_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'group_chat', 'content', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['content', 'sender__username']
    readonly_fields = ['timestamp']
