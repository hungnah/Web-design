# Tính năng Đổi điểm がんばりポイント sang Voucher Giảm giá

## Tổng quan
Tính năng mới cho phép người dùng Việt Nam đổi điểm がんばりポイント (ganbari points) để nhận voucher giảm giá tại các địa điểm khác nhau.

## Các loại Voucher có sẵn

| Loại Voucher | Điểm cần thiết | Giảm giá | Mô tả |
|--------------|----------------|-----------|-------|
| Coffee Shop | 50 điểm | 10% | Giảm giá tại các quán cà phê |
| Restaurant | 100 điểm | 10% | Giảm giá tại nhà hàng |
| Shopping | 150 điểm | 10% | Giảm giá khi mua sắm |
| Transport | 75 điểm | 10% | Giảm giá giao thông công cộng |
| Entertainment | 200 điểm | 10% | Giảm giá giải trí |

## Cách sử dụng

### 1. Truy cập trang đổi điểm
- Đăng nhập vào tài khoản
- Vào Dashboard người Việt
- Nhấn nút "Đổi điểm" trong phần Quick Stats

### 2. Chọn loại voucher
- Chọn loại voucher muốn đổi
- Hệ thống sẽ hiển thị các voucher phù hợp với số điểm hiện có
- Nhấn "Đổi điểm ngay"

### 3. Xem voucher của mình
- Nhấn nút "Voucher" trong Dashboard
- Hoặc truy cập trực tiếp `/my-vouchers/`
- Xem danh sách tất cả voucher đã đổi

### 4. Sử dụng voucher
- Nhấn nút "Sử dụng voucher" trên voucher còn hiệu lực
- Voucher sẽ được đánh dấu là đã sử dụng

## Cách kiếm điểm がんばりポイント

| Hoạt động | Điểm nhận được |
|-----------|----------------|
| Học bài mới | +10 điểm |
| Làm quiz | +5 điểm |
| Gặp gỡ bạn Nhật | +20 điểm |
| Tham gia sự kiện | +15 điểm |

## Tính năng kỹ thuật

### Models
- `DiscountVoucher`: Lưu trữ thông tin voucher
- `CustomUser.point`: Trường điểm hiện tại của user

### Views
- `point_exchange`: Xử lý đổi điểm
- `my_vouchers`: Hiển thị danh sách voucher
- `use_voucher`: Đánh dấu voucher đã sử dụng

### Templates
- `point_exchange.html`: Trang đổi điểm
- `my_vouchers.html`: Trang xem voucher
- `vietnamese_dashboard.html`: Cập nhật với nút đổi điểm

### URLs
- `/point-exchange/`: Trang đổi điểm
- `/my-vouchers/`: Trang xem voucher
- `/use-voucher/<id>/`: Sử dụng voucher

## Bảo mật
- Chỉ user đã đăng nhập mới có thể đổi điểm
- Kiểm tra số điểm đủ trước khi cho phép đổi
- Voucher có thời hạn 30 ngày
- Không thể hoàn tác sau khi đổi điểm

## Admin Panel
- Quản lý tất cả voucher trong hệ thống
- Xem thống kê sử dụng
- Theo dõi trạng thái voucher

## Lưu ý
- Điểm sẽ bị trừ ngay khi đổi voucher
- Voucher hết hạn sẽ tự động bị vô hiệu hóa
- Mỗi voucher chỉ có thể sử dụng một lần
- Hệ thống sẽ hiển thị cảnh báo nếu không đủ điểm
