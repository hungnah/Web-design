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
    
    # Debug logging
    print(f"DEBUG: User {request.user.username} (nationality: {request.user.nationality}) trying to access chat room {room_id}")
    print(f"DEBUG: Chat room post: {chat_room.post}")
    print(f"DEBUG: Chat room partner_request: {chat_room.partner_request}")
    
    if chat_room.post:
        print(f"DEBUG: Post japanese_user: {chat_room.post.japanese_user}")
        print(f"DEBUG: Post vietnamese_user: {chat_room.post.vietnamese_user}")
        print(f"DEBUG: Post japanese_partner: {chat_room.post.japanese_partner}")
        print(f"DEBUG: Post vietnamese_partner: {chat_room.post.vietnamese_partner}")
        print(f"DEBUG: Current user ID: {request.user.id}")
        
        # Check all possible user fields in the post
        post_user_ids = []
        if chat_room.post.japanese_user:
            post_user_ids.append(chat_room.post.japanese_user.id)
        if chat_room.post.vietnamese_user:
            post_user_ids.append(chat_room.post.vietnamese_user.id)
        if chat_room.post.japanese_partner:
            post_user_ids.append(chat_room.post.japanese_partner.id)
        if chat_room.post.vietnamese_partner:
            post_user_ids.append(chat_room.post.vietnamese_partner.id)
        
        print(f"DEBUG: Post user IDs: {post_user_ids}")
        print(f"DEBUG: Current user in post users: {request.user.id in post_user_ids}")
        
        if request.user.id not in post_user_ids:
            print(f"DEBUG: Access denied - user not in post users")
            messages.error(request, 'You do not have access to this chat room.')
            return redirect('dashboard')
    elif chat_room.partner_request:
        print(f"DEBUG: Partner request requester: {chat_room.partner_request.requester}")
        print(f"DEBUG: Partner request accepted_by: {chat_room.partner_request.accepted_by}")
        print(f"DEBUG: Current user ID: {request.user.id}")
        
        # For partner requests, both the requester and the person who accepted can access
        partner_request_user_ids = []
        if chat_room.partner_request.requester:
            partner_request_user_ids.append(chat_room.partner_request.requester.id)
        if chat_room.partner_request.accepted_by:
            partner_request_user_ids.append(chat_room.partner_request.accepted_by.id)
        
        print(f"DEBUG: Partner request user IDs: {partner_request_user_ids}")
        print(f"DEBUG: Current user in partner request users: {request.user.id in partner_request_user_ids}")
        
        if request.user.id not in partner_request_user_ids:
            print(f"DEBUG: Access denied - user not in partner request users")
            messages.error(request, 'You do not have access to this chat room.')
            return redirect('dashboard')
    
    print(f"DEBUG: Access granted - proceeding to chat room")
    
    # Additional debug info for template
    if chat_room.post:
        print(f"DEBUG: Template context - post: {chat_room.post}")
        print(f"DEBUG: Template context - japanese_user: {chat_room.post.japanese_user}")
        print(f"DEBUG: Template context - vietnamese_user: {chat_room.post.vietnamese_user}")
        print(f"DEBUG: Template context - japanese_partner: {chat_room.post.japanese_partner}")
        print(f"DEBUG: Template context - vietnamese_partner: {chat_room.post.vietnamese_partner}")
        print(f"DEBUG: Template context - current user: {request.user}")
    
    messages_list = chat_room.messages.all()
    
    context = {
        'chat_room': chat_room,
        'chat_messages': messages_list,
    }
    
    return render(request, 'chat_system/chat_room.html', context)

