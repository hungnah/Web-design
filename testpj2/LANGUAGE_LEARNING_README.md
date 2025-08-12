# Language Learning Dashboard - Vietnam-Japan Connect

## 🎯 Tổng quan

Hệ thống Language Learning Dashboard đã được thiết kế lại hoàn toàn theo kiểu hiện đại, tương tự như các ứng dụng học ngôn ngữ chuyên nghiệp. Giao diện mới bao gồm:

- **Dashboard hiện đại** với layout 2 cột
- **Language Cards** hiển thị bài học như các ngôn ngữ
- **Vocabulary Builder** với các level khác nhau
- **Sidebar Navigation** với các chức năng chính
- **Progress Tracking** và thống kê học tập

## 🚀 Tính năng chính

### 1. Dashboard Layout
- **Main Content Area**: Hiển thị các bài học và nội dung chính
- **Right Sidebar**: Navigation, buttons và tracker
- **Responsive Design**: Tương thích với mọi thiết bị

### 2. Language Learning Cards
Mỗi bài học được hiển thị như một "language card" với:
- Hình ảnh minh họa
- Icon thể hiện chủ đề
- Tag mức độ khó
- Thanh tiến độ
- Thống kê từ vựng đã học
- Thời gian học tập
- Nút "Start Learning"

### 3. Vocabulary Builder
- **Level 1**: Basic Greetings, Self Introduction
- **Level 2**: Shopping, Restaurant
- **Level 3**: Transportation, Weather
- **No Mastery**: Advanced Topics (locked)

### 4. Navigation Sidebar
- Languages
- Vocabulary Builder
- Sentence Builder
- Resources
- Learning Sessions
- Monthly Tracker
- Yearly Tracker
- Other Info

### 5. Action Buttons
- New Word
- New Sentence
- New Learning Session

### 6. Progress Tracker
- Today's Progress
- Weekly Goal
- Total Study Time

## 📚 Nội dung bài học

### Bài học cơ bản (10 bài)
1. **Chào hỏi cơ bản** - Basic Greetings
2. **Giới thiệu bản thân** - Self Introduction
3. **Hỏi đường** - Asking for Directions
4. **Mua sắm** - Shopping
5. **Nhà hàng / Gọi món** - Restaurant
6. **Giao thông / Đi lại** - Transportation
7. **Thời tiết** - Weather
8. **Gia đình** - Family
9. **Sức khỏe / Trường hợp khẩn cấp** - Health & Emergency
10. **Thời gian / Lịch trình** - Time & Schedule

### Bài học nâng cao (10 bài)
1. **Chào hỏi nâng cao** - Advanced Greetings
2. **Mua sắm nâng cao** - Advanced Shopping
3. **Nhà hàng nâng cao** - Advanced Restaurant
4. **Giao thông nâng cao** - Advanced Transportation
5. **Thời tiết nâng cao** - Advanced Weather
6. **Gia đình nâng cao** - Advanced Family
7. **Sức khỏe cơ bản** - Basic Health
8. **Lịch trình nâng cao** - Advanced Schedule
9. **Chỉ đường nâng cao** - Advanced Directions
10. **Giới thiệu nâng cao** - Advanced Self Introduction

### Bài học văn hóa (10 bài)
1. **Văn hóa chào hỏi Việt Nam** - Vietnamese Greeting Culture
2. **Văn hóa gia đình Việt Nam** - Vietnamese Family Culture
3. **Văn hóa ẩm thực Việt Nam** - Vietnamese Food Culture
4. **Văn hóa mua sắm Việt Nam** - Vietnamese Shopping Culture
5. **Văn hóa giao thông Việt Nam** - Vietnamese Traffic Culture
6. **Khí hậu và mùa màng Việt Nam** - Vietnamese Climate & Seasons
7. **Văn hóa giao tiếp Nhật Bản** - Japanese Communication Culture
8. **Văn hóa ẩm thực Nhật Bản** - Japanese Food Culture
9. **Văn hóa mua sắm Nhật Bản** - Japanese Shopping Culture
10. **Hệ thống giao thông Nhật Bản** - Japanese Transportation System

