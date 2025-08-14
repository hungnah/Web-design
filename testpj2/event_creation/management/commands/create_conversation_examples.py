from django.core.management.base import BaseCommand
from event_creation.models import VietnamesePhrase, ConversationExample

class Command(BaseCommand):
    help = 'Create conversation examples for language learning'

    def handle(self, *args, **options):
        # Get or create phrases
        greeting_phrase, created = VietnamesePhrase.objects.get_or_create(
            vietnamese_text="Chào buổi sáng",
            defaults={
                'category': 'greetings',
                'difficulty': 'beginner',
                'japanese_translation': 'おはようございます',
                'english_translation': 'Good morning'
            }
        )
        
        if created:
            self.stdout.write(f'Created phrase: {greeting_phrase.vietnamese_text}')
        
        # Create conversation example for greetings
        conversation, created = ConversationExample.objects.get_or_create(
            phrase=greeting_phrase,
            defaults={
                'title': 'Chào buổi sáng 「おはよう」を学ぼう',
                'vietnamese_title': 'Học cách chào buổi sáng',
                'japanese_title': 'おはようの挨拶を学ぼう',
                'line_1_teacher': 'Chào buổi sáng. (おはようございます。)',
                'line_1_student': 'Chào buổi sáng. (おはようございます。)',
                'line_2_teacher': 'Chào nhé! (thân mật) (おはよう。)',
                'line_2_student': 'Chào nhé! (thân mật) (おはよう。)',
                'line_3_teacher': 'Chào buổi sáng, bạn có khỏe không? (おはよう、お元気ですか?)',
                'line_3_student': 'Vâng, tôi khỏe. Cảm ơn bạn! (はい、元気です。ありがとうございます!)',
                'line_1_teacher_jp': 'おはようございます。',
                'line_1_student_jp': 'おはようございます。',
                'line_2_teacher_jp': 'おはよう。',
                'line_2_student_jp': 'おはよう。',
                'line_3_teacher_jp': 'おはよう、お元気ですか?',
                'line_3_student_jp': 'はい、元気です。ありがとうございます!',
            }
        )
        
        if created:
            self.stdout.write(f'Created conversation example: {conversation.title}')
        
        # Create another example for asking names
        name_phrase, created = VietnamesePhrase.objects.get_or_create(
            vietnamese_text="Tên bạn là gì?",
            defaults={
                'category': 'greetings',
                'difficulty': 'beginner',
                'japanese_translation': 'お名前は何ですか？',
                'english_translation': 'What is your name?'
            }
        )
        
        if created:
            self.stdout.write(f'Created phrase: {name_phrase.vietnamese_text}')
        
        name_conversation, created = ConversationExample.objects.get_or_create(
            phrase=name_phrase,
            defaults={
                'title': 'Hỏi tên 「名前を尋ねる」を学ぼう',
                'vietnamese_title': 'Học cách hỏi tên',
                'japanese_title': '名前の尋ね方を学ぼう',
                'line_1_teacher': 'Xin chào! Tên bạn là gì? (こんにちは！お名前は何ですか？)',
                'line_1_student': 'Xin chào! Tên tôi là Tanaka. (こんにちは！私の名前は田中です。)',
                'line_2_teacher': 'Rất vui được gặp bạn, Tanaka! (田中さん、お会いできて嬉しいです！)',
                'line_2_student': 'Rất vui được gặp bạn! (お会いできて嬉しいです！)',
                'line_3_teacher': 'Bạn đến từ đâu? (どちらから来られましたか？)',
                'line_3_student': 'Tôi đến từ Tokyo. (東京から来ました。)',
                'line_1_teacher_jp': 'こんにちは！お名前は何ですか？',
                'line_1_student_jp': 'こんにちは！私の名前は田中です。',
                'line_2_teacher_jp': '田中さん、お会いできて嬉しいです！',
                'line_2_student_jp': 'お会いできて嬉しいです！',
                'line_3_teacher_jp': 'どちらから来られましたか？',
                'line_3_student_jp': '東京から来ました。',
            }
        )
        
        if created:
            self.stdout.write(f'Created conversation example: {name_conversation.title}')
        
        # Create example for restaurant phrases
        restaurant_phrase, created = VietnamesePhrase.objects.get_or_create(
            vietnamese_text="Chúng ta có thể hẹn gặp vào...",
            defaults={
                'category': 'food',
                'difficulty': 'intermediate',
                'japanese_translation': '私たちは...に会うことができます',
                'english_translation': 'We can meet at...'
            }
        )
        
        if created:
            self.stdout.write(f'Created phrase: {restaurant_phrase.vietnamese_text}')
        
        restaurant_conversation, created = ConversationExample.objects.get_or_create(
            phrase=restaurant_phrase,
            defaults={
                'title': 'Hẹn gặp tại nhà hàng 「レストランで待ち合わせ」を学ぼう',
                'vietnamese_title': 'Học cách hẹn gặp tại nhà hàng',
                'japanese_title': 'レストランでの待ち合わせ方を学ぼう',
                'line_1_teacher': 'Chúng ta có thể hẹn gặp vào lúc nào? (私たちは何時に会うことができますか？)',
                'line_1_student': 'Chúng ta có thể hẹn gặp vào 7 giờ tối. (私たちは午後7時に会うことができます。)',
                'line_2_teacher': 'Tuyệt! Chúng ta gặp nhau ở đâu? (素晴らしい！どこで会いましょうか？)',
                'line_2_student': 'Chúng ta có thể gặp nhau tại nhà hàng ABC. (ABCレストランで会うことができます。)',
                'line_3_teacher': 'Được rồi! Tôi sẽ đặt bàn trước. (分かりました！事前にテーブルを予約します。)',
                'line_3_student': 'Cảm ơn bạn rất nhiều! (どうもありがとうございます！)',
                'line_1_teacher_jp': '私たちは何時に会うことができますか？',
                'line_1_student_jp': '私たちは午後7時に会うことができます。',
                'line_2_teacher_jp': '素晴らしい！どこで会いましょうか？',
                'line_2_student_jp': 'ABCレストランで会うことができます。',
                'line_3_teacher_jp': '分かりました！事前にテーブルを予約します。',
                'line_3_student_jp': 'どうもありがとうございます！',
            }
        )
        
        if created:
            self.stdout.write(f'Created conversation example: {restaurant_conversation.title}')
        
        self.stdout.write(self.style.SUCCESS('Successfully created conversation examples'))
