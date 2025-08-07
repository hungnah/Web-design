# Vietnam Talk & Taste

Website học tiếng Việt qua văn hóa ẩm thực truyền thống Việt Nam.

## Tính năng chính

### 🗣️ Talk - Học tiếng Việt
- **Chủ đề đa dạng**: Giao tiếp tại nhà hàng, sân bay, khách sạn
- **Mẫu câu thực tế**: Với phiên âm và tình huống sử dụng
- **Mini games**: Luyện tập qua trò chơi tương tác
- **Lộ trình học tập**: Phù hợp với mục tiêu (du học sinh, khách tham quan, định cư)

### 🍜 Taste - Văn hóa ẩm thực
- **Món ăn truyền thống**: Phở, bún bò Huế, bánh chưng và nhiều món khác
- **Câu chuyện lịch sử**: Gắn liền với từng món ăn
- **Cách gọi món**: Bằng tiếng Việt với phiên âm
- **Thông tin nguyên liệu**: Bao gồm cảnh báo dị ứng
- **Mẹo văn hóa**: Phép tắc bàn ăn, cách dùng đũa, phong tục Tết

### 🔗 Liên kết thông minh
- Chuyển đổi mượt mà giữa học tập và khám phá văn hóa
- Từ khóa trong bài học được liên kết với món ăn tương ứng

## Cài đặt

### Yêu cầu hệ thống
- Python 3.8+
- Django 5.2.4
- SQLite (mặc định)

### Các bước cài đặt

1. **Clone repository**
```bash
git clone <repository-url>
cd vietnam-talk-taste
```

2. **Tạo virtual environment**
```bash
python -m venv venv
```

3. **Kích hoạt virtual environment**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Cài đặt dependencies**
```bash
pip install -r requirements.txt
```

5. **Chạy migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Tạo superuser (tùy chọn)**
```bash
python manage.py createsuperuser
```

7. **Chạy server**
```bash
python manage.py runserver
```

8. **Truy cập website**
- Website: http://localhost:8000
- Admin: http://localhost:8000/admin

## Cấu trúc dự án

```
vietnam_talk_taste/
├── talk/                    # App học tiếng Việt
│   ├── models.py           # Models cho chủ đề, bài học, mẫu câu
│   ├── views.py            # Views cho các trang học tập
│   ├── urls.py             # URL patterns
│   └── admin.py            # Admin interface
├── food_culture/           # App văn hóa ẩm thực
│   ├── models.py           # Models cho món ăn, nguyên liệu
│   ├── views.py            # Views cho các trang ẩm thực
│   ├── urls.py             # URL patterns
│   └── admin.py            # Admin interface
├── templates/              # HTML templates
│   ├── base.html           # Template cơ sở
│   ├── talk/               # Templates cho app talk
│   └── food_culture/       # Templates cho app food_culture
├── static/                 # CSS, JS, images
└── media/                  # Uploaded files
```

## Sử dụng

### Cho người dùng
1. **Chọn mục tiêu học tập**: Du học sinh, khách tham quan, hoặc định cư
2. **Chọn chủ đề**: Giao tiếp tại nhà hàng, sân bay, khách sạn
3. **Học mẫu câu**: Với phiên âm và tình huống sử dụng
4. **Chơi mini games**: Luyện tập kiến thức
5. **Khám phá món ăn**: Click vào từ khóa để tìm hiểu văn hóa ẩm thực

### Cho admin
1. **Truy cập admin panel**: http://localhost:8000/admin
2. **Thêm chủ đề học tập**: Tạo các chủ đề mới
3. **Thêm bài học**: Tạo nội dung học tập
4. **Thêm món ăn**: Tạo thông tin món ăn truyền thống
5. **Tạo liên kết**: Kết nối từ khóa với món ăn

## Tính năng nổi bật

- **Responsive design**: Tương thích với mọi thiết bị
- **Modern UI**: Giao diện đẹp mắt với Bootstrap 5
- **Interactive learning**: Mini games và tương tác
- **Cultural integration**: Học ngôn ngữ qua văn hóa
- **Smart linking**: Liên kết thông minh giữa học tập và ẩm thực

## Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:
1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## License

MIT License - xem file LICENSE để biết thêm chi tiết.
