"""
Event Creation Views
Handles creation and management of language exchange content:
- Vietnamese phrases and lessons for Japanese learners
- Language exchange posts creation and editing
- Partner requests for finding language exchange partners
- Post acceptance and chat room creation
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import VietnamesePhrase, CafeLocation, LanguageExchangePost, PartnerRequest, Lesson, LessonPhrase, QuizQuestion
from .forms import LanguageExchangePostForm, PartnerRequestForm
from chat_system.models import ChatRoom, Message

@login_required
def phrase_list(request):
    """
    Display Vietnamese phrases with filtering options for Japanese users
    Allows filtering by category and difficulty level
    """
    if request.user.nationality != 'japanese':
        return redirect('dashboard')
    
    category = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    
    phrases = VietnamesePhrase.objects.all()
    
    if category:
        phrases = phrases.filter(category=category)
    if difficulty:
        phrases = phrases.filter(difficulty=difficulty)
    
    context = {
        'phrases': phrases,
        'categories': VietnamesePhrase.CATEGORY_CHOICES,
        'difficulties': VietnamesePhrase.DIFFICULTY_CHOICES,
        'selected_category': category,
        'selected_difficulty': difficulty,
    }
    
    return render(request, 'event_creation/phrase_list.html', context)

@login_required
def lessons(request):
    """Display Vietnamese language lessons"""
    if request.user.nationality != 'japanese':
        return redirect('dashboard')
    
    category = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    
    lessons = Lesson.objects.all()
    
    if category:
        lessons = lessons.filter(category=category)
    if difficulty:
        lessons = lessons.filter(difficulty=difficulty)
    
    context = {
        'lessons': lessons,
        'categories': Lesson.CATEGORY_CHOICES,
        'difficulties': Lesson.DIFFICULTY_CHOICES,
        'selected_category': category,
        'selected_difficulty': difficulty,
    }
    
    return render(request, 'event_creation/lessons.html', context)

@login_required
def lesson_detail(request, lesson_id):
    """Display lesson detail with phrases and quiz questions"""
    if request.user.nationality != 'japanese':
        return redirect('dashboard')
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    phrases = lesson.phrases.all()
    quiz_questions = lesson.quiz_questions.all()
    
    context = {
        'lesson': lesson,
        'phrases': phrases,
        'quiz_questions': quiz_questions,
    }
    
    return render(request, 'event_creation/lesson_detail.html', context)

@login_required
def lesson_quiz(request, lesson_id):
    """Display quiz for a specific lesson"""
    if request.user.nationality != 'japanese':
        return redirect('dashboard')
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    quiz_questions = lesson.quiz_questions.all()
    
    if request.method == 'POST':
        # Handle quiz submission
        score = 0
        total_questions = quiz_questions.count()
        user_answers = {}
        
        for question in quiz_questions:
            answer_key = f'question_{question.id}'
            user_answer = request.POST.get(answer_key)
            user_answers[question.id] = user_answer
            
            if user_answer == question.correct_answer:
                score += 1
        
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        context = {
            'lesson': lesson,
            'quiz_questions': quiz_questions,
            'user_answers': user_answers,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage,
            'show_results': True,
        }
        
        return render(request, 'event_creation/lesson_quiz.html', context)
    
    context = {
        'lesson': lesson,
        'quiz_questions': quiz_questions,
        'show_results': False,
    }
    
    return render(request, 'event_creation/lesson_quiz.html', context)

@login_required
def create_post(request, phrase_id):
    """Create a language exchange post"""
    if request.user.nationality != 'japanese':
        return redirect('dashboard')
    
    phrase = get_object_or_404(VietnamesePhrase, id=phrase_id)
    
    if request.method == 'POST':
        form = LanguageExchangePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.japanese_user = request.user
            post.phrase = phrase
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('my_posts')
    else:
        form = LanguageExchangePostForm()
    
    context = {
        'phrase': phrase,
        'form': form,
    }
    
    return render(request, 'event_creation/create_post.html', context)

@login_required
def edit_post(request, post_id):
    """Edit a language exchange post"""
    if request.user.nationality != 'japanese':
        return redirect('dashboard')
    
    post = get_object_or_404(LanguageExchangePost, id=post_id, japanese_user=request.user)
    
    # Only allow editing active posts (not matched ones)
    if post.status != 'active':
        messages.error(request, 'Chỉ có thể chỉnh sửa bài đăng chưa được chấp nhận.')
        return redirect('my_posts')
    
    if request.method == 'POST':
        form = LanguageExchangePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bài đăng đã được cập nhật thành công!')
            return redirect('my_posts')
    else:
        form = LanguageExchangePostForm(instance=post)
    
    context = {
        'post': post,
        'form': form,
    }
    
    return render(request, 'event_creation/edit_post.html', context)

@login_required
def my_posts(request):
    """Display user's own posts"""
    if request.user.nationality == 'japanese':
        posts = LanguageExchangePost.objects.filter(japanese_user=request.user)
    else:
        posts = LanguageExchangePost.objects.filter(vietnamese_user=request.user)
    
    # Calculate counts for statistics
    matched_posts_count = posts.filter(status='matched').count()
    active_posts_count = posts.filter(status='active').count()
    
    # Get recent accepted posts for notifications
    recent_accepted_posts = posts.filter(status='matched').order_by('-updated_at')[:3]
    
    context = {
        'posts': posts,
        'matched_posts_count': matched_posts_count,
        'active_posts_count': active_posts_count,
        'recent_accepted_posts': recent_accepted_posts,
    }
    
    return render(request, 'event_creation/my_posts.html', context)

@login_required
def accept_post(request, post_id):
    """Accept a language exchange post"""
    if request.user.nationality != 'vietnamese':
        return redirect('dashboard')
    
    post = get_object_or_404(LanguageExchangePost, id=post_id, status='active')
    post.vietnamese_user = request.user
    post.status = 'matched'
    post.save()
    
    # Create chat room
    chat_room, created = ChatRoom.objects.get_or_create(post=post)
    
    # Create welcome message
    welcome_message = f"Xin chào! Tôi đã chấp nhận bài đăng của bạn. Hãy cùng trò chuyện và học tiếng Việt nhé!"
    Message.objects.create(
        chat_room=chat_room,
        sender=request.user,
        content=welcome_message
    )
    
    messages.success(request, f'Đã chấp nhận bài đăng thành công! Bạn có thể chat với {post.japanese_user.full_name or post.japanese_user.username} ngay bây giờ.')
    return redirect('chat_room', room_id=chat_room.id)

@login_required
def cancel_accept_post(request, post_id):
    """Cancel accepting a language exchange post"""
    if request.user.nationality != 'vietnamese':
        return redirect('dashboard')
    
    post = get_object_or_404(LanguageExchangePost, id=post_id, status='matched', vietnamese_user=request.user)
    
    # Reset post status
    post.vietnamese_user = None
    post.status = 'active'
    post.save()
    
    # Delete chat room and messages
    try:
        chat_room = ChatRoom.objects.get(post=post)
        chat_room.delete()
    except ChatRoom.DoesNotExist:
        pass
    
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