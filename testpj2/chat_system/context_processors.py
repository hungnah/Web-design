from django.db.models import Q
from .models import ChatRoom, Message
from event_creation.models import LanguageExchangePost, PartnerRequest

def unread_messages_count(request):
    """Add unread messages count to template context"""
    if request.user.is_authenticated:
        # Get all chat rooms where user is involved
        chat_rooms = []
        
        # For LanguageExchangePost chats
        if request.user.nationality == 'japanese':
            accepted_posts = request.user.japanese_posts.filter(status='matched')
            for post in accepted_posts:
                try:
                    chat_room = ChatRoom.objects.get(post=post)
                    chat_rooms.append(chat_room)
                except ChatRoom.DoesNotExist:
                    pass
        else:
            accepted_posts = request.user.vietnamese_posts.filter(status='matched')
            for post in accepted_posts:
                try:
                    chat_room = ChatRoom.objects.get(post=post)
                    chat_rooms.append(chat_room)
                except ChatRoom.DoesNotExist:
                    pass
        
        # For PartnerRequest chats
        if request.user.nationality == 'japanese':
            partner_requests = request.user.accepted_partner_requests.filter(status='matched')
            for partner_request in partner_requests:
                try:
                    chat_room = ChatRoom.objects.get(partner_request=partner_request)
                    chat_rooms.append(chat_room)
                except ChatRoom.DoesNotExist:
                    pass
        else:
            partner_requests = request.user.partner_requests.filter(status='matched')
            for partner_request in partner_requests:
                try:
                    chat_room = ChatRoom.objects.get(partner_request=partner_request)
                    chat_rooms.append(chat_room)
                except ChatRoom.DoesNotExist:
                    pass
        
        # Count unread messages
        total_unread = 0
        for chat_room in chat_rooms:
            unread_count = chat_room.messages.filter(is_read=False).exclude(sender=request.user).count()
            total_unread += unread_count
        
        return {'unread_messages_count': total_unread}
    
    return {'unread_messages_count': 0}
