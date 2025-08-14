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
from .models import VietnamesePhrase, CafeLocation, LanguageExchangePost, PartnerRequest, Lesson, LessonPhrase, QuizQuestion, TheorySection
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
    
    context = {
        'post_id': post_id,
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
    # if request.user.nationality != 'japanese':
    #     return redirect('dashboard')
    
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
    """Display lesson detail with phrases, theory sections, and quiz questions"""
    if request.user.nationality != 'japanese':
        return redirect('dashboard')
    """Display lesson detail with phrases"""
    # if request.user.nationality != 'japanese':
    #     return redirect('dashboard')
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    phrases = lesson.phrases.all()
    theory_sections = lesson.theory_sections.all()
    quiz_questions = lesson.quiz_questions.all()
    
    context = {
        'lesson': lesson,
        'phrases': phrases,
        'theory_sections': theory_sections,
        'quiz_questions': quiz_questions,
    }
    
    return render(request, 'event_creation/lesson_detail.html', context)

@login_required
def theory_section_detail(request, lesson_id, section_id):
    """Display theory section detail with phrases and conversation examples"""
    if request.user.nationality != 'japanese':
        return redirect('dashboard')
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    theory_section = get_object_or_404(TheorySection, id=section_id, lesson=lesson)
    phrases = theory_section.phrases.all()
    conversations = theory_section.conversations.all()
    
    context = {
        'lesson': lesson,
        'theory_section': theory_section,
        'phrases': phrases,
        'conversations': conversations,
    }
    
    return render(request, 'event_creation/theory_section_detail.html', context)

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
def create_post(request, phrase_id=None):
    """Create a language exchange post for both Vietnamese and Japanese users"""
    phrase = None
    
    if phrase_id:
        phrase = get_object_or_404(VietnamesePhrase, id=phrase_id)
    
    # Test form creation
    test_form = LanguageExchangePostForm(user=request.user)
    print(f"DEBUG: Test form created for user {request.user.username}")
    print(f"DEBUG: Form fields: {list(test_form.fields.keys())}")
    print(f"DEBUG: User type field initial: {test_form.fields['user_type'].initial}")
    
    if request.method == 'POST':
        print(f"DEBUG: POST request received from user {request.user.username} with nationality {request.user.nationality}")
        form = LanguageExchangePostForm(request.POST, user=request.user)
        print(f"DEBUG: Form is valid: {form.is_valid()}")
        if form.is_valid():
            print(f"DEBUG: Form data: {form.cleaned_data}")
            post = form.save(commit=False)
            
            # Set user based on nationality
            if request.user.nationality == 'vietnamese':
                post.vietnamese_user = request.user
                post.user_type = 'vietnamese'
                print(f"DEBUG: Set Vietnamese user: {post.vietnamese_user}")
            elif request.user.nationality == 'japanese':
                post.japanese_user = request.user
                post.user_type = 'japanese'
                print(f"DEBUG: Set Japanese user: {post.japanese_user}")
            
            post.phrase = phrase
            print(f"DEBUG: About to save post with user_type: {post.user_type}")
            try:
                post.save()
                print(f"DEBUG: Post saved successfully with ID: {post.id}")
                
                if request.user.nationality == 'vietnamese':
                    messages.success(request, 'Bài đăng đã được tạo thành công! Người dùng Nhật Bản sẽ có thể xem và chấp nhận.')
                else:
                    messages.success(request, '投稿が正常に作成されました！ベトナムのユーザーが閲覧・承認できるようになります。')
                
                return redirect('my_posts')
            except Exception as e:
                print(f"DEBUG: Error saving post: {e}")
                messages.error(request, f'Lỗi khi tạo bài đăng: {e}')
        else:
            print(f"DEBUG: Form errors: {form.errors}")
            for field, errors in form.errors.items():
                print(f"DEBUG: Field {field} errors: {errors}")
    else:
        form = LanguageExchangePostForm(user=request.user)
    
    context = {
        'phrase': phrase,
        'form': form,
        'debug': True,  # Enable debug mode
    }
    
    return render(request, 'event_creation/create_post.html', context)

@login_required
def edit_post(request, post_id):
    """Edit a language exchange post for both Vietnamese and Japanese users"""
    if request.user.nationality == 'vietnamese':
        post = get_object_or_404(LanguageExchangePost, id=post_id, vietnamese_user=request.user, user_type='vietnamese')
    else:
        post = get_object_or_404(LanguageExchangePost, id=post_id, japanese_user=request.user, user_type='japanese')
    
    # Only allow editing active posts (not matched ones)
    if post.status != 'active':
        if request.user.nationality == 'vietnamese':
            messages.error(request, 'Chỉ có thể chỉnh sửa bài đăng chưa được chấp nhận.')
        else:
            messages.error(request, '承認されていない投稿のみ編集できます。')
        return redirect('my_posts')
    
    if request.method == 'POST':
        form = LanguageExchangePostForm(request.POST, instance=post, user=request.user)
        if form.is_valid():
            form.save()
            if request.user.nationality == 'vietnamese':
                messages.success(request, 'Bài đăng đã được cập nhật thành công!')
            else:
                messages.success(request, '投稿が正常に更新されました！')
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
    """Display user's own posts for both Vietnamese and Japanese users"""
    if request.user.nationality == 'vietnamese':
        posts = LanguageExchangePost.objects.filter(vietnamese_user=request.user, user_type='vietnamese')
    else:
        posts = LanguageExchangePost.objects.filter(japanese_user=request.user, user_type='japanese')
    
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
def accept_post(request, post_id, phrase_id):
    """Accept a language exchange post - Vietnamese users accept Japanese posts, Japanese users accept Vietnamese posts"""
    phrase = get_object_or_404(VietnamesePhrase, id=phrase_id)
    post = get_object_or_404(LanguageExchangePost, id=post_id, status='active')
    
    # Check if user can accept this post
    if request.user.nationality == 'vietnamese':
        # Vietnamese users can only accept posts created by Japanese users
        if post.user_type != 'japanese':
            messages.error(request, 'Bạn chỉ có thể chấp nhận bài đăng từ người dùng Nhật Bản.')
            return redirect('dashboard')
        if post.vietnamese_user:
            messages.error(request, 'Bài đăng này đã được chấp nhận bởi người dùng khác.')
            return redirect('dashboard')
        
        # Set Vietnamese partner
        post.vietnamese_partner = request.user
        post.phrase = phrase
        post.status = 'matched'
        post.save()
        
        welcome_message = f"Xin chào! Tôi đã chấp nhận bài đăng của bạn. Hãy cùng trò chuyện và học tiếng Việt nhé!"
        
    elif request.user.nationality == 'japanese':
        # Japanese users can only accept posts created by Vietnamese users
        if post.user_type != 'vietnamese':
            messages.error(request, 'ベトナムのユーザーの投稿のみ承認できます。')
            return redirect('dashboard')
        if post.japanese_user:
            messages.error(request, 'この投稿は既に他のユーザーによって承認されています。')
            return redirect('dashboard')
        
        # Set Japanese partner
        post.japanese_partner = request.user
        post.phrase = phrase
        post.status = 'matched'
        post.save()
        
        welcome_message = f"こんにちは！あなたの投稿を承認しました。一緒にベトナム語を学びましょう！"
    
    # Create chat room
    chat_room, created = ChatRoom.objects.get_or_create(post=post)
    
    # Create welcome message
    Message.objects.create(
        chat_room=chat_room,
        sender=request.user,
        content=welcome_message
    )
    
    if request.user.nationality == 'vietnamese':
        messages.success(request, f'Đã chấp nhận bài đăng thành công! Bạn có thể chat với {post.creator.full_name or post.creator.username} ngay bây giờ.')
    else:
        messages.success(request, f'投稿の承認が完了しました！今すぐ{post.creator.full_name or post.creator.username}とチャットできます。')
    
    return redirect('chat_room', room_id=chat_room.id)

@login_required
def cancel_accept_post(request, post_id):
    """Cancel accepting a language exchange post for both Vietnamese and Japanese users"""
    if request.user.nationality == 'vietnamese':
        post = get_object_or_404(LanguageExchangePost, id=post_id, status='matched', vietnamese_partner=request.user)
        
        # Reset post status
        post.vietnamese_partner = None
        post.status = 'active'
        post.save()
        
        messages.success(request, 'Đã hủy chấp nhận bài đăng.')
        
    elif request.user.nationality == 'japanese':
        post = get_object_or_404(LanguageExchangePost, id=post_id, status='matched', japanese_partner=request.user)
        
        # Reset post status
        post.japanese_partner = None
        post.status = 'active'
        post.save()
        
        messages.success(request, '投稿の承認をキャンセルしました。')
    
    # Delete chat room and messages
    try:
        chat_room = ChatRoom.objects.get(post=post)
        chat_room.delete()
    except ChatRoom.DoesNotExist:
        pass
    
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
def all_theory_sections(request):
    """Display all theory sections across all lessons"""
    if request.user.nationality != 'japanese':
        return redirect('dashboard')
    
    category = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    
    lessons = Lesson.objects.all()
    
    if category:
        lessons = lessons.filter(category=category)
    if difficulty:
        lessons = lessons.filter(difficulty=difficulty)
    
    # Get theory sections for filtered lessons
    theory_sections = TheorySection.objects.filter(lesson__in=lessons).select_related('lesson')
    
    # Calculate total unique lessons
    total_lessons = lessons.count()
    
    context = {
        'lessons': lessons,
        'theory_sections': theory_sections,
        'total_lessons': total_lessons,
        'categories': Lesson.CATEGORY_CHOICES,
        'difficulties': Lesson.DIFFICULTY_CHOICES,
        'selected_category': category,
        'selected_difficulty': difficulty,
    }
    
    return render(request, 'event_creation/all_theory_sections.html', context)