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
from django.db.models import Q
from event_creation.models import LanguageExchangePost, PartnerRequest

@login_required
def available_posts(request):
    """
    Display available language exchange posts for Vietnamese users
    Allows filtering by city and shows only active (unmatched) posts
    """
    if request.user.nationality != 'vietnamese':
        return redirect('dashboard')
    
    city = request.GET.get('city', request.user.city)
    posts = LanguageExchangePost.objects.filter(
        japanese_user__nationality='japanese',
        cafe_location__city=city
    ).select_related('japanese_user', 'phrase', 'cafe_location')
    
    # Only show active posts (not accepted ones)
    posts = posts.filter(status='active')
    
    context = {
        'posts': posts,
        'selected_city': city,
        'cities': request.user.CITY_CHOICES,
    }
    
    return render(request, 'event_search/available_posts.html', context)

@login_required
def find_partners(request):
    """
    Find compatible language exchange partners based on user nationality
    Japanese users can help Vietnamese users learn Japanese and vice versa
    Supports filtering by city and request type
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
    
    context = {
        'partner_requests': compatible_requests,
        'selected_city': city,
        'selected_request_type': request_type,
        'cities': request.user.CITY_CHOICES,
        'request_types': PartnerRequest.REQUEST_TYPE_CHOICES,
    }
    
    return render(request, 'event_search/find_partners.html', context)