from django.core.management.base import BaseCommand
from event_creation.models import Lesson, TheorySection, TheoryPhrase

class Command(BaseCommand):
    help = 'Create comprehensive Vietnamese language lessons'

    def handle(self, *args, **options):
        self.stdout.write('Creating Vietnamese language lessons...')
        
        lessons_data = [
            {
                'category': 'greetings',
                'title': 'Chào hỏi cơ bản (Basic Greetings)',
                'description': 'Học các câu chào hỏi cơ bản trong tiếng Việt',
                'difficulty': 'beginner',
                'phrases': [
                    ('Chào buổi sáng', 'おはようございます', 'Good morning', 'chào buổi sáng', 'Dùng từ 5h sáng đến 11h sáng', True),
                    ('Chào buổi trưa', 'こんにちは', 'Good afternoon', 'chào buổi trưa', 'Dùng từ 11h trưa đến 5h chiều', True),
                    ('Chào buổi tối', 'こんばんは', 'Good evening', 'chào buổi tối', 'Dùng từ 5h chiều đến 10h tối', True),
                    ('Bạn khỏe không?', 'お元気ですか？', 'How are you?', 'bạn khỏe không', 'Hỏi thăm sức khỏe', True),
                ]
            },
            {
                'category': 'self_introduction',
                'title': 'Giới thiệu bản thân (Self Introduction)',
                'description': 'Học cách giới thiệu bản thân một cách tự tin',
                'difficulty': 'beginner',
                'phrases': [
                    ('Tôi tên là...', '私の名前は...です', 'My name is...', 'tôi tên là', 'Dùng để giới thiệu tên', True),
                    ('Tôi ... tuổi', '私は...歳です', 'I am ... years old', 'tôi ... tuổi', 'Giới thiệu tuổi', True),
                    ('Tôi đến từ...', '私は...から来ました', 'I come from...', 'tôi đến từ', 'Giới thiệu quê quán', True),
                    ('Tôi là sinh viên', '私は学生です', 'I am a student', 'tôi là sinh viên', 'Giới thiệu nghề nghiệp', True),
                ]
            },
            {
                'category': 'asking_directions',
                'title': 'Hỏi đường (Asking for Directions)',
                'description': 'Học cách hỏi đường và chỉ đường trong tiếng Việt',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Xin lỗi, bạn có thể chỉ đường không?', 'すみません、道を教えていただけますか？', 'Excuse me, can you show me the way?', 'xin lỗi, bạn có thể chỉ đường không', 'Cách hỏi đường lịch sự', True),
                    ('Làm sao để đến...?', '...にはどうやって行けばいいですか？', 'How do I get to...?', 'làm sao để đến', 'Hỏi đường đến địa điểm cụ thể', True),
                    ('Đi thẳng', 'まっすぐ行ってください', 'Go straight', 'đi thẳng', 'Chỉ đường thẳng', True),
                    ('Rẽ phải', '右に曲がってください', 'Turn right', 'rẽ phải', 'Chỉ hướng rẽ phải', True),
                ]
            },
            {
                'category': 'shopping',
                'title': 'Mua sắm (Shopping)',
                'description': 'Học các câu nói cần thiết khi đi mua sắm',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Cái này giá bao nhiêu?', 'これはいくらですか？', 'How much is this?', 'cái này giá bao nhiêu', 'Hỏi giá sản phẩm', True),
                    ('Tôi muốn mua cái này', 'これを買いたいです', 'I want to buy this', 'tôi muốn mua cái này', 'Thông báo muốn mua', True),
                    ('Có thể giảm giá không?', '値引きできますか？', 'Can you reduce the price?', 'có thể giảm giá không', 'Mặc cả giá', True),
                    ('Cho tôi túi nhé', '袋をください', 'Please give me a bag', 'cho tôi túi nhé', 'Yêu cầu túi đựng', True),
                ]
            },
            {
                'category': 'restaurant',
                'title': 'Nhà hàng / Gọi món (Restaurant)',
                'description': 'Học cách gọi món và giao tiếp trong nhà hàng',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Cho tôi xem thực đơn', 'メニューを見せてください', 'Please show me the menu', 'cho tôi xem thực đơn', 'Yêu cầu xem menu', True),
                    ('Tôi muốn gọi món...', '...を注文したいです', 'I would like to order...', 'tôi muốn gọi món', 'Gọi món cụ thể', True),
                    ('Món này rất ngon', 'この料理はとてもおいしい', 'This dish is very delicious', 'món này rất ngon', 'Khen món ăn', True),
                    ('Xin hóa đơn', 'お会計をお願いします', 'The bill, please', 'xin hóa đơn', 'Yêu cầu thanh toán', True),
                ]
            },
            {
                'category': 'transportation',
                'title': 'Giao thông / Đi lại (Transportation)',
                'description': 'Học cách sử dụng các phương tiện giao thông công cộng',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Xe buýt dừng ở đâu?', 'バスはどこで止まりますか？', 'Where does the bus stop?', 'xe buýt dừng ở đâu', 'Hỏi điểm dừng xe buýt', True),
                    ('Có taxi ở gần đây không?', 'この近くにタクシーはありますか？', 'Is there a taxi nearby?', 'có taxi ở gần đây không', 'Hỏi về taxi', True),
                    ('Tôi muốn đến...', '...に行きたいです', 'I want to go to...', 'tôi muốn đến', 'Nói địa điểm muốn đến', True),
                    ('Tôi muốn mua vé đến...', '...行きの切符を買いたいです', 'I want to buy a ticket to...', 'tôi muốn mua vé đến', 'Mua vé đến địa điểm', True),
                ]
            },
            {
                'category': 'weather',
                'title': 'Thời tiết (Weather)',
                'description': 'Học cách nói về thời tiết và khí hậu Việt Nam',
                'difficulty': 'beginner',
                'phrases': [
                    ('Hôm nay trời nắng', '今日は晴れです', 'It is sunny today', 'hôm nay trời nắng', 'Mô tả thời tiết nắng', True),
                    ('Trời mưa', '雨が降っています', 'It is raining', 'trời mưa', 'Mô tả thời tiết mưa', True),
                    ('Trời lạnh', '寒いです', 'It is cold', 'trời lạnh', 'Mô tả thời tiết lạnh', True),
                    ('Mùa mưa bắt đầu', '雨季が始まりました', 'Rainy season has begun', 'mùa mưa bắt đầu', 'Nói về mùa mưa', True),
                ]
            },
            {
                'category': 'family',
                'title': 'Gia đình (Family)',
                'description': 'Học cách giới thiệu và nói về gia đình',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Đây là gia đình tôi', 'これは私の家族です', 'This is my family', 'đây là gia đình tôi', 'Giới thiệu gia đình', True),
                    ('Bố tôi', '私の父', 'My father', 'bố tôi', 'Gọi bố', True),
                    ('Mẹ tôi', '私の母', 'My mother', 'mẹ tôi', 'Gọi mẹ', True),
                    ('Gia đình bạn có mấy người?', 'ご家族は何人ですか？', 'How many people are in your family?', 'gia đình bạn có mấy người', 'Hỏi về số lượng thành viên', True),
                ]
            },
            {
                'category': 'health_emergency',
                'title': 'Sức khỏe / Trường hợp khẩn cấp (Health & Emergency)',
                'description': 'Học các câu nói cần thiết khi gặp vấn đề về sức khỏe',
                'difficulty': 'advanced',
                'phrases': [
                    ('Tôi bị ốm', '私は病気です', 'I am sick', 'tôi bị ốm', 'Nói về tình trạng ốm', True),
                    ('Tôi cần gặp bác sĩ', '医者に診てもらう必要があります', 'I need to see a doctor', 'tôi cần gặp bác sĩ', 'Yêu cầu gặp bác sĩ', True),
                    ('Gọi cấp cứu!', '救急車を呼んでください！', 'Call an ambulance!', 'gọi cấp cứu', 'Yêu cầu cấp cứu', True),
                    ('Có ai giúp tôi không?', '誰か助けてくれませんか？', 'Can anyone help me?', 'có ai giúp tôi không', 'Kêu gọi sự giúp đỡ', True),
                ]
            },
            {
                'category': 'time_schedule',
                'title': 'Thời gian / Lịch trình (Time & Schedule)',
                'description': 'Học cách nói về thời gian và lập lịch trình',
                'difficulty': 'beginner',
                'phrases': [
                    ('Bây giờ là mấy giờ?', '今何時ですか？', 'What time is it now?', 'bây giờ là mấy giờ', 'Hỏi giờ hiện tại', True),
                    ('Bây giờ là... giờ', '今...時です', 'It is ... o\'clock now', 'bây giờ là ... giờ', 'Trả lời về giờ', True),
                    ('Khi nào chúng ta gặp nhau?', 'いつ会いましょうか？', 'When shall we meet?', 'khi nào chúng ta gặp nhau', 'Hỏi về thời gian gặp mặt', True),
                    ('Bạn có rảnh vào... không?', '...はお暇ですか？', 'Are you free on...?', 'bạn có rảnh vào', 'Hỏi về lịch rảnh', True),
                ]
            }
        ]
        
        created_lessons = 0
        created_sections = 0
        created_phrases = 0
        
        for lesson_data in lessons_data:
            # Create or get lesson
            lesson, created = Lesson.objects.get_or_create(
                category=lesson_data['category'],
                defaults={
                    'title': lesson_data['title'],
                    'description': lesson_data['description'],
                    'difficulty': lesson_data['difficulty']
                }
            )
            
            if created:
                created_lessons += 1
                self.stdout.write(f'Created lesson: {lesson.title}')
            
            # Create theory section for this lesson
            section, created = TheorySection.objects.get_or_create(
                lesson=lesson,
                title=f'Phần lý thuyết - {lesson_data["title"]}',
                defaults={
                    'description': f'Lý thuyết cơ bản cho bài học {lesson_data["title"]}',
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
                f'Successfully created: {created_lessons} lessons, {created_sections} sections, {created_phrases} phrases!'
            )
        )