## 🛠️ Cài đặt và sử dụng

### 1. Chạy lệnh tạo nội dung
```bash
# Tạo tất cả nội dung (30 bài học)
python manage.py setup_all_content

# Hoặc tạo từng phần riêng biệt
python manage.py create_lessons
python manage.py create_additional_lessons
python manage.py create_culture_lessons
python manage.py create_phrases
python manage.py create_quizzes
python manage.py create_theory_data
python manage.py seed_content
```

### 2. Truy cập dashboard
- Đăng nhập với tài khoản người dùng Nhật Bản
- Truy cập `/lessons/` để xem dashboard mới
- Mỗi bài học có thể click để xem chi tiết

### 3. Tính năng học tập
- **Progress Tracking**: Theo dõi tiến độ học tập
- **Vocabulary Building**: Xây dựng từ vựng theo level
- **Cultural Learning**: Học về văn hóa hai nước
- **Interactive Lessons**: Bài học tương tác với quiz

## 🎨 Thiết kế giao diện

### Color Scheme
- **Primary**: #007bff (Blue)
- **Secondary**: #6c757d (Gray)
- **Success**: #27ae60 (Green)
- **Warning**: #f39c12 (Orange)
- **Danger**: #e74c3c (Red)
- **Info**: #17a2b8 (Cyan)

### Typography
- **Font Family**: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- **Headers**: Bold, uppercase với letter-spacing
- **Body Text**: Regular weight với line-height 1.6

### Components
- **Cards**: Border radius 15px, shadow effects
- **Buttons**: Gradient backgrounds, hover animations
- **Progress Bars**: Smooth transitions, gradient fills
- **Icons**: Font Awesome icons với consistent sizing

## 📱 Responsive Design

### Breakpoints
- **Desktop**: > 1200px (Full layout)
- **Tablet**: 768px - 1200px (Stacked layout)
- **Mobile**: < 768px (Single column)

### Mobile Optimizations
- Touch-friendly buttons
- Swipeable cards
- Optimized spacing
- Simplified navigation

## 🔧 Tùy chỉnh

### Thêm bài học mới
1. Tạo command mới trong `management/commands/`
2. Định nghĩa cấu trúc bài học
3. Chạy command để tạo nội dung
4. Cập nhật dashboard nếu cần

### Thay đổi giao diện
- CSS variables trong file `lessons.html`
- Responsive breakpoints
- Color schemes
- Component styling

## 📊 Thống kê hệ thống

- **Tổng số bài học**: 30
- **Tổng số câu nói**: 150+
- **Số chủ đề**: 10
- **Mức độ khó**: 3 (Beginner, Intermediate, Advanced)
- **Bài học văn hóa**: 10
- **Ngôn ngữ hỗ trợ**: Tiếng Việt, Tiếng Nhật, Tiếng Anh

## 🎯 Roadmap tương lai

### Phase 1 (Hoàn thành)
- ✅ Dashboard redesign
- ✅ 30 bài học cơ bản và nâng cao
- ✅ Bài học văn hóa
- ✅ Responsive design

### Phase 2 (Kế hoạch)
- 🔄 Progress tracking system
- 🔄 Gamification elements
- 🔄 Social learning features
- 🔄 Advanced analytics

### Phase 3 (Tương lai)
- 📋 AI-powered recommendations
- 📋 Voice recognition
- 📋 Virtual reality lessons
- 📋 Global community features

## 🤝 Đóng góp

Để đóng góp vào dự án:

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📞 Hỗ trợ

Nếu có vấn đề hoặc câu hỏi:

- Tạo issue trên GitHub
- Liên hệ team development
- Xem documentation chi tiết

---

**Vietnam-Japan Connect** - Kết nối văn hóa, kết nối tương lai! 🇻🇳🇯🇵
