from django.core.management.base import BaseCommand
from event_creation.models import VietnamesePhrase

class Command(BaseCommand):
    help = 'Create comprehensive Vietnamese phrases for language exchange posts'

    def handle(self, *args, **options):
        self.stdout.write('Creating comprehensive Vietnamese phrases...')
        
        phrases_data = [
            # Greetings - Beginner
            ('greetings', 'beginner', 'Xin chào!', 'こんにちは！', 'Hello!'),
            ('greetings', 'beginner', 'Chào buổi sáng.', 'おはようございます。', 'Good morning.'),
            ('greetings', 'beginner', 'Chào buổi trưa.', 'こんにちは。', 'Good afternoon.'),
            ('greetings', 'beginner', 'Chào buổi tối.', 'こんばんは。', 'Good evening.'),
            ('greetings', 'beginner', 'Bạn khỏe không?', 'お元気ですか？', 'How are you?'),
            ('greetings', 'beginner', 'Tôi khỏe, cảm ơn.', '元気です、ありがとう。', 'I\'m fine, thank you.'),
            ('greetings', 'beginner', 'Hẹn gặp lại!', 'また会いましょう！', 'See you again!'),
            ('greetings', 'beginner', 'Tạm biệt!', 'さようなら！', 'Goodbye!'),
            
            # Greetings - Intermediate
            ('greetings', 'intermediate', 'Chào bạn, lâu rồi không gặp!', 'こんにちは、久しぶりですね！', 'Hello, long time no see!'),
            ('greetings', 'intermediate', 'Bạn có khỏe không?', 'お元気ですか？', 'How are you doing?'),
            ('greetings', 'intermediate', 'Cảm ơn bạn đã hỏi thăm.', 'お気遣いありがとうございます。', 'Thank you for asking.'),
            ('greetings', 'intermediate', 'Chúc bạn một ngày tốt lành!', '良い一日をお過ごしください！', 'Have a good day!'),
            
            # Family - Beginner
            ('family', 'beginner', 'Đây là gia đình tôi.', 'これは私の家族です。', 'This is my family.'),
            ('family', 'beginner', 'Tôi có anh trai.', '私は兄がいます。', 'I have an older brother.'),
            ('family', 'beginner', 'Tôi có em gái.', '私は妹がいます。', 'I have a younger sister.'),
            ('family', 'beginner', 'Bố tôi là giáo viên.', '私の父は教師です。', 'My father is a teacher.'),
            ('family', 'beginner', 'Mẹ tôi là bác sĩ.', '私の母は医者です。', 'My mother is a doctor.'),
            ('family', 'beginner', 'Tôi yêu gia đình tôi.', '私は家族を愛しています。', 'I love my family.'),
            
            # Family - Intermediate
            ('family', 'intermediate', 'Gia đình tôi có 5 người.', '私の家族は5人です。', 'My family has 5 people.'),
            ('family', 'intermediate', 'Tôi sống với bố mẹ.', '私は両親と一緒に住んでいます。', 'I live with my parents.'),
            ('family', 'intermediate', 'Tôi có con trai và con gái.', '私は息子と娘がいます。', 'I have a son and daughter.'),
            
            # Health - Beginner
            ('health', 'beginner', 'Tôi khỏe mạnh.', '私は健康です。', 'I am healthy.'),
            ('health', 'beginner', 'Tôi bị ốm.', '私は病気です。', 'I am sick.'),
            ('health', 'beginner', 'Tôi cần nghỉ ngơi.', '私は休む必要があります。', 'I need to rest.'),
            ('health', 'beginner', 'Tôi uống thuốc.', '私は薬を飲みます。', 'I take medicine.'),
            ('health', 'beginner', 'Tôi tập thể dục.', '私は運動します。', 'I exercise.'),
            
            # Health - Intermediate
            ('health', 'intermediate', 'Tôi cảm thấy mệt mỏi.', '私は疲れています。', 'I feel tired.'),
            ('health', 'intermediate', 'Tôi bị đau đầu.', '私は頭痛がします。', 'I have a headache.'),
            ('health', 'intermediate', 'Tôi cần gặp bác sĩ.', '私は医者に診てもらう必要があります。', 'I need to see a doctor.'),
            
            # Time - Beginner
            ('time', 'beginner', 'Bây giờ là mấy giờ?', '今何時ですか？', 'What time is it now?'),
            ('time', 'beginner', 'Tôi thức dậy lúc 7 giờ.', '私は7時に起きます。', 'I wake up at 7 o\'clock.'),
            ('time', 'beginner', 'Tôi đi ngủ lúc 11 giờ.', '私は11時に寝ます。', 'I go to sleep at 11 o\'clock.'),
            ('time', 'beginner', 'Hôm nay là thứ mấy?', '今日は何曜日ですか？', 'What day is today?'),
            ('time', 'beginner', 'Tôi có cuộc hẹn lúc 3 giờ.', '私は3時に約束があります。', 'I have an appointment at 3 o\'clock.'),
            
            # Time - Intermediate
            ('time', 'intermediate', 'Tôi sẽ đến trong 30 phút.', '私は30分後に到着します。', 'I will arrive in 30 minutes.'),
            ('time', 'intermediate', 'Cuộc hẹn bị trễ 15 phút.', '約束は15分遅れています。', 'The appointment is 15 minutes late.'),
            
            # Weather - Beginner
            ('weather', 'beginner', 'Hôm nay trời nắng.', '今日は晴れです。', 'It is sunny today.'),
            ('weather', 'beginner', 'Hôm nay trời mưa.', '今日は雨です。', 'It is rainy today.'),
            ('weather', 'beginner', 'Hôm nay trời lạnh.', '今日は寒いです。', 'It is cold today.'),
            ('weather', 'beginner', 'Hôm nay trời nóng.', '今日は暑いです。', 'It is hot today.'),
            ('weather', 'beginner', 'Trời đẹp quá!', '天気がとても良いですね！', 'The weather is so nice!'),
            
            # Weather - Intermediate
            ('weather', 'intermediate', 'Dự báo thời tiết thế nào?', '天気予報はどうですか？', 'What\'s the weather forecast?'),
            ('weather', 'intermediate', 'Tôi thích thời tiết mùa thu.', '私は秋の天気が好きです。', 'I like autumn weather.'),
            
            # Directions - Beginner
            ('directions', 'beginner', 'Nhà hàng ở đâu?', 'レストランはどこですか？', 'Where is the restaurant?'),
            ('directions', 'beginner', 'Đi thẳng.', 'まっすぐ行ってください。', 'Go straight.'),
            ('directions', 'beginner', 'Rẽ phải.', '右に曲がってください。', 'Turn right.'),
            ('directions', 'beginner', 'Rẽ trái.', '左に曲がってください。', 'Turn left.'),
            ('directions', 'beginner', 'Gần đây.', 'この近くです。', 'Near here.'),
            
            # Directions - Intermediate
            ('directions', 'intermediate', 'Bạn có thể chỉ đường không?', '道案内してもらえますか？', 'Can you give me directions?'),
            ('directions', 'intermediate', 'Tôi bị lạc đường.', '私は道に迷いました。', 'I am lost.'),
            
            # Self Introduction - Beginner
            ('self_intro', 'beginner', 'Tôi tên là...', '私の名前は...です。', 'My name is...'),
            ('self_intro', 'beginner', 'Tôi đến từ Việt Nam.', '私はベトナムから来ました。', 'I am from Vietnam.'),
            ('self_intro', 'beginner', 'Tôi là sinh viên.', '私は学生です。', 'I am a student.'),
            ('self_intro', 'beginner', 'Tôi thích học tiếng Nhật.', '私は日本語を勉強するのが好きです。', 'I like learning Japanese.'),
            ('self_intro', 'beginner', 'Rất vui được gặp bạn!', 'お会いできて嬉しいです！', 'Nice to meet you!'),
            
            # Self Introduction - Intermediate
            ('self_intro', 'intermediate', 'Tôi làm việc tại công ty...', '私は...会社で働いています。', 'I work at... company.'),
            ('self_intro', 'intermediate', 'Tôi đã học tiếng Nhật được 2 năm.', '私は日本語を2年間勉強しています。', 'I have been learning Japanese for 2 years.'),
            
            # Food & Dining - Beginner
            ('food', 'beginner', 'Cho tôi xem thực đơn.', 'メニューを見せてください。', 'Please show me the menu.'),
            ('food', 'beginner', 'Tôi muốn gọi món phở.', 'フォーを注文したいです。', 'I\'d like to order pho.'),
            ('food', 'beginner', 'Món này rất ngon!', 'この料理はとてもおいしい！', 'This dish is very delicious!'),
            ('food', 'beginner', 'Xin cho hóa đơn.', 'お会計をお願いします。', 'The bill, please.'),
            ('food', 'beginner', 'Tôi thích ăn cơm.', 'ご飯を食べるのが好きです。', 'I like eating rice.'),
            ('food', 'beginner', 'Cho tôi thêm nước.', '水を追加してください。', 'Please add more water.'),
            
            # Food & Dining - Intermediate
            ('food', 'intermediate', 'Món này có cay không?', 'この料理は辛いですか？', 'Is this dish spicy?'),
            ('food', 'intermediate', 'Tôi bị dị ứng với...', '私は...にアレルギーがあります。', 'I am allergic to...'),
            ('food', 'intermediate', 'Có thể nấu ít muối không?', '塩を少なめに調理できますか？', 'Can you cook with less salt?'),
            ('food', 'intermediate', 'Món này được nấu như thế nào?', 'この料理はどのように調理されますか？', 'How is this dish cooked?'),
            
            # Shopping - Beginner
            ('shopping', 'beginner', 'Cái này giá bao nhiêu?', 'これはいくらですか？', 'How much is this?'),
            ('shopping', 'beginner', 'Tôi muốn mua cái này.', 'これを買いたいです。', 'I want to buy this.'),
            ('shopping', 'beginner', 'Cho tôi túi nhé.', '袋をください。', 'Please give me a bag.'),
            ('shopping', 'beginner', 'Có thể xem cái khác không?', '他のものを見せてもらえますか？', 'Can I see something else?'),
            ('shopping', 'beginner', 'Tôi đang tìm...', '私は...を探しています。', 'I am looking for...'),
            
            # Shopping - Intermediate
            ('shopping', 'intermediate', 'Có thể trả bằng thẻ không?', 'カードで払えますか？', 'Can I pay by card?'),
            ('shopping', 'intermediate', 'Có thể giảm giá không?', '値引きできますか？', 'Can you reduce the price?'),
            ('shopping', 'intermediate', 'Quá đắt rồi.', '高すぎます。', 'Too expensive.'),
            ('shopping', 'intermediate', 'Bạn có thể bán với giá... không?', '...円で売ってくれませんか？', 'Can you sell it for...?'),
            ('shopping', 'intermediate', 'Có bảo hành không?', '保証はありますか？', 'Is there a warranty?'),
            
            # Transportation - Beginner
            ('transport', 'beginner', 'Tôi muốn mua vé đến Hà Nội.', 'ハノイ行きの切符を買いたいです。', 'I want to buy a ticket to Hanoi.'),
            ('transport', 'beginner', 'Xe buýt dừng ở đâu?', 'バスはどこで止まりますか？', 'Where does the bus stop?'),
            ('transport', 'beginner', 'Có taxi ở gần đây không?', 'この近くにタクシーはありますか？', 'Is there a taxi nearby?'),
            ('transport', 'beginner', 'Tôi muốn đến...', '...に行きたいです。', 'I want to go to...'),
            ('transport', 'beginner', 'Bao nhiêu tiền?', 'いくらですか？', 'How much?'),
            
            # Transportation - Intermediate
            ('transport', 'intermediate', 'Có chuyến nào vào... không?', '...発の便はありますか？', 'Is there a flight at...?'),
            ('transport', 'intermediate', 'Chuyến này có muộn không?', 'この便は遅れていますか？', 'Is this flight delayed?'),
            ('transport', 'intermediate', 'Tôi bị lỡ chuyến.', '乗り遅れました。', 'I missed my flight.'),
            ('transport', 'intermediate', 'Có thể đổi vé không?', 'チケットを変更できますか？', 'Can I change my ticket?'),
            
            # Emergency - Intermediate
            ('emergency', 'intermediate', 'Tôi cần gặp bác sĩ.', '医者に診てもらう必要があります。', 'I need to see a doctor.'),
            ('emergency', 'intermediate', 'Gọi cấp cứu giúp tôi!', '救急車を呼んでください！', 'Call an ambulance!'),
            ('emergency', 'intermediate', 'Tôi bị đau...', '私は...が痛いです。', 'I have pain in...'),
            ('emergency', 'intermediate', 'Có ai giúp tôi không?', '誰か助けてくれませんか？', 'Can anyone help me?'),
            ('emergency', 'intermediate', 'Tôi cần giúp đỡ.', '助けが必要です。', 'I need help.'),
            
            # Daily Life - Beginner
            ('daily', 'beginner', 'Bây giờ là mấy giờ?', '今何時ですか？', 'What time is it now?'),
            ('daily', 'beginner', 'Hôm nay trời nắng.', '今日は晴れです。', 'It is sunny today.'),
            ('daily', 'beginner', 'Tôi thích...', '私は...が好きです。', 'I like...'),
            ('daily', 'beginner', 'Tôi không thích...', '私は...が好きではありません。', 'I don\'t like...'),
            ('daily', 'beginner', 'Bạn có thể... không?', '...できますか？', 'Can you...?'),
            
            # Daily Life - Intermediate
            ('daily', 'intermediate', 'Tôi đang học tiếng Việt.', '私はベトナム語を勉強しています。', 'I am learning Vietnamese.'),
            ('daily', 'intermediate', 'Bạn có thể nói chậm hơn không?', 'もっとゆっくり話せますか？', 'Can you speak slower?'),
            ('daily', 'intermediate', 'Tôi không hiểu.', '分かりません。', 'I don\'t understand.'),
            ('daily', 'intermediate', 'Bạn có thể giải thích lại không?', 'もう一度説明してもらえますか？', 'Can you explain again?'),
            
            # Business - Intermediate
            ('business', 'intermediate', 'Tôi muốn gặp...', '...に会いたいです。', 'I want to meet...'),
            ('business', 'intermediate', 'Bạn có thể gọi lại cho tôi không?', '後で電話してもらえますか？', 'Can you call me back?'),
            ('business', 'intermediate', 'Tôi sẽ gửi email cho bạn.', 'メールを送ります。', 'I will send you an email.'),
            ('business', 'intermediate', 'Chúng ta có thể hẹn gặp vào...', '...に会うことができます。', 'We can meet on...'),
            ('business', 'intermediate', 'Xin lỗi vì sự cố.', 'トラブルで申し訳ありません。', 'Sorry for the trouble.'),
            
            # Travel - Beginner
            ('travel', 'beginner', 'Tôi muốn đi du lịch.', '旅行に行きたいです。', 'I want to travel.'),
            ('travel', 'beginner', 'Đây là lần đầu tôi đến Việt Nam.', 'ベトナムに来るのは初めてです。', 'This is my first time in Vietnam.'),
            ('travel', 'beginner', 'Tôi thích Việt Nam.', 'ベトナムが好きです。', 'I like Vietnam.'),
            ('travel', 'beginner', 'Bạn có thể chụp ảnh giúp tôi không?', '写真を撮ってもらえますか？', 'Can you take a photo for me?'),
            ('travel', 'beginner', 'Đây là địa điểm đẹp.', 'ここは美しい場所です。', 'This is a beautiful place.'),
            
            # Travel - Intermediate
            ('travel', 'intermediate', 'Bạn có thể giới thiệu địa điểm nào đẹp không?', '美しい場所を紹介してもらえますか？', 'Can you recommend a beautiful place?'),
            ('travel', 'intermediate', 'Tôi muốn tìm hiểu văn hóa Việt Nam.', 'ベトナム文化を学びたいです。', 'I want to learn about Vietnamese culture.'),
            ('travel', 'intermediate', 'Có thể hướng dẫn tôi không?', '案内してもらえますか？', 'Can you guide me?'),
            ('travel', 'intermediate', 'Tôi muốn thử món ăn địa phương.', '地元の料理を試してみたいです。', 'I want to try local food.'),
        ]
        
        created_phrases = 0
        for category, difficulty, vietnamese, japanese, english in phrases_data:
            phrase, created = VietnamesePhrase.objects.get_or_create(
                category=category,
                difficulty=difficulty,
                vietnamese_text=vietnamese,
                defaults={
                    'japanese_translation': japanese,
                    'english_translation': english,
                }
            )
            
            if created:
                created_phrases += 1
                self.stdout.write(f'Created phrase: {vietnamese}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_phrases} Vietnamese phrases!')
        )
