"""
Event Creation Views
Handles creation and management of language exchange content:
- Vietnamese phrases for Japanese learners
- Language exchange posts creation and editing
- Partner requests for finding language exchange partners
- Post acceptance and chat room creation
- Cultural lessons and challenges
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import VietnamesePhrase, CulturalLocation, LanguageExchangePost, PartnerRequest, CulturalLesson, CulturalChallenge
from .forms import LanguageExchangePostForm, PartnerRequestForm
from chat_system.models import ChatRoom, Message

@login_required
def phrase_list(request, post_id=None):
    """
    Display Vietnamese phrases with filtering options for Japanese users
    Allows filtering by category and difficulty level
    """
    # if request.user.nationality != 'japanese':
    #     return redirect('dashboard')
    
    category = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    
    phrases = VietnamesePhrase.objects.all()
    
    if category:
        phrases = phrases.filter(category=category)
    if difficulty:
        phrases = phrases.filter(difficulty=difficulty)
    
    # Validate post_id if provided
    post = None
    if post_id:
        try:
            post = LanguageExchangePost.objects.get(id=post_id)
            # Check if user is trying to accept their own post
            if (post.vietnamese_user == request.user) or (post.japanese_user == request.user):
                messages.error(request, 'Bạn không thể chấp nhận bài đăng của chính mình.')
                return redirect('/search/available-posts/')
            
            # Check if post is still available
            if post.status != 'active':
                status_messages = {
                    'matched': 'Bài đăng này đã được chấp nhận bởi người khác.',
                    'completed': 'Bài đăng này đã hoàn thành.',
                    'cancelled': 'Bài đăng này đã bị hủy.'
                }
                error_msg = status_messages.get(post.status, 'Bài đăng này không còn khả dụng để chấp nhận.')
                messages.error(request, error_msg)
                return redirect('/search/available-posts/')
                
        except LanguageExchangePost.DoesNotExist:
            messages.error(request, 'Bài đăng không tồn tại trong hệ thống.')
            return redirect('/search/available-posts/')
    
    context = {
        'post_id': post_id,
        'post': post,
        'phrases': phrases,
        'categories': VietnamesePhrase.CATEGORY_CHOICES,
        'difficulties': VietnamesePhrase.DIFFICULTY_CHOICES,
        'selected_category': category,
        'selected_difficulty': difficulty,
    }
    
    return render(request, 'event_creation/phrase_list.html', context)











@login_required
def create_post(request, phrase_id=None):
    """Create a language exchange post - Both Vietnamese and Japanese users can create posts"""
    phrase = None
    
    if phrase_id:
        phrase = get_object_or_404(VietnamesePhrase, id=phrase_id)
    
    if request.method == 'POST':
        form = LanguageExchangePostForm(request.POST, user=request.user)
        print(f"Form data received: {request.POST}")
        print(f"Form is valid: {form.is_valid()}")
        
        if form.is_valid():
            try:
                post = form.save(commit=False)
                # Allow both Vietnamese and Japanese users to create posts
                if request.user.nationality == 'japanese':
                    post.japanese_user = request.user
                    post.vietnamese_user = None  # This is now allowed since we changed the model
                    print(f"Creating post for Japanese user: {request.user.username}")
                else:
                    post.vietnamese_user = request.user
                    post.japanese_user = None
                    print(f"Creating post for Vietnamese user: {request.user.username}")
                
                post.phrase = phrase
                print(f"Post data before save: japanese_user={post.japanese_user}, vietnamese_user={post.vietnamese_user}")
                
                post.save()
                # Save many-to-many relationships
                form.save_m2m()
                print(f"Post saved successfully with ID: {post.id}")
                # Show success message in appropriate language
                if request.user.nationality == 'japanese':
                    messages.success(request, '投稿が正常に作成されました！')
                else:
                    messages.success(request, 'Bài đăng đã được tạo thành công!')
                return redirect('my_posts')
            except Exception as e:
                # Log the error for debugging
                print(f"Error saving post: {e}")
                if request.user.nationality == 'japanese':
                    messages.error(request, '投稿の作成中にエラーが発生しました。もう一度お試しください。')
                else:
                    messages.error(request, 'Có lỗi xảy ra khi tạo bài đăng. Vui lòng thử lại.')
        else:
            print(f"Form errors: {form.errors}")
            if request.user.nationality == 'japanese':
                messages.error(request, 'フォームにエラーがあります。入力内容を確認してください。')
            else:
                messages.error(request, 'Form có lỗi. Vui lòng kiểm tra lại thông tin nhập.')
    else:
        form = LanguageExchangePostForm(user=request.user)
    
    context = {
        'phrase': phrase,
        'form': form,
    }
    
    return render(request, 'event_creation/create_post.html', context)

@login_required
def edit_post(request, post_id):
    """Edit a language exchange post - Both Vietnamese and Japanese users can edit their own posts"""
    
    # Get the post, allowing both japanese_user and vietnamese_user to edit their own posts
    post = get_object_or_404(
        LanguageExchangePost, 
        id=post_id
    )
    
    # Check if user owns this post
    if not (post.japanese_user == request.user or post.vietnamese_user == request.user):
        if request.user.nationality == 'japanese':
            messages.error(request, 'この投稿を編集する権限がありません。')
        else:
            messages.error(request, 'Bạn không có quyền chỉnh sửa bài đăng này.')
        return redirect('my_posts')
    
    # Only allow editing active posts (not matched ones)
    if post.status != 'active':
        if request.user.nationality == 'japanese':
            messages.error(request, 'マッチング済みの投稿は編集できません。')
        else:
            messages.error(request, 'Chỉ có thể chỉnh sửa bài đăng chưa được chấp nhận.')
        return redirect('my_posts')
    
    if request.method == 'POST':
        form = LanguageExchangePostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            # Save many-to-many relationships
            form.save_m2m()
            if request.user.nationality == 'japanese':
                messages.success(request, '投稿が正常に更新されました！')
            else:
                messages.success(request, 'Bài đăng đã được cập nhật thành công!')
            return redirect('my_posts')
    else:
        form = LanguageExchangePostForm(instance=post, user=request.user)
    
    context = {
        'post': post,
        'form': form,
    }
    
    return render(request, 'event_creation/edit_post.html', context)

@login_required
def my_posts(request):
    """Display user's own posts (only posts they created, not accepted)"""
    if request.user.nationality == 'vietnamese':
        # For Vietnamese users, show posts they created (where they are vietnamese_user and japanese_user is None initially)
        posts = LanguageExchangePost.objects.filter(
            vietnamese_user=request.user,
            japanese_user__isnull=True
        )
    else:
        # For Japanese users, show posts they created (where they are japanese_user and vietnamese_user is None initially)
        posts = LanguageExchangePost.objects.filter(
            japanese_user=request.user,
            vietnamese_user__isnull=True
        )
    
    # Calculate counts for statistics
    matched_posts_count = posts.filter(status='matched').count()
    active_posts_count = posts.filter(status='active').count()
    
    # Get recent accepted posts for notifications (only for Japanese users who created posts)
    recent_accepted_posts = []
    if request.user.nationality == 'japanese':
        recent_accepted_posts = posts.filter(status='matched').order_by('-updated_at')[:3]
    
    context = {
        'posts': posts,
        'matched_posts_count': matched_posts_count,
        'active_posts_count': active_posts_count,
        'recent_accepted_posts': recent_accepted_posts,
    }
    
    return render(request, 'event_creation/my_posts.html', context)

