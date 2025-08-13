# Hệ thống Quản lý Chat Room - Vietnam-Japan Connect

## Tổng quan

Hệ thống này đã được cập nhật để tự động quản lý chat rooms dựa trên trạng thái đánh giá của người dùng. Khi cả hai bên đã đánh giá đầy đủ, chat room sẽ tự động bị đóng và không còn hiển thị trong danh sách chat.

## Cách hoạt động

### 1. Tạo kết nối mới
- Khi một người Nhật chấp nhận bài đăng của người Việt, hệ thống sẽ:
  - Tạo chat room mới
  - Tạo ConnectionHistory record với status 'active'
  - Chat room hoạt động bình thường

### 2. Quá trình đánh giá
- Khi một bên đánh giá:
  - Status của ConnectionHistory được cập nhật thành 'waiting_japanese_rating' hoặc 'waiting_vietnamese_rating'
  - Chat room vẫn hoạt động để hai bên có thể trao đổi

### 3. Hoàn thành đánh giá
- Khi cả hai bên đã đánh giá:
  - Status của ConnectionHistory được cập nhật thành 'fully_rated'
  - LanguageExchangePost hoặc PartnerRequest status được cập nhật thành 'completed'
  - Chat room được tự động vô hiệu hóa (is_active = False)
  - Chat room không còn hiển thị trong danh sách chat

## Các thay đổi chính

### Models
- **ConnectionHistory**: Thêm logic tự động cập nhật trạng thái và vô hiệu hóa chat room
- **ChatRoom**: Thêm method `deactivate_if_completed()` để tự động vô hiệu hóa

### Views
- **my_chats**: Chỉ hiển thị chat rooms đang hoạt động (is_active=True)
- **chat_room**: Kiểm tra is_active trước khi cho phép truy cập
- **send_message/get_messages**: Kiểm tra is_active trước khi xử lý tin nhắn
- **accept_post/accept_partner_request**: Tự động tạo ConnectionHistory

### Templates
- **connection_history.html**: Hiển thị thông báo rõ ràng về việc chat đã bị đóng

## Lợi ích

1. **Tự động hóa**: Không cần can thiệp thủ công để đóng chat rooms
2. **Bảo mật**: Ngăn truy cập vào chat rooms đã hoàn thành
3. **Trải nghiệm người dùng**: Rõ ràng về trạng thái của từng kết nối
4. **Quản lý dữ liệu**: Tự động cập nhật trạng thái của các models liên quan

## Luồng hoạt động

```
1. Tạo kết nối → ConnectionHistory (active) + ChatRoom (active)
2. Một bên đánh giá → ConnectionHistory (waiting_*) + ChatRoom (active)
3. Cả hai đánh giá → ConnectionHistory (fully_rated) + ChatRoom (inactive)
4. Chat room bị ẩn khỏi danh sách và không thể truy cập
```

## Lưu ý kỹ thuật

- Tất cả các thay đổi đều được xử lý tự động thông qua Django signals và model methods
- Không cần migration mới vì các trường cần thiết đã có sẵn
- Hệ thống tương thích ngược với dữ liệu cũ
- Có xử lý exception để tránh lỗi khi ConnectionHistory chưa được tạo
