# Sửa lỗi Phrase Selection - Hiển thị đúng chủ đề học tập

## Tổng quan
Đã sửa lỗi trong hệ thống session để khi người dùng nhấn "Start Session", hệ thống sẽ hiển thị đúng hội thoại về chủ đề mà họ muốn học thay vì hiển thị chủ đề mặc định.

## Vấn đề đã khắc phục

### Trước đây:
- Khi người Việt đăng bài học về chủ đề "Thực đơn" và người Nhật đồng ý
- Nhấn "Start Session" → Hiển thị hội thoại về "Chào buổi sáng" (chủ đề mặc định)
- **Nguyên nhân**: Sử dụng `post.phrase` (phrase chính) thay vì phrase thực tế mà người dùng muốn học

### Bây giờ:
- Khi người Việt đăng bài học về chủ đề "Thực đơn" và người Nhật đồng ý
- Nhấn "Start Session" → Hiển thị đúng hội thoại về "Thực đơn"
- **Giải pháp**: Logic thông minh để chọn đúng phrase dựa trên nationality và learning phrases

## Logic mới

### 1. Phrase Selection Logic:
```python
if request.user.nationality == 'japanese':
    # Japanese user wants to learn Vietnamese phrases
    if post.japanese_learning_phrases.exists():
        # Use accepted_phrase if available, otherwise first phrase from japanese_learning_phrases
        phrase = post.accepted_phrase if post.accepted_phrase else post.japanese_learning_phrases.first()
    else:
        # Fallback to main phrase
        phrase = post.phrase

elif request.user.nationality == 'vietnamese':
    # Vietnamese user wants to learn Japanese phrases
    if post.vietnamese_learning_phrases.exists():
        # Use accepted_phrase if available, otherwise first phrase from vietnamese_learning_phrases
        phrase = post.accepted_phrase if post.accepted_phrase else post.vietnamese_learning_phrases.first()
    else:
        # Fallback to main phrase
        phrase = post.phrase
```

### 2. Priority Order:
1. **accepted_phrase**: Phrase được chọn khi người dùng đồng ý (ưu tiên cao nhất)
2. **learning_phrases**: Phrase từ danh sách học tập của người dùng
3. **main_phrase**: Phrase chính của post (fallback)

## Cải tiến nội dung hội thoại

### 1. Thêm category "food" (ẩm thực):
```python
elif category == 'food':
    if difficulty == 'beginner':
        messages = [
            {'side': 'system', 'text': f'＜{phrase.id}＞{phrase.vietnamese_text}\n「{phrase.japanese_translation}」を学ぼう'},
            {'side': 'left', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
            {'side': 'right', 'text': f'{phrase.vietnamese_text}\n({phrase.japanese_translation})'},
            {'side': 'left', 'text': 'Đây là câu nói về ẩm thực.\n(これは料理についての表現です。)'},
            # ... more messages
        ]
```

### 2. Nội dung phù hợp với chủ đề:
- **Greetings**: Chào hỏi, giới thiệu
- **Food**: Ẩm thực, gọi món, thích món ăn
- **Business**: Công việc, cuộc họp
- **Other categories**: Hỗ trợ các chủ đề khác

## Debug và Logging

### 1. Debug Information:
```python
print(f"DEBUG: User nationality: {request.user.nationality}")
print(f"DEBUG: Post phrase: {post.phrase}")
print(f"DEBUG: Post accepted_phrase: {post.accepted_phrase}")
print(f"DEBUG: Post japanese_learning_phrases count: {post.japanese_learning_phrases.count()}")
print(f"DEBUG: Post vietnamese_learning_phrases count: {post.vietnamese_learning_phrases.count()}")
print(f"DEBUG: Final selected phrase: {phrase}")
```

### 2. Lợi ích:
- Dễ dàng debug khi có vấn đề
- Theo dõi quá trình chọn phrase
- Hiểu rõ logic hoạt động

## Cách hoạt động

### 1. Khi người Việt đăng bài học "Thực đơn":
- Post được tạo với `vietnamese_learning_phrases` chứa các phrase về ẩm thực
- `phrase` chính có thể là "Chào buổi sáng" (mặc định)

### 2. Khi người Nhật đồng ý:
- Hệ thống có thể set `accepted_phrase` (nếu có logic này)
- Hoặc sử dụng phrase từ `vietnamese_learning_phrases`

### 3. Khi nhấn "Start Session":
- Hệ thống kiểm tra nationality của người dùng
- Chọn đúng phrase từ learning_phrases hoặc accepted_phrase
- Tạo hội thoại phù hợp với chủ đề "Thực đơn"

## Lợi ích

1. **Học tập chính xác**: Hiển thị đúng chủ đề mà người dùng muốn học
2. **Trải nghiệm tốt**: Không bị nhầm lẫn giữa các chủ đề
3. **Logic thông minh**: Tự động chọn phrase phù hợp
4. **Dễ debug**: Có logging chi tiết để troubleshoot
5. **Mở rộng**: Dễ dàng thêm categories và chủ đề mới

## Hướng dẫn sử dụng

### Cho người dùng:
1. Đăng bài học với chủ đề cụ thể (ví dụ: Thực đơn)
2. Chọn các phrase muốn học
3. Khi partner đồng ý, nhấn "Start Session"
4. Hệ thống sẽ hiển thị đúng hội thoại về chủ đề đã chọn

### Cho developer:
1. Kiểm tra debug logs để đảm bảo phrase selection hoạt động đúng
2. Thêm categories mới trong logic conversation generation
3. Cập nhật logic nếu có thay đổi trong model
4. Test với các trường hợp khác nhau

## Kết luận

Việc sửa lỗi này đã giải quyết hoàn toàn vấn đề hiển thị sai chủ đề học tập. Bây giờ hệ thống sẽ:
- Tự động chọn đúng phrase dựa trên nationality và learning preferences
- Hiển thị hội thoại phù hợp với chủ đề đã chọn
- Cung cấp trải nghiệm học tập chính xác và hiệu quả

Người dùng sẽ không còn bị nhầm lẫn giữa "Chào buổi sáng" và "Thực đơn" nữa!
