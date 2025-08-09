# Vietnam-Japan Connect

Ứng dụng kết nối người Việt Nam và Nhật Bản để trao đổi ngôn ngữ và văn hóa.

## Tính năng chính

- **Đăng ký/Đăng nhập**: Hệ thống xác thực người dùng với thông tin cá nhân
- **Học cụm từ tiếng Việt**: Người Nhật có thể học các cụm từ tiếng Việt cơ bản
- **Tạo bài đăng trao đổi ngôn ngữ**: Người Nhật có thể tạo bài đăng để tìm người Việt Nam trao đổi ngôn ngữ
- **Tìm kiếm đối tác**: Người Việt Nam có thể tìm và chấp nhận các bài đăng trao đổi ngôn ngữ
- **Chat trực tuyến**: Hệ thống chat để người dùng có thể giao tiếp
- **Quản lý hồ sơ**: Cập nhật thông tin cá nhân và sở thích

## Cài đặt

1. **Clone dự án**:
```bash
git clone <repository-url>
cd testpj2
```

2. **Tạo môi trường ảo**:
```bash
python -m venv venv
```

3. **Kích hoạt môi trường ảo**:
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

4. **Cài đặt dependencies**:
```bash
pip install -r requirements.txt
```

5. **Chạy migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Tạo dữ liệu mẫu**:
```bash
python create_sample_data.py
```

7. **Tạo superuser** (tùy chọn):
```bash
python manage.py createsuperuser
```

8. **Chạy server**:
```bash
python manage.py runserver
```

## Truy cập ứng dụng

- **Trang chủ**: http://localhost:8000/
- **Admin panel**: http://localhost:8000/admin/
- **Đăng ký**: http://localhost:8000/auth/register/
- **Đăng nhập**: http://localhost:8000/auth/login/

## Tài khoản mẫu

### Người dùng Nhật Bản:
- Username: `yuki_tanaka`
- Password: `password123`

### Người dùng Việt Nam:
- Username: `minh_nguyen`
- Password: `password123`

## Cấu trúc dự án

```
testpj2/
├── vietnam_japan_connect/     # Cấu hình chính Django
├── user_auth/                 # Ứng dụng xác thực người dùng
├── chat_app/                  # Ứng dụng chat và trao đổi ngôn ngữ
├── templates/                 # Templates HTML
├── static/                    # File tĩnh (CSS, JS, images)
├── media/                     # File upload (ảnh đại diện, audio)
├── requirements.txt           # Dependencies
└── create_sample_data.py     # Script tạo dữ liệu mẫu
```

## Công nghệ sử dụng

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (development)
- **Forms**: Django Crispy Forms với Bootstrap 5
- **Authentication**: Django built-in authentication với custom user model

## Tính năng chi tiết

### Cho người dùng Nhật Bản:
1. **Học cụm từ tiếng Việt**: Xem danh sách cụm từ theo danh mục và độ khó
2. **Tạo bài đăng**: Chọn cụm từ muốn học và tạo bài đăng tìm đối tác
3. **Chat với đối tác**: Giao tiếp với người Việt Nam qua hệ thống chat

### Cho người dùng Việt Nam:
1. **Tìm bài đăng**: Xem các bài đăng từ người Nhật trong thành phố
2. **Chấp nhận bài đăng**: Chấp nhận bài đăng để bắt đầu trao đổi ngôn ngữ
3. **Chat với đối tác**: Giao tiếp với người Nhật qua hệ thống chat

## Phát triển

### Thêm cụm từ mới:
1. Truy cập admin panel: http://localhost:8000/admin/
2. Đăng nhập với tài khoản superuser
3. Vào mục "Vietnamese phrases"
4. Thêm cụm từ mới với thông tin đầy đủ

### Thêm địa điểm cafe:
1. Vào admin panel
2. Vào mục "Cafe locations"
3. Thêm địa điểm cafe mới

## Troubleshooting

### Lỗi thường gặp:

1. **Lỗi migration**:
```bash
python manage.py makemigrations --empty app_name
python manage.py migrate
```

2. **Lỗi static files**:
```bash
python manage.py collectstatic
```

3. **Lỗi database**:
```bash
python manage.py flush  # Xóa dữ liệu và tạo lại
python create_sample_data.py
```

## Đóng góp

1. Fork dự án
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## License

Dự án này được phát hành dưới MIT License.
