from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .forms import CustomUserCreationForm, UserProfileForm, PostForm, ApplicationForm
from .models import UserProfile, Post, Application, GroupChat, Message
from django.contrib.auth.models import User
import json

def home(request):
    """Trang chủ - hiển thị bài đăng theo thành phố"""
    # Khởi tạo selected_city từ GET parameter hoặc None
    selected_city = request.GET.get('city')
    
    if request.user.is_authenticated:
        # Lấy thành phố của user hoặc thành phố được chọn
        if selected_city:
            posts = Post.objects.filter(city=selected_city, is_active=True)
        else:
            try:
                user_city = request.user.profile.city
                posts = Post.objects.filter(city=user_city, is_active=True)
                selected_city = user_city  # Cập nhật selected_city cho context
            except UserProfile.DoesNotExist:
                posts = Post.objects.filter(is_active=True)
    else:
        posts = Post.objects.filter(is_active=True)
    
    context = {
        'posts': posts,
        'cities': UserProfile.CITY_CHOICES,
        'selected_city': selected_city,
    }
    return render(request, 'main/home.html', context)

def register(request):
    """Đăng ký tài khoản"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Đăng ký thành công! Vui lòng cập nhật thông tin cá nhân.')
            return redirect('profile_setup')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'main/register.html', {'form': form})

def user_login(request):
    """Đăng nhập"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Chào mừng {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    
    return render(request, 'main/login.html')

@login_required
def user_logout(request):
    """Đăng xuất"""
    logout(request)
    messages.success(request, 'Đã đăng xuất thành công.')
    return redirect('home')

@login_required
def profile_setup(request):
    """Cập nhật thông tin cá nhân"""
    try:
        profile = request.user.profile
        form = UserProfileForm(instance=profile)
        is_update = True
    except UserProfile.DoesNotExist:
        form = UserProfileForm()
        is_update = False
    
    if request.method == 'POST':
        if is_update:
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
        else:
            form = UserProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
            return redirect('home')
    
    return render(request, 'main/profile_setup.html', {
        'form': form,
        'is_update': is_update
    })

@login_required
def create_post(request):
    """Đăng bài tuyển người đi chơi"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Đăng bài thành công!')
            return redirect('home')
    else:
        form = PostForm()
    
    return render(request, 'main/create_post.html', {'form': form})

@login_required
def post_detail(request, post_id):
    """Chi tiết bài đăng"""
    post = get_object_or_404(Post, id=post_id)
    applications = post.applications.all()
    has_applied = applications.filter(applicant=request.user).exists()
    
    if request.method == 'POST' and not has_applied:
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.post = post
            application.save()
            messages.success(request, 'Đã gửi đơn ứng tuyển!')
            return redirect('post_detail', post_id=post_id)
    else:
        form = ApplicationForm()
    
    context = {
        'post': post,
        'applications': applications,
        'form': form,
        'has_applied': has_applied,
    }
    return render(request, 'main/post_detail.html', context)

@login_required
def my_posts(request):
    """Bài đăng của tôi"""
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'main/my_posts.html', {'posts': posts})

@login_required
def my_applications(request):
    """Đơn ứng tuyển của tôi"""
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_at')
    return render(request, 'main/my_applications.html', {'applications': applications})

@login_required
def manage_applications(request, post_id):
    """Quản lý đơn ứng tuyển cho bài đăng"""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    applications = post.applications.all()
    
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')
        
        if application_id and action:
            application = get_object_or_404(Application, id=application_id, post=post)
            
            if action == 'approve':
                application.status = 'approved'
                application.save()
                post.current_participants += 1
                post.save()
                
                # Tạo hoặc cập nhật group chat
                group_chat, created = GroupChat.objects.get_or_create(post=post)
                group_chat.participants.add(application.applicant)
                
                messages.success(request, f'Đã chấp nhận {application.applicant.profile.full_name}')
            
            elif action == 'reject':
                application.status = 'rejected'
                application.save()
                messages.success(request, f'Đã từ chối {application.applicant.profile.full_name}')
    
    return render(request, 'main/manage_applications.html', {
        'post': post,
        'applications': applications
    })

@login_required
def chat_room(request, post_id):
    """Phòng chat cho bài đăng"""
    post = get_object_or_404(Post, id=post_id)
    
    # Kiểm tra xem user có tham gia bài đăng này không
    is_author = post.author == request.user
    is_participant = post.applications.filter(applicant=request.user, status='approved').exists()
    
    if not (is_author or is_participant):
        messages.error(request, 'Bạn không có quyền truy cập phòng chat này.')
        return redirect('home')
    
    try:
        group_chat = post.group_chat
        messages_list = group_chat.messages.all()
    except GroupChat.DoesNotExist:
        messages_list = []
    
    context = {
        'post': post,
        'messages': messages_list,
        'is_author': is_author,
    }
    return render(request, 'main/chat_room.html', context)

@csrf_exempt
@login_required
def send_message(request, post_id):
    """API gửi tin nhắn"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            
            if not content:
                return JsonResponse({'error': 'Nội dung tin nhắn không được để trống'}, status=400)
            
            post = get_object_or_404(Post, id=post_id)
            group_chat, created = GroupChat.objects.get_or_create(post=post)
            
            # Tạo tin nhắn mới
            message = Message.objects.create(
                group_chat=group_chat,
                sender=request.user,
                content=content
            )
            
            return JsonResponse({
                'id': message.id,
                'content': message.content,
                'sender': message.sender.profile.full_name,
                'timestamp': message.timestamp.strftime('%H:%M')
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dữ liệu không hợp lệ'}, status=400)
    
    return JsonResponse({'error': 'Phương thức không được hỗ trợ'}, status=405)
