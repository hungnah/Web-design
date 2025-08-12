from django.core.management.base import BaseCommand
from event_creation.models import Lesson, TheorySection, TheoryPhrase

class Command(BaseCommand):
    help = 'Create additional Vietnamese language lessons to enrich the learning system'

    def handle(self, *args, **options):
        self.stdout.write('Creating additional Vietnamese language lessons...')
        
        additional_lessons_data = [
            {
                'category': 'greetings',
                'title': 'Chào hỏi nâng cao (Advanced Greetings)',
                'description': 'Học các câu chào hỏi phức tạp và văn hóa giao tiếp Việt Nam',
                'difficulty': 'advanced',
                'phrases': [
                    ('Chào bạn, rất vui được gặp bạn', 'こんにちは、お会いできて嬉しいです', 'Hello, nice to meet you', 'chào bạn, rất vui được gặp bạn', 'Chào hỏi lịch sự khi gặp lần đầu', True),
                    ('Bạn có khỏe không? Tôi rất khỏe, cảm ơn bạn', 'お元気ですか？私はとても元気です、ありがとうございます', 'How are you? I am very well, thank you', 'bạn có khỏe không, tôi rất khỏe, cảm ơn bạn', 'Hỏi thăm và trả lời về sức khỏe', True),
                    ('Chúc bạn một ngày tốt lành', '良い一日をお過ごしください', 'Have a nice day', 'chúc bạn một ngày tốt lành', 'Chúc phúc khi chia tay', True),
                    ('Hẹn gặp lại bạn', 'またお会いしましょう', 'See you again', 'hẹn gặp lại bạn', 'Lời chào tạm biệt', True),
                ]
            },
            {
                'category': 'shopping',
                'title': 'Mua sắm nâng cao (Advanced Shopping)',
                'description': 'Học cách mặc cả, đổi trả và giao tiếp phức tạp khi mua sắm',
                'difficulty': 'advanced',
                'phrases': [
                    ('Bạn có thể giảm giá thêm được không?', 'もう少し値引きしていただけませんか？', 'Can you reduce the price a bit more?', 'bạn có thể giảm giá thêm được không', 'Mặc cả giá sâu hơn', True),
                    ('Tôi muốn đổi cái này', 'これを交換したいです', 'I want to exchange this', 'tôi muốn đổi cái này', 'Yêu cầu đổi hàng', True),
                    ('Có bảo hành không?', '保証はありますか？', 'Is there a warranty?', 'có bảo hành không', 'Hỏi về bảo hành', True),
                    ('Tôi sẽ suy nghĩ và quay lại sau', '考えて後で戻ってきます', 'I will think about it and come back later', 'tôi sẽ suy nghĩ và quay lại sau', 'Từ chối mua một cách lịch sự', True),
                ]
            },
            {
                'category': 'restaurant',
                'title': 'Nhà hàng nâng cao (Advanced Restaurant)',
                'description': 'Học cách gọi món phức tạp và giao tiếp với nhân viên nhà hàng',
                'difficulty': 'advanced',
                'phrases': [
                    ('Tôi bị dị ứng với...', '私は...にアレルギーがあります', 'I am allergic to...', 'tôi bị dị ứng với', 'Thông báo về dị ứng thực phẩm', True),
                    ('Món này có cay không?', 'この料理は辛いですか？', 'Is this dish spicy?', 'món này có cay không', 'Hỏi về độ cay của món ăn', True),
                    ('Tôi muốn món ăn chay', 'ベジタリアン料理が欲しいです', 'I want vegetarian food', 'tôi muốn món ăn chay', 'Yêu cầu món chay', True),
                    ('Có thể nấu món này ít muối hơn không?', 'この料理を塩分控えめで作っていただけますか？', 'Can you cook this dish with less salt?', 'có thể nấu món này ít muối hơn không', 'Yêu cầu điều chỉnh gia vị', True),
                ]
            },
            {
                'category': 'transportation',
                'title': 'Giao thông nâng cao (Advanced Transportation)',
                'description': 'Học cách sử dụng các phương tiện giao thông phức tạp và đặt vé',
                'difficulty': 'advanced',
                'phrases': [
                    ('Tôi muốn đặt vé máy bay đến...', '...行きの航空券を予約したいです', 'I want to book a flight to...', 'tôi muốn đặt vé máy bay đến', 'Đặt vé máy bay', True),
                    ('Có chuyến bay nào rẻ hơn không?', 'もっと安い便はありますか？', 'Are there any cheaper flights?', 'có chuyến bay nào rẻ hơn không', 'Hỏi về giá vé rẻ', True),
                    ('Tôi muốn thuê xe tự lái', 'レンタカーを借りたいです', 'I want to rent a car', 'tôi muốn thuê xe tự lái', 'Thuê xe tự lái', True),
                    ('Làm sao để đến sân bay?', '空港にはどうやって行けばいいですか？', 'How do I get to the airport?', 'làm sao để đến sân bay', 'Hỏi đường đến sân bay', True),
                ]
            },
            {
                'category': 'weather',
                'title': 'Thời tiết nâng cao (Advanced Weather)',
                'description': 'Học cách mô tả thời tiết chi tiết và thảo luận về khí hậu',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Hôm nay trời âm u', '今日は曇りです', 'It is cloudy today', 'hôm nay trời âm u', 'Mô tả thời tiết âm u', True),
                    ('Nhiệt độ hôm nay là bao nhiêu?', '今日の気温は何度ですか？', 'What is the temperature today?', 'nhiệt độ hôm nay là bao nhiêu', 'Hỏi về nhiệt độ', True),
                    ('Trời sẽ mưa vào buổi chiều', '午後は雨が降るでしょう', 'It will rain in the afternoon', 'trời sẽ mưa vào buổi chiều', 'Dự báo thời tiết', True),
                    ('Mùa này thời tiết thế nào?', 'この季節の天気はどうですか？', 'How is the weather in this season?', 'mùa này thời tiết thế nào', 'Hỏi về thời tiết theo mùa', True),
                ]
            },
            {
                'category': 'family',
                'title': 'Gia đình nâng cao (Advanced Family)',
                'description': 'Học cách mô tả mối quan hệ gia đình phức tạp và văn hóa gia đình Việt Nam',
                'difficulty': 'advanced',
                'phrases': [
                    ('Anh trai tôi', '私の兄', 'My older brother', 'anh trai tôi', 'Gọi anh trai', True),
                    ('Chị gái tôi', '私の姉', 'My older sister', 'chị gái tôi', 'Gọi chị gái', True),
                    ('Em trai tôi', '私の弟', 'My younger brother', 'em trai tôi', 'Gọi em trai', True),
                    ('Em gái tôi', '私の妹', 'My younger sister', 'em gái tôi', 'Gọi em gái', True),
                    ('Gia đình tôi có 5 người', '私の家族は5人です', 'My family has 5 people', 'gia đình tôi có 5 người', 'Mô tả số lượng thành viên', True),
                ]
            },
            {
                'category': 'health_emergency',
                'title': 'Sức khỏe cơ bản (Basic Health)',
                'description': 'Học các câu nói cơ bản về sức khỏe và bệnh tật',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Tôi bị đau đầu', '私は頭痛がします', 'I have a headache', 'tôi bị đau đầu', 'Mô tả triệu chứng đau đầu', True),
                    ('Tôi bị sốt', '私は熱があります', 'I have a fever', 'tôi bị sốt', 'Mô tả triệu chứng sốt', True),
                    ('Bạn có thể cho tôi thuốc không?', '薬をくれませんか？', 'Can you give me medicine?', 'bạn có thể cho tôi thuốc không', 'Yêu cầu thuốc', True),
                    ('Tôi cần nghỉ ngơi', '休憩が必要です', 'I need to rest', 'tôi cần nghỉ ngơi', 'Yêu cầu nghỉ ngơi', True),
                ]
            },
            {
                'category': 'time_schedule',
                'title': 'Lịch trình nâng cao (Advanced Schedule)',
                'description': 'Học cách lập lịch trình chi tiết và quản lý thời gian',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Bạn có rảnh vào thứ Hai không?', '月曜日はお暇ですか？', 'Are you free on Monday?', 'bạn có rảnh vào thứ hai không', 'Hỏi về lịch rảnh cụ thể', True),
                    ('Chúng ta hẹn gặp nhau lúc 2 giờ chiều nhé', '午後2時に会いましょう', 'Let us meet at 2 PM', 'chúng ta hẹn gặp nhau lúc 2 giờ chiều nhé', 'Đặt lịch hẹn cụ thể', True),
                    ('Tôi có lịch hẹn vào buổi sáng', '午前中に予定があります', 'I have an appointment in the morning', 'tôi có lịch hẹn vào buổi sáng', 'Thông báo về lịch hẹn', True),
                    ('Bạn có thể đổi lịch được không?', '予定を変更できますか？', 'Can you change the schedule?', 'bạn có thể đổi lịch được không', 'Yêu cầu thay đổi lịch', True),
                ]
            },
            {
                'category': 'asking_directions',
                'title': 'Chỉ đường nâng cao (Advanced Directions)',
                'description': 'Học cách chỉ đường chi tiết và sử dụng bản đồ',
                'difficulty': 'advanced',
                'phrases': [
                    ('Bạn có thể chỉ đường đến bệnh viện gần nhất không?', '一番近い病院への道を教えていただけませんか？', 'Can you show me the way to the nearest hospital?', 'bạn có thể chỉ đường đến bệnh viện gần nhất không', 'Hỏi đường đến bệnh viện', True),
                    ('Đi bao xa thì đến?', 'どのくらいの距離がありますか？', 'How far is it?', 'đi bao xa thì đến', 'Hỏi về khoảng cách', True),
                    ('Có thể đi bộ được không?', '歩いて行けますか？', 'Can I walk there?', 'có thể đi bộ được không', 'Hỏi về khả năng đi bộ', True),
                    ('Bạn có thể vẽ bản đồ không?', '地図を描いていただけませんか？', 'Can you draw a map?', 'bạn có thể vẽ bản đồ không', 'Yêu cầu vẽ bản đồ', True),
                ]
            },
            {
                'category': 'self_introduction',
                'title': 'Giới thiệu nâng cao (Advanced Self Introduction)',
                'description': 'Học cách giới thiệu bản thân chi tiết và chuyên nghiệp',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Tôi làm việc tại công ty...', '私は...会社で働いています', 'I work at... company', 'tôi làm việc tại công ty', 'Giới thiệu nơi làm việc', True),
                    ('Tôi thích đọc sách và du lịch', '私は読書と旅行が好きです', 'I like reading books and traveling', 'tôi thích đọc sách và du lịch', 'Giới thiệu sở thích', True),
                    ('Tôi đã học tiếng Việt được 1 năm', '私はベトナム語を1年間勉強しています', 'I have been studying Vietnamese for 1 year', 'tôi đã học tiếng Việt được 1 năm', 'Giới thiệu về việc học ngôn ngữ', True),
                    ('Rất vui được làm quen với bạn', 'お知り合いになれて嬉しいです', 'Nice to meet you', 'rất vui được làm quen với bạn', 'Lời kết khi giới thiệu', True),
                ]
            }
        ]
        
        created_lessons = 0
        created_sections = 0
        created_phrases = 0
        
        for lesson_data in additional_lessons_data:
            # Create or get lesson
            lesson, created = Lesson.objects.get_or_create(
                category=lesson_data['category'],
                title=lesson_data['title'],
                defaults={
                    'description': lesson_data['description'],
                    'difficulty': lesson_data['difficulty']
                }
            )
            
            if created:
                created_lessons += 1
                self.stdout.write(f'Created lesson: {lesson.title}')
            else:
                self.stdout.write(f'Updated lesson: {lesson.title}')
            
            # Create theory section for this lesson
            section, created = TheorySection.objects.get_or_create(
                lesson=lesson,
                title=f'Phần lý thuyết - {lesson_data["title"]}',
                defaults={
                    'description': f'Lý thuyết chi tiết cho bài học {lesson_data["title"]}',
                    'order': 1
                }
            )
            
            if created:
                created_sections += 1
                self.stdout.write(f'  Created section: {section.title}')
            
            # Create phrases for this section
            for i, phrase_data in enumerate(lesson_data['phrases']):
                phrase, created = TheoryPhrase.objects.get_or_create(
                    theory_section=section,
                    vietnamese_text=phrase_data[0],
                    defaults={
                        'japanese_translation': phrase_data[1],
                        'english_translation': phrase_data[2],
                        'pronunciation_guide': phrase_data[3],
                        'usage_note': phrase_data[4],
                        'is_essential': phrase_data[5],
                        'order': i + 1
                    }
                )
                
                if created:
                    created_phrases += 1
                    self.stdout.write(f'    Created phrase: {phrase.vietnamese_text}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created: {created_lessons} additional lessons, {created_sections} sections, {created_phrases} phrases!'
            )
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 Additional lessons have been added to enrich the learning experience!'
            )
        )
        
        self.stdout.write('\n📚 New content includes:')
        self.stdout.write('   • Advanced greetings and cultural communication')
        self.stdout.write('   • Complex shopping scenarios and bargaining')
        self.stdout.write('   • Advanced restaurant ordering and special requests')
        self.stdout.write('   • Transportation booking and complex directions')
        self.stdout.write('   • Detailed weather descriptions and climate discussion')
        self.stdout.write('   • Extended family relationships and Vietnamese culture')
        self.stdout.write('   • Basic health symptoms and medical communication')
        self.stdout.write('   • Advanced scheduling and time management')
        self.stdout.write('   • Complex direction giving and map usage')
        self.stdout.write('   • Professional self-introduction techniques')
