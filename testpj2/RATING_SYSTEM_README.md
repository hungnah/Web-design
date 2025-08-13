# Hệ thống Đánh giá 2 Chiều - Connection History

## 🎯 Tổng quan
Hệ thống đánh giá 2 chiều cho phép cả người Nhật và người Việt đánh giá lẫn nhau sau mỗi phiên học, đảm bảo tính công bằng và minh bạch trong việc đánh giá chất lượng học tập.

## 🔄 Luồng hoạt động

### 1. **Trạng thái ban đầu: `active`**
- Kết nối mới được tạo với trạng thái "Đang hoạt động"
- Cả hai bên đều có thể đánh giá

### 2. **Sau khi một bên đánh giá:**
- **Người Nhật đánh giá trước:**
  - Trạng thái chuyển thành `waiting_vietnamese_rating`
  - Người Nhật không thể đánh giá lại
  - Người Việt vẫn có thể đánh giá

- **Người Việt đánh giá trước:**
  - Trạng thái chuyển thành `waiting_japanese_rating`
  - Người Việt không thể đánh giá lại
  - Người Nhật vẫn có thể đánh giá

### 3. **Sau khi cả hai đã đánh giá:**
- Trạng thái chuyển thành `fully_rated`
- Kết nối được hoàn thành hoàn toàn
- Không ai có thể đánh giá lại

## 📊 Trạng thái kết nối

| Trạng thái | Mô tả | Màu sắc |
|------------|-------|---------|
| `active` | Đang hoạt động, chưa có đánh giá nào | Xanh dương |
| `waiting_japanese_rating` | Chờ đánh giá từ người Nhật | Vàng |
| `waiting_vietnamese_rating` | Chờ đánh giá từ người Việt | Vàng |
| `fully_rated` | Đã đánh giá đầy đủ | Xanh lá |
| `cancelled` | Đã hủy | Đỏ |
| `no_show` | Không tham gia | Xám |

## 🎨 Giao diện người dùng

### Dashboard
- **Thống kê mới:**
  - Tổng số kết nối
  - Đã đánh giá đầy đủ
  - Chờ đánh giá
  - Điểm trung bình

### Trang lịch sử kết nối
- **Hiển thị trạng thái:** Sử dụng `get_rating_status()` để hiển thị trạng thái dễ hiểu
- **Nút đánh giá:** Chỉ hiển thị khi người dùng có thể đánh giá
- **Thông báo trạng thái:** Hiển thị rõ ràng trạng thái hiện tại

### Trang đánh giá
- **Thông tin kết nối:** Hiển thị đầy đủ thông tin phiên học
- **Form đánh giá:** Hệ thống sao 1-5 + nhận xét
- **Thông báo:** Giải thích rõ về hệ thống đánh giá 2 chiều

## 🔧 Cách sử dụng

### 1. **Xem lịch sử kết nối**
```
URL: /create/connection-history/
Chức năng: Hiển thị danh sách kết nối với trạng thái mới
```

### 2. **Đánh giá kết nối**
```
URL: /create/rate-connection/<connection_id>/
Chức năng: Form đánh giá với hệ thống sao và nhận xét
```

### 3. **Quản lý qua Admin**
```
URL: /admin/event_creation/connectionhistory/
Chức năng: Quản lý tất cả kết nối và trạng thái
```

## 💡 Logic xử lý

### Model Methods
```python
def update_status(self):
    """Cập nhật trạng thái dựa trên đánh giá"""
    if self.japanese_rating and self.vietnamese_rating:
        self.status = 'fully_rated'
    elif self.japanese_rating and not self.vietnamese_rating:
        self.status = 'waiting_vietnamese_rating'
    elif not self.japanese_rating and self.vietnamese_rating:
        self.status = 'waiting_japanese_rating'
    else:
        self.status = 'active'
    self.save()

def can_rate(self, user):
    """Kiểm tra xem người dùng có thể đánh giá không"""
    if user == self.japanese_user:
        return not self.japanese_rating
    elif user == self.vietnamese_user:
        return not self.vietnamese_rating
    return False

def get_rating_status(self):
    """Lấy trạng thái đánh giá hiện tại"""
    # Logic hiển thị trạng thái dễ hiểu
```

### View Logic
```python
@login_required
def rate_connection(request, connection_id):
    connection = get_object_or_404(ConnectionHistory, id=connection_id)
    user = request.user
    
    # Kiểm tra quyền đánh giá
    if not connection.can_rate(user):
        messages.error(request, 'Bạn không thể đánh giá kết nối này!')
        return redirect('connection_history')
    
    # Xử lý đánh giá và cập nhật trạng thái
    connection.update_status()
```

## 🎯 Lợi ích của hệ thống

### 1. **Công bằng và minh bạch**
- Cả hai bên đều có cơ hội đánh giá
- Không ai bị thiệt thòi

### 2. **Chất lượng học tập**
- Đánh giá 2 chiều giúp cải thiện chất lượng
- Phản hồi từ cả hai phía

### 3. **Trách nhiệm**
- Mỗi người phải hoàn thành đánh giá
- Tạo động lực học tập

### 4. **Theo dõi tiến độ**
- Trạng thái rõ ràng cho mỗi kết nối
- Thống kê chi tiết về quá trình đánh giá

## 🚀 Tính năng nâng cao

### 1. **Thông báo tự động**
- Nhắc nhở khi cần đánh giá
- Thông báo khi đối phương đã đánh giá

### 2. **Phân tích dữ liệu**
- Thống kê điểm đánh giá theo thời gian
- So sánh chất lượng giữa các đối tác

### 3. **Hệ thống điểm thưởng**
- Điểm thưởng cho việc đánh giá đúng hạn
- Xếp hạng người dùng dựa trên đánh giá

## 🔍 Troubleshooting

### Lỗi thường gặp
1. **Không thể đánh giá:** Kiểm tra `can_rate()` method
2. **Trạng thái không cập nhật:** Gọi `update_status()` sau khi thay đổi đánh giá
3. **Hiển thị trạng thái sai:** Sử dụng `get_rating_status()` thay vì `get_status_display()`

### Giải pháp
1. **Kiểm tra quyền:** Đảm bảo user có quyền đánh giá
2. **Cập nhật trạng thái:** Luôn gọi `update_status()` sau khi thay đổi
3. **Template:** Sử dụng đúng method để hiển thị trạng thái

## 📝 Kết luận

Hệ thống đánh giá 2 chiều tạo ra một môi trường học tập công bằng và minh bạch, nơi cả người Nhật và người Việt đều có thể đóng góp ý kiến để cải thiện chất lượng học tập. Việc theo dõi trạng thái đánh giá giúp đảm bảo mọi kết nối đều được hoàn thành một cách đầy đủ và chất lượng.
