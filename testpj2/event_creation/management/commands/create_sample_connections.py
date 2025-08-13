from django.core.management.base import BaseCommand
from django.utils import timezone
from event_creation.models import ConnectionHistory
from user_profile.models import CustomUser
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Create sample connection history data for testing'

    def handle(self, *args, **options):
        # Lấy danh sách người dùng
        japanese_users = CustomUser.objects.filter(nationality='japanese')
        vietnamese_users = CustomUser.objects.filter(nationality='vietnamese')
        
        if not japanese_users.exists():
            self.stdout.write(
                self.style.WARNING('No Japanese users found. Please create some Japanese users first.')
            )
            return
            
        if not vietnamese_users.exists():
            self.stdout.write(
                self.style.WARNING('No Vietnamese users found. Please create some Vietnamese users first.')
            )
            return
        
        # Tạo dữ liệu mẫu
        connections_created = 0
        
        for i in range(min(10, len(japanese_users) * len(vietnamese_users))):
            japanese_user = random.choice(japanese_users)
            vietnamese_user = random.choice(vietnamese_users)
            
            # Tạo ngày phiên học ngẫu nhiên trong 30 ngày qua
            days_ago = random.randint(1, 30)
            session_date = timezone.now() - timedelta(days=days_ago)
            
            # Thời lượng phiên học ngẫu nhiên (30-120 phút)
            session_duration = random.randint(30, 120)
            
            # Loại phiên học ngẫu nhiên
            session_type = random.choice(['online', 'offline'])
            
            # Trạng thái ngẫu nhiên (chủ yếu là active để có thể đánh giá)
            status = random.choices(['active', 'waiting_japanese_rating', 'waiting_vietnamese_rating', 'fully_rated', 'cancelled', 'no_show'], weights=[0.4, 0.2, 0.2, 0.1, 0.05, 0.05])[0]
            
            # Đánh giá từ người Nhật (1-5 sao)
            japanese_rating = random.randint(3, 5) if status == 'completed' else None
            japanese_comment = None
            if japanese_rating and random.random() > 0.3:  # 70% có nhận xét
                comments = [
                    "とても良いレッスンでした。ベトナム語の発音が上手になりました。",
                    "楽しい時間を過ごせました。また一緒に勉強したいです。",
                    "ベトナムの文化についても学べて良かったです。",
                    "丁寧に教えてくれてありがとうございました。",
                    "会話の練習ができて良かったです。",
                    "文法の説明が分かりやすかったです。",
                    "実用的なフレーズを教えてもらいました。",
                    "発音の練習が楽しかったです。",
                    "ベトナムの習慣についても知ることができました。",
                    "次回も楽しみにしています。"
                ]
                japanese_comment = random.choice(comments)
            
            # Đánh giá từ người Việt (1-5 sao, ít hơn)
            vietnamese_rating = None
            vietnamese_comment = None
            if status == 'completed' and random.random() > 0.6:  # 40% có đánh giá
                vietnamese_rating = random.randint(3, 5)
                if random.random() > 0.5:  # 50% có nhận xét
                    comments = [
                        "Người Nhật rất lịch sự và kiên nhẫn.",
                        "Học được nhiều từ vựng mới.",
                        "Cách dạy rất dễ hiểu.",
                        "Thời gian học tập hiệu quả.",
                        "Giao tiếp bằng tiếng Nhật tốt.",
                        "Hiểu thêm về văn hóa Nhật Bản.",
                        "Phát âm tiếng Nhật được cải thiện.",
                        "Bài học thú vị và bổ ích.",
                        "Đối tác học tập rất tốt.",
                        "Mong muốn học tập thêm."
                    ]
                    vietnamese_comment = random.choice(comments)
            
            # Ghi chú bổ sung
            notes = None
            if random.random() > 0.7:  # 30% có ghi chú
                note_templates = [
                    "Phiên học diễn ra tại quán cà phê {cafe}",
                    "Sử dụng tài liệu học tập từ bài {lesson}",
                    "Tập trung vào chủ đề {topic}",
                    "Có sử dụng video call để hỗ trợ",
                    "Thực hành giao tiếp thực tế",
                    "Ôn tập từ vựng đã học trước đó",
                    "Luyện tập phát âm cơ bản",
                    "Thảo luận về văn hóa hai nước",
                    "Sử dụng flashcards để học từ mới",
                    "Thực hành đặt câu đơn giản"
                ]
                topics = ['chào hỏi', 'giới thiệu', 'mua sắm', 'nhà hàng', 'giao thông', 'thời tiết', 'gia đình']
                cafes = ['Highlands Coffee', 'The Coffee House', 'Phúc Long', 'Trung Nguyên', 'Cộng Cà Phê']
                lessons = ['bài 1', 'bài 2', 'bài 3', 'bài 4', 'bài 5']
                
                note = random.choice(note_templates)
                if '{cafe}' in note:
                    note = note.replace('{cafe}', random.choice(cafes))
                elif '{topic}' in note:
                    note = note.replace('{topic}', random.choice(topics))
                elif '{lesson}' in note:
                    note = note.replace('{lesson}', random.choice(lessons))
                
                notes = note
            
            # Tạo connection history
            connection, created = ConnectionHistory.objects.get_or_create(
                japanese_user=japanese_user,
                vietnamese_user=vietnamese_user,
                session_date=session_date,
                defaults={
                    'session_duration': session_duration,
                    'session_type': session_type,
                    'japanese_rating': japanese_rating,
                    'japanese_comment': japanese_comment,
                    'vietnamese_rating': vietnamese_rating,
                    'vietnamese_comment': vietnamese_comment,
                    'notes': notes,
                }
            )
            
            # Cập nhật trạng thái dựa trên đánh giá
            if created:
                connection.update_status()
            
            if created:
                connections_created += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created connection: {japanese_user.username} - {vietnamese_user.username} '
                        f'({session_date.strftime("%Y-%m-%d")})'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {connections_created} sample connections!'
            )
        )
