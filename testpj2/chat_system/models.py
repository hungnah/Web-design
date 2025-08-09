"""
Chat System Models
This module handles real-time messaging between language exchange partners.
Manages chat rooms and messages for both language exchange posts and partner requests.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone

class ChatRoom(models.Model):
    """
    Chat room for communication between language exchange partners
    Can be associated with either a LanguageExchangePost or PartnerRequest
    """
    # Link to either a language exchange post or partner request (mutually exclusive)
    post = models.OneToOneField('event_creation.LanguageExchangePost', on_delete=models.CASCADE, 
                               null=True, blank=True, help_text="Associated language exchange post")
    partner_request = models.OneToOneField('event_creation.PartnerRequest', on_delete=models.CASCADE, 
                                          null=True, blank=True, help_text="Associated partner request")
    
    # Chat room metadata
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the chat room was created")
    is_active = models.BooleanField(default=True, help_text="Whether the chat room is still active")
    
    def __str__(self):
        if self.post:
            return f"Chat for {self.post}"
        elif self.partner_request:
            return f"Chat for {self.partner_request}"
        return f"Chat Room {self.id}"

class Message(models.Model):
    """
    Individual messages within a chat room
    Supports read status tracking for notification purposes
    """
    # Message relationships
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages',
                                 help_text="The chat room this message belongs to")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              help_text="User who sent the message")
    
    # Message content and metadata
    content = models.TextField(help_text="The message text content")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="When the message was sent")
    is_read = models.BooleanField(default=False, help_text="Whether the recipient has read the message")
    
    class Meta:
        ordering = ['timestamp']  # Order messages chronologically
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"