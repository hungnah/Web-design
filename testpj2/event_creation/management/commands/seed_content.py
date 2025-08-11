from django.core.management.base import BaseCommand
from event_creation.models import VietnamesePhrase, CafeLocation


class Command(BaseCommand):
    help = "Seed initial content: Vietnamese phrases (for post creation) and cafe locations"

    def handle(self, *args, **options):
        phrases = [
            # greetings
            ("greetings", "beginner", "Xin chào!", "こんにちは！", "Hello!"),
            ("greetings", "beginner", "Chào buổi sáng.", "おはようございます。", "Good morning."),
            ("greetings", "beginner", "Bạn khỏe không?", "お元気ですか？", "How are you?"),
            ("greetings", "beginner", "Tôi khỏe, cảm ơn.", "元気です、ありがとう。", "I'm fine, thank you."),
            ("greetings", "beginner", "Hẹn gặp lại!", "また会いましょう！", "See you again!"),
            # food
            ("food", "beginner", "Cho tôi xem thực đơn.", "メニューを見せてください。", "Please show me the menu."),
            ("food", "beginner", "Tôi muốn gọi món phở.", "フォーを注文したいです。", "I'd like to order pho."),
            ("food", "beginner", "Xin cho hóa đơn.", "お会計をお願いします。", "The bill, please."),
            ("food", "beginner", "Món này rất ngon!", "この料理はとてもおいしい！", "This dish is very delicious!"),
            # shopping
            ("shopping", "beginner", "Cái này giá bao nhiêu?", "これはいくらですか？", "How much is this?"),
            ("shopping", "beginner", "Tôi muốn mua cái này.", "これを買いたいです。", "I want to buy this."),
            ("shopping", "intermediate", "Có thể trả bằng thẻ không?", "カードで払えますか？", "Can I pay by card?"),
            ("shopping", "beginner", "Cho tôi túi nhé.", "袋をください。", "Please give me a bag."),
            # transport
            ("transport", "beginner", "Tôi muốn mua vé đến Hà Nội.", "ハノイ行きの切符を買いたいです。", "I want to buy a ticket to Hanoi."),
            ("transport", "beginner", "Xe buýt dừng ở đâu?", "バスはどこで止まりますか？", "Where does the bus stop?"),
            ("transport", "beginner", "Có taxi ở gần đây không?", "この近くにタクシーはありますか？", "Is there a taxi nearby?"),
            # emergency
            ("emergency", "intermediate", "Tôi cần gặp bác sĩ.", "医者に診てもらう必要があります。", "I need to see a doctor."),
            ("emergency", "intermediate", "Gọi cấp cứu giúp tôi!", "救急車を呼んでください！", "Call an ambulance!"),
            # daily
            ("daily", "beginner", "Bây giờ là mấy giờ?", "今何時ですか？", "What time is it now?"),
            ("daily", "beginner", "Hôm nay trời nắng.", "今日は晴れです。", "It is sunny today."),
        ]

        created_phrases = 0
        for category, level, vi, ja, en in phrases:
            _, created = VietnamesePhrase.objects.get_or_create(
                category=category,
                difficulty=level,
                vietnamese_text=vi,
                defaults={
                    "japanese_translation": ja,
                    "english_translation": en,
                },
            )
            if created:
                created_phrases += 1

        locations = [
            ("Cafe Tranquil", "5 Nguyễn Quang Bích, Hoàn Kiếm", "hanoi"),
            ("The Workshop", "27 Ngô Đức Kế, Quận 1", "hochiminh"),
            ("Mun Coffee", "20 Lạch Tray, Ngô Quyền", "haiphong"),
            ("43 Factory", "Lê Văn Duyệt, Sơn Trà", "danang"),
            ("Cafe 1985", "Hai Bà Trưng, Ninh Kiều", "cantho"),
        ]

        created_locations = 0
        for name, address, city in locations:
            _, created = CafeLocation.objects.get_or_create(
                name=name,
                address=address,
                city=city,
                defaults={"description": "Địa điểm gợi ý để hẹn gặp"},
            )
            if created:
                created_locations += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded: phrases={created_phrases}, locations={created_locations}"
        ))


