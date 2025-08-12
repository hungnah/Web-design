from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from event_creation.models import Lesson, TheorySection, TheoryPhrase, ConversationExample, ConversationLine

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample theory sections with basic conversation phrases'

    def handle(self, *args, **options):
        self.stdout.write('Creating theory sections...')
        
        # Get or create a lesson for greetings
        lesson, created = Lesson.objects.get_or_create(
            category='greetings',
            defaults={
                'title': 'Chào hỏi cơ bản (Basic Greetings)',
                'description': 'Học các câu chào hỏi cơ bản trong tiếng Việt',
                'difficulty': 'beginner'
            }
        )
        
        if created:
            self.stdout.write(f'Created lesson: {lesson.title}')
        else:
            self.stdout.write(f'Using existing lesson: {lesson.title}')
        
        # Create theory section for basic greetings
        theory_section, created = TheorySection.objects.get_or_create(
            lesson=lesson,
            title='Chào hỏi cơ bản hàng ngày',
            defaults={
                'description': 'Các câu chào hỏi cơ bản mà bạn có thể sử dụng mỗi ngày',
                'order': 1
            }
        )
        
        if created:
            self.stdout.write(f'Created theory section: {theory_section.title}')
        
        # Create essential phrases
        essential_phrases = [
            {
                'vietnamese_text': 'Xin chào',
                'japanese_translation': 'こんにちは',
                'english_translation': 'Hello',
                'pronunciation_guide': 'sin chào',
                'usage_note': 'Dùng để chào hỏi vào ban ngày',
                'is_essential': True,
                'order': 1
            },
            {
                'vietnamese_text': 'Chào bạn',
                'japanese_translation': 'こんにちは',
                'english_translation': 'Hello (informal)',
                'pronunciation_guide': 'chào bạn',
                'usage_note': 'Cách chào thân thiện với bạn bè',
                'is_essential': True,
                'order': 2
            },
            {
                'vietnamese_text': 'Tôi tên là...',
                'japanese_translation': '私の名前は...です',
                'english_translation': 'My name is...',
                'pronunciation_guide': 'tôi tên là',
                'usage_note': 'Dùng để giới thiệu tên của mình',
                'is_essential': True,
                'order': 3
            },
            {
                'vietnamese_text': 'Rất vui được gặp bạn',
                'japanese_translation': 'お会いできて嬉しいです',
                'english_translation': 'Nice to meet you',
                'pronunciation_guide': 'rất vui được gặp bạn',
                'usage_note': 'Dùng khi gặp ai đó lần đầu',
                'is_essential': True,
                'order': 4
            },
            {
                'vietnamese_text': 'Bạn khỏe không?',
                'japanese_translation': 'お元気ですか？',
                'english_translation': 'How are you?',
                'pronunciation_guide': 'bạn khỏe không',
                'usage_note': 'Hỏi thăm sức khỏe',
                'is_essential': True,
                'order': 5
            },
            {
                'vietnamese_text': 'Tôi khỏe, cảm ơn bạn',
                'japanese_translation': '元気です、ありがとうございます',
                'english_translation': 'I am fine, thank you',
                'pronunciation_guide': 'tôi khỏe, cảm ơn bạn',
                'usage_note': 'Trả lời khi ai đó hỏi thăm sức khỏe',
                'is_essential': True,
                'order': 6
            },
            {
                'vietnamese_text': 'Tạm biệt',
                'japanese_translation': 'さようなら',
                'english_translation': 'Goodbye',
                'pronunciation_guide': 'tạm biệt',
                'usage_note': 'Dùng để chào tạm biệt',
                'is_essential': True,
                'order': 7
            },
            {
                'vietnamese_text': 'Hẹn gặp lại',
                'japanese_translation': 'また会いましょう',
                'english_translation': 'See you again',
                'pronunciation_guide': 'hẹn gặp lại',
                'usage_note': 'Cách chào tạm biệt thân thiện',
                'is_essential': False,
                'order': 8
            }
        ]
        
        for phrase_data in essential_phrases:
            phrase, created = TheoryPhrase.objects.get_or_create(
                theory_section=theory_section,
                vietnamese_text=phrase_data['vietnamese_text'],
                defaults=phrase_data
            )
            if created:
                self.stdout.write(f'Created phrase: {phrase.vietnamese_text}')
        
        # Create conversation example
        conversation, created = ConversationExample.objects.get_or_create(
            theory_section=theory_section,
            title='Hội thoại giới thiệu bản thân',
            defaults={
                'description': 'Cuộc trò chuyện giữa hai người lần đầu gặp nhau',
                'order': 1
            }
        )
        
        if created:
            self.stdout.write(f'Created conversation: {conversation.title}')
        
        # Create conversation lines
        conversation_lines = [
            {
                'speaker': 'person_a',
                'vietnamese_text': 'Xin chào! Tôi tên là Mai. Rất vui được gặp bạn.',
                'japanese_translation': 'こんにちは！私の名前はマイです。お会いできて嬉しいです。',
                'english_translation': 'Hello! My name is Mai. Nice to meet you.',
                'order': 1
            },
            {
                'speaker': 'person_b',
                'vietnamese_text': 'Xin chào Mai! Tôi tên là Tanaka. Rất vui được gặp bạn.',
                'japanese_translation': 'こんにちは、マイさん！私の名前は田中です。お会いできて嬉しいです。',
                'english_translation': 'Hello Mai! My name is Tanaka. Nice to meet you.',
                'order': 2
            },
            {
                'speaker': 'person_a',
                'vietnamese_text': 'Bạn khỏe không?',
                'japanese_translation': 'お元気ですか？',
                'english_translation': 'How are you?',
                'order': 3
            },
            {
                'speaker': 'person_b',
                'vietnamese_text': 'Tôi khỏe, cảm ơn bạn. Còn bạn thì sao?',
                'japanese_translation': '元気です、ありがとうございます。あなたはどうですか？',
                'english_translation': 'I am fine, thank you. How about you?',
                'order': 4
            },
            {
                'speaker': 'person_a',
                'vietnamese_text': 'Tôi cũng khỏe. Hẹn gặp lại bạn nhé!',
                'japanese_translation': '私も元気です。また会いましょう！',
                'english_translation': 'I am also fine. See you again!',
                'order': 5
            },
            {
                'speaker': 'person_b',
                'vietnamese_text': 'Hẹn gặp lại! Tạm biệt!',
                'japanese_translation': 'また会いましょう！さようなら！',
                'english_translation': 'See you again! Goodbye!',
                'order': 6
            }
        ]
        
        for line_data in conversation_lines:
            line, created = ConversationLine.objects.get_or_create(
                conversation=conversation,
                order=line_data['order'],
                defaults=line_data
            )
            if created:
                self.stdout.write(f'Created conversation line: {line.vietnamese_text[:30]}...')
        
        # Create another theory section for self-introduction
        intro_section, created = TheorySection.objects.get_or_create(
            lesson=lesson,
            title='Giới thiệu bản thân chi tiết',
            defaults={
                'description': 'Học cách giới thiệu bản thân một cách chi tiết hơn',
                'order': 2
            }
        )
        
        if created:
            self.stdout.write(f'Created theory section: {intro_section.title}')
        
        # Create phrases for self-introduction
        intro_phrases = [
            {
                'vietnamese_text': 'Tôi đến từ Nhật Bản',
                'japanese_translation': '私は日本から来ました',
                'english_translation': 'I come from Japan',
                'pronunciation_guide': 'tôi đến từ nhật bản',
                'usage_note': 'Dùng để giới thiệu quê quán',
                'is_essential': True,
                'order': 1
            },
            {
                'vietnamese_text': 'Tôi là sinh viên',
                'japanese_translation': '私は学生です',
                'english_translation': 'I am a student',
                'pronunciation_guide': 'tôi là sinh viên',
                'usage_note': 'Dùng để giới thiệu nghề nghiệp',
                'is_essential': True,
                'order': 2
            },
            {
                'vietnamese_text': 'Tôi thích học tiếng Việt',
                'japanese_translation': '私はベトナム語を勉強するのが好きです',
                'english_translation': 'I like learning Vietnamese',
                'pronunciation_guide': 'tôi thích học tiếng việt',
                'usage_note': 'Dùng để nói về sở thích',
                'is_essential': False,
                'order': 3
            },
            {
                'vietnamese_text': 'Bạn có thể nói tiếng Nhật không?',
                'japanese_translation': '日本語を話せますか？',
                'english_translation': 'Can you speak Japanese?',
                'pronunciation_guide': 'bạn có thể nói tiếng nhật không',
                'usage_note': 'Hỏi về khả năng ngoại ngữ',
                'is_essential': False,
                'order': 4
            }
        ]
        
        for phrase_data in intro_phrases:
            phrase, created = TheoryPhrase.objects.get_or_create(
                theory_section=intro_section,
                vietnamese_text=phrase_data['vietnamese_text'],
                defaults=phrase_data
            )
            if created:
                self.stdout.write(f'Created phrase: {phrase.vietnamese_text}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created theory sections with sample data!')
        )