@login_required
def my_accepted_posts(request):
    """Display posts that the user has accepted (for Vietnamese users)"""
    if request.user.nationality != 'vietnamese':
        return redirect('my_posts')
    
    # Show posts where Vietnamese user accepted (where they are vietnamese_user but japanese_user is not None)
    accepted_posts = LanguageExchangePost.objects.filter(
        vietnamese_user=request.user,
        japanese_user__isnull=False
    )
    
    # Calculate counts for statistics
    matched_posts_count = accepted_posts.filter(status='matched').count()
    completed_posts_count = accepted_posts.filter(status='completed').count()
    
    context = {
        'posts': accepted_posts,
        'matched_posts_count': matched_posts_count,
        'completed_posts_count': completed_posts_count,
    }
    
    return render(request, 'event_creation/my_accepted_posts.html', context)

@login_required
def accept_post(request, post_id, phrase_id):
    """Accept a language exchange post - Both Vietnamese and Japanese users can accept posts"""
    
    try:
        phrase = get_object_or_404(VietnamesePhrase, id=phrase_id)
        
        # Check if post exists and is active
        try:
            post = LanguageExchangePost.objects.get(id=post_id)
        except LanguageExchangePost.DoesNotExist:
            if request.user.nationality == 'japanese':
                messages.error(request, '投稿がシステムに存在しません。')
            else:
                messages.error(request, 'Bài đăng không tồn tại trong hệ thống.')
            return redirect('available_posts')
        
        # Check if post is still available
        if post.status != 'active':
            if request.user.nationality == 'japanese':
                status_messages = {
                    'matched': 'この投稿は既に他の人によって受け入れられています。',
                    'completed': 'この投稿は完了しています。',
                    'cancelled': 'この投稿はキャンセルされています。'
                }
            else:
                status_messages = {
                    'matched': 'Bài đăng này đã được chấp nhận bởi người khác.',
                    'completed': 'Bài đăng này đã hoàn thành.',
                    'cancelled': 'Bài đăng này đã bị hủy.'
                }
            error_msg = status_messages.get(post.status, 'この投稿は受け入れることができません。' if request.user.nationality == 'japanese' else 'Bài đăng này không còn khả dụng để chấp nhận.')
            messages.error(request, error_msg)
            return redirect('available_posts')
        
        # Check if user is trying to accept their own post
        if (post.vietnamese_user == request.user) or (post.japanese_user == request.user):
            if request.user.nationality == 'japanese':
                messages.error(request, '自分の投稿を受け入れることはできません。')
            else:
                messages.error(request, 'Bạn không thể chấp nhận bài đăng của chính mình.')
            return redirect('available_posts')
        
        # Set the appropriate user based on nationality
        if request.user.nationality == 'japanese':
            post.japanese_user = request.user
        else:
            post.vietnamese_user = request.user
        
        # Store the phrase chosen by the person who accepted the post
        post.accepted_phrase = phrase
        
        post.phrase = phrase
        post.status = 'matched'
        post.save()
        
        # Create chat room
        chat_room, created = ChatRoom.objects.get_or_create(post=post)
        
        # Create welcome message in appropriate language
        if request.user.nationality == 'japanese':
            welcome_message = f"こんにちは！あなたの投稿を受け入れました。一緒にベトナム語を学びましょう！"
        else:
            welcome_message = f"Xin chào! Tôi đã chấp nhận bài đăng của bạn. Hãy cùng trò chuyện và học tiếng Nhật nhé!"
        
        Message.objects.create(
            chat_room=chat_room,
            sender=request.user,
            content=welcome_message
        )
        
        if request.user.nationality == 'japanese':
            messages.success(request, f'投稿を受け入れました！今すぐパートナーとチャットを始めることができます。')
        else:
            messages.success(request, f'Đã chấp nhận bài đăng thành công! Bạn có thể bắt đầu chat với partner ngay bây giờ.')
        return redirect('chat_room', room_id=chat_room.id)
        
    except Exception as e:
        if request.user.nationality == 'japanese':
            messages.error(request, f'エラーが発生しました: {str(e)}')
        else:
            messages.error(request, f'Đã xảy ra lỗi: {str(e)}')
        return redirect('available_posts')

