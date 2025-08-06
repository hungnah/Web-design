# PlayTogether - Kết nối cộng đồng

PlayTogether là một trang web giúp mọi người có thể rủ nhau đi chơi cùng địa điểm, đặc biệt dành cho các thành phố lớn ở Việt Nam.

## Tính năng chính

### 🔐 Đăng ký và Đăng nhập
- Đăng ký tài khoản mới với username và password
- Đăng nhập vào hệ thống
- Cập nhật thông tin cá nhân (họ tên, giới tính, ngày sinh, thành phố)

### 📍 Quản lý địa điểm
- Hỗ trợ 5 thành phố: Hà Nội, Hồ Chí Minh, Hải Phòng, Đà Nẵng, Cần Thơ
- Lọc bài đăng theo thành phố
- Chuyển đổi địa điểm dễ dàng

### 📝 Đăng bài tuyển người
- Tạo bài đăng với thông tin chi tiết:
  - Tiêu đề và mô tả
  - Địa điểm cụ thể
  - Thời gian và thời lượng
  - Chi phí dự kiến
  - Số người tối đa

### 📋 Ứng tuyển và Quản lý
- Ứng tuyển vào bài đăng với lời nhắn
- Chủ bài đăng có thể chấp nhận/từ chối ứng viên
- Theo dõi trạng thái đơn ứng tuyển

### 💬 Chat realtime
- Tự động tạo nhóm chat khi ứng viên được chấp nhận
- Chat realtime giữa các thành viên
- Giao diện chat thân thiện

## Công nghệ sử dụng

- **Backend**: Django 5.2.4
- **Database**: SQLite3
- **Frontend**: Bootstrap 5, JavaScript
- **Realtime**: Django Channels
- **Authentication**: Django Auth System

## Cài đặt và chạy

### 1. Clone repository
```bash
git clone <repository-url>
cd playtogether
```

### 2. Tạo môi trường ảo (khuyến nghị)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Chạy migrations
```bash
python manage.py migrate
```

### 5. Tạo superuser (tùy chọn)
```bash
python manage.py createsuperuser
```

### 6. Chạy server
```bash
python manage.py runserver
```

### 7. Truy cập website
Mở trình duyệt và truy cập: http://127.0.0.1:8000

## Cấu trúc project

```
playtogether/
├── main/                    # App chính
│   ├── models.py           # Database models
│   ├── views.py            # Views và logic
│   ├── forms.py            # Forms
│   ├── admin.py            # Admin interface
│   └── templates/main/     # Templates
├── playtogether/           # Project settings
│   ├── settings.py         # Cấu hình
│   ├── urls.py             # URL routing
│   └── asgi.py             # ASGI config
├── templates/              # Base templates
├── static/                 # Static files
├── media/                  # Uploaded files
└── manage.py              # Django management
```

## Models

### UserProfile
- Thông tin cá nhân của user
- Họ tên, giới tính, ngày sinh, thành phố
- Ảnh đại diện và giới thiệu

### Post
- Bài đăng tuyển người đi chơi
- Thông tin sự kiện, địa điểm, thời gian
- Số người tham gia và chi phí

### Application
- Đơn ứng tuyển của user
- Trạng thái: chờ duyệt/đã duyệt/từ chối
- Lời nhắn ứng tuyển

### GroupChat & Message
- Nhóm chat cho sự kiện
- Tin nhắn realtime

## Hướng dẫn sử dụng

### Đăng ký và cập nhật thông tin
1. Truy cập trang chủ
2. Click "Đăng ký" và điền thông tin
3. Sau khi đăng ký, cập nhật thông tin cá nhân
4. Chọn thành phố nơi bạn ở

### Đăng bài tuyển người
1. Click "Đăng bài" trên navigation
2. Điền đầy đủ thông tin sự kiện
3. Submit để tạo bài đăng

### Ứng tuyển vào bài đăng
1. Xem danh sách bài đăng trên trang chủ
2. Click "Xem chi tiết" để xem thông tin
3. Click "Ứng tuyển" và viết lời nhắn
4. Submit đơn ứng tuyển

### Quản lý ứng viên (chủ bài đăng)
1. Vào "Bài đăng của tôi"
2. Click "Quản lý" cho bài đăng có ứng viên
3. Chấp nhận hoặc từ chối ứng viên

### Chat với nhóm
1. Khi ứng viên được chấp nhận, tự động tạo nhóm chat
2. Vào "Chat" để trò chuyện với nhóm
3. Tin nhắn được gửi realtime

## Admin Interface

Truy cập http://127.0.0.1:8000/admin để quản lý:
- Users và UserProfiles
- Posts và Applications
- GroupChats và Messages

## Đóng góp

1. Fork project
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## License

MIT License

## Liên hệ

- Email: support@playtogether.com
- Website: https://playtogether.com 