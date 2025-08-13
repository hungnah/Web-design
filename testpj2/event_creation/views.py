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
from django.db.models import Q, Avg
from .models import VietnamesePhrase, CafeLocation, LanguageExchangePost, PartnerRequest, Lesson, LessonPhrase, QuizQuestion, TheorySection, ConnectionHistory
from .forms import LanguageExchangePostForm, PartnerRequestForm
from chat_system.models import ChatRoom, Message
from user_profile.models import CustomUser

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
    """Create a language exchange post"""
    # if request.user.nationality != 'japanese':
    #     return redirect('dashboard')
    phrase = None
    
    if phrase_id:
        phrase = get_object_or_404(VietnamesePhrase, id=phrase_id)
    
    if request.method == 'POST':
        form = LanguageExchangePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.vietnamese_user = request.user
            post.japanese_user_id = None
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
    # if request.user.nationality != 'japanese':
    #     return redirect('dashboard')
    
    post = get_object_or_404(LanguageExchangePost, id=post_id, vietnamese_user=request.user)
    
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
    if request.user.nationality == 'vietnamese':
        posts = LanguageExchangePost.objects.filter(vietnamese_user=request.user)
    else:
        posts = LanguageExchangePost.objects.filter(japanese_user=request.user)
    
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
    """Accept a language exchange post"""
    if request.user.nationality != 'japanese':
        return redirect('dashboard')
    
    phrase = get_object_or_404(VietnamesePhrase, id=phrase_id)
    
    post = get_object_or_404(LanguageExchangePost, id=post_id, status='active')
    post.japanese_user = request.user
    post.phrase = phrase
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
    
    # Tạo ConnectionHistory để theo dõi kết nối
    ConnectionHistory.objects.create(
        japanese_user=request.user,
        vietnamese_user=post.vietnamese_user,
        language_exchange_post=post,
        session_date=post.meeting_date,
        session_duration=60,  # Mặc định 60 phút
        session_type='offline',  # Mặc định offline
        status='active'
    )
    
    messages.success(request, f'Đã chấp nhận bài đăng thành công! Bạn có thể chat với {post.vietnamese_user.full_name or post.vietnamese_user.username} ngay bây giờ.')
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
    
    # Tạo ConnectionHistory để theo dõi kết nối
    # Xác định ai là người Nhật, ai là người Việt
    if request.user.nationality == 'japanese':
        japanese_user = request.user
        vietnamese_user = partner_request.requester
    else:
        japanese_user = partner_request.requester
        vietnamese_user = request.user
    
    ConnectionHistory.objects.create(
        japanese_user=japanese_user,
        vietnamese_user=vietnamese_user,
        partner_request=partner_request,
        session_date=timezone.now(),  # Sử dụng thời gian hiện tại
        session_duration=60,  # Mặc định 60 phút
        session_type='offline',  # Mặc định offline
        status='active'
    )
    
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

