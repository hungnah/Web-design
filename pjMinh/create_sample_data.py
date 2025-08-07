#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vietnam_talk_taste.settings')
django.setup()

from talk.models import UserGoal, Topic, Lesson, Sentence, MiniGame
from food_culture.models import TraditionalFood, Ingredient, OrderingPhrase, CulturalTip, FoodLink

def create_sample_data():
    print("Creating sample data...")
    
    # Create User Goals
    goals_data = [
        {
            'name': 'student',
            'description': 'Học tiếng Việt để hòa nhập cuộc sống học tập tại Việt Nam'
        },
        {
            'name': 'tourist',
            'description': 'Học các câu giao tiếp cơ bản cho chuyến du lịch Việt Nam'
        },
        {
            'name': 'resident',
            'description': 'Học tiếng Việt để sống và làm việc tại Việt Nam'
        }
    ]
    
    for goal_data in goals_data:
        goal, created = UserGoal.objects.get_or_create(
            name=goal_data['name'],
            defaults={'description': goal_data['description']}
        )
        if created:
            print(f"Created UserGoal: {goal.get_name_display()}")
    
    # Create Topics
    topics_data = [
        {
            'name': 'Giao tiếp tại nhà hàng',
            'description': 'Học cách gọi món, đặt bàn và giao tiếp với nhân viên nhà hàng',
            'order': 1
        },
        {
            'name': 'Giao tiếp tại sân bay',
            'description': 'Học cách làm thủ tục check-in, check-out và giao tiếp tại sân bay',
            'order': 2
        },
        {
            'name': 'Giao tiếp tại khách sạn',
            'description': 'Học cách đặt phòng, check-in và giao tiếp với nhân viên khách sạn',
            'order': 3
        }
    ]
    
    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            name=topic_data['name'],
            defaults=topic_data
        )
        if created:
            print(f"Created Topic: {topic.name}")
    
    # Create Traditional Foods
    foods_data = [
        {
            'name': 'Phở',
            'vietnamese_name': 'Phở',
            'english_name': 'Pho',
            'description': 'Món ăn quốc hồn quốc túy của Việt Nam với nước dùng đậm đà và bánh phở mềm mại',
            'history_story': 'Phở xuất hiện vào đầu thế kỷ 20 tại Nam Định, sau đó lan rộng ra Hà Nội và toàn quốc. Món ăn này kết hợp giữa ẩm thực Việt Nam và ảnh hưởng từ ẩm thực Pháp.',
            'region': 'Miền Bắc',
            'difficulty_level': 1
        },
        {
            'name': 'Bún bò Huế',
            'vietnamese_name': 'Bún bò Huế',
            'english_name': 'Hue Beef Noodle Soup',
            'description': 'Món ăn đặc trưng của xứ Huế với hương vị cay nồng đặc biệt',
            'history_story': 'Bún bò Huế có nguồn gốc từ cung đình Huế, được chế biến theo công thức riêng của vùng đất cố đô với nước dùng cay và các loại rau sống phong phú.',
            'region': 'Miền Trung',
            'difficulty_level': 2
        },
        {
            'name': 'Bánh chưng',
            'vietnamese_name': 'Bánh chưng',
            'english_name': 'Square Sticky Rice Cake',
            'description': 'Món ăn truyền thống không thể thiếu trong dịp Tết Nguyên Đán',
            'history_story': 'Theo truyền thuyết, bánh chưng được Lang Liêu sáng tạo để dâng lên vua Hùng. Hình vuông của bánh tượng trưng cho đất, thể hiện sự biết ơn với thiên nhiên.',
            'region': 'Miền Bắc',
            'difficulty_level': 3
        }
    ]
    
    for food_data in foods_data:
        food, created = TraditionalFood.objects.get_or_create(
            name=food_data['name'],
            defaults=food_data
        )
        if created:
            print(f"Created TraditionalFood: {food.name}")
    
    # Xóa các bài học, mẫu câu, minigame cũ để tránh trùng lặp
    MiniGame.objects.all().delete()
    Sentence.objects.all().delete()
    Lesson.objects.all().delete()

    # --- Nhà hàng ---
    restaurant_topic = Topic.objects.get(name='Giao tiếp tại nhà hàng')
    restaurant_lessons = [
        {
            'title': 'Ordering Food',
            'description': 'Learn how to order food at a Vietnamese restaurant.',
            'content': '<p>Useful phrases for ordering food.</p>',
            'order': 1,
            'sentences': [
                {'vietnamese': 'Tôi muốn gọi món phở', 'english': 'I want to order pho', 'pronunciation': 'toy muốn gọi món phở', 'usage_context': 'Order pho', 'order': 1},
                {'vietnamese': 'Cho tôi một ly nước cam', 'english': 'Give me an orange juice', 'pronunciation': 'cho toy một ly nước cam', 'usage_context': 'Order a drink', 'order': 2},
                {'vietnamese': 'Tôi bị dị ứng với đậu phộng', 'english': 'I am allergic to peanuts', 'pronunciation': 'toy bị dị ứng với đậu phộng', 'usage_context': 'Allergy warning', 'order': 3},
            ],
        },
        {
            'title': 'Booking a Table',
            'description': 'How to book a table in advance.',
            'content': '<p>Useful phrases for booking a table.</p>',
            'order': 2,
            'sentences': [
                {'vietnamese': 'Tôi muốn đặt bàn cho bốn người', 'english': 'I want to book a table for four', 'pronunciation': 'toy muốn đặt bàn cho bốn người', 'usage_context': 'Book a table', 'order': 1},
                {'vietnamese': 'Bàn gần cửa sổ còn không?', 'english': 'Is the table by the window available?', 'pronunciation': 'bàn gần cửa sổ còn không', 'usage_context': 'Ask for a window seat', 'order': 2},
                {'vietnamese': 'Tôi sẽ đến lúc 7 giờ tối', 'english': 'I will arrive at 7 PM', 'pronunciation': 'toy sẽ đến lúc bảy giờ tối', 'usage_context': 'Tell the time of arrival', 'order': 3},
            ],
        },
        {
            'title': 'Paying the Bill',
            'description': 'How to ask for the bill and pay.',
            'content': '<p>Useful phrases for paying at a restaurant.</p>',
            'order': 3,
            'sentences': [
                {'vietnamese': 'Tính tiền giúp tôi', 'english': 'The bill, please', 'pronunciation': 'tính tiền giúp toy', 'usage_context': 'Ask for the bill', 'order': 1},
                {'vietnamese': 'Tôi muốn trả bằng thẻ', 'english': 'I want to pay by card', 'pronunciation': 'toy muốn trả bằng thẻ', 'usage_context': 'Pay by card', 'order': 2},
                {'vietnamese': 'Có thể xuất hóa đơn không?', 'english': 'Can I have an invoice?', 'pronunciation': 'có thể xuất hóa đơn không', 'usage_context': 'Ask for an invoice', 'order': 3},
            ],
        },
    ]
    for lesson_info in restaurant_lessons:
        lesson, _ = Lesson.objects.get_or_create(
            title=lesson_info['title'],
            topic=restaurant_topic,
            defaults={k: lesson_info[k] for k in ['description', 'content', 'order']}
        )
        for sentence_data in lesson_info['sentences']:
            Sentence.objects.get_or_create(
                vietnamese=sentence_data['vietnamese'],
                lesson=lesson,
                defaults={**sentence_data, 'lesson': lesson}
            )

    # --- Sân bay ---
    airport_topic = Topic.objects.get(name='Giao tiếp tại sân bay')
    airport_lessons = [
        {
            'title': 'Check-in Procedures',
            'description': 'Learn how to check in at the airport.',
            'content': '<p>Useful phrases for airport check-in.</p>',
            'order': 1,
            'sentences': [
                {'vietnamese': 'Tôi muốn làm thủ tục check-in', 'english': 'I want to check in', 'pronunciation': 'toy muốn làm thủ tục check-in', 'usage_context': 'At the check-in counter', 'order': 1},
                {'vietnamese': 'Hộ chiếu của tôi đây', 'english': 'Here is my passport', 'pronunciation': 'hộ chiếu của toy đây', 'usage_context': 'Give your passport', 'order': 2},
                {'vietnamese': 'Tôi có hành lý ký gửi', 'english': 'I have checked baggage', 'pronunciation': 'toy có hành lý ký gửi', 'usage_context': 'Check in luggage', 'order': 3},
            ],
        },
        {
            'title': 'Asking for Directions',
            'description': 'How to ask for directions at the airport.',
            'content': '<p>Useful phrases for finding your way.</p>',
            'order': 2,
            'sentences': [
                {'vietnamese': 'Cổng ra số mấy?', 'english': 'Which is the gate number?', 'pronunciation': 'cổng ra số mấy', 'usage_context': 'Ask for the gate', 'order': 1},
                {'vietnamese': 'Nhà vệ sinh ở đâu?', 'english': 'Where is the restroom?', 'pronunciation': 'nhà vệ sinh ở đâu', 'usage_context': 'Ask for the restroom', 'order': 2},
                {'vietnamese': 'Tôi bị lạc đường', 'english': 'I am lost', 'pronunciation': 'toy bị lạc đường', 'usage_context': 'Lost in the airport', 'order': 3},
            ],
        },
        {
            'title': 'Security Check',
            'description': 'How to go through security at the airport.',
            'content': '<p>Useful phrases for security check.</p>',
            'order': 3,
            'sentences': [
                {'vietnamese': 'Tôi có mang chất lỏng', 'english': 'I have liquids', 'pronunciation': 'toy có mang chất lỏng', 'usage_context': 'Declare liquids', 'order': 1},
                {'vietnamese': 'Tôi không có vật sắc nhọn', 'english': 'I have no sharp objects', 'pronunciation': 'toy không có vật sắc nhọn', 'usage_context': 'Declare no sharp objects', 'order': 2},
                {'vietnamese': 'Tôi cần giúp đỡ', 'english': 'I need help', 'pronunciation': 'toy cần giúp đỡ', 'usage_context': 'Ask for help', 'order': 3},
            ],
        },
    ]
    for lesson_info in airport_lessons:
        lesson, _ = Lesson.objects.get_or_create(
            title=lesson_info['title'],
            topic=airport_topic,
            defaults={k: lesson_info[k] for k in ['description', 'content', 'order']}
        )
        for sentence_data in lesson_info['sentences']:
            Sentence.objects.get_or_create(
                vietnamese=sentence_data['vietnamese'],
                lesson=lesson,
                defaults={**sentence_data, 'lesson': lesson}
            )

    # --- Khách sạn ---
    hotel_topic = Topic.objects.get(name='Giao tiếp tại khách sạn')
    hotel_lessons = [
        {
            'title': 'Booking a Room',
            'description': 'How to book a hotel room.',
            'content': '<p>Useful phrases for booking a room.</p>',
            'order': 1,
            'sentences': [
                {'vietnamese': 'Tôi muốn đặt phòng', 'english': 'I want to book a room', 'pronunciation': 'toy muốn đặt phòng', 'usage_context': 'Book a room', 'order': 1},
                {'vietnamese': 'Phòng này giá bao nhiêu?', 'english': 'How much is this room?', 'pronunciation': 'phòng này giá bao nhiêu', 'usage_context': 'Ask for the price', 'order': 2},
                {'vietnamese': 'Khách sạn có wifi không?', 'english': 'Does the hotel have wifi?', 'pronunciation': 'khách sạn có wifi không', 'usage_context': 'Ask about wifi', 'order': 3},
            ],
        },
        {
            'title': 'Checking In',
            'description': 'How to check in at the hotel.',
            'content': '<p>Useful phrases for checking in.</p>',
            'order': 2,
            'sentences': [
                {'vietnamese': 'Tôi đã đặt phòng trước', 'english': 'I have a reservation', 'pronunciation': 'toy đã đặt phòng trước', 'usage_context': 'Have a reservation', 'order': 1},
                {'vietnamese': 'Cho tôi xem phòng', 'english': 'Show me the room', 'pronunciation': 'cho toy xem phòng', 'usage_context': 'Ask to see the room', 'order': 2},
                {'vietnamese': 'Tôi cần hộ chiếu', 'english': 'I need a passport', 'pronunciation': 'toy cần hộ chiếu', 'usage_context': 'Ask for passport', 'order': 3},
            ],
        },
        {
            'title': 'Checking Out',
            'description': 'How to check out and pay.',
            'content': '<p>Useful phrases for checking out.</p>',
            'order': 3,
            'sentences': [
                {'vietnamese': 'Tôi muốn trả phòng', 'english': 'I want to check out', 'pronunciation': 'toy muốn trả phòng', 'usage_context': 'Check out', 'order': 1},
                {'vietnamese': 'Tôi cần hóa đơn', 'english': 'I need an invoice', 'pronunciation': 'toy cần hóa đơn', 'usage_context': 'Ask for invoice', 'order': 2},
                {'vietnamese': 'Có thể gọi taxi giúp tôi không?', 'english': 'Can you call a taxi for me?', 'pronunciation': 'có thể gọi taxi giúp toy không', 'usage_context': 'Ask for a taxi', 'order': 3},
            ],
        },
    ]
    for lesson_info in hotel_lessons:
        lesson, _ = Lesson.objects.get_or_create(
            title=lesson_info['title'],
            topic=hotel_topic,
            defaults={k: lesson_info[k] for k in ['description', 'content', 'order']}
        )
        for sentence_data in lesson_info['sentences']:
            Sentence.objects.get_or_create(
                vietnamese=sentence_data['vietnamese'],
                lesson=lesson,
                defaults={**sentence_data, 'lesson': lesson}
            )

    print("Sample data creation completed!")

if __name__ == '__main__':
    create_sample_data()
