"""
User Profile Views
Handles user authentication, registration, profile management, and dashboard display.
Supports both Vietnamese and Japanese users with different dashboard experiences.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, ProfileUpdateForm

from event_creation.models import LanguageExchangePost, PartnerRequest
from .forms import PointExchangeForm
from .models import DiscountVoucher

from .decorators import complete_profile_required

class CustomLoginView(LoginView):
    """
    Custom login view that redirects already authenticated users to dashboard
    and adds cache control headers to prevent back button issues
    """
    template_name = 'user_profile/login.html'
    success_url = reverse_lazy('dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        # If user is already authenticated, redirect to dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Add cache control headers to prevent caching
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        response['X-Frame-Options'] = 'DENY'
        return response
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Add cache control headers to prevent caching
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        response['X-Frame-Options'] = 'DENY'
        return response
    
    def get_success_url(self):
        return reverse('dashboard')
    
    def form_valid(self, form):
        """Handle successful login"""
        response = super().form_valid(form)
        # Clear any existing session data that might cause issues
        self.request.session.set_expiry(0)  # Session expires when browser closes
        return response

def register(request):
    """
    User registration view supporting both Vietnamese and Japanese users
    Validates age requirement (18+) and creates new user account
    """
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create new user and automatically log them in
            user = form.save()
            login(request, user)
            # Clear session data and set expiry
            request.session.set_expiry(0)
            messages.success(request, 'Registration successful! Welcome to Vietnam-Japan Connect!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        # Display empty registration form
        form = CustomUserCreationForm()
    
    response = render(request, 'user_profile/register.html', {'form': form})
    # Add cache control headers to prevent caching
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['X-Frame-Options'] = 'DENY'
    return response

def custom_logout(request):
    """Custom logout view that clears session and prevents back button issues"""
    # Clear session data
    request.session.flush()
    logout(request)
    
    # Redirect to home with message
    
    return redirect('home')

@login_required
@complete_profile_required
def dashboard(request):
    """
    Main dashboard view with different experiences for Vietnamese and Japanese users
    Japanese users: See their posts and learning materials
    Vietnamese users: See available posts and statistics
    """
    user = request.user
    
    # Set language preference based on nationality
    if user.nationality == 'japanese':
        user.preferred_language = 'ja'
        user.save()
        
        # Get user's recent language exchange posts
        recent_posts = LanguageExchangePost.objects.filter(
            vietnamese_user__nationality='vietnamese',
            status='active'
        ).select_related('phrase', 'cultural_location', 'vietnamese_user').order_by('-created_at')[:5]
        
        context = {
            'user': user,
            'recent_posts': recent_posts,
        }
        response = render(request, 'user_profile/japanese_dashboard.html', context)
    else:
        # Vietnamese user dashboard
        # For Vietnamese users, get available posts from Japanese users in their city
        available_posts = LanguageExchangePost.objects.filter(
            japanese_user__nationality='japanese',
            status='active'
        ).select_related('japanese_user', 'phrase', 'cultural_location')
        
        # Filter by user's city if specified
        if user.city and user.city != 'any':
            available_posts = available_posts.filter(cultural_location__city=user.city)
        
        # Order by most recent posts first and add some variety
        available_posts = available_posts.order_by('-created_at')
        
        # Add some additional context for better user experience
        for post in available_posts:
            # Ensure we have the necessary related data
            if not hasattr(post, 'phrase') or not post.phrase:
                continue

        # Get user's recent language exchange posts
        recent_posts = user.vietnamese_posts.all().select_related('phrase', 'cultural_location')[:5]
        
        # Calculate statistics
        accepted_posts_count = user.vietnamese_posts.filter(status='matched').count()
        available_posts_count = available_posts.count()
        
        context = {
            'user': user,
            'available_posts': available_posts[:6],  # Show first 6 posts
            'accepted_posts_count': accepted_posts_count,
            'available_posts_count': available_posts_count,
            'recent_posts' : recent_posts,
        }
        response = render(request, 'user_profile/vietnamese_dashboard.html', context)
    
    # Add cache control headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['X-Frame-Options'] = 'DENY'
    
    return response

@login_required
@complete_profile_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    response = render(request, 'user_profile/profile.html', {'form': form})
    # Add cache control headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['X-Frame-Options'] = 'DENY'
    
    return response

def guide(request):
    """Hướng dẫn sử dụng web bằng tiếng Nhật hoặc tiếng Việt"""
    language = request.GET.get('lang', 'ja')  # Default to Japanese
    if language == 'vi':
        response = render(request, 'user_profile/guide_vi.html')
    else:
        response = render(request, 'user_profile/guide.html')
    
    # Add cache control headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['X-Frame-Options'] = 'DENY'
    
    return response

def home(request):
    """Trang chủ với giới thiệu về website"""
    # Nếu người dùng đã đăng nhập, redirect về dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    response = render(request, 'home.html')
    # Thêm cache control headers để ngăn back button
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@login_required
def change_password_ajax(request):
    """Handle password change via AJAX modal on profile page."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

    form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return JsonResponse({'success': True, 'message': 'Đổi mật khẩu thành công'})

    # Collect field errors
    errors = {field: msgs for field, msgs in form.errors.items()}
    return JsonResponse({'success': False, 'errors': errors}, status=400)