@login_required
def send_message(request, room_id):
    """Send a message via AJAX"""
    print(f"DEBUG: send_message called for room {room_id} by user {request.user.username}")
    print(f"DEBUG: Request method: {request.method}")
    print(f"DEBUG: Request POST data: {request.POST}")
    
    if request.method == 'POST':
        chat_room = get_object_or_404(ChatRoom, id=room_id)
        content = request.POST.get('content', '').strip()
        
        print(f"DEBUG: Chat room found: {chat_room}")
        print(f"DEBUG: Content: '{content}'")
        
        # Check if user has access to this chat room
        if chat_room.post:
            print(f"DEBUG: Chat room has post: {chat_room.post}")
            print(f"DEBUG: Post japanese_user: {chat_room.post.japanese_user}")
            print(f"DEBUG: Post vietnamese_user: {chat_room.post.vietnamese_user}")
            print(f"DEBUG: Post japanese_partner: {chat_room.post.japanese_partner}")
            print(f"DEBUG: Post vietnamese_partner: {chat_room.post.vietnamese_partner}")
            print(f"DEBUG: Current user: {request.user} (ID: {request.user.id})")
            
            # Check all possible user fields in the post
            post_user_ids = []
            if chat_room.post.japanese_user:
                post_user_ids.append(chat_room.post.japanese_user.id)
            if chat_room.post.vietnamese_user:
                post_user_ids.append(chat_room.post.vietnamese_user.id)
            if chat_room.post.japanese_partner:
                post_user_ids.append(chat_room.post.japanese_partner.id)
            if chat_room.post.vietnamese_partner:
                post_user_ids.append(chat_room.post.vietnamese_partner.id)
            
            print(f"DEBUG: Post user IDs: {post_user_ids}")
            print(f"DEBUG: Current user in post users: {request.user.id in post_user_ids}")
            
            if request.user.id not in post_user_ids:
                print(f"DEBUG: Access denied - user not in post users")
                return JsonResponse({'success': False, 'error': 'Access denied'})
        elif chat_room.partner_request:
            print(f"DEBUG: Chat room has partner request: {chat_room.partner_request}")
            if request.user != chat_room.partner_request.requester and request.user != chat_room.partner_request.accepted_by:
                print(f"DEBUG: Access denied - user not in partner request users")
                return JsonResponse({'success': False, 'error': 'Access denied'})
        
        if content:
            print(f"DEBUG: Creating message with content: '{content}'")
            message = Message.objects.create(
                chat_room=chat_room,
                sender=request.user,
                content=content
            )
            print(f"DEBUG: Message created successfully: {message}")
            
            return JsonResponse({
                'success': True,
                'message': {
                    'id': message.id,
                    'content': message.content,
                    'sender': message.sender.username,
                    'timestamp': message.timestamp.strftime('%H:%M'),
                }
            })
        else:
            print(f"DEBUG: Content is empty")
    
    print(f"DEBUG: Returning failure response")
    return JsonResponse({'success': False, 'error': 'Invalid request or empty content'})

