import requests
import logging
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser

logger = logging.getLogger(__name__)

def google_oauth_login(request):
    """Redirect user to Google OAuth"""
    try:
        oauth_url = (
            f"{settings.GOOGLE_OAUTH2_AUTH_URL}?"
            f"client_id={settings.GOOGLE_OAUTH2_CLIENT_ID}&"
            f"redirect_uri={settings.GOOGLE_OAUTH2_REDIRECT_URI}&"
            f"scope=email profile&"
            f"response_type=code&"
            f"access_type=offline"
        )
        logger.info(f"Redirecting user to Google OAuth: {oauth_url}")
        return redirect(oauth_url)
    except Exception as e:
        logger.error(f"Error in google_oauth_login: {e}")
        messages.error(request, 'Không thể kết nối với Google. Vui lòng thử lại.')
        return redirect('login')

@csrf_exempt
def google_oauth_callback(request):
    """Handle Google OAuth callback"""
    try:
        code = request.GET.get('code')
        error = request.GET.get('error')
        
        if error:
            logger.error(f"Google OAuth error: {error}")
            messages.error(request, 'Đăng nhập Google thất bại.')
            return redirect('login')
        
        if not code:
            logger.error("No authorization code received from Google")
            messages.error(request, 'Không nhận được mã xác thực từ Google.')
            return redirect('login')
        
        logger.info("Received authorization code from Google")
        
        # Exchange code for access token
        token_data = {
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.GOOGLE_OAUTH2_REDIRECT_URI,
        }
        
        logger.info("Exchanging code for access token")
        token_response = requests.post(
            settings.GOOGLE_OAUTH2_TOKEN_URL,
            data=token_data,
            timeout=10
        )
        
        if token_response.status_code != 200:
            logger.error(f"Token exchange failed: {token_response.status_code} - {token_response.text}")
            messages.error(request, 'Không thể lấy token từ Google.')
            return redirect('login')
        
        token_info = token_response.json()
        access_token = token_info.get('access_token')
        
        if not access_token:
            logger.error("No access token received from Google")
            messages.error(request, 'Không nhận được access token từ Google.')
            return redirect('login')
        
        logger.info("Successfully received access token from Google")
        
        # Get user info from Google
        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(
            settings.GOOGLE_OAUTH2_USERINFO_URL,
            headers=headers,
            timeout=10
        )
        
        if user_response.status_code != 200:
            logger.error(f"User info request failed: {user_response.status_code} - {user_response.text}")
            messages.error(request, 'Không thể lấy thông tin người dùng từ Google.')
            return redirect('login')
        
        user_info = user_response.json()
        logger.info(f"Received user info from Google: {user_info.get('email', 'No email')}")
        
        # Validate required fields
        if not user_info.get('email'):
            logger.error("No email received from Google")
            messages.error(request, 'Google không cung cấp email. Vui lòng thử lại.')
            return redirect('login')
        
        # Create or get user
        user, created = CustomUser.objects.get_or_create(
            email=user_info['email'],
            defaults={
                'username': user_info['email'],
                'first_name': user_info.get('given_name', ''),
                'last_name': user_info.get('family_name', ''),
                'is_active': True,
            }
        )
        
        if created:
            # Set random password for Google users
            import secrets
            random_password = secrets.token_urlsafe(16)
            user.set_password(random_password)
            user.save()
            logger.info(f"Created new user via Google OAuth: {user.email}")
            messages.success(request, 'Tài khoản Google đã được tạo thành công!')
        else:
            logger.info(f"Existing user logged in via Google OAuth: {user.email}")
        
        # Login user
        login(request, user)
        messages.success(request, f'Chào mừng {user.get_full_name() or user.email}!')
        
        # Redirect to appropriate page
        if hasattr(settings, 'LOGIN_REDIRECT_URL'):
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return redirect('home')  # or your dashboard URL
            
    except requests.RequestException as e:
        logger.error(f"Google OAuth request failed: {e}")
        messages.error(request, 'Lỗi kết nối với Google. Vui lòng thử lại.')
        return redirect('login')
    except Exception as e:
        logger.error(f"Google OAuth error: {e}")
        messages.error(request, 'Đã xảy ra lỗi. Vui lòng thử lại.')
        return redirect('login')