@login_required
def point_exchange(request):
    """
    Disabled: Previously allowed exchanging points for vouchers. Now disabled because both sides are equal.
    """
    messages.error(request, 'Tính năng đổi điểm sang voucher đã bị tắt.')
    return redirect('dashboard')

@login_required
def my_vouchers(request):
    """
    View to display user's discount vouchers
    Only show active vouchers (not used or expired)
    """
    try:
        print(f"Debug: Getting vouchers for user: {request.user.username}")
        # Only show active vouchers that are still valid
        from django.utils import timezone
        now = timezone.now()
        
        active_vouchers = DiscountVoucher.objects.filter(
            user=request.user,
            status='active',
            valid_until__gt=now
        ).order_by('-created_at')
        
        # Also get used vouchers for statistics (but don't display them)
        used_vouchers = DiscountVoucher.objects.filter(
            user=request.user,
            status='used'
        )
        
        expired_vouchers = DiscountVoucher.objects.filter(
            user=request.user,
            status='active',
            valid_until__lte=now
        )
        
        print(f"Debug: Found {active_vouchers.count()} active vouchers")
        
        context = {
            'vouchers': active_vouchers,  # Only show active vouchers
            'user_points': request.user.point,
            'total_vouchers': active_vouchers.count() + used_vouchers.count() + expired_vouchers.count(),
            'active_vouchers_count': active_vouchers.count(),
            'used_vouchers_count': used_vouchers.count(),
            'expired_vouchers_count': expired_vouchers.count(),
        }
        return render(request, 'user_profile/my_vouchers.html', context)
    except Exception as e:
        print(f"Debug: Error in my_vouchers: {str(e)}")
        messages.error(request, f'Có lỗi xảy ra: {str(e)}')
        return redirect('/auth/dashboard/')

@login_required
def use_voucher(request, voucher_id):
    """
    View to mark a voucher as used
    Supports both GET (redirect) and POST (AJAX) requests
    """
    try:
        voucher = DiscountVoucher.objects.get(id=voucher_id, user=request.user)
        print(f"Debug: Voucher found: {voucher.id}, status: {voucher.status}")
        
        # Check if voucher can be used
        from django.utils import timezone
        now = timezone.now()
        
        if voucher.status == 'active' and now <= voucher.valid_until:
            print(f"Debug: Voucher is valid")
            # Mark voucher as used
            voucher.status = 'used'
            voucher.used_at = now
            voucher.save()
            print(f"Debug: Voucher marked as used successfully")
            
            # Update user points (optional: you can add points back or keep them deducted)
            # For now, we'll keep the points deducted as per the original design
            
            if request.method == 'POST':
                # Return JSON response for AJAX requests
                return JsonResponse({
                    'success': True,
                    'message': 'Voucher đã được sử dụng thành công!',
                    'voucher_id': voucher_id
                })
            else:
                # Return redirect for GET requests (fallback)
                messages.success(request, 'Voucher đã được sử dụng thành công!')
        else:
            print(f"Debug: Voucher is not valid")
            error_msg = 'Voucher đã hết hạn hoặc đã được sử dụng.'
            
            if request.method == 'POST':
                return JsonResponse({
                    'success': False,
                    'message': error_msg
                }, status=400)
            else:
                messages.error(request, error_msg)
                
    except DiscountVoucher.DoesNotExist:
        print(f"Debug: Voucher not found with id: {voucher_id}")
        error_msg = 'Voucher không tồn tại.'
        
        if request.method == 'POST':
            return JsonResponse({
                'success': False,
                'message': error_msg
            }, status=404)
        else:
            messages.error(request, error_msg)
            
    except Exception as e:
        print(f"Debug: Error in use_voucher: {str(e)}")
        error_msg = f'Có lỗi xảy ra: {str(e)}'
        
        if request.method == 'POST':
            return JsonResponse({
                'success': False,
                'message': error_msg
            }, status=500)
        else:
            messages.error(request, error_msg)
    
    # For GET requests, redirect back to vouchers page
    return redirect('/auth/my-vouchers/')

@login_required
def voucher_history(request):
    """
    View to display all vouchers including used and expired ones
    """
    try:
        print(f"Debug: Getting voucher history for user: {request.user.username}")
        
        # Get all vouchers for the user
        from django.utils import timezone
        all_vouchers = DiscountVoucher.objects.filter(user=request.user).order_by('-created_at')
        
        # Separate vouchers by status
        now = timezone.now()
        active_vouchers = [v for v in all_vouchers if v.status == 'active' and v.valid_until > now]
        used_vouchers = [v for v in all_vouchers if v.status == 'used']
        expired_vouchers = [v for v in all_vouchers if v.status == 'active' and v.valid_until <= now]
        
        context = {
            'all_vouchers': all_vouchers,
            'active_vouchers': active_vouchers,
            'used_vouchers': used_vouchers,
            'expired_vouchers': expired_vouchers,
            'user_points': request.user.point,
        }
        return render(request, 'user_profile/voucher_history.html', context)
    except Exception as e:
        print(f"Debug: Error in voucher_history: {str(e)}")
        messages.error(request, f'Có lỗi xảy ra: {str(e)}')
        return redirect('/auth/my-vouchers/')