@login_required
def cancel_accept_post(request, post_id):
    """Cancel accepting a language exchange post - Both Vietnamese and Japanese users can cancel their accepted posts"""
    
    # Get the post, allowing both japanese_user and vietnamese_user to cancel their accepted posts
    post = get_object_or_404(
        LanguageExchangePost, 
        id=post_id, 
        status='matched'
    )
    
    # Check if user owns this post
    if not (post.japanese_user == request.user or post.vietnamese_user == request.user):
        if request.user.nationality == 'japanese':
            messages.error(request, 'この投稿をキャンセルする権限がありません。')
        else:
            messages.error(request, 'Bạn không có quyền hủy bài đăng này.')
        return redirect('dashboard')
    
    # Reset post status based on user nationality
    if request.user.nationality == 'japanese':
        post.japanese_user = None
    else:
        post.vietnamese_user = None
    post.status = 'active'
    post.save()
    
    # Delete chat room and messages
    try:
        chat_room = ChatRoom.objects.get(post=post)
        chat_room.delete()
    except ChatRoom.DoesNotExist:
        pass
    
    if request.user.nationality == 'japanese':
        messages.success(request, '投稿の受け入れをキャンセルしました。')
    else:
        messages.success(request, 'Đã hủy chấp nhận bài đăng.')
    return redirect('dashboard')

@login_required
def create_partner_request(request):
    """Create a partner request"""
    if request.method == 'POST':
        form = PartnerRequestForm(request.POST, user=request.user)
        if form.is_valid():
            partner_request = form.save(commit=False)
            partner_request.requester = request.user
            partner_request.save()
            messages.success(request, 'Partner request created successfully!')
            return redirect('my_partner_requests')
    else:
        form = PartnerRequestForm(user=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'event_creation/create_partner_request.html', context)

