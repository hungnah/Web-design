# Tính năng Lịch sử Kết nối (Connection History)

## Tổng quan
Tính năng Lịch sử Kết nối cho phép người dùng Nhật và Việt xem lịch sử các phiên học đã hoàn thành, bao gồm đánh giá và nhận xét từ cả hai bên.

## Tính năng chính

### 1. Xem lịch sử kết nối
- **URL**: `/create/connection-history/`
- **Quyền truy cập**: Đăng nhập bắt buộc
- **Chức năng**: 
  - Hiển thị danh sách tất cả các kết nối đã thực hiện
  - Thống kê tổng quan (tổng số kết nối, kết nối hoàn thành, điểm trung bình)
  - Phân biệt giao diện cho người Nhật và người Việt

### 2. Thêm lịch sử kết nối mới
- **URL**: `/create/add-connection-history/`
- **Quyền truy cập**: Đăng nhập bắt buộc
- **Chức năng**:
  - Tạo kết nối mới giữa người dùng Nhật và Việt
  - Nhập thông tin phiên học (ngày, thời lượng, loại phiên)
  - Đánh giá từ người Nhật (điểm 1-5 sao + nhận xét)
  - Ghi chú bổ sung

## Cấu trúc dữ liệu

### Model ConnectionHistory
```python
class ConnectionHistory(models.Model):
    # Thông tin kết nối
    japanese_user = models.ForeignKey(CustomUser, related_name='japanese_connections')
    vietnamese_user = models.ForeignKey(CustomUser, related_name='vietnamese_connections')
    
    # Liên kết với post gốc (tùy chọn)
    language_exchange_post = models.ForeignKey(LanguageExchangePost, null=True, blank=True)
    partner_request = models.ForeignKey(PartnerRequest, null=True, blank=True)
    
    # Thông tin phiên học
    session_date = models.DateTimeField()
    session_duration = models.PositiveIntegerField()  # phút
    session_type = models.CharField(choices=[('online', 'Trực tuyến'), ('offline', 'Trực tiếp')])
    status = models.CharField(choices=[('completed', 'Hoàn thành'), ('cancelled', 'Đã hủy'), ('no_show', 'Không tham gia')])
    
    # Đánh giá từ người Nhật
    japanese_rating = models.PositiveIntegerField(null=True, blank=True)  # 1-5
    japanese_comment = models.TextField(null=True, blank=True)
    japanese_rating_date = models.DateTimeField(auto_now_add=True)
    
    # Đánh giá từ người Việt (tùy chọn)
    vietnamese_rating = models.PositiveIntegerField(null=True, blank=True)  # 1-5
    vietnamese_comment = models.TextField(null=True, blank=True)
    vietnamese_rating_date = models.DateTimeField(null=True, blank=True)
    
    # Ghi chú bổ sung
    notes = models.TextField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## Cách sử dụng

### 1. Xem lịch sử kết nối
1. Đăng nhập vào hệ thống
2. Truy cập dashboard của bạn
3. Click vào nút "Lịch sử kết nối" hoặc "接続履歴"
4. Xem danh sách các kết nối và thống kê

### 2. Thêm kết nối mới
1. Truy cập `/create/add-connection-history/`
2. Chọn người dùng Nhật và Việt
3. Nhập thông tin phiên học
4. Đánh giá từ người Nhật (bắt buộc)
5. Lưu thông tin

### 3. Quản lý qua Admin
- Truy cập Django Admin
- Vào phần "Lịch sử kết nối"
- Có thể thêm, sửa, xóa các kết nối
- Xem thống kê và báo cáo

## Giao diện người dùng

### Dashboard tích hợp
- **Người Nhật**: Nút "接続履歴" trong dashboard
- **Người Việt**: Nút "Lịch sử kết nối" trong dashboard

### Template chính
- `connection_history.html`: Hiển thị danh sách kết nối
- `add_connection_history.html`: Form thêm kết nối mới

## Dữ liệu mẫu

### Tạo dữ liệu mẫu
```bash
python manage.py create_sample_connections
```

### Dữ liệu được tạo
- 10 kết nối mẫu với đánh giá ngẫu nhiên
- Nhận xét bằng tiếng Nhật và tiếng Việt
- Ghi chú bổ sung về phiên học

## Tính năng bổ sung

### 1. Thống kê
- Tổng số kết nối
- Số kết nối hoàn thành
- Điểm trung bình đánh giá

### 2. Lọc và tìm kiếm
- Theo trạng thái (hoàn thành, đã hủy, không tham gia)
- Theo loại phiên (trực tuyến, trực tiếp)
- Theo ngày tháng

### 3. Đánh giá và nhận xét
- Hệ thống sao 1-5
- Nhận xét bằng tiếng Nhật và tiếng Việt
- Ngày đánh giá tự động

## Bảo mật và quyền truy cập

### Quyền truy cập
- Chỉ người dùng đã đăng nhập mới có thể xem lịch sử
- Mỗi người dùng chỉ thấy kết nối của mình
- Admin có thể xem và quản lý tất cả kết nối

### Bảo vệ dữ liệu
- Sử dụng `@login_required` decorator
- Kiểm tra quyền truy cập trong view
- Dữ liệu được phân tách theo người dùng

## Tích hợp với hệ thống hiện tại

### Liên kết với các model khác
- `LanguageExchangePost`: Kết nối với bài đăng gốc
- `PartnerRequest`: Kết nối với yêu cầu tìm đối tác
- `CustomUser`: Thông tin người dùng Nhật và Việt

### Dashboard tích hợp
- Thêm nút truy cập vào dashboard của cả hai loại người dùng
- Hiển thị thống kê nhanh về kết nối

## Hướng phát triển tương lai

### 1. Tính năng mới
- Xuất báo cáo PDF/Excel
- Thông báo khi có đánh giá mới
- Hệ thống điểm thưởng dựa trên đánh giá

### 2. Cải thiện giao diện
- Biểu đồ thống kê trực quan
- Lọc nâng cao theo nhiều tiêu chí
- Tìm kiếm theo từ khóa

### 3. Tích hợp AI
- Phân tích cảm xúc từ nhận xét
- Gợi ý cải thiện dựa trên đánh giá
- Dự đoán xu hướng kết nối

## Troubleshooting

### Lỗi thường gặp
1. **Lỗi NOT NULL constraint**: Kiểm tra các trường bắt buộc trong model
2. **Lỗi quyền truy cập**: Đảm bảo người dùng đã đăng nhập
3. **Lỗi template**: Kiểm tra đường dẫn template và context data

### Giải pháp
1. Chạy `python manage.py makemigrations` và `python manage.py migrate`
2. Kiểm tra decorator `@login_required` trong view
3. Xác nhận template tồn tại và có đúng cú pháp

## Kết luận

Tính năng Lịch sử Kết nối cung cấp một cách thức hiệu quả để theo dõi và đánh giá các phiên học ngôn ngữ giữa người Nhật và người Việt. Tính năng này giúp:

- Tăng cường trách nhiệm và chất lượng học tập
- Cung cấp dữ liệu để cải thiện hệ thống
- Tạo động lực cho người dùng thông qua đánh giá tích cực
- Xây dựng cộng đồng học tập bền vững
