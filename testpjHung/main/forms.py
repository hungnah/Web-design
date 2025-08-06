from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post, Application

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Tên đăng nhập',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Mật khẩu'
        self.fields['password2'].label = 'Xác nhận mật khẩu'
        
        # Add Bootstrap classes
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'gender', 'birth_date', 'city', 'bio', 'avatar']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'full_name': 'Họ tên',
            'gender': 'Giới tính',
            'birth_date': 'Ngày sinh',
            'city': 'Thành phố',
            'bio': 'Giới thiệu',
            'avatar': 'Ảnh đại diện',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes for remaining fields
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'city', 'location', 'date', 'time', 'duration', 'estimated_cost', 'max_participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Tiêu đề',
            'description': 'Mô tả',
            'city': 'Thành phố',
            'location': 'Địa điểm cụ thể',
            'date': 'Ngày',
            'time': 'Giờ',
            'duration': 'Thời lượng (giờ)',
            'estimated_cost': 'Chi phí dự kiến (VNĐ)',
            'max_participants': 'Số người tối đa',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes for remaining fields
        for field_name, field in self.fields.items():
            if field_name not in ['date', 'time', 'description', 'city']:
                field.widget.attrs.update({'class': 'form-control'})

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Viết lời nhắn cho người đăng bài...', 'class': 'form-control'}),
        }
        labels = {
            'message': 'Lời nhắn',
        } 