@login_required
def my_partner_requests(request):
    """Display user's own partner requests"""
    partner_requests = PartnerRequest.objects.filter(requester=request.user)
    
    context = {
        'partner_requests': partner_requests,
    }
    
    return render(request, 'event_creation/my_partner_requests.html', context)

@login_required
def accept_partner_request(request, request_id):
    """Accept a partner request"""
    partner_request = get_object_or_404(PartnerRequest, id=request_id, status='active')
    
    # Check if user is compatible
    if request.user.nationality == partner_request.requester.nationality:
        messages.error(request, 'You cannot accept a request from someone with the same nationality.')
        return redirect('find_partners')
    
    # Create chat room
    chat_room, created = ChatRoom.objects.get_or_create(partner_request=partner_request)
    
    # Update partner request status and set accepted_by
    partner_request.status = 'matched'
    partner_request.accepted_by = request.user
    partner_request.save()
    
    messages.success(request, 'Partner request accepted! You can now chat with your language partner.')
    return redirect('chat_room', room_id=chat_room.id)



@login_required
def cultural_lessons(request):
    """Display cultural lessons for different locations"""
    city = request.GET.get('city', '')
    difficulty = request.GET.get('difficulty', '')
    
    lessons = CulturalLesson.objects.all()
    
    if city:
        lessons = lessons.filter(location__city=city)
    if difficulty:
        lessons = lessons.filter(difficulty=difficulty)
    
    context = {
        'lessons': lessons,
        'cities': CulturalLocation.objects.values_list('city', flat=True).distinct(),
        'difficulties': CulturalLesson.DIFFICULTY_CHOICES,
        'selected_city': city,
        'selected_difficulty': difficulty,
    }
    
    return render(request, 'event_creation/cultural_lessons.html', context)

@login_required
def cultural_challenges(request):
    """Display cultural challenges for different locations"""
    city = request.GET.get('city', '')
    difficulty = request.GET.get('difficulty', '')
    
    challenges = CulturalChallenge.objects.all()
    
    if city:
        challenges = challenges.filter(location__city=city)
    if difficulty:
        challenges = challenges.filter(difficulty=difficulty)
    
    context = {
        'challenges': challenges,
        'cities': CulturalLocation.objects.values_list('city', flat=True).distinct(),
        'difficulties': CulturalChallenge.DIFFICULTY_CHOICES,
        'selected_city': city,
        'selected_difficulty': difficulty,
    }
    
    return render(request, 'event_creation/cultural_challenges.html', context)

@login_required
def start_working_session(request, post_id):
    """Start a working session for a matched language exchange post"""
    post = get_object_or_404(LanguageExchangePost, id=post_id)
    
    # Check if user is part of this post
    if request.user not in [post.japanese_user, post.vietnamese_user]:
        messages.error(request, 'Bạn không có quyền truy cập phiên làm việc này.')
        return redirect('my_accepted_posts')
    
    # Check if post is matched
    if post.status != 'matched':
        messages.error(request, 'Chỉ có thể bắt đầu phiên làm việc với bài đăng đã được kết nối.')
        return redirect('my_accepted_posts')
    
    # Get the accepted phrase for this session
    accepted_phrase = post.accepted_phrase
    
    if not accepted_phrase:
        messages.error(request, 'Chưa có cụm từ nào được chọn cho phiên làm việc này.')
        return redirect('my_accepted_posts')
    
    # Map phrase category to lesson template number (1-10)
    # This maps the phrase category to a specific lesson template
    category_to_lesson = {
        'greetings': 1,
        'food': 2, 
        'shopping': 3,
        'transport': 4,
        'emergency': 5,
        'daily': 6,
        'business': 7,
        'travel': 8,
        'culture': 9,
        'tourism': 10,
    }
    
    # Default to lesson 1 if category not found
    lesson_number = category_to_lesson.get(accepted_phrase.category, 1)
    
    # Determine partner_id (the other user in the post)
    if request.user == post.japanese_user:
        partner_id = post.vietnamese_user.id if post.vietnamese_user else None
    else:
        partner_id = post.japanese_user.id if post.japanese_user else None
    
    if not partner_id:
        messages.error(request, 'Không thể xác định đối tác cho phiên làm việc này.')
        return redirect('my_accepted_posts')
    
    # Redirect to study session with lesson template number
    return redirect('study', partner_id=partner_id, post_id=post_id, phrase_id=lesson_number)