@login_required
def get_messages(request, room_id):
    """Get messages via AJAX for real-time updates"""
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    
    # Check access
    if chat_room.post:
        # Check all possible user fields in the post
        post_user_ids = []
        if chat_room.post.japanese_user:
            post_user_ids.append(chat_room.post.japanese_user.id)
        if chat_room.post.vietnamese_user:
            post_user_ids.append(chat_room.post.vietnamese_user.id)
        if chat_room.post.japanese_partner:
            post_user_ids.append(chat_room.post.japanese_partner.id)
        if chat_room.post.vietnamese_partner:
            post_user_ids.append(chat_room.post.vietnamese_partner.id)
        
        if request.user.id not in post_user_ids:
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
        ).select_related('vietnamese_user', 'phrase', 'cafe_location')
        
        print(f"DEBUG: Found {accepted_posts.count()} accepted posts for Japanese user {request.user.username}")
        
        for post in accepted_posts:
            print(f"DEBUG: Processing post {post.id}: japanese_user={post.japanese_user}, vietnamese_partner={post.vietnamese_partner}")
            
            try:
                chat_room = ChatRoom.objects.get(post=post)
                print(f"DEBUG: Found existing chat room {chat_room.id} for post {post.id}")
                # Determine the correct partner for display
                partner = post.vietnamese_user if post.vietnamese_user else post.vietnamese_partner
                chat_rooms.append({
                    'chat_room': chat_room,
                    'type': 'post',
                    'partner': partner,
                    'title': f"Chat với {partner.full_name or partner.username}",
                    'subtitle': f"Học: {post.phrase.vietnamese_text}",
                    'last_message': chat_room.messages.last(),
                    'unread_count': chat_room.messages.filter(is_read=False).exclude(sender=request.user).count(),
                    'meeting_info': f"{post.cafe_location.name} - {post.meeting_date.strftime('%d/%m/%Y %H:%M')}"
                })
            except ChatRoom.DoesNotExist:
                print(f"DEBUG: Creating new chat room for post {post.id}")
                # Create missing chat room
                chat_room = ChatRoom.objects.create(post=post)
                print(f"DEBUG: Created chat room {chat_room.id} with post={chat_room.post}")
                # Create welcome message
                welcome_message = f"Xin chào! Tôi đã chấp nhận bài đăng của bạn. Hãy cùng trò chuyện và học tiếng Việt nhé!"
                Message.objects.create(
                    chat_room=chat_room,
                    sender=partner,
                    content=welcome_message
                )
                chat_rooms.append({
                    'chat_room': chat_room,
                    'type': 'post',
                    'partner': partner,
                    'title': f"Chat với {partner.full_name or partner.username}",
                    'subtitle': f"Học: {post.phrase.vietnamese_text}",
                    'last_message': chat_room.messages.last(),
                    'unread_count': chat_room.messages.filter(is_read=False).exclude(sender=request.user).count(),
                    'meeting_info': f"{post.cafe_location.name} - {post.meeting_date.strftime('%d/%m/%Y %H:%M')}"
                })
    else:
        # Vietnamese user's accepted posts (posts created by Japanese users that Vietnamese user accepted)
        accepted_posts = LanguageExchangePost.objects.filter(
            japanese_user__isnull=False,  # Posts created by Japanese users
            vietnamese_partner=request.user,  # Vietnamese user accepted these posts
            status='matched'
        ).select_related('japanese_user', 'phrase', 'cafe_location')
        
        print(f"DEBUG: Found {accepted_posts.count()} accepted posts for Vietnamese user {request.user.username}")
        
        for post in accepted_posts:
            print(f"DEBUG: Processing post {post.id}: japanese_user={post.japanese_user}, vietnamese_partner={post.vietnamese_partner}")
            
            if post.japanese_user:  # Check if japanese_user exists
                try:
                    chat_room = ChatRoom.objects.get(post=post)
                    print(f"DEBUG: Found existing chat room {chat_room.id} for post {post.id}")
                    # Determine the correct partner for display
                    partner = post.japanese_user if post.japanese_user else post.japanese_partner
                    chat_rooms.append({
                        'chat_room': chat_room,
                        'type': 'post',
                        'partner': partner,
                        'title': f"Chat với {partner.full_name or partner.username}",
                        'subtitle': f"Học: {post.phrase.vietnamese_text}",
                        'last_message': chat_room.messages.last(),
                        'unread_count': chat_room.messages.filter(is_read=False).exclude(sender=request.user).count(),
                        'meeting_info': f"{post.cafe_location.name} - {post.meeting_date.strftime('%d/%m/%Y %H:%M')}"
                    })
                except ChatRoom.DoesNotExist:
                    print(f"DEBUG: Creating new chat room for post {post.id}")
                    # Create missing chat room
                    chat_room = ChatRoom.objects.create(post=post)
                    print(f"DEBUG: Created chat room {chat_room.id} with post={chat_room.post}")
                    # Create welcome message
                    welcome_message = f"Xin chào! Tôi đã chấp nhận bài đăng của bạn. Hãy cùng trò chuyện và học tiếng Việt nhé!"
                    Message.objects.create(
                        chat_room=chat_room,
                        sender=request.user,
                        content=welcome_message
                    )
                    chat_rooms.append({
                        'chat_room': chat_room,
                        'type': 'post',
                        'partner': partner,
                        'title': f"Chat với {partner.full_name or partner.username}",
                        'subtitle': f"Học: {post.phrase.vietnamese_text}",
                        'last_message': chat_room.messages.last(),
                        'unread_count': chat_room.messages.filter(is_read=False).exclude(sender=request.user).count(),
                        'meeting_info': f"{post.cafe_location.name} - {post.meeting_date.strftime('%d/%m/%Y %H:%M')}"
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
                    'partner': partner_request.accepted_by,
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