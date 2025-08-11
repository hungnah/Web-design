# Vietnam-Japan Connect - Content Setup Guide

## Tổng quan
Hệ thống này cung cấp các bài học tiếng Việt phong phú để người dùng Nhật Bản có thể tạo bài đăng trao đổi ngôn ngữ và học tiếng Việt.

## Nội dung có sẵn

### 📚 Bài học tiếng Việt (10 bài)
1. **Chào hỏi cơ bản** - Beginner
2. **Giới thiệu bản thân** - Beginner  
3. **Hỏi đường** - Intermediate
4. **Mua sắm** - Intermediate
5. **Nhà hàng / Gọi món** - Intermediate
6. **Giao thông / Đi lại** - Intermediate
7. **Thời tiết** - Beginner
8. **Gia đình** - Intermediate
9. **Sức khỏe / Trường hợp khẩn cấp** - Advanced
10. **Thời gian / Lịch trình** - Beginner

### 🗣️ Câu nói tiếng Việt (60+ câu)
- **Chào hỏi**: 8 câu (Beginner + Intermediate)
- **Ẩm thực**: 10 câu (Beginner + Intermediate)
- **Mua sắm**: 9 câu (Beginner + Intermediate)
- **Giao thông**: 9 câu (Beginner + Intermediate)
- **Khẩn cấp**: 5 câu (Intermediate)
- **Cuộc sống hàng ngày**: 9 câu (Beginner + Intermediate)
- **Kinh doanh**: 5 câu (Intermediate)
- **Du lịch**: 9 câu (Beginner + Intermediate)

### 🧠 Câu hỏi Quiz (20+ câu)
Mỗi bài học có 2-3 câu hỏi quiz để kiểm tra kiến thức.

### 📖 Phần lý thuyết
Mỗi bài học có phần lý thuyết với:
- Các câu nói cần thiết
- Hướng dẫn phát âm
- Ghi chú cách sử dụng
- Ví dụ hội thoại

## Cách sử dụng

### 1. Tạo tất cả nội dung (Khuyến nghị)
```bash
python manage.py setup_all_content
```

### 2. Tạo từng phần riêng biệt

#### Tạo bài học
```bash
python manage.py create_lessons
```

#### Tạo câu nói tiếng Việt
```bash
python manage.py create_phrases
```

#### Tạo câu hỏi quiz
```bash
python manage.py create_quizzes
```

#### Tạo phần lý thuyết
```bash
python manage.py create_theory_data
```

#### Tạo nội dung cơ bản
```bash
python manage.py seed_content
```

## Cấu trúc dữ liệu

### Bài học (Lesson)
- **category**: Chủ đề (greetings, self_introduction, asking_directions, etc.)
- **title**: Tiêu đề bài học
- **description**: Mô tả bài học
- **difficulty**: Mức độ (beginner, intermediate, advanced)
- **image**: Hình ảnh minh họa (tùy chọn)

### Phần lý thuyết (TheorySection)
- **lesson**: Liên kết với bài học
- **title**: Tiêu đề phần lý thuyết
- **description**: Mô tả phần lý thuyết
- **order**: Thứ tự hiển thị

### Câu nói lý thuyết (TheoryPhrase)
- **theory_section**: Liên kết với phần lý thuyết
- **vietnamese_text**: Câu tiếng Việt
- **japanese_translation**: Bản dịch tiếng Nhật
- **english_translation**: Bản dịch tiếng Anh
- **pronunciation_guide**: Hướng dẫn phát âm
- **usage_note**: Ghi chú cách sử dụng
- **is_essential**: Có phải câu nói cần thiết không

### Câu hỏi Quiz (QuizQuestion)
- **lesson**: Liên kết với bài học
- **question**: Câu hỏi
- **option_a, option_b, option_c, option_d**: Các lựa chọn
- **correct_answer**: Đáp án đúng
- **explanation**: Giải thích đáp án

### Câu nói tiếng Việt (VietnamesePhrase)
- **category**: Chủ đề
- **difficulty**: Mức độ
- **vietnamese_text**: Câu tiếng Việt
- **japanese_translation**: Bản dịch tiếng Nhật
- **english_translation**: Bản dịch tiếng Anh

## Tính năng cho người dùng

### 👥 Người dùng Nhật Bản
- Xem danh sách bài học tiếng Việt
- Lọc bài học theo chủ đề và mức độ
- Học từng bài học với phần lý thuyết
- Làm quiz để kiểm tra kiến thức
- Tạo bài đăng trao đổi ngôn ngữ
- Tìm đối tác học tiếng Việt

### 👥 Người dùng Việt Nam
- Xem các bài đăng trao đổi ngôn ngữ
- Chấp nhận lời mời học tiếng Nhật
- Hẹn gặp tại các địa điểm được đề xuất
- Trò chuyện với người học tiếng Nhật

## Địa điểm gợi ý
- **Hà Nội**: Cafe Tranquil
- **Hồ Chí Minh**: The Workshop
- **Hải Phòng**: Mun Coffee
- **Đà Nẵng**: 43 Factory
- **Cần Thơ**: Cafe 1985

## Lưu ý
- Tất cả nội dung được tạo bằng tiếng Việt, tiếng Nhật và tiếng Anh
- Các bài học được sắp xếp theo mức độ từ dễ đến khó
- Người dùng có thể tạo bài đăng sử dụng các câu nói có sẵn
- Hệ thống hỗ trợ tìm kiếm và lọc nội dung theo nhiều tiêu chí

## Hỗ trợ
Nếu gặp vấn đề khi tạo nội dung, hãy kiểm tra:
1. Database connection
2. Model migrations
3. File permissions
4. Django version compatibility
