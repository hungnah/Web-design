"""
Chat System Views
Handles real-time messaging between language exchange partners:
- Chat room display and access control
- AJAX-based message sending and receiving
- Message read status tracking
- User chat room listing
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import ChatRoom, Message
from event_creation.models import LanguageExchangePost, PartnerRequest

@login_required
def chat_room(request, room_id):
    """
    Display chat room interface with access control
    Ensures only authorized users can access each chat room
    """
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    
    # Check if user is part of this chat
    if chat_room.post:
        if request.user not in [chat_room.post.japanese_user, chat_room.post.vietnamese_user]:
            messages.error(request, 'You do not have access to this chat room.')
            return redirect('dashboard')
    elif chat_room.partner_request:
        # For partner requests, both the requester and the person who accepted can access
        if request.user != chat_room.partner_request.requester and request.user != chat_room.partner_request.accepted_by:
            messages.error(request, 'You do not have access to this chat room.')
            return redirect('dashboard')
    
    messages_list = chat_room.messages.all()
    
    context = {
        'chat_room': chat_room,
        'chat_messages': messages_list,
    }
    
    return render(request, 'chat_system/chat_room.html', context)

@login_required
def send_message(request, room_id):
    """Send a message via AJAX"""
    if request.method == 'POST':
        chat_room = get_object_or_404(ChatRoom, id=room_id)
        content = request.POST.get('content', '').strip()
        
        # Check if user has access to this chat room
        if chat_room.post:
            if request.user not in [chat_room.post.japanese_user, chat_room.post.vietnamese_user]:
                return JsonResponse({'success': False, 'error': 'Access denied'})
        elif chat_room.partner_request:
            if request.user != chat_room.partner_request.requester and request.user != chat_room.partner_request.accepted_by:
                return JsonResponse({'success': False, 'error': 'Access denied'})
        
        if content:
            message = Message.objects.create(
                chat_room=chat_room,
                sender=request.user,
                content=content
            )
            
            return JsonResponse({
                'success': True,
                'message': {
                    'id': message.id,
                    'content': message.content,
                    'sender': message.sender.username,
                    'timestamp': message.timestamp.strftime('%H:%M'),
                }
            })
    
    return JsonResponse({'success': False})

@login_required
def get_messages(request, room_id):
    """Get messages via AJAX for real-time updates"""
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    
    # Check access
    if chat_room.post:
        if request.user not in [chat_room.post.japanese_user, chat_room.post.vietnamese_user]:
            return JsonResponse({'success': False, 'error': 'Access denied'})
    elif chat_room.partner_request:
        if request.user != chat_room.partner_request.requester and request.user != chat_room.partner_request.accepted_by:
            return JsonResponse({'success': False, 'error': 'Access denied'})
    
    # Mark messages as read
    chat_room.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    # Get messages with better ordering and prefetch related
    messages_list = chat_room.messages.select_related('sender').order_by('timestamp')
    messages_data = []
    
    for message in messages_list:
        messages_data.append({
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'sender_name': message.sender.full_name or message.sender.username,
            'timestamp': message.timestamp.strftime('%H:%M'),
            'is_own': message.sender == request.user,
            'is_read': message.is_read,
        })
    
    return JsonResponse({
        'success': True,
        'messages': messages_data,
        'room_id': room_id,
        'timestamp': timezone.now().isoformat()
    })

@login_required
def my_chats(request):
    """Display user's chat rooms"""
    # Get chat rooms where user is involved
    chat_rooms = []
    
    # For LanguageExchangePost chats
    if request.user.nationality == 'japanese':
        # Japanese user's posts that have been accepted
        accepted_posts = LanguageExchangePost.objects.filter(
            japanese_user=request.user,
            status='matched'
        ).select_related('vietnamese_user', 'phrase', 'cultural_location')
        
        for post in accepted_posts:
            try:
                chat_room = ChatRoom.objects.get(post=post)
                # Determine what to display in subtitle based on learning phrases
                if post.japanese_learning_phrases.exists() and post.vietnamese_learning_phrases.exists():
                    subtitle = f"Người Nhật học: {post.japanese_learning_phrases.first().vietnamese_text} | Người Việt học: {post.vietnamese_learning_phrases.first().vietnamese_text}"
                elif post.japanese_learning_phrases.exists():
                    subtitle = f"Người Nhật học: {post.japanese_learning_phrases.first().vietnamese_text}"
                elif post.vietnamese_learning_phrases.exists():
                    subtitle = f"Người Việt học: {post.vietnamese_learning_phrases.first().vietnamese_text}"
                else:
                    subtitle = "Không có nội dung học tập"
                
                chat_rooms.append({
                    'chat_room': chat_room,
                    'type': 'post',
                    'partner': post.vietnamese_user,
                    'title': f"Chat với {post.vietnamese_user.full_name or post.vietnamese_user.username}",
                    'subtitle': subtitle,
                    'last_message': chat_room.messages.last(),
                    'unread_count': chat_room.messages.filter(is_read=False).exclude(sender=request.user).count(),
                    'meeting_info': f"{post.cultural_location.name if post.cultural_location else 'Không có địa điểm'} - {post.meeting_date.strftime('%d/%m/%Y %H:%M')}"
                })
            except ChatRoom.DoesNotExist:
                # Create missing chat room
                chat_room = ChatRoom.objects.create(post=post)
                # Create welcome message
                welcome_message = f"Xin chào! Tôi đã chấp nhận bài đăng của bạn. Hãy cùng trò chuyện và học tiếng Việt nhé!"
                Message.objects.create(
                    chat_room=chat_room,
                    sender=post.vietnamese_user,
                    content=welcome_message
                )
                
                # Determine what to display in subtitle based on learning phrases
                if post.japanese_learning_phrases.exists() and post.vietnamese_learning_phrases.exists():
                    subtitle = f"Người Nhật học: {post.japanese_learning_phrases.first().vietnamese_text} | Người Việt học: {post.vietnamese_learning_phrases.first().vietnamese_text}"
                elif post.japanese_learning_phrases.exists():
                    subtitle = f"Người Nhật học: {post.japanese_learning_phrases.first().vietnamese_text}"
                elif post.vietnamese_learning_phrases.exists():
                    subtitle = f"Người Việt học: {post.vietnamese_learning_phrases.first().vietnamese_text}"
                else:
                    subtitle = "Không có nội dung học tập"
                
                chat_rooms.append({
                    'chat_room': chat_room,
                    'type': 'post',
                    'partner': post.vietnamese_user,
                    'title': f"Chat với {post.vietnamese_user.full_name or post.vietnamese_user.username}",
                    'subtitle': subtitle,
                    'last_message': chat_room.messages.last(),
                    'unread_count': chat_room.messages.filter(is_read=False).exclude(sender=request.user).count(),
                    'meeting_info': f"{post.cultural_location.name if post.cultural_location else 'Không có địa điểm'} - {post.meeting_date.strftime('%d/%m/%Y %H:%M')}"
                })
    else:
        # Vietnamese user's accepted posts
        accepted_posts = LanguageExchangePost.objects.filter(
            vietnamese_user=request.user,
            status='matched'
        ).select_related('japanese_user', 'phrase', 'cultural_location')
        
        for post in accepted_posts:
            try:
                chat_room = ChatRoom.objects.get(post=post)
                # Determine what to display in subtitle based on learning phrases
                if post.japanese_learning_phrases.exists() and post.vietnamese_learning_phrases.exists():
                    subtitle = f"Người Nhật học: {post.japanese_learning_phrases.first().vietnamese_text} | Người Việt học: {post.vietnamese_learning_phrases.first().vietnamese_text}"
                elif post.japanese_learning_phrases.exists():
                    subtitle = f"Người Nhật học: {post.japanese_learning_phrases.first().vietnamese_text}"
                elif post.vietnamese_learning_phrases.exists():
                    subtitle = f"Người Việt học: {post.vietnamese_learning_phrases.first().vietnamese_text}"
                else:
                    subtitle = "Không có nội dung học tập"
                
                chat_rooms.append({
                    'chat_room': chat_room,
                    'type': 'post',
                    'partner': post.japanese_user if post.japanese_user else 'Không có người dùng Nhật',
                    'title': f"Chat với {post.japanese_user.full_name or post.japanese_user.username if post.japanese_user else 'Không có người dùng Nhật'}",
                    'subtitle': subtitle,
                    'last_message': chat_room.messages.last(),
                    'unread_count': chat_room.messages.filter(is_read=False).exclude(sender=request.user).count(),
                    'meeting_info': f"{post.cultural_location.name if post.cultural_location else 'Không có địa điểm'} - {post.meeting_date.strftime('%d/%m/%Y %H:%M')}"
                })
            except ChatRoom.DoesNotExist:
                # Create missing chat room
                chat_room = ChatRoom.objects.create(post=post)
                # Create welcome message
                welcome_message = f"Xin chào! Tôi đã chấp nhận bài đăng của bạn. Hãy cùng trò chuyện và học tiếng Việt nhé!"
                Message.objects.create(
                    chat_room=chat_room,
                    sender=request.user,
                    content=welcome_message
                )
                
                # Determine what to display in subtitle based on learning phrases
                if post.japanese_learning_phrases.exists() and post.vietnamese_learning_phrases.exists():
                    subtitle = f"Người Nhật học: {post.japanese_learning_phrases.first().vietnamese_text} | Người Việt học: {post.vietnamese_learning_phrases.first().vietnamese_text}"
                elif post.japanese_learning_phrases.exists():
                    subtitle = f"Người Nhật học: {post.japanese_learning_phrases.first().vietnamese_text}"
                elif post.vietnamese_learning_phrases.exists():
                    subtitle = f"Người Việt học: {post.vietnamese_learning_phrases.first().vietnamese_text}"
                else:
                    subtitle = "Không có nội dung học tập"
                
                chat_rooms.append({
                    'chat_room': chat_room,
                    'type': 'post',
                    'partner': post.japanese_user if post.japanese_user else 'Không có người dùng Nhật',
                    'title': f"Chat với {post.japanese_user.full_name or post.japanese_user.username if post.japanese_user else 'Không có người dùng Nhật'}",
                    'subtitle': subtitle,
                    'last_message': chat_room.messages.last(),
                    'unread_count': chat_room.messages.filter(is_read=False).exclude(sender=request.user).count(),
                    'meeting_info': f"{post.cultural_location.name if post.cultural_location else 'Không có địa điểm'} - {post.meeting_date.strftime('%d/%m/%Y %H:%M')}"
                })
    
    # For PartnerRequest chats
    if request.user.nationality == 'japanese':
        # Japanese users can see partner requests they accepted
        partner_requests = PartnerRequest.objects.filter(
            status='matched',
            accepted_by=request.user
        ).select_related('requester')
        
        for partner_request in partner_requests:
            try:
                chat_room = ChatRoom.objects.get(partner_request=partner_request)
                chat_rooms.append({
                    'chat_room': chat_room,
                    'type': 'partner_request',
                    'partner': partner_request.requester,
                    'title': f"Partner Request: {partner_request.title}",
                    'subtitle': f"Loại: {partner_request.get_request_type_display()}",
                    'last_message': chat_room.messages.last(),
                    'unread_count': chat_room.messages.filter(is_read=False).exclude(sender=request.user).count()
                })
            except ChatRoom.DoesNotExist:
                pass
    else:
        # Vietnamese users can see their own partner requests that were accepted
        partner_requests = PartnerRequest.objects.filter(
            requester=request.user,
            status='matched'
        ).select_related('accepted_by')
        
        for partner_request in partner_requests:
            try:
                chat_room = ChatRoom.objects.get(partner_request=partner_request)
                chat_rooms.append({
                    'chat_room': chat_room,
                    'type': 'partner_request',
                    'partner': partner_request.accepted_by if partner_request.accepted_by else 'Không có người chấp nhận',
                    'title': f"Partner Request: {partner_request.title}",
                    'subtitle': f"Loại: {partner_request.get_request_type_display()}",
                    'last_message': chat_room.messages.last(),
                    'unread_count': chat_room.messages.filter(is_read=False).exclude(sender=request.user).count()
                })
            except ChatRoom.DoesNotExist:
                pass
    
    # Sort by last message time
    def get_sort_key(chat_info):
        if chat_info['last_message']:
            return chat_info['last_message'].timestamp
        return chat_info['chat_room'].created_at
    
    chat_rooms.sort(key=get_sort_key, reverse=True)
    
    context = {
        'chat_rooms': chat_rooms,
    }
    
    return render(request, 'chat_system/my_chats.html', context)