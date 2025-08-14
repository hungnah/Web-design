"""
Event Search Views
Handles searching and browsing of language exchange opportunities:
- Finding available language exchange posts by Japanese users
- Searching for compatible language exchange partners
- Filtering by city, language type, and other criteria
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Case, When, IntegerField
from event_creation.models import LanguageExchangePost, PartnerRequest

@login_required
def available_posts(request):
    """
    Display available language exchange posts for both Vietnamese and Japanese users
    Allows filtering by city and shows only active (unmatched) posts
    Prioritizes posts from users who have been matched before
    """
    city = request.GET.get('city', request.user.city)
    
    # Get posts from users of the opposite nationality
    if request.user.nationality == 'vietnamese':
        # Vietnamese users see posts from Japanese users
        posts = LanguageExchangePost.objects.filter(
            japanese_user__nationality='japanese',
            user_type='japanese',
            cafe_location__city=city,
            status='active'
        ).select_related('japanese_user', 'phrase', 'cafe_location')
        opposite_users = 'japanese'
    else:
        # Japanese users see posts from Vietnamese users
        posts = LanguageExchangePost.objects.filter(
            vietnamese_user__nationality='vietnamese',
            user_type='vietnamese',
            cafe_location__city=city,
            status='active'
        ).select_related('vietnamese_user', 'phrase', 'cafe_location')
        opposite_users = 'vietnamese'
    
    # Get users that current user has chatted with before
    from chat_system.models import ChatRoom
    previous_chat_users = set()
    
    # Find all chat rooms where current user was involved
    user_chat_rooms = ChatRoom.objects.filter(
        Q(post__japanese_user=request.user) | 
        Q(post__vietnamese_user=request.user) |
        Q(post__japanese_partner=request.user) |
        Q(post__vietnamese_partner=request.user) |
        Q(partner_request__requester=request.user) |
        Q(partner_request__accepted_by=request.user)
    )
    
    # Extract unique users from previous chats
    for chat_room in user_chat_rooms:
        if chat_room.post:
            if chat_room.post.creator == request.user:
                if chat_room.post.partner:
                    previous_chat_users.add(chat_room.post.partner.id)
            elif chat_room.post.partner == request.user:
                previous_chat_users.add(chat_room.post.creator.id)
        elif chat_room.partner_request:
            if chat_room.partner_request.requester == request.user:
                if chat_room.partner_request.accepted_by:
                    previous_chat_users.add(chat_room.partner_request.accepted_by.id)
            else:
                previous_chat_users.add(chat_room.partner_request.requester.id)
    
    # Annotate posts with priority (previous chat users get higher priority)
    if opposite_users == 'japanese':
        posts = posts.annotate(
            priority=Case(
                When(japanese_user__id__in=previous_chat_users, then=1),
                default=0,
                output_field=IntegerField(),
            )
        ).order_by('-priority', '-created_at')
    else:
        posts = posts.annotate(
            priority=Case(
                When(vietnamese_user__id__in=previous_chat_users, then=1),
                default=0,
                output_field=IntegerField(),
            )
        ).order_by('-priority', '-created_at')
    
    context = {
        'posts': posts,
        'selected_city': city,
        'cities': request.user.CITY_CHOICES,
        'opposite_users': opposite_users
    }
    
    return render(request, 'event_search/available_posts.html', context)



@login_required
def find_partners(request):
    """
    Find compatible language exchange partners based on user nationality
    Japanese users can help Vietnamese users learn Japanese and vice versa
    Supports filtering by city and request type
    Prioritizes users who have been matched before
    """
    city = request.GET.get('city', '')
    request_type = request.GET.get('request_type', '')
    
    # Find compatible partner requests based on user nationality
    if request.user.nationality == 'japanese':
        # Japanese users can help Vietnamese users learn Japanese
        compatible_requests = PartnerRequest.objects.filter(
            status='active',
            requester__nationality='vietnamese',
            request_type__in=['vietnamese_to_japanese', 'both']
        )
    else:
        # Vietnamese users can help Japanese users learn Vietnamese
        compatible_requests = PartnerRequest.objects.filter(
            status='active',
            requester__nationality='japanese',
            request_type__in=['japanese_to_vietnamese', 'both']
        )
    
    # Filter by city if specified
    if city and city != 'any':
        compatible_requests = compatible_requests.filter(
            Q(preferred_city=city) | Q(preferred_city='any')
        )
    
    # Filter by request type if specified
    if request_type:
        compatible_requests = compatible_requests.filter(request_type=request_type)
    
    # Get users that current user has chatted with before
    from chat_system.models import ChatRoom
    previous_chat_users = set()
    
    # Find all chat rooms where current user was involved
    user_chat_rooms = ChatRoom.objects.filter(
        Q(post__japanese_user=request.user) | 
        Q(post__vietnamese_user=request.user) |
        Q(partner_request__requester=request.user) |
        Q(partner_request__accepted_by=request.user)
    )
    
    # Extract unique users from previous chats
    for chat_room in user_chat_rooms:
        if chat_room.post:
            if chat_room.post.japanese_user == request.user:
                previous_chat_users.add(chat_room.post.vietnamese_user.id)
            else:
                previous_chat_users.add(chat_room.post.japanese_user.id)
        elif chat_room.partner_request:
            if chat_room.partner_request.requester == request.user:
                if chat_room.partner_request.accepted_by:
                    previous_chat_users.add(chat_room.partner_request.accepted_by.id)
            else:
                previous_chat_users.add(chat_room.partner_request.requester.id)
    
    # Annotate requests with priority (previous chat users get higher priority)
    compatible_requests = compatible_requests.annotate(
        priority=Case(
            When(requester__id__in=previous_chat_users, then=1),
            default=0,
            output_field=IntegerField(),
        )
    ).order_by('-priority', '-created_at')
    
    context = {
        'partner_requests': compatible_requests,
        'selected_city': city,
        'selected_request_type': request_type,
        'cities': request.user.CITY_CHOICES,
        'request_types': PartnerRequest.REQUEST_TYPE_CHOICES,
    }
    
    return render(request, 'event_search/find_partners.html', context)