@login_required
def connection_history(request):
    """
    Hiển thị lịch sử kết nối và đánh giá cho người dùng
    """
    user = request.user
    
    if user.nationality == 'japanese':
        # Người Nhật xem kết nối với người Việt
        connections = ConnectionHistory.objects.filter(
            japanese_user=user
        ).select_related('vietnamese_user').prefetch_related().order_by('-session_date')
        
        # Thống kê
        total_connections = connections.count()
        completed_connections = connections.filter(status='fully_rated').count()
        waiting_rating = connections.filter(status='waiting_vietnamese_rating').count()
        average_rating = connections.filter(japanese_rating__isnull=False).aggregate(
            avg_rating=Avg('japanese_rating')
        )['avg_rating'] or 0
        
        # Thêm thông tin can_rate cho mỗi connection
        for connection in connections:
            connection.can_rate_value = connection.can_rate(user)
            # Đảm bảo rating values là số nguyên hợp lệ
            if connection.japanese_rating is not None and connection.japanese_rating != "":
                try:
                    connection.japanese_rating = int(connection.japanese_rating)
                    if connection.japanese_rating < 1 or connection.japanese_rating > 10:
                        connection.japanese_rating = None
                except (ValueError, TypeError):
                    connection.japanese_rating = None
            if connection.vietnamese_rating is not None and connection.vietnamese_rating != "":
                try:
                    connection.vietnamese_rating = int(connection.vietnamese_rating)
                    if connection.vietnamese_rating < 1 or connection.vietnamese_rating > 10:
                        connection.vietnamese_rating = None
                except (ValueError, TypeError):
                    connection.vietnamese_rating = None
            
            # Đảm bảo comment values là string hợp lệ
            if connection.japanese_comment is not None:
                connection.japanese_comment = str(connection.japanese_comment).strip()
                if connection.japanese_comment == "" or connection.japanese_comment.lower() == "none":
                    connection.japanese_comment = None
            if connection.vietnamese_comment is not None:
                connection.vietnamese_comment = str(connection.vietnamese_comment).strip()
                if connection.vietnamese_comment == "" or connection.vietnamese_comment.lower() == "none":
                    connection.vietnamese_comment = None
            
            # Debug: In ra thông tin đánh giá
            # print(f"Connection {connection.id}: Japanese rating: {connection.japanese_rating}, Vietnamese rating: {connection.vietnamese_rating}")
            # print(f"Connection {connection.id}: Japanese comment: {connection.japanese_comment}")
            # print(f"Connection {connection.id}: Status: {connection.status}")
        
        context = {
            'connections': connections,
            'total_connections': total_connections,
            'completed_connections': completed_connections,
            'waiting_rating': waiting_rating,
            'average_rating': round(average_rating, 1),
            'user_type': 'japanese',
            'page_title': 'Lịch sử kết nối của tôi',
            'debug': False  # Tắt debug
        }
        
    else:
        # Người Việt xem kết nối với người Nhật
        connections = ConnectionHistory.objects.filter(
            vietnamese_user=user
        ).select_related('japanese_user').prefetch_related().order_by('-session_date')
        
        # Thống kê
        total_connections = connections.count()
        completed_connections = connections.filter(status='fully_rated').count()
        waiting_rating = connections.filter(status='waiting_japanese_rating').count()
        average_rating = connections.filter(vietnamese_rating__isnull=False).aggregate(
            avg_rating=Avg('vietnamese_rating')
        )['avg_rating'] or 0
        
        # Thêm thông tin can_rate cho mỗi connection
        for connection in connections:
            connection.can_rate_value = connection.can_rate(user)
            # Đảm bảo rating values là số nguyên hợp lệ
            if connection.japanese_rating is not None:
                connection.japanese_rating = int(connection.japanese_rating)
            if connection.vietnamese_rating is not None:
                connection.vietnamese_rating = int(connection.vietnamese_rating)
            # Debug: In ra thông tin đánh giá
            # print(f"Connection {connection.id}: Japanese rating: {connection.japanese_rating}, Vietnamese rating: {connection.vietnamese_rating}")
            # print(f"Connection {connection.id}: Japanese comment: {connection.japanese_comment}")
            # print(f"Connection {connection.id}: Status: {connection.status}")
        
        context = {
            'connections': connections,
            'total_connections': total_connections,
            'completed_connections': completed_connections,
            'waiting_rating': waiting_rating,
            'average_rating': round(average_rating, 1),
            'user_type': 'vietnamese',
            'page_title': 'Lịch sử kết nối của tôi',
            'debug': False  # Tắt debug
        }
    
    return render(request, 'event_creation/connection_history.html', context)

@login_required
def rate_connection(request, connection_id):
    """
    Đánh giá kết nối từ người dùng
    """
    connection = get_object_or_404(ConnectionHistory, id=connection_id)
    user = request.user
    
    # Kiểm tra quyền đánh giá
    if not connection.can_rate(user):
        messages.error(request, 'Bạn không thể đánh giá kết nối này!')
        return redirect('connection_history')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and rating.isdigit() and 1 <= int(rating) <= 10:
            rating = int(rating)
            
            # Cập nhật đánh giá
            if user == connection.japanese_user:
                connection.japanese_rating = rating
                connection.japanese_comment = comment
                connection.japanese_rating_date = timezone.now()
            elif user == connection.vietnamese_user:
                connection.vietnamese_rating = rating
                connection.vietnamese_comment = comment
                connection.vietnamese_rating_date = timezone.now()
            
            # Cập nhật trạng thái
            connection.update_status()
            
            messages.success(request, 'Đánh giá của bạn đã được lưu thành công!')
            return redirect('connection_history')
        else:
            messages.error(request, 'Vui lòng chọn điểm đánh giá từ 1-10!')
    
    context = {
        'connection': connection,
        'user_type': 'japanese' if user.nationality == 'japanese' else 'vietnamese',
        'page_title': 'Đánh giá kết nối'
    }
    
    return render(request, 'event_creation/rate_connection.html', context)

@login_required
def add_connection_history(request):
    """
    Thêm lịch sử kết nối mới (dành cho admin hoặc người dùng có quyền)
    """
    if request.method == 'POST':
        # Xử lý form thêm kết nối mới
        japanese_user_id = request.POST.get('japanese_user')
        vietnamese_user_id = request.POST.get('vietnamese_user')
        session_date = request.POST.get('session_date')
        session_duration = request.POST.get('session_duration')
        session_type = request.POST.get('session_type')
        japanese_rating = request.POST.get('japanese_rating')
        japanese_comment = request.POST.get('japanese_comment')
        language_exchange_post_id = request.POST.get('language_exchange_post')
        partner_request_id = request.POST.get('partner_request')
        
        try:
            japanese_user = CustomUser.objects.get(id=japanese_user_id, nationality='japanese')
            vietnamese_user = CustomUser.objects.get(id=vietnamese_user_id, nationality='vietnamese')
            
            # Xử lý language_exchange_post hoặc partner_request nếu có
            language_exchange_post = None
            partner_request = None
            
            if language_exchange_post_id:
                language_exchange_post = LanguageExchangePost.objects.get(id=language_exchange_post_id)
            elif partner_request_id:
                partner_request = PartnerRequest.objects.get(id=partner_request_id)
            
            connection = ConnectionHistory.objects.create(
                japanese_user=japanese_user,
                vietnamese_user=vietnamese_user,
                language_exchange_post=language_exchange_post,
                partner_request=partner_request,
                session_date=session_date,
                session_duration=session_duration,
                session_type=session_type,
                japanese_rating=japanese_rating,
                japanese_comment=japanese_comment,
                notes=request.POST.get('notes', '')
            )
            
            # Tạo chat room nếu có language_exchange_post hoặc partner_request
            if language_exchange_post or partner_request:
                try:
                    from chat_system.models import ChatRoom
                    if language_exchange_post:
                        chat_room, created = ChatRoom.objects.get_or_create(post=language_exchange_post)
                    else:
                        chat_room, created = ChatRoom.objects.get_or_create(partner_request=partner_request)
                    
                    if created:
                        # Tạo tin nhắn chào mừng
                        from chat_system.models import Message
                        welcome_message = f"Kết nối mới đã được tạo giữa {japanese_user.full_name or japanese_user.username} và {vietnamese_user.full_name or vietnamese_user.username}"
                        Message.objects.create(
                            chat_room=chat_room,
                            sender=japanese_user,
                            content=welcome_message
                        )
                except Exception as e:
                    # Log lỗi nhưng không dừng quá trình
                    print(f"Lỗi khi tạo chat room: {e}")
            
            # Cập nhật trạng thái nếu có đánh giá
            if japanese_rating:
                try:
                    rating = int(japanese_rating)
                    if 1 <= rating <= 10:
                        connection.japanese_rating = rating
                        connection.save()
                        connection.update_status()
                    else:
                        messages.error(request, 'Điểm đánh giá phải từ 1-10!')
                        return redirect('add_connection_history')
                except ValueError:
                    messages.error(request, 'Điểm đánh giá không hợp lệ!')
                    return redirect('add_connection_history')
            
            messages.success(request, 'Đã thêm lịch sử kết nối thành công!')
            return redirect('connection_history')
            
        except CustomUser.DoesNotExist:
            messages.error(request, 'Không tìm thấy người dùng!')
        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')
    
    # Hiển thị form thêm kết nối
    japanese_users = CustomUser.objects.filter(nationality='japanese')
    vietnamese_users = CustomUser.objects.filter(nationality='vietnamese')
    
    # Lấy danh sách language exchange posts và partner requests
    language_exchange_posts = LanguageExchangePost.objects.filter(status='matched')
    partner_requests = PartnerRequest.objects.filter(status='matched')
    
    context = {
        'japanese_users': japanese_users,
        'vietnamese_users': vietnamese_users,
        'language_exchange_posts': language_exchange_posts,
        'partner_requests': partner_requests,
        'page_title': 'Thêm lịch sử kết nối'
    }
    
    return render(request, 'event_creation/add_connection_history.html', context)