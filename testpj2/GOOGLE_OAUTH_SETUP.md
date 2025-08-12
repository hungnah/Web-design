# 🔐 Google OAuth Integration Guide

## 📋 Tổng quan

Hướng dẫn này sẽ giúp bạn tích hợp Google OAuth vào hệ thống Vietnam-Japan Connect để cho phép người dùng đăng nhập và đăng ký bằng tài khoản Google.

## 🚀 Bước 1: Thiết lập Google Cloud Console

### 1.1 Tạo project mới
1. Truy cập [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo project mới hoặc chọn project hiện có
3. Đặt tên project: `vietnam-japan-connect`             

### 1.2 Bật Google+ API
1. Vào **APIs & Services** > **Library**
2. Tìm kiếm "Google+ API" hoặc "Google Identity"
3. Bật **Google+ API** và **Google Identity API**

### 1.3 Tạo OAuth 2.0 Credentials
1. Vào **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth 2.0 Client IDs**
3. Chọn **Web application**
4. Điền thông tin:
   - **Name**: Vietnam-Japan Connect OAuth
   - **Authorized JavaScript origins**: 
     - `http://localhost:8000`
     - `https://yourdomain.com`
   - **Authorized redirect URIs**:
     - `http://localhost:8000/auth/google/callback/`
     - `https://yourdomain.com/auth/google/callback/`

### 1.4 Lưu thông tin credentials
- **Client ID**: `your-client-id.apps.googleusercontent.com` //566554554772-21ftbvjdlhim06422ee4ou3qu4b8iuq6.apps.googleusercontent.com
- **Client Secret**: `your-client-secret`//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

## 🛠️ Bước 2: Cài đặt dependencies

### 2.1 Cài đặt packages
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install requests-oauthlib
```

### 2.2 Thêm vào requirements.txt
```txt
google-auth==2.23.0
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
requests-oauthlib==1.3.1
```

## 🔧 Bước 3: Cập nhật Django Settings

### 3.1 Thêm Google OAuth settings
```python
# settings.py

# Google OAuth Settings
GOOGLE_OAUTH2_CLIENT_ID = 'your-client-id.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'your-client-secret'
GOOGLE_OAUTH2_REDIRECT_URI = 'http://localhost:8000/auth/google/callback/'

# OAuth URLs
GOOGLE_OAUTH2_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_OAUTH2_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_OAUTH2_USERINFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'
```

### 3.2 Cài đặt Google OAuth URLs
```python
# urls.py (main project)
from django.urls import path, include

urlpatterns = [
    # ... existing urls
    path('auth/', include('user_profile.oauth_urls')),
]
```

## 📁 Bước 4: Tạo OAuth Views

### 4.1 Tạo file oauth_views.py
```python
# user_profile/oauth_views.py
import requests
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from .models import CustomUser

def google_oauth_login(request):
    """Redirect user to Google OAuth"""
    oauth_url = (
        f"{settings.GOOGLE_OAUTH2_AUTH_URL}?"
        f"client_id={settings.GOOGLE_OAUTH2_CLIENT_ID}&"
        f"redirect_uri={settings.GOOGLE_OAUTH2_REDIRECT_URI}&"
        f"scope=email profile&"
        f"response_type=code&"
        f"access_type=offline"
    )
    return redirect(oauth_url)

def google_oauth_callback(request):
    """Handle Google OAuth callback"""
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error:
        messages.error(request, 'Đăng nhập Google thất bại.')
        return redirect('login')
    
    if not code:
        messages.error(request, 'Không nhận được mã xác thực từ Google.')
        return redirect('login')
    
    # Exchange code for access token
    token_data = {
        'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.GOOGLE_OAUTH2_REDIRECT_URI,
    }
    
    token_response = requests.post(
        settings.GOOGLE_OAUTH2_TOKEN_URL,
        data=token_data
    )
    
    if token_response.status_code != 200:
        messages.error(request, 'Không thể lấy token từ Google.')
        return redirect('login')
    
    token_info = token_response.json()
    access_token = token_info.get('access_token')
    
    # Get user info from Google
    headers = {'Authorization': f'Bearer {access_token}'}
    user_response = requests.get(
        settings.GOOGLE_OAUTH2_USERINFO_URL,
        headers=headers
    )
    
    if user_response.status_code != 200:
        messages.error(request, 'Không thể lấy thông tin người dùng từ Google.')
        return redirect('login')
    
    user_info = user_response.json()
    
    # Create or get user
    user, created = CustomUser.objects.get_or_create(
        email=user_info['email'],
        defaults={
            'username': user_info['email'],
            'first_name': user_info.get('given_name', ''),
            'last_name': user_info.get('family_name', ''),
            'is_active': True,
            'google_id': user_info['id'],
        }
    )
    
    if created:
        # Set random password for Google users
        user.set_password(CustomUser.objects.make_random_password())
        user.save()
        messages.success(request, 'Tài khoản Google đã được tạo thành công!')
    
    # Login user
    login(request, user)
    messages.success(request, f'Chào mừng {user.get_full_name()}!')
    
    return redirect('dashboard')
```

### 4.2 Tạo file oauth_urls.py
```python
# user_profile/oauth_urls.py
from django.urls import path
from . import oauth_views

app_name = 'oauth'

urlpatterns = [
    path('google/', oauth_views.google_oauth_login, name='google_login'),
    path('google/callback/', oauth_views.google_oauth_callback, name='google_callback'),
]
```

## 🎨 Bước 5: Cập nhật giao diện

### 5.1 Cập nhật nút Google trong login.html
```html
<!-- Thay thế nút Google hiện tại -->
<button type="button" class="btn-google" onclick="window.location.href='{% url 'oauth:google_login' %}'">
    <div class="google-icon"></div>
    <span>Đăng nhập bằng Google</span>
</button>
```

### 5.2 Thêm nút Google vào trang đăng ký
```html
<!-- Trong register.html -->
<div class="divider">
    <span>hoặc</span>
</div>

<button type="button" class="btn-google" onclick="window.location.href='{% url 'oauth:google_login' %}'">
    <div class="google-icon"></div>
    <span>Đăng ký bằng Google</span>
</button>
```

## 🔒 Bước 6: Bảo mật và xử lý lỗi

### 6.1 Thêm CSRF protection
```python
# oauth_views.py
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def google_oauth_callback(request):
    # ... existing code
```

### 6.2 Xử lý lỗi chi tiết
```python
# oauth_views.py
import logging

logger = logging.getLogger(__name__)

def google_oauth_callback(request):
    try:
        # ... existing code
    except requests.RequestException as e:
        logger.error(f"Google OAuth request failed: {e}")
        messages.error(request, 'Lỗi kết nối với Google. Vui lòng thử lại.')
        return redirect('login')
    except Exception as e:
        logger.error(f"Google OAuth error: {e}")
        messages.error(request, 'Đã xảy ra lỗi. Vui lòng thử lại.')
        return redirect('login')
```

## 📱 Bước 7: Responsive Design

### 7.1 CSS cho mobile
```css
@media (max-width: 480px) {
    .btn-google {
        padding: 0.875rem 1.5rem;
        font-size: 0.9rem;
    }
    
    .google-icon {
        width: 18px;
        height: 18px;
    }
}
```

### 7.2 Touch optimization
```css
.btn-google {
    min-height: 44px; /* Minimum touch target */
    -webkit-tap-highlight-color: transparent;
}

.btn-google:active {
    transform: scale(0.98);
}
```

## 🧪 Bước 8: Testing

### 8.1 Test local development
```bash
# Chạy server
python manage.py runserver

# Test OAuth flow
# 1. Truy cập /login/
# 2. Click "Đăng nhập bằng Google"
# 3. Chọn tài khoản Google
# 4. Kiểm tra callback
```

### 8.2 Test production
```bash
# Cập nhật redirect URIs trong Google Console
# Test với domain thực tế
# Kiểm tra HTTPS
```

## 🚀 Bước 9: Deployment

### 9.1 Environment variables
```bash
# .env file
GOOGLE_OAUTH2_CLIENT_ID=your-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-client-secret
GOOGLE_OAUTH2_REDIRECT_URI=https://yourdomain.com/auth/google/callback/
```

### 9.2 Production settings
```python
# settings.py
import os

GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')
GOOGLE_OAUTH2_REDIRECT_URI = os.environ.get('GOOGLE_OAUTH2_REDIRECT_URI')
```

## 📊 Bước 10: Monitoring và Analytics

### 10.1 Logging
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/oauth.log',
        },
    },
    'loggers': {
        'user_profile.oauth_views': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 10.2 Analytics tracking
```python
# oauth_views.py
def google_oauth_callback(request):
    # ... existing code
    
    # Track successful login
    if created:
        # New user registration
        analytics.track('user_registered', {
            'method': 'google',
            'user_id': user.id
        })
    else:
        # Existing user login
        analytics.track('user_logged_in', {
            'method': 'google',
            'user_id': user.id
        })
```

## 🔧 Troubleshooting

### Lỗi thường gặp:
1. **Invalid redirect URI**: Kiểm tra redirect URI trong Google Console
2. **Client ID/Secret**: Đảm bảo credentials đúng
3. **HTTPS required**: Production phải dùng HTTPS
4. **Scope permissions**: Kiểm tra quyền truy cập email/profile

### Debug tips:
```python
# Thêm debug logging
import logging
logger = logging.getLogger(__name__)

logger.debug(f"Token response: {token_response.text}")
logger.debug(f"User info: {user_info}")
```

## 📚 Tài liệu tham khảo

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Django Authentication](https://docs.djangoproject.com/en/stable/topics/auth/)
- [Google Identity Platform](https://developers.google.com/identity)

---

**Lưu ý**: Hướng dẫn này cung cấp framework cơ bản. Trong thực tế, bạn cần:
- Xử lý bảo mật kỹ lưỡng hơn
- Thêm rate limiting
- Implement proper error handling
- Test thoroughly trước khi deploy production
