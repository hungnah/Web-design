from django.core.management.base import BaseCommand
from event_creation.models import Lesson, TheorySection, TheoryPhrase

class Command(BaseCommand):
    help = 'Create Vietnamese and Japanese culture lessons for cultural understanding'

    def handle(self, *args, **options):
        self.stdout.write('Creating Vietnamese and Japanese culture lessons...')
        
        culture_lessons_data = [
            {
                'category': 'greetings',
                'title': 'Văn hóa chào hỏi Việt Nam (Vietnamese Greeting Culture)',
                'description': 'Tìm hiểu về văn hóa chào hỏi và giao tiếp của người Việt Nam',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Chào ông/bà', 'おじいさん/おばあさん、こんにちは', 'Hello sir/madam', 'chào ông bà', 'Chào hỏi người lớn tuổi một cách lịch sự', True),
                    ('Chào anh/chị', 'お兄さん/お姉さん、こんにちは', 'Hello brother/sister', 'chào anh chị', 'Chào hỏi người cùng tuổi hoặc lớn hơn', True),
                    ('Chào em', 'こんにちは', 'Hello', 'chào em', 'Chào hỏi người nhỏ tuổi hơn', True),
                    ('Xin chào quý khách', 'いらっしゃいませ', 'Welcome', 'xin chào quý khách', 'Chào hỏi khách hàng trong kinh doanh', True),
                ]
            },
            {
                'category': 'family',
                'title': 'Văn hóa gia đình Việt Nam (Vietnamese Family Culture)',
                'description': 'Tìm hiểu về văn hóa gia đình và mối quan hệ trong gia đình Việt Nam',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Gia đình là trên hết', '家族が一番大切です', 'Family comes first', 'gia đình là trên hết', 'Thể hiện tầm quan trọng của gia đình', True),
                    ('Kính trên nhường dưới', '目上の人を敬い、目下の人に譲る', 'Respect elders, yield to juniors', 'kính trên nhường dưới', 'Nguyên tắc ứng xử trong gia đình', True),
                    ('Con cái phải hiếu thảo', '子供は親孝行しなければならない', 'Children must be filial', 'con cái phải hiếu thảo', 'Đạo lý truyền thống Việt Nam', True),
                    ('Gia đình sum vầy', '家族が集まる', 'Family gathering', 'gia đình sum vầy', 'Mô tả gia đình đoàn tụ', True),
                ]
            },
            {
                'category': 'restaurant',
                'title': 'Văn hóa ẩm thực Việt Nam (Vietnamese Food Culture)',
                'description': 'Tìm hiểu về văn hóa ẩm thực và cách thưởng thức món ăn Việt Nam',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Món ăn Việt Nam rất ngon', 'ベトナム料理はとてもおいしいです', 'Vietnamese food is very delicious', 'món ăn Việt Nam rất ngon', 'Khen ngợi ẩm thực Việt Nam', True),
                    ('Phở là món ăn truyền thống', 'フォーは伝統的な料理です', 'Pho is a traditional dish', 'phở là món ăn truyền thống', 'Giới thiệu món phở', True),
                    ('Ăn cơm tấm đi', 'コムタムを食べましょう', 'Let us eat com tam', 'ăn cơm tấm đi', 'Gợi ý ăn cơm tấm', True),
                    ('Uống trà đá', '氷茶を飲みましょう', 'Let us drink iced tea', 'uống trà đá', 'Gợi ý uống trà đá', True),
                ]
            },
            {
                'category': 'shopping',
                'title': 'Văn hóa mua sắm Việt Nam (Vietnamese Shopping Culture)',
                'description': 'Tìm hiểu về văn hóa mua sắm và mặc cả ở Việt Nam',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Mặc cả là văn hóa', '値引き交渉は文化です', 'Bargaining is culture', 'mặc cả là văn hóa', 'Giải thích về văn hóa mặc cả', True),
                    ('Chợ truyền thống', '伝統市場', 'Traditional market', 'chợ truyền thống', 'Giới thiệu về chợ truyền thống', True),
                    ('Mua sắm online', 'オンラインショッピング', 'Online shopping', 'mua sắm online', 'Mua sắm trực tuyến', True),
                    ('Hàng thủ công mỹ nghệ', '手工芸品', 'Handicrafts', 'hàng thủ công mỹ nghệ', 'Đồ thủ công truyền thống', True),
                ]
            },
            {
                'category': 'transportation',
                'title': 'Văn hóa giao thông Việt Nam (Vietnamese Traffic Culture)',
                'description': 'Tìm hiểu về văn hóa giao thông và cách di chuyển ở Việt Nam',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Xe máy là phương tiện chính', 'バイクが主要な交通手段です', 'Motorcycles are the main transportation', 'xe máy là phương tiện chính', 'Giới thiệu về xe máy', True),
                    ('Giao thông đông đúc', '交通が混雑しています', 'Traffic is congested', 'giao thông đông đúc', 'Mô tả tình trạng giao thông', True),
                    ('Đi xe buýt công cộng', '公共交通機関のバスに乗る', 'Take public bus', 'đi xe buýt công cộng', 'Sử dụng xe buýt công cộng', True),
                    ('Thuê xe đạp', '自転車を借りる', 'Rent a bicycle', 'thuê xe đạp', 'Thuê xe đạp để tham quan', True),
                ]
            },
            {
                'category': 'weather',
                'title': 'Khí hậu và mùa màng Việt Nam (Vietnamese Climate & Seasons)',
                'description': 'Tìm hiểu về khí hậu, mùa màng và thời tiết đặc trưng của Việt Nam',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Việt Nam có 4 mùa', 'ベトナムには4つの季節があります', 'Vietnam has 4 seasons', 'Việt Nam có 4 mùa', 'Giới thiệu về 4 mùa', True),
                    ('Mùa xuân ấm áp', '春は暖かいです', 'Spring is warm', 'mùa xuân ấm áp', 'Mô tả mùa xuân', True),
                    ('Mùa hè nóng bức', '夏は暑いです', 'Summer is hot', 'mùa hè nóng bức', 'Mô tả mùa hè', True),
                    ('Mùa thu mát mẻ', '秋は涼しいです', 'Autumn is cool', 'mùa thu mát mẻ', 'Mô tả mùa thu', True),
                    ('Mùa đông lạnh giá', '冬は寒いです', 'Winter is cold', 'mùa đông lạnh giá', 'Mô tả mùa đông', True),
                ]
            },
            {
                'category': 'self_introduction',
                'title': 'Văn hóa giao tiếp Nhật Bản (Japanese Communication Culture)',
                'description': 'Tìm hiểu về văn hóa giao tiếp và cách ứng xử của người Nhật',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Người Nhật rất lịch sự', '日本人はとても礼儀正しいです', 'Japanese people are very polite', 'người Nhật rất lịch sự', 'Nhận xét về văn hóa Nhật', True),
                    ('Cúi chào khi gặp mặt', '会った時に頭を下げて挨拶する', 'Bow when meeting', 'cúi chào khi gặp mặt', 'Văn hóa cúi chào', True),
                    ('Tôn trọng người khác', '他人を尊重する', 'Respect others', 'tôn trọng người khác', 'Giá trị văn hóa Nhật', True),
                    ('Làm việc nhóm hiệu quả', 'チームワークが効果的です', 'Effective teamwork', 'làm việc nhóm hiệu quả', 'Văn hóa làm việc nhóm', True),
                ]
            },
            {
                'category': 'restaurant',
                'title': 'Văn hóa ẩm thực Nhật Bản (Japanese Food Culture)',
                'description': 'Tìm hiểu về văn hóa ẩm thực và cách thưởng thức món ăn Nhật Bản',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Sushi là món ăn nổi tiếng', '寿司は有名な料理です', 'Sushi is a famous dish', 'sushi là món ăn nổi tiếng', 'Giới thiệu về sushi', True),
                    ('Ăn bằng đũa', '箸で食べる', 'Eat with chopsticks', 'ăn bằng đũa', 'Cách ăn truyền thống', True),
                    ('Nói "Itadakimasu" trước khi ăn', '食べる前に「いただきます」と言う', 'Say "Itadakimasu" before eating', 'nói itadakimasu trước khi ăn', 'Văn hóa trước bữa ăn', True),
                    ('Uống trà xanh', '緑茶を飲む', 'Drink green tea', 'uống trà xanh', 'Thưởng thức trà xanh', True),
                ]
            },
            {
                'category': 'shopping',
                'title': 'Văn hóa mua sắm Nhật Bản (Japanese Shopping Culture)',
                'description': 'Tìm hiểu về văn hóa mua sắm và dịch vụ khách hàng ở Nhật Bản',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Dịch vụ khách hàng tuyệt vời', 'カスタマーサービスが素晴らしいです', 'Excellent customer service', 'dịch vụ khách hàng tuyệt vời', 'Khen ngợi dịch vụ', True),
                    ('Mua sắm tại trung tâm thương mại', 'ショッピングモールで買い物する', 'Shop at shopping mall', 'mua sắm tại trung tâm thương mại', 'Mua sắm tại mall', True),
                    ('Mua quà lưu niệm', 'お土産を買う', 'Buy souvenirs', 'mua quà lưu niệm', 'Mua quà kỷ niệm', True),
                    ('Thanh toán bằng thẻ', 'カードで支払う', 'Pay by card', 'thanh toán bằng thẻ', 'Phương thức thanh toán', True),
                ]
            },
            {
                'category': 'transportation',
                'title': 'Hệ thống giao thông Nhật Bản (Japanese Transportation System)',
                'description': 'Tìm hiểu về hệ thống giao thông công cộng hiện đại của Nhật Bản',
                'difficulty': 'intermediate',
                'phrases': [
                    ('Tàu điện ngầm rất tiện lợi', '地下鉄はとても便利です', 'Subway is very convenient', 'tàu điện ngầm rất tiện lợi', 'Khen ngợi tàu điện ngầm', True),
                    ('Tàu Shinkansen nhanh chóng', '新幹線は速いです', 'Shinkansen is fast', 'tàu shinkansen nhanh chóng', 'Giới thiệu về tàu cao tốc', True),
                    ('Mua vé tại máy bán vé tự động', '自動販売機で切符を買う', 'Buy tickets at vending machine', 'mua vé tại máy bán vé tự động', 'Cách mua vé', True),
                    ('Sử dụng thẻ IC', 'ICカードを使う', 'Use IC card', 'sử dụng thẻ IC', 'Thanh toán bằng thẻ IC', True),
                ]
            }
        ]
        
        created_lessons = 0
        created_sections = 0
        created_phrases = 0
        
        for lesson_data in culture_lessons_data:
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
                    'description': f'Lý thuyết văn hóa cho bài học {lesson_data["title"]}',
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
                f'Successfully created: {created_lessons} culture lessons, {created_sections} sections, {created_phrases} phrases!'
            )
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 Culture lessons have been added to enhance cultural understanding!'
            )
        )
        
        self.stdout.write('\n📚 New cultural content includes:')
        self.stdout.write('   • Vietnamese greeting and communication culture')
        self.stdout.write('   • Vietnamese family values and relationships')
        self.stdout.write('   • Vietnamese food culture and traditional dishes')
        self.stdout.write('   • Vietnamese shopping culture and bargaining')
        self.stdout.write('   • Vietnamese traffic and transportation culture')
        self.stdout.write('   • Vietnamese climate and seasonal characteristics')
        self.stdout.write('   • Japanese communication and etiquette culture')
        self.stdout.write('   • Japanese food culture and dining etiquette')
        self.stdout.write('   • Japanese shopping culture and customer service')
        self.stdout.write('   • Japanese transportation system and convenience')
