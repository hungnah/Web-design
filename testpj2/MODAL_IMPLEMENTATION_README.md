# Modal Dialog Implementation for Phrase List

## Tổng quan (Overview)

Đã thêm modal dialog cho nút cam "テキストを見る" (See Text) trong trang phrase list. Modal này hiển thị thông tin chi tiết của phrase khi người dùng ấn vào nút.

## Tính năng (Features)

### 1. Modal Dialog
- **Responsive Design**: Modal tự động điều chỉnh kích thước theo màn hình
- **Beautiful UI**: Sử dụng gradient colors và modern design
- **Smooth Animations**: Hiệu ứng mở/đóng mượt mà

### 2. Nội dung Modal
- **Phrase Display**: Hiển thị câu tiếng Việt với font size lớn
- **Translations**: Bản dịch tiếng Nhật và tiếng Anh
- **Category & Difficulty**: Badge hiển thị danh mục và độ khó
- **Audio Player**: Nếu có file âm thanh
- **Learning Tips**: 3 mẹo học tập hữu ích

### 3. Interactive Elements
- **Hover Effects**: Hiệu ứng hover cho cards và buttons
- **Keyboard Navigation**: Hỗ trợ phím Escape để đóng modal
- **Click Outside**: Click bên ngoài để đóng modal
- **Smooth Scrolling**: Cuộn mượt khi mở modal

## Cách sử dụng (How to Use)

### 1. Mở Modal
- Ấn vào nút cam "テキストを見る" trên bất kỳ phrase card nào
- Modal sẽ mở với hiệu ứng scale và fade-in

### 2. Đóng Modal
- Click nút "閉じる" (Đóng) 
- Nhấn phím Escape
- Click bên ngoài modal

### 3. Navigation
- Modal có 2 buttons ở footer:
  - **閉じる/Đóng**: Đóng modal
  - **学習を開始/Bắt đầu học**: Chuyển đến trang học tập

## Technical Implementation

### 1. HTML Structure
```html
<!-- Modal Trigger Button -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#phraseModal{{ phrase.id }}">
    テキストを見る
</button>

<!-- Modal -->
<div class="modal fade" id="phraseModal{{ phrase.id }}">
    <!-- Modal content -->
</div>
```

### 2. CSS Classes
- `.modal-content`: Styling cho modal container
- `.phrase-card`: Styling cho phrase cards
- `.translation-card`: Styling cho translation sections
- `.learning-tips-card`: Styling cho learning tips
- `.tip-item`: Styling cho individual tips

### 3. JavaScript Features
- **Bootstrap Modal**: Sử dụng Bootstrap 5 modal system
- **Custom Animations**: Scale và fade effects
- **Event Listeners**: Keyboard và click events
- **Smooth Scrolling**: Custom scroll animation

## Responsive Design

### Mobile (< 768px)
- Modal padding giảm xuống 1rem
- Font size phrase text giảm xuống 1.5rem
- Tip items stack vertically

### Desktop (≥ 768px)
- Full modal padding (2rem)
- Large phrase text (2rem)
- Tips arranged horizontally

## Browser Compatibility

- **Chrome**: ✅ Full support
- **Firefox**: ✅ Full support  
- **Safari**: ✅ Full support
- **Edge**: ✅ Full support
- **Mobile Browsers**: ✅ Responsive support

## Dependencies

- **Bootstrap 5.3.0**: Modal system và responsive grid
- **Font Awesome 6.0.0**: Icons
- **jQuery 3.6.0**: DOM manipulation (optional)

## Customization

### 1. Colors
Có thể thay đổi màu sắc trong CSS variables:
```css
:root {
    --primary-color: #ff6b35;
    --secondary-color: #f7931e;
    --success-color: #28a745;
    --warning-color: #ffc107;
}
```

### 2. Animations
Có thể điều chỉnh timing và effects:
```css
.modal-dialog {
    transition: transform 0.3s ease-out;
}
```

### 3. Content
Có thể thêm/bớt sections trong modal:
- Thêm cultural context
- Thêm pronunciation guide
- Thêm example sentences

## Troubleshooting

### 1. Modal không mở
- Kiểm tra Bootstrap JS đã load
- Kiểm tra console errors
- Đảm bảo data-bs-target đúng

### 2. Styling issues
- Kiểm tra CSS conflicts
- Đảm bảo custom CSS load sau Bootstrap
- Kiểm tra responsive breakpoints

### 3. Performance
- Modal content được render server-side
- Không có AJAX requests
- Animations sử dụng CSS transforms

## Future Enhancements

1. **AJAX Loading**: Load modal content dynamically
2. **Audio Recording**: Cho phép user record pronunciation
3. **Progress Tracking**: Track learning progress
4. **Social Sharing**: Share phrases on social media
5. **Offline Support**: Cache phrases for offline use

## Support

Nếu có vấn đề gì, hãy kiểm tra:
1. Browser console errors
2. Django server logs
3. Network tab trong DevTools
4. Bootstrap version compatibility
