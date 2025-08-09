"""
Chat System Admin Configuration
Provides Django admin interface for managing chat functionality:
- Chat rooms between language exchange partners
- Messages within chat rooms
- Read status tracking for notifications
"""

from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    """Admin interface for managing chat rooms between language partners"""
    list_display = ['id', 'post', 'partner_request', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['post__japanese_user__username', 'partner_request__requester__username']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for managing messages within chat rooms"""
    list_display = ['sender', 'chat_room', 'content', 'timestamp', 'is_read']
    list_filter = ['timestamp', 'is_read', 'sender__nationality']
    search_fields = ['content', 'sender__username']
    date_hierarchy = 'timestamp'  # Provides date-based